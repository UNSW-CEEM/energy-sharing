import os
import sys
import pandas as pd
import numpy as np
import logging

from ..mike_model import en_utilities as util
from ..mike_model.pv import PVCollectionFactory

class Scenario:
    """Contains a single set of input parameters, but may contain multiple load profiles."""

    def __init__(self, scenario_name, study, timeseries, use_threading=False):
        # ------------------------------
        # Set up key scenario parameters
        # ------------------------------
        self.name = scenario_name
        self.study = study
        self.ts = timeseries
        self.use_threading = use_threading

        self.label = self.study.name + '_' + "{:03}".format(int(self.name))

        # Copy all scenario parameters to allow for threading:
        if use_threading == 'True':
            with lock:
                self.parameters = study.study_parameters.loc[self.name].copy()
        else:
            self.parameters = study.study_parameters.loc[self.name].copy()
        # --------------------------------------------
        # Set up network arrangement for this scenario
        # --------------------------------------------
        self.arrangement = self.parameters['arrangement']
        self.pv_exists = not (self.parameters.isnull()['pv_filename']
                              or 'bau' in self.arrangement
                              or self.arrangement == 'en') \
                         and study.pv_exists
        if any(word in self.arrangement for word in ['btm_s_c', 'btm_s_u', 'btm_p_c', 'btm_p_u', 'btm_i_c']):
            self.pv_allocation = 'load_dependent'
        else:
            self.pv_allocation = 'fixed'

        # -----------------------------------
        # Set up flags for logging timeseries
        # -----------------------------------
        if 'output_types' in self.parameters.index:
            if 'log_timeseries_detailed' in self.parameters.fillna('')['output_types']:
                self.log_timeseries_detailed = True
            else:
                self.log_timeseries_detailed = False
            if 'log_timeseries_brief' in self.parameters.fillna('')['output_types']:
                self.log_timeseries_brief = True
            else:
                self.log_timeseries_brief = False
        else:
            self.log_timeseries_brief = False
            self.log_timeseries_detailed = False

        # -----------------------------------------------------------------
        # Set up load profiles, resident list & results df for the scenario
        # -----------------------------------------------------------------
        # if same load profile(s) used for all scenarios, this comes from Study
        # If different loads used, get resident list from first load
        self.load_folder = self.parameters['load_folder']
        if study.different_loads:
            load_path = os.path.join(study.base_path, 'load_profiles', self.load_folder)
            self.load_list = os.listdir(load_path)

            # read all load profiles into dict of dfs
            # ---------------------------------------
            self.dict_load_profiles = {}
            for load_name in self.load_list:
                loadFile = os.path.join(load_path, load_name)
                temp_load = pd.read_csv(loadFile,
                                        parse_dates=['timestamp'],
                                        dayfirst=True)
                temp_load = temp_load.set_index('timestamp')
                if not 'cp' in temp_load.columns:
                    temp_load['cp'] = 0
                self.dict_load_profiles[load_name] = temp_load.copy()
            # use first load profile in list to establish list of residents:
            # --------------------------------------------------------------
            templist = list(self.dict_load_profiles[
                                self.load_list[0]].columns.values)  # list of potential child meters - residents + cp
            self.resident_list = []
            for i in templist:
                if type(i) == 'str':
                    self.resident_list += [i]
                else:
                    self.resident_list += [str(i)]
        else:
            # Loads are the same for every scenario and have been read already:
            # -----------------------------------------------------------------
            self.dict_load_profiles = study.dict_load_profiles.copy()
            self.resident_list = study.resident_list.copy()  # includes cp
            self.load_list = study.load_list.copy()

        self.households = [c for c in self.resident_list if c != 'cp']
        self.results = pd.DataFrame()

        # ---------------------------------
        # read PV profile for this scenario
        # ---------------------------------
        if not self.pv_exists:
            # self.pv = pd.DataFrame(index=self.ts.get_date_times(), columns=self.resident_list).fillna(0)
            self.pv = PVCollectionFactory().empty_collection(self.ts.get_date_times(), self.resident_list)
        else:
            self.pvFile = os.path.join(study.pv_path, self.parameters['pv_filename'])
            if '.csv' not in self.pvFile:
                self.pvFile = self.pvFile + '.csv'
            if not os.path.exists(self.pvFile):
                logging.info('***************Exception!!! PV file %s NOT FOUND', self.pvFile)
                print('***************Exception!!! PV file %s NOT FOUND: ', self.pvFile)
                sys.exit("PV file missing")
            else:
                # Load pv generation data:
                # -----------------------
                # self.pv = pd.read_csv(self.pvFile, parse_dates=['timestamp'], dayfirst=True)
                # self.pv.data.set_index('timestamp', inplace=True)
                self.pv = PVCollectionFactory().from_file(self.pvFile)
                
                # if not self.pv.data.index.equals(pd.DatetimeIndex(data=self.ts.get_date_times())):
                if not pd.DatetimeIndex(data=self.pv.get_date_times()).equals(pd.DatetimeIndex(data=self.ts.get_date_times())):
                    logging.info('***************Exception!!! PV %s index does not align with load ', self.pvFile)
                    sys.exit("PV has bad timeseries")
                # Scaleable PV has a 1kW generation input file scaled to array size:
                self.pv_scaleable = ('pv_scaleable' in self.parameters.index) and \
                                    self.parameters.fillna(False)['pv_scaleable']
                if self.pv_scaleable:
                    self.pv_kW_peak = self.parameters['pv_kW_peak']
                    # self.pv = self.pv * self.pv_kW_peak
                    self.pv.scale(self.pv_kW_peak)
            if self.pv.get_aggregate_sum() == 0:
                self.pv_exists = False
                # self.pv = pd.DataFrame(index=pd.DatetimeIndex(data=self.ts.get_date_times()), columns=self.resident_list).fillna(0)
                self.pv = PVCollectionFactory().empty_collection(self.ts.get_date_times(),self.resident_list)

        # ---------------------------------------
        # Set up tariffs for this scenario
        # ---------------------------------------
        # Customer tariffs can be individually allocated, or can be fixed for all residents
        # if 'all residents' is present in scenario csv, it trumps individual customer tariffs
        # and is copied across (except for cp):
        if 'all_residents' in self.parameters.index:
            if (self.parameters['all_residents'] == ''):
                logging.info('Missing tariff data for all_residents in study csv')
            else:  # read tariff for each customer
                for c in self.households:
                    if use_threading == 'True':
                        with lock:
                            self.parameters[c] = self.parameters['all_residents']
                    else:
                        self.parameters[c] = self.parameters['all_residents']
        # --------------------------------------------
        # Create list of tariffs used in this scenario
        # --------------------------------------------
        self.customers_with_tariffs = self.resident_list + ['parent']
        self.dnsp_tariff = self.parameters['network_tariff']
        self.tariff_in_use = self.parameters[self.customers_with_tariffs]  # tariff ids for each customer
        self.tariff_short_list = self.tariff_in_use.tolist() + [self.dnsp_tariff]  # list of tariffs in use
        self.tariff_short_list = list(set(self.tariff_short_list))  # drop duplicates
        for tariff_id in self.tariff_short_list:

            if tariff_id not in study.tariff_data.lookup.index:
                msg = '******Exception: Tariff ' + tariff_id + ' is not in tariff_lookup.csv'
                exit(msg)
        #  Slice tariff_lookup table for this scenario
        self.tariff_lookup = study.tariff_data.lookup.loc[self.tariff_short_list]

        self.dynamic_list = [t for t in self.tariff_short_list
                             if any(
                word in self.tariff_lookup.loc[t, 'tariff_type'] for word in ['Block', 'block', 'Dynamic', 'dynamic'])]
        # Currently only includes block, could also add demand tariffs
        # if needed - e.g. for demand tariffs on < 12 month period
        self.solar_list = [t for t in self.tariff_short_list
                           if any(word in self.tariff_lookup.loc[t, 'tariff_type'] for word in ['Solar', 'solar'])]
        solar_block_list = [t for t in self.solar_list
                            if any(word in self.tariff_lookup.loc[t, 'tariff_type'] for word in ['Block', 'block'])]
        self.solar_inst_list = [t for t in self.solar_list
                                if any(word in self.tariff_lookup.loc[t, 'tariff_type'] for word in ['Inst', 'inst'])]
        self.demand_list = [t for t in self.tariff_short_list
                            if 'Demand' in self.tariff_lookup.loc[t, 'tariff_type']]
        self.has_demand_charges = len(self.demand_list) > 0
        self.has_dynamic_tariff = len(self.dynamic_list) > 0
        #  previously:(list(set(self.tariff_short_list).intersection(self.dynamic_list)))
        self.has_solar_block = len(solar_block_list) > 0
        self.has_solar_inst = len(self.solar_inst_list) > 0

        #  Slice  static tariffs for this scenario
        # ----------------------------------------
        self.static_imports = study.tariff_data.static_imports[self.tariff_short_list]
        self.static_exports = study.tariff_data.static_exports[self.tariff_short_list]
        if len(self.solar_list) > 0:
            self.static_solar_imports = study.tariff_data.static_solar_imports[self.solar_list]

        # ------------------------------------
        # identify batteries for this scenario
        # ------------------------------------
        if self.arrangement != 'bau':
            possible_batteries = [i for i in self.parameters.index if 'battery' in i]
            # Central battery
            # ---------------
            if 'central_battery_id' in possible_batteries and 'central_battery_strategy' in possible_batteries:
                self.central_battery_id = self.parameters['central_battery_id']
                self.central_battery_strategy = self.parameters['central_battery_strategy']
                self.has_central_battery = not pd.isnull(self.central_battery_id) and \
                                           not pd.isnull(self.central_battery_strategy)
                if 'central_battery_capacity_kWh' in self.parameters.index:
                    if not pd.isnull(self.parameters['central_battery_capacity_kWh']):
                        self.central_battery_capacity_kWh = self.parameters['central_battery_capacity_kWh']
                    else:
                        self.central_battery_capacity_kWh = 1
                    possible_batteries.remove('central_battery_capacity_kWh')
                else:
                    self.central_battery_capacity_kWh = 1
                possible_batteries.remove('central_battery_id')
                possible_batteries.remove('central_battery_strategy')

            else:
                self.has_central_battery = False

            # Possible individual batteries:
            # ------------------------------
            if any('_battery_id' in i for i in possible_batteries) \
                    and any('_battery_strategy' in i for i in possible_batteries):
                self.has_ind_batteries = 'maybe'
            else:
                self.has_ind_batteries = 'none'
            # Battery capex to override values in battery_lookup.csv:
            # --------------------------------------------------------
            if 'battery_capex_per_kWh' in self.parameters.index:
                if not np.isnan(self.parameters['battery_capex_per_kWh']):
                    self.battery_capex_per_kWh = self.parameters['battery_capex_per_kWh']
                else:
                    self.battery_capex_per_kWh = 0.0
            else:
                self.battery_capex_per_kWh = 0.0
        else:  # 'bau` arrangement has no batteries by definition:
            self.has_central_battery = False
            self.has_ind_batteries = 'none'

        # --------------------------------------------------------
        # Set up annual capex & opex costs for en in this scenario
        # --------------------------------------------------------
        # Annual capex repayments for embedded network or for btm_s or btm_p network

        if 'en' in self.arrangement or 'btm_s' in self.arrangement or 'btm_p' in self.arrangement:
            self.en_cap_id = self.parameters['en_capex_id']
            if self.arrangement in ['btm_s_c', 'btm_p_c']:
                # -----------------------------------
                # metering capex for all units and cp:
                # ------------------------------------
                self.en_capex = study.en_capex.loc[self.en_cap_id, 'site_capex'] + \
                                (study.en_capex.loc[self.en_cap_id, 'unit_capex'] *
                                 len(self.resident_list))
            else:
                # ----------------------------
                # metering capex for units only
                # ----------------------------
                self.en_capex = study.en_capex.loc[self.en_cap_id, 'site_capex'] + \
                                (study.en_capex.loc[self.en_cap_id, 'unit_capex'] *
                                 len(self.households))
        else:
            self.en_capex = 0.0

        self.a_term = self.parameters['a_term']
        self.a_rate = self.parameters['a_rate']

        if self.en_capex > 0.0:
            self.en_capex_repayment = -12 * np.pmt(rate=self.a_rate / 12,
                                                   nper=12 * self.a_term,
                                                   pv=self.en_capex,
                                                   fv=0,
                                                   when='end')
        else:
            self.en_capex_repayment = 0.0
        # ------------------------------------------------
        # Opex for embedded network or btm metering costs:
        # ------------------------------------------------
        if 'en' in self.arrangement or 'btm_s' in self.arrangement or 'btm_p' in self.arrangement:
            if self.arrangement in ['btm_s_c', 'btm_p_c']:
                # -----------------------------------
                # billing / opex for all units and cp:
                # ------------------------------------
                self.en_opex = study.en_capex.loc[self.en_cap_id, 'site_opex'] + \
                               (study.en_capex.loc[self.en_cap_id, 'unit_opex'] * len(self.resident_list))
            else:
                # ------------------------------
                # billing / opex for units only:
                # ------------------------------
                self.en_opex = study.en_capex.loc[self.en_cap_id, 'site_opex'] + \
                               (study.en_capex.loc[self.en_cap_id, 'unit_opex'] * len(self.households))
        else:
            self.en_opex = 0
        # --------------------------------------------------------
        # Calc total annual capex repayments for pv in this scenario
        # --------------------------------------------------------
        self.pv_cap_id = self.parameters['pv_cap_id']
        if not self.pv_exists:
            self.pv_capex_repayment = 0
        else:
            # Calculate pv capex
            # ------------------
            # PV capex includes inverter replacement if amortization period > inverter lifetime
            self.pv_capex = study.pv_capex_table.loc[self.pv_cap_id, 'pv_capex'] + \
                            (int(self.a_term / study.pv_capex_table.loc[self.pv_cap_id, 'inverter_life'] - 0.01) * \
                             study.pv_capex_table.loc[self.pv_cap_id, 'inverter_cost'])

            #  Option to use standard 1kW PV output and scale
            #  with pv_capex and inverter cost given as $/kW
            self.pv_scaleable = ('pv_scaleable' in self.parameters.index) and \
                                self.parameters.fillna(False)['pv_scaleable']
            # pv capex is scaleable if pv is scaleable....
            if self.pv_scaleable:
                self.pv_capex_scaleable = True
            else:
                self.pv_capex_scaleable = False
            # .... unless otherwise specified ....
            if 'pv_capex_scaleable' in self.parameters.index:
                if self.parameters.fillna('missing')['pv_capex_scaleable'] != 'missing':
                    self.pv_capex_scaleable = self.parameters['pv_capex_scaleable']

            if self.pv_capex_scaleable:
                self.pv_capex = self.pv_capex * self.pv_kW_peak

            # Calculate annual repayments
            # ---------------------------
            if self.pv_capex > 0:
                self.pv_capex_repayment = -12 * np.pmt(rate=self.a_rate / 12,
                                                       nper=12 * self.a_term,
                                                       pv=self.pv_capex,
                                                       fv=0,
                                                       when='end')
            else:
                self.pv_capex_repayment = 0

    def calcFinancials(self, net):
        """ Calculates financial results for specific net within scenario.

         Includes: cashflows for whole period  - for each resident
                   cashflows for net and retailer."""

        # This function and Customer.calcCashflow() are the heart of the finances
        # -------------------------------
        # Calculate cashflows for net
        # -------------------------------
        # Use net import and export which are summed from resident & cp import and export
        # (plus dynamic battery calcs)
        # to calculate external cashflows.
        # NB if non-en scenario, tariffs are zero, so cashflows =0
        net.calc_cash_flow()

        # ----------------------------------
        # Cashflows for individual residents
        # ----------------------------------
        for c in net.resident_list:
            net.resident[c].calc_cash_flow()
            net.receipts_from_residents += net.resident[c].energy_bill
            net.cum_resident_total_payments += net.resident[c].total_payment
            net.cum_local_solar_bill += net.resident[c].local_solar_bill

        # ----------------------------
        # External retailer cashflows:
        # ----------------------------
        net.retailer.calc_cash_flow()
        # -----------------
        # Retailer receipts
        # -----------------
        if 'bau' in self.arrangement or 'cp_only' in self.arrangement or 'btm' in self.arrangement:
            net.energy_bill = 0
            net.total_payment = 0
            net.retailer_receipt = net.receipts_from_residents.copy()
            net.receipts_from_residents = 0  # because this is eno receipts
        elif 'en' in self.arrangement:
            net.retailer_receipt = net.energy_bill.copy()
        else:
            print('************************Unknown net arrangement********************')
            logging.info('************************Unknown net arrangement********************')
        # -------------------------
        # Solar Retailer Financials
        # -------------------------
        if 'btm_p' in self.arrangement:
            net.solar_retailer_profit = net.cum_local_solar_bill - \
                                        (net.solar_retailer.en_capex_repayment +
                                         net.solar_retailer.en_opex +
                                         net.solar_retailer.bat_capex_repayment +
                                         net.solar_retailer.pv_capex_repayment) * 100
        else:
            net.solar_retailer_profit = 0
        # ----------------------------
        # Total Net Costs for Building
        # ----------------------------
        # total_building_payment is sum of customer payments to retailer (+ cap/opex)
        #  en and solar retailer, less ENO profit
        net.total_building_payment = net.cum_resident_total_payments + net.total_payment - net.receipts_from_residents
        net.checksum_total_payments = net.retailer_receipt + net.solar_retailer_profit + (self.en_opex + self.en_capex_repayment + self.pv_capex_repayment + self.total_battery_capex_repayment) * 100 - net.total_building_payment

        # #TODO sort out battery capex for 'cp_only'
        # NB checksum: These two total should be the same for all arrangements
        if abs(net.checksum_total_payments) > 0.005:
            print('**************CHECKSUM ERROR***See log ******* Study: ', self.study.name, ' Scenario: ', self.name)
            logging.info('**************CHECKSUM ERROR************************')
            logging.info('Study: %s  Scenario: %s ', self.study.name, self.name)
            logging.info('Tot Building Cost %f Checksum %f', net.total_building_payment, net.checksum_total_payments)

        # ----------------------
        # NPV for whole building
        # ----------------------
        net.npv_whole_building = -sum(net.total_building_payment / (12 * (1 + self.a_rate / 12) ** t)
                                      for t in np.arange(1, 12 * self.a_term))

    def collate_network_results(self, net):
        """ Collates financial and energy results for specific net within scenario.

                 Includes: cashflows for whole period  - for each resident
                           cashflows for net and retailer
                           total imports and exports,
                           self consumption and pv_ratio."""
        # ---------------------------------------------------------------
        # Collate all results for network / eno  in one row of results df
        # ---------------------------------------------------------------
        # includes c -> $ conversion
        result_list = [net.total_building_payment / 100,
                       net.checksum_total_payments / 100,
                       net.receipts_from_residents / 100,
                       net.energy_bill / 100,
                       net.total_payment / 100,
                       net.npv_whole_building / 100,
                       net.demand_charge / 100,
                       net.bat_capex_repayment,
                       (net.receipts_from_residents - net.total_payment) / 100,
                       net.retailer_receipt / 100,
                       net.retailer.energy_bill / 100,
                       net.solar_retailer_profit / 100,
                       net.total_building_load,
                       net.total_building_export,
                       net.total_import,
                       net.cp_ratio,
                       net.pv_ratio,
                       net.self_consumption,
                       net.self_sufficiency,
                       net.self_consumption_OLD,
                       net.self_sufficiency_OLD,
                       net.central_battery_capacity,
                       net.total_battery_losses,
                       net.battery_cycles,
                       net.battery_SOH] + \
                      [net.resident['cp'].energy_bill / 100] + \
                      [net.resident[c].energy_bill / 100 for c in net.resident_list if c != 'cp'] + \
                      [net.resident['cp'].local_solar_bill / 100] + \
                      [net.resident[c].local_solar_bill / 100 for c in net.resident_list if c != 'cp'] + \
                      [net.resident['cp'].total_payment / 100] + \
                      [net.resident[c].total_payment / 100 for c in net.resident_list if c != 'cp']

        result_labels = ['total$_building_costs',
                         'checksum_total_payments$',
                         'eno$_receipts_from_residents',
                         'eno$_energy_bill',
                         'eno$_total_payment',
                         'eno$_npv_building',
                         'eno$_demand_charge',
                         'eno$_bat_capex_repay',
                         'eno_net$',
                         'retailer_receipt$',
                         'retailer_bill$',
                         'solar_retailer_profit',
                         'total_building_load',
                         'export_kWh',
                         'import_kWh',
                         'cp_ratio',
                         'pv_ratio',
                         'self-consumption',
                         'self-sufficiency',
                         'self-consumption_OLD',
                         'self-sufficiency_OLD',
                         'central_battery_capacity_kWh',
                         'total_battery_losses',
                         'central_battery_cycles',
                         'central_battery_SOH'] + \
                        ['cust_bill_cp'] + \
                        ['cust_bill_' + '%s' % r for r in net.resident_list if r != 'cp'] + \
                        ['cust_solar_bill_cp'] + \
                        ['cust_solar_bill_' + '%s' % r for r in net.resident_list if r != 'cp'] + \
                        ['cust_total$_cp'] + \
                        ['cust_total$_' + '%s' % r for r in net.resident_list if r != 'cp']

        self.results = self.results.append(pd.Series(result_list,
                                                     index=result_labels,
                                                     name=net.load_name))

    def log_scenario_data(self):
        """Saves a csv file for each scenario and logs a row of results to output df."""

        # ---------------------------------
        # Save all results for the scenario
        # ---------------------------------
        op_scenario_file = os.path.join(self.study.scenario_path, self.label + '.csv')
        util.df_to_csv(self.results, op_scenario_file)
        # create parameter lists
        cols = self.results.columns.tolist()

        # Scenario label and key parameters for scenario
        self.study.op.loc[self.name, 'scenario_label'] = self.label
        self.study.op.loc[self.name, 'arrangement'] = self.arrangement
        self.study.op.loc[self.name, 'number_of_households'] = len(self.households)
        self.study.op.loc[self.name, 'load_folder'] = self.load_folder

        # Scenario total capex and opex repayments
        # ----------------------------------------
        self.study.op.loc[self.name, 'en_opex'] = self.en_opex
        self.study.op.loc[self.name, 'en_capex_repayment'] = self.en_capex_repayment
        self.study.op.loc[self.name, 'pv_capex_repayment'] = self.pv_capex_repayment

        # ----------------------------------------------------------------
        # Customer payments averaged for all residents, all load profiles:
        # ----------------------------------------------------------------
        cust_bill_list = [c for c in cols if 'cust_bill_' in c and 'cp' not in c]
        cust_total_list = [c for c in cols if 'cust_total$_' in c and 'cp' not in c]
        cust_solar_list = [c for c in cols if 'cust_solar_bill_' in c and 'cp' not in c]
        self.study.op.loc[self.name, 'average_hh_bill$'] = self.results[cust_bill_list].mean().mean()
        self.study.op.loc[self.name, 'std_hh_bill$'] = self.results[cust_bill_list].values.std(ddof=1)
        self.study.op.loc[self.name, 'average_hh_solar_bill$'] = self.results[cust_solar_list].mean().mean()
        self.study.op.loc[self.name, 'std_hh_solar_bill$'] = self.results[cust_solar_list].values.std(ddof=1)
        self.study.op.loc[self.name, 'average_hh_total$'] = self.results[cust_total_list].mean().mean()
        self.study.op.loc[self.name, 'std_hh_total$'] = self.results[cust_total_list].values.std(ddof=1)
        # ----------------------------------------
        # Reduced data logging for different_loads
        # ----------------------------------------
        if self.study.different_loads:
            # Don't log individual customer $ if each scenario has different load profiles
            # (because each scenario may have different number of residents):
            cols = [c for c in cols if c not in (cust_bill_list + cust_total_list + cust_solar_list)]  # .tolist()
        # -------------------------------------
        # Average results across multiple loads
        # -------------------------------------
        # For remaining parameters in results, average across multiple load profiles:
        mcols = [c + '_mean' for c in cols]
        stdcols = [c + '_std' for c in cols]
        for c in cols:
            i = cols.index(c)
            self.study.op.loc[self.name, mcols[i]] = self.results.loc[:, c].mean(axis=0)
            self.study.op.loc[self.name, stdcols[i]] = self.results.loc[:, c].std(axis=0)

    def get_study(self):
        return self.study

    def get_timeseries(self):
        return self.ts