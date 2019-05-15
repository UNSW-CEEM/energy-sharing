import logging
import os
import numpy as np
import pandas as pd
import sys

from ..mike_model.battery import Battery
from ..mike_model.customer import Customer
from ..mike_model import en_utilities as util


class Network(Customer):
    """A group of customers (residents) with loads, flows, financials, and is itself an aggregated customer.

    In embedded network scenarios, this object is equivalent to the ENO, takes payments from residents,
    and pays the retailer. It may be the strata body (when resident 'cp' has null tariffs) or a retailer or ENO.
    In other scenarios, it has no meaning irw, just passes energy and $ between other players"""

    def __init__(self, scenario, study, timeseries):
        # just residents, not cp
        # self.households = scenario.households.copy()
        # residents (inc cp) with batteries - initial state
        self.battery_list = []
        # (these may change later if different_loads)
        # initialise characteristics of the network as a customer:

        self.study = study
        self.ts = timeseries

        super().__init__('network', self.study, self.ts)
        #  initialise the customers / members within the network
        # (includes residents and cp)
        self.resident = {c: Customer(name=c, study=self.study, timeseries=self.ts) for c in (self.study.get_participant_names() + ['cp'])}
        self.retailer = Customer(name='retailer', study=self.study, timeseries=self.ts)
        if 'btm_p' in scenario.arrangement:
            self.solar_retailer = Customer(name='solar_retailer', study=self.study, timeseries=self.ts)

    def initialise_building_loads(self, load_name, scenario):
        """Initialise network for new load profiles."""
        # read load data
        # --------------
        self.load_name = load_name
        self.nl_profile = scenario.load_profiles.get_profile(load_name)

        # set eno load, cumulative load and generation to zero
        # ----------------------------------------------------
        self.initialise_customer_load(np.zeros(self.ts.get_num_steps()))
        self.cum_resident_imports = np.zeros(self.ts.get_num_steps())
        self.cum_resident_exports = np.zeros(self.ts.get_num_steps())
        self.cum_local_imports = np.zeros(self.ts.get_num_steps())
        self.total_aggregated_coincidence = np.zeros(self.ts.get_num_steps())
        self.sum_of_coincidences = np.zeros(self.ts.get_num_steps())
        self.total_discharge = np.zeros(self.ts.get_num_steps())

        # initialise residents' loads
        # ---------------------------
        for c in self.study.get_participant_names() + ['cp']:
            self.resident[c].initialise_customer_load(customer_load=np.array(self.nl_profile.get_load_data(self.study.get_load_profile(c))).astype(np.float64))

        # Calculate total site load
        # --------------------------
        self.total_building_load = self.nl_profile.get_aggregate_sum()

        # Initialise cash totals
        # ----------------------
        self.receipts_from_residents = 0.0
        self.total_building_payment = 0.0
        self.cum_resident_total_payments = 0.0
        self.cum_local_solar_bill = 0.0
        self.energy_bill = 0.0

    def initialiseAllTariffs(self, scenario):
        # initialise parent meter tariff
        self.initialise_customer_tariff(scenario.tariff_in_use['parent'], scenario)
        # initialise internal customer tariffs
        for c in self.study.get_participant_names() + ['cp']:
            self.resident[c].initialise_customer_tariff(scenario.tariff_in_use[c], scenario)
        # initialise retailer's network tariff
        self.retailer.initialise_customer_tariff(scenario.dnsp_tariff, scenario)
        # copy tariff parameter(s) from scenario
        self.has_dynamic_tariff = scenario.has_dynamic_tariff

    def allocatePV(self, scenario, pv):
        """set up and allocate pv generation for this scenario."""

        # PV allocation is used to allocate PV capex costs for some arrangements
        # Copy profile from scenario and then allocate
        # Allocation happens here as the Customers are part of the Network (not scenario)
        self.pv_exists = scenario.pv_exists
        self.pv = pv.copy()

        # Set up PV dataframe for each scenario:
        # --------------------------------------
        if 'en' in scenario.arrangement:
            # rename single column in pv file if necessary
            # TODO Change PV allocation to allow individual distributed PV within EN
            if self.pv.get_num_systems() == 1:
                system_name = self.pv.get_system_names()[0]
                self.pv.rename_system(system_name, 'central')
            # if 'shared_solar_profile' in scenario.parameters:
            #     if scenario.parameters['shared_solar_profile']:
            #         pv.copy_system(scenario.parameters['shared_solar_profile'], 'central')
                

        elif 'cp_only' in scenario.arrangement:
            # no action required
            # rename single column in pv file if necessary
            if 'cp' not in self.pv._data.columns:
                system_name = self.pv.get_system_names()[0]
                self.pv.rename_system(system_name, 'cp')

        elif 'btm_i_u' in scenario.arrangement:
            # For btm_i, if only single pv column, split equally between all units (NOT CP)
            # If more than 1 column, leave as allocated
            if self.pv.get_num_systems() == 1:
                # self.pv.data.columns = ['total']
                system_name = self.pv.get_system_names()[0]
                self.pv.rename_system(system_name, 'total')
                for r in scenario.households:
                    # self.pv.data[r] = self.pv.data['total'] / len(scenario.households)
                    self.pv.copy_system('total', r)
                    self.pv.scale_system(r, 1.0/ len(scenario.households) )
                # self.pv.data = self.pv.data.drop('total', axis=1)
                self.pv.delete_system('total')

        elif 'btm_i_c' in scenario.arrangement:
            # For btm_i_c, if only single pv column, split % to cp according tp cp_ratio and split remainder equally between all units
            # If more than 1 column, leave as allocated
            print("BTM_IC HOME")
            if self.pv.get_num_systems() == 1:
                # self.pv.data.columns = ['total']
                system_name = self.pv.get_system_names()[0]
                self.pv.rename_system(system_name, 'total')
                
                # self.pv.data['cp'] = self.pv.data['total'] * (self.resident['cp'].load.sum() / self.total_building_load)
                self.pv.copy_system('total', 'cp')
                self.pv.scale_system('cp', self.resident['cp'].load.sum() / self.total_building_load)
                for r in scenario.households:
                    # self.pv.data[r] = (self.pv.data['total'] - self.pv.data['cp']) / len(scenario.households)
                    self.pv.copy_system('total', r)
                    self.pv.subtract_system(r, 'cp')
                    self.scale_system(r, 1.0/ len(scenario.households))
                self.pv.data = self.pv.data.drop('total', axis=1)
                # self.pv.delete_system('total')

        elif any(word in scenario.arrangement for word in ['btm_s_c', 'btm_p_c']):
            # For btm_s_c and btm_p_c, split pv between all residents INCLUDING CP according to INSTANTANEOUS load
            if self.pv.get_num_systems() != 1:
                self.pv.aggregate_systems('total')
            system_name = self.pv.get_system_names()[0]
            self.pv.rename_system(system_name, 'total')
            # LUKE
            # OK - so here we are going through every load timeperiod,
            # Dividing by the total network load (to find fraction of network load used)
            # If there's no data, filling in 1/ num_residents
            # Then multiplying pv by that fraction. 
            
            network_load_fractions = self.nl_profile.to_df().div(self.nl_profile.get_aggregate_data(), axis=0).fillna(1 / len(self.study.get_load_profiles()))
            self.pv.multiply_by_timeseries('total', network_load_fractions)

        elif any(word in scenario.arrangement for word in ['btm_s_u', 'btm_p_u']):
            # For btm_s_u and btm_p_u, split pv between all residents EXCLUDING CP according to INSTANTANEOUS  load
            if self.pv.get_num_systems() != 1:
                self.pv.aggregate_systems('total')
            system_name = self.pv.get_system_names()[0]
            self.pv.rename_system(system_name, 'total')
            # Get units only
            load_units_only = self.nl_profile.to_df().copy().drop('cp', axis=1)
            load_fractions = load_units_only.div(load_units_only.sum(axis=1), axis=0).fillna(1 / len(self.study.get_load_profiles()))
            self.pv.multiply_by_timeseries('total', load_fractions)
            if('cp' in self.pv.get_system_names()):
                self.pv.scale_system('cp', 0)

        elif 'bau' not in scenario.arrangement:
            logging.info('*********** Exception!!! Invalid technical arrangement %s for scenario %s',
                         scenario.arrangement, scenario.name)
            print('***************Exception!!! Invalid technical arrangement ', scenario.arrangement, ' for scenario ',
                  scenario.name)
            sys.exit("Invalid technical Arrangement")


        # HOLY GRAIL HERE
        # Add blank columns for all residents with no pv and for central
        # -----------------------------------------------------------
        blank_column_names = [x for x in (self.study.get_solar_profiles() + ['central', 'cp']) if x not in self.pv.get_system_names()]
        # self.pv.data = pd.concat([self.pv.data, pd.DataFrame(columns=blank_column_names)], sort=False).fillna(0)
        for system_name in blank_column_names:
            self.pv.add_zero_system(system_name)

        # Initialise all residents with their allocated PV generation
        # -----------------------------------------------------------
        for c in self.study.get_participant_names():
            self.resident[c].initialise_customer_pv(np.array(self.pv.get_data(self.study.get_solar_profile(c))).astype(np.float64))
        self.initialise_customer_pv(np.array(self.pv.get_data('central')).astype(np.float64))


    
    def initialiseAllBatteries(self, scenario):
        """Initialise central and individual batteries as required."""
        # -------------------------------
        # Total battery losses in network
        # -------------------------------
        self.total_battery_losses = 0

        # ---------------
        # Central Battery
        # ---------------
        self.has_central_battery = scenario.has_central_battery
        if self.has_central_battery:
            self.battery = Battery(scenario=scenario,
                                   battery_id=scenario.central_battery_id,
                                   battery_strategy=scenario.central_battery_strategy,
                                   battery_capacity=scenario.central_battery_capacity_kWh)

        # --------------------
        # Individual Batteries
        # --------------------
        self.cum_ind_bat_charge = np.zeros(self.ts.get_num_steps())
        self.tot_ind_bat_capacity = 0
        self.any_resident_has_battery = False
        self.any_householder_has_battery = False

        # CP battery
        # ----------
        if 'cp_battery_id' in scenario.parameters and 'cp_battery_strategy' in scenario.parameters:
            if not pd.isnull(scenario.parameters['cp_battery_id']) and \
                    not pd.isnull(scenario.parameters['cp_battery_strategy']):
                self.resident['cp'].has_battery = True
                self.any_resident_has_battery = True  # NB 'resident' here means householder or cp
                self.battery_list = ['cp']
                scenario.has_ind_batteries = 'True'
                cp_battery_capacity_kWh = 1
                # Scalable battery:
                if 'cp_battery_capacity_kWh' in scenario.parameters:
                    if not pd.isnull(scenario.parameters['cp_battery_capacity_kWh']):
                        cp_battery_capacity_kWh = scenario.parameters['cp_battery_capacity_kWh']
                # Initialise battery:
                self.resident['cp'].battery = Battery(scenario=scenario,
                                                      battery_id=scenario.parameters['cp_battery_id'],
                                                      battery_strategy=scenario.parameters['cp_battery_strategy'],
                                                      battery_capacity=cp_battery_capacity_kWh)
                self.tot_ind_bat_capacity += self.resident['cp'].battery.capacity_kWh
            else:
                self.resident['cp'].has_battery = False
        else:
            self.resident['cp'].has_battery = False

        # Household batteries - all the same
        # ----------------------------------
        bat_name = 'all_battery_id'
        bat_strategy = 'all_battery_strategy'
        if bat_name in scenario.parameters and bat_strategy in scenario.parameters and \
                not pd.isnull(scenario.parameters[bat_name]) and \
                not pd.isnull(scenario.parameters[bat_strategy]):
            self.any_resident_has_battery = True
            self.any_householder_has_battery = True
            self.battery_list += [n for n in self.study.get_participant_names()]
            scenario.has_ind_batteries = 'True'
            all_battery_capacity_kWh = 1
            # Scalable batteries:
            if 'all_battery_capacity_kWh' in scenario.parameters:
                if not pd.isnull(scenario.parameters['all_battery_capacity_kWh']):
                    all_battery_capacity_kWh = scenario.parameters['all_battery_capacity_kWh']
            for c in self.study.get_participant_names():
                self.resident[c].battery = Battery(scenario=scenario,
                                                   battery_id=scenario.parameters[bat_name],
                                                   battery_strategy=scenario.parameters[bat_strategy],
                                                   battery_capacity=all_battery_capacity_kWh)
                self.resident[c].has_battery = True
                self.tot_ind_bat_capacity += self.resident[c].battery.capacity_kWh

        # Household batteries - separately defined
        # ----------------------------------------
        elif scenario.has_ind_batteries != 'none':
            for c in self.study.get_participant_names():
                
                bat_name = str(c) + '_battery_id'
                bat_strategy = str(c) + '_battery_strategy'
                bat_capacity = str(c) + '_battery_capacity_kWh'
                battery_capacity_kWh = 1
                if bat_name in scenario.parameters and bat_strategy in scenario.parameters:
                    if not pd.isnull(scenario.parameters[bat_name]) and \
                            not pd.isnull(scenario.parameters[bat_strategy]):
                        self.resident[c].has_battery = True
                        self.any_resident_has_battery = True
                        self.any_householder_has_battery = True
                        self.battery_list.append(c)
                        scenario.has_ind_batteries = 'True'
                        # Scalable battery:
                        if bat_capacity in scenario.parameters:
                            if not pd.isnull(scenario.parameters[bat_capacity]):
                                battery_capacity_kWh = scenario.parameters[bat_capacity]
                    self.resident[c].battery = Battery(scenario=scenario,
                                                       battery_id=scenario.parameters[bat_name],
                                                       battery_strategy=scenario.parameters[bat_strategy],
                                                       battery_capacity=battery_capacity_kWh)
                    self.tot_ind_bat_capacity += self.resident[c].battery.capacity_kWh
                else:
                    self.resident[c].has_battery = False
            else:
                self.resident[c].has_battery = False

        # No individual household batteries
        # ---------------------------------
        else:
            for c in self.study.get_participant_names():
                self.resident[c].has_battery = False
            self.any_householder_has_battery = False

        # Flag battery arrangements that don't exist in the model:
        # --------------------------------------------------------
        if 'btm' in scenario.arrangement and self.has_central_battery:
            logging.info('***************Warning!!! Scenario %s has btm arrangement with central battery \
                       - not included in this model', str(scenario.name))
            print('***************Warning!!! Scenario %s has btm arrangement with central battery \
                       - not included in this model', str(scenario.name))
        if 'cp_only' in scenario.arrangement and self.any_householder_has_battery:
            logging.info('***************Warning!!! Scenario %s has cp_only arrangement with unit battery(s) \
                                   - not included in this model', str(scenario.name))
            print('***************Warning!!! Scenario %s has cp_only arrangement with unit battery(s) \
                                   - not included in this model', str(scenario.name))

        if 'cp_only' in scenario.arrangement and self.has_central_battery:
            logging.info('***************Warning!!! Scenario %s has cp_only arrangement with central battery(s) \
                                          - not included in this model', str(scenario.name))
            logging.info('*************** For cp_only with battery, use cp_battery *******************')
            print('***************Warning!!! Scenario %s has cp_only arrangement with central battery(s) \
                                          - not included in this model', str(scenario.name))

        if ('bau' == scenario.arrangement) and (self.any_resident_has_battery or self.has_central_battery):
            logging.info('***************Warning!!! Scenario %s is bau with battery(s) \
                                   - please use `bau_bat`', str(scenario.name))
            print('***************Warning!!! Scenario %s is bau with battery(s) \
                                    - please use `bau_bat`', str(scenario.name))

    def resetAllBatteries(self, scenario):
        """reset batteries to new as required."""
        # Central Battery
        # ---------------
        if self.has_central_battery:
            # self.battery.reset(annual_load=np.array(self.network_load.sum(axis=1)))
            self.battery.reset(annual_load=np.array(self.nl_profile.get_aggregate_data()))
        # Individual Batteries
        # --------------------
        self.cum_ind_bat_charge = np.zeros(self.ts.get_num_steps())
        # self.tot_ind_bat_capacity = 0
        # self.any_resident_has_battery = False
        if self.any_resident_has_battery:
            for c in self.battery_list:
                self.resident[c].battery.reset(annual_load=self.resident[c].load)
            # NB ###@@@@@ check max here for ind bats
        self.total_battery_losses = 0

    def calcBuildingStaticEnergyFlows(self):
        """Calculate all internal energy flows for all timesteps (no storage or dm)."""

        # Calculate flows for each resident and cumulative values for ENO
        for c in self.study.get_participant_names():
            self.resident[c].calc_static_energy()
            # Cumulative load and generation are what the "ENO" presents to the retailer:
            self.cum_resident_imports += self.resident[c].imports
            self.cum_resident_exports += self.resident[c].exports
            # Cumulative local imports are load presented to solar_retailer (in btm_s PPA scenario)
            self.cum_local_imports += self.resident[c].solar_allocation

        # Calculate aggregate flows for ENO
        self.flows = self.generation + self.cum_resident_exports - self.cum_resident_imports
        self.exports = self.flows.clip(0)
        self.imports = (-1 * self.flows).clip(0)
        pass

    def calcAllDemandCharges(self):
        """Calculates demand charges for ENO and for all residents."""
        self.calc_demand_charge()
        for c in self.study.get_participant_names() + ['cp']:
            self.resident[c].calc_demand_charge()
        self.retailer.calc_demand_charge()

    def calcBuildingDynamicEnergyFlows(self, step):
        """Calculate all internal energy flows for SINGLE timestep (with storage)."""

        # ---------------------------------------------------------------
        # Calculate flows for each resident and cumulative values for ENO
        # ---------------------------------------------------------------
        for c in self.study.get_participant_names():
            # Calc flows (inc battery dispatch) for each resident
            # ---------------------------------------------------
            self.resident[c].calc_dynamic_energy(step)
            # Cumulative load and generation are what the "ENO" presents to the retailer:
            self.cum_resident_imports[step] += self.resident[c].imports[step]
            self.cum_resident_exports[step] += self.resident[c].exports[step]
            # Log cumulative charge state and amount of discharge (charge)
            if self.resident[c].has_battery:
                self.cum_ind_bat_charge[step] += self.resident[c].battery.charge_level_kWh

        # ----------------------------------------------------------------------------------------
        # Calculate energy flow without central  battery, then modify by calling battery.dispatch:
        # ----------------------------------------------------------------------------------------
        self.flows[step] = self.generation[step] \
                           + self.cum_resident_exports[step] \
                           - self.cum_resident_imports[step]
        if self.has_central_battery:
            self.flows[step] = self.battery.dispatch(generation=self.generation[step] + self.cum_resident_exports[step],
                                                     load=self.cum_resident_imports[step],
                                                     step=step)
        else:
            self.flows[step] = self.generation[step] \
                               + self.cum_resident_exports[step] \
                               - self.cum_resident_imports[step]
        # Calc imports and exports
        # ------------------------
        self.exports[step] = self.flows[step].clip(0)
        self.imports[step] = (-1 * self.flows[step]).clip(0)

    def allocateAllCapex(self, scenario):
        """ Allocates capex repayments and opex to customers according to arrangement"""
        # For some arrangements, this depends on pv allocation, so must FOLLOW allocatePV call
        # Called once per load profile where capex is allocated according to load; once per scenario otherwise
        # Moved from start of iterations to end to incorporate battery lifecycle impacts

        # Initialise all to zero:
        # -----------------------
        self.en_opex = 0
        self.pv_capex_repayment = 0
        self.en_capex_repayment = 0
        self.bat_capex_repayment = 0
        scenario.total_battery_capex_repayment = 0

        # Individual battery capex:
        # -------------------------
        for c in self.study.get_participant_names() + ['cp']:
            self.resident[c].pv_capex_repayment = 0
            self.resident[c].bat_capex_repayment = 0
            if self.resident[c].has_battery:
                self.resident[c].bat_capex = self.resident[c].battery.calcBatCapex()
                self.resident[c].bat_capex_repayment = -12 * np.pmt(rate=scenario.a_rate / 12,
                                                                    nper=12 * scenario.a_term,
                                                                    pv=self.resident[c].bat_capex,
                                                                    fv=0,
                                                                    when='end')
                scenario.total_battery_capex_repayment += self.resident[c].bat_capex_repayment
            else:
                self.resident[c].bat_capex_repayment = 0

        # Central battery capex
        # ---------------------
        if self.has_central_battery:
            central_bat_capex = self.battery.calcBatCapex()
        else:
            central_bat_capex = 0
            central_bat_capex_repayment = 0
        if central_bat_capex > 0:
            central_bat_capex_repayment = -12 * np.pmt(rate=scenario.a_rate / 12,
                                                       nper=12 * scenario.a_term,
                                                       pv=central_bat_capex,
                                                       fv=0,
                                                       when='end')
        else:
            central_bat_capex_repayment = 0
        scenario.total_battery_capex_repayment += central_bat_capex_repayment

        # Allocate network, pv and battery capex & opex payments depending on network arrangements
        # ----------------------------------------------------------------------------------------
        # TODO Allocation of capex needs refining. e.g in some `btm_s` arrangements, capex is payable by owners, not residents
        if 'en' in scenario.arrangement:
            # For en, all capex & opex are borne by the ENO
            self.en_opex = scenario.en_opex
            self.pv_capex_repayment = scenario.pv_capex_repayment
            self.en_capex_repayment = scenario.en_capex_repayment
            self.bat_capex_repayment = central_bat_capex_repayment

        elif 'cp_only' in scenario.arrangement:
            # pv and central battery capex allocated to customer 'cp' (ie strata)
            self.resident['cp'].pv_capex_repayment = scenario.pv_capex_repayment
            self.resident['cp'].bat_capex_repayment += central_bat_capex_repayment

        elif 'btm_i' in scenario.arrangement:
            # For btm_i apportion pv AND central bat capex costs according to pv allocation
            
            pv_customers = [c for c in self.study.get_participant_names() if self.pv.get_system_sum(self.study.get_solar_profile(c)) > 0]
            for c in pv_customers:
                pv_id = self.study.get_solar_profile(c)
                # self.resident[c].pv_capex_repayment = self.pv.data[c].sum() / self.pv.data.sum().sum() * scenario.pv_capex_repayment
                self.resident[c].pv_capex_repayment = self.pv.get_system_sum(pv_id) / self.pv.get_aggregate_sum() * scenario.pv_capex_repayment
                # self.resident[c].bat_capex_repayment += self.pv.data[c].sum() / self.pv.data.sum().sum() * central_bat_capex_repayment
                self.resident[c].bat_capex_repayment += self.pv.get_system_sum(pv_id) / self.pv.get_aggregate_sum() * central_bat_capex_repayment

        elif 'btm_s_c' in scenario.arrangement:
            # For btm_s_c, apportion capex costs equally between units and cp.
            # (Not ideal - needs more sophisticated analysis of practical btm_s arrangements)
            for c in self.study.get_participant_names():
                self.resident[c].pv_capex_repayment = scenario.pv_capex_repayment / len(self.study.get_participant_names())
                self.resident[c].en_capex_repayment = scenario.en_capex_repayment / len(self.study.get_participant_names())
                self.resident[c].en_opex = scenario.en_opex / len(self.study.get_participant_names())
                self.resident[c].bat_capex_repayment += central_bat_capex_repayment / len(self.study.get_participant_names())

        elif 'btm_s_u' in scenario.arrangement:
            # For btm_s_u, apportion capex costs equally between units only
            # (Not ideal - needs more sophisticated analysis of practical btm_s arrangements)
            for c in self.study.get_participant_names():
                self.resident[c].pv_capex_repayment = scenario.pv_capex_repayment / len(self.study.get_participant_names())
                self.resident[c].en_opex = scenario.en_opex / len(self.study.get_participant_names())
                self.resident[c].en_capex_repayment = scenario.en_capex_repayment / len(self.study.get_participant_names())
                self.resident[c].bat_capex_repayment += central_bat_capex_repayment / len(self.study.get_participant_names())

        elif 'btm_p' in scenario.arrangement:
            # all solar and btm capex costs paid by solar retailer
            self.solar_retailer.pv_capex_repayment = scenario.pv_capex_repayment
            self.solar_retailer.en_capex_repayment = scenario.en_capex_repayment
            self.solar_retailer.en_opex = scenario.en_opex
            self.solar_retailer.bat_capex_repayment = central_bat_capex_repayment
        pass

    def calcEnergyMetrics(self, scenario):

        # -----------------------------------------------
        # calculate total exports / imports & pvr, cpr
        # ----------------------------------------------
        if 'bau' in scenario.arrangement or 'cp_only' in scenario.arrangement or 'btm' in scenario.arrangement:
            # Building export is sum of customer exports
            # Building import is sum of customer imports
            self.total_building_export = 0
            self.total_import = 0
            for c in self.study.get_participant_names():
                self.total_building_export += self.resident[c].exports.sum()
                self.total_import += self.resident[c].imports.sum()
        elif 'en' in scenario.arrangement:
            # For en scenarios, import and exports are aggregated:
            self.total_building_export = self.exports.sum()
            self.total_import = self.imports.sum()

        # self.pv_ratio = self.pv.data.sum().sum() / self.total_building_load * 100
        self.pv_ratio = self.pv.get_aggregate_sum() / self.total_building_load * 100
        self.cp_ratio = self.resident['cp'].load.sum() / self.total_building_load * 100

        # ----------------------------------------------------------------------
        # Calc sum of battery losses & discharge across all batteries in network
        # ----------------------------------------------------------------------
        if self.has_central_battery:
            self.central_battery_capacity = self.battery.capacity_kWh
            self.total_battery_losses += self.battery.cumulative_losses
            self.battery_cycles = self.battery.number_cycles
            self.battery_SOH = self.battery.SOH
            self.total_discharge = self.battery.net_discharge
        else:
            self.central_battery_capacity = 0
            self.battery_cycles = 0
            self.battery_SOH = 0
            self.total_discharge = np.zeros(self.ts.get_num_steps())

        for c in self.battery_list:
            self.total_battery_losses += self.resident[c].battery.cumulative_losses
            self.total_discharge += self.resident[c].battery.net_discharge
        # ----------------------------------------------
        # Calculate Self-Consumption & Self-Sufficiency
        # ----------------------------------------------
        # 1) Luthander method: accounts correctly for battery losses
        # ----------------------------------------------------------
        # Calculate coincidence (ie overlap of load and generation profiles accounting for battery losses)
        # ...for individual or btm PV:
        if self.pv_exists:
            for c in self.study.get_participant_names():
                if self.resident[c].has_battery:
                    self.resident[c].coincidence = np.minimum(self.resident[c].load,
                                                              self.resident[c].generation +
                                                              self.resident[c].battery.net_discharge)
                else:
                    self.resident[c].coincidence = np.minimum(self.resident[c].load,
                                                              self.resident[c].generation)
                self.sum_of_coincidences += self.resident[c].coincidence
            # ... for central PV:
            self.total_aggregated_coincidence = np.minimum(self.nl_profile.get_aggregate_data(), pd.Series(self.pv.get_data('central')) + self.total_discharge)

            if 'en_pv' in scenario.arrangement:
                self.self_consumption = np.sum(self.total_aggregated_coincidence) / self.pv.get_aggregate_sum() * 100
                self.self_sufficiency = np.sum(self.total_aggregated_coincidence) / self.total_building_load * 100
            else:
                self.self_consumption = np.sum(self.sum_of_coincidences) / self.pv.get_aggregate_sum() * 100
                self.self_sufficiency = np.sum(self.sum_of_coincidences) / self.total_building_load * 100
        else:
            self.self_consumption = 100
            self.self_sufficiency = 0

        # 2) OLD VERSIONS - for checking. Same for non battery scenarios and for SS
        # -------------------------------------------------------------------------
        if scenario.pv_exists:
            self.self_consumption_OLD = 100 - (self.total_building_export / self.pv.get_aggregate_sum() * 100)
            self.self_sufficiency_OLD = 100 - (self.total_import / self.total_building_load * 100)
        else:
            self.self_consumption_OLD = 100  # NB No PV implies 100% self consumption
            self.self_sufficiency_OLD = 0

    def logTimeseriesDetailed(self, scenario):
        """Logs timeseries data for whole building to csv file."""

        timedata = pd.DataFrame(index=pd.DatetimeIndex(data=self.ts.get_date_times()))
        timedata['network_load'] = self.nl_profile.get_aggregate_data()
        timedata['pv_generation'] = self.pv.get_aggregate_data()
        timedata['grid_import'] = self.imports
        timedata['grid_export'] = self.exports
        timedata['sum_of_customer_imports'] = self.cum_resident_imports
        timedata['sum_of_customer_exports'] = self.cum_resident_exports

        if scenario.has_central_battery:
            timedata['battery_SOC'] = self.battery.SOC_log
            timedata['battery_charge_kWh'] = self.battery.SOC_log * self.battery.capacity_kWh / 100
        if scenario.has_ind_batteries == 'True':
            timedata['ind_battery_SOC'] = self.cum_ind_bat_charge / self.tot_ind_bat_capacity * 100
       

        time_file = os.path.join(self.study.timeseries_path,
                                 self.scenario.label + '_' +
                                 scenario.arrangement + '_' +
                                 self.load_name)
        util.df_to_csv(timedata, time_file)

    def logTimeseriesBrief(self, scenario):
        """Logs basic timeseries data for whole building to csv file."""

        timedata = pd.DataFrame(index=pd.DatetimeIndex(data=self.ts.get_date_times()))
        # timedata['network_load'] = self.network_load.sum(axis=1)
        timedata['network_load'] = self.network_load.get_aggregate_data()
        # timedata['pv_generation'] = self.pv.sum(axis=1)
        timedata['grid_import'] = self.imports
        # timedata['grid_export'] = self.exports
        timedata['sum_of_customer_imports'] = self.cum_resident_imports
        # timedata['sum_of_customer_exports'] = self.cum_resident_exports

        time_file = os.path.join(self.study.timeseries_path,
                                 self.scenario.label + '_' +
                                 scenario.arrangement + '_' +
                                 self.load_name)
        util.df_to_csv(timedata, time_file)