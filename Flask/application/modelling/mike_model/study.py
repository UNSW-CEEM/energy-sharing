import os
import logging
import sys
import pandas as pd
import numpy as np

from ..mike_model import en_utilities as util

from ..mike_model.network import Network
from ..mike_model.scenario import Scenario
from ..mike_model.tariff_data import TariffData
from ..mike_model.timeseries import Timeseries
from ..mike_model.load import LoadCollection


class Study:
    """A set of different scenarios to be compared."""

    def __init__(self,
                 base_path,
                 project,
                 study_name,
                 
                 ):
        
        # --------------------------------
        # Set up paths and files for Study
        # --------------------------------
        # All input and output datafiles are located relative to base_path and base_path\project
        self.base_path = base_path
        self.name = study_name
        self.project_path = os.path.join(self.base_path, 'studies', project)

        self.use_threading = False

        # reference files
        # ---------------
        self.reference_path = os.path.join(self.base_path, 'reference')  # 'reference_TEST'
        self.input_path = os.path.join(self.project_path, 'inputs')
        tariff_name = 'tariff_lookup.csv'
        self.t_lookupFile = os.path.join(self.reference_path, tariff_name)
        capex_pv_name = 'capex_pv_lookup.csv'
        self.capexpv_file = os.path.join(self.reference_path, capex_pv_name)
        capex_en_name = 'capex_en_lookup.csv'
        self.capexen_file = os.path.join(self.reference_path, capex_en_name)
        battery_lookup_name = 'battery_lookup.csv'
        self.battery_file = os.path.join(self.reference_path, battery_lookup_name)
        battery_strategies_name = 'battery_control_strategies.csv'
        self.battery_strategies_file = os.path.join(self.reference_path, battery_strategies_name)
        dst_lookup_name = 'dst_lookup.csv'
        self.dst_file = os.path.join(self.reference_path, dst_lookup_name)

        # study file contains all scenarios
        # ---------------------------------
        study_filename = 'study_' + study_name + '.csv'
        study_file = os.path.join(self.input_path, study_filename)

        # --------------------
        # read study scenarios
        # --------------------
        self.study_parameters = pd.read_csv(study_file)
        self.study_parameters.set_index('scenario', inplace=True)
        self.scenario_list = [s for s in self.study_parameters.index if not pd.isnull(s)]
        # Read list of output requirements and strip from df

        if 'output_types' in self.study_parameters.columns:
            self.output_list = self.study_parameters['output_types'].dropna().tolist()
        else:
            self.output_list = []

        # --------------------------
        #  read Daylight Savings Time
        # --------------------------
        if 'dst' in self.study_parameters.columns:
            if self.study_parameters.isnull()['dst'].all():
                self.dst = 'nsw'
            else:
                self.dst = self.study_parameters['dst'].drop_duplicates().tolist()[0]
        else:
            self.dst = 'nsw'
        temp_df = pd.read_csv(self.dst_file, index_col=[0])
        cols = temp_df.columns.tolist()
        self.dst_lookup = pd.read_csv(self.dst_file, index_col=[0], parse_dates=cols, dayfirst=True)
        pass

        # -------------------
        # Set up output paths
        # -------------------
        override_output = False
        if override_output:
            self.output_path = override_output
        else:
            self.output_path = os.path.join(self.project_path, 'outputs')
        
        os.makedirs(self.output_path, exist_ok=True)
        self.output_path = os.path.join(self.output_path, study_name)
        os.makedirs(self.output_path, exist_ok=True)
        self.scenario_path = os.path.join(self.output_path, 'scenarios')
        os.makedirs(self.scenario_path, exist_ok=True)
        if 'log_timeseries_detailed' in self.output_list:
            self.timeseries_path = os.path.join(self.output_path, 'timeseries_d')
            os.makedirs(self.timeseries_path, exist_ok=True)
        if 'log_timeseries_brief' in self.output_list:
            self.timeseries_path = os.path.join(self.output_path, 'timeseries_b')
            os.makedirs(self.timeseries_path, exist_ok=True)

        # --------------
        #  Locate pv data
        # --------------
        self.pv_path = os.path.join(self.base_path, 'pv_profiles')
        if os.path.exists(self.pv_path):
            self.pv_list = os.listdir(self.pv_path)
            if len(self.pv_list) > 0:
                self.pv_exists = True
            else:
                self.pv_exists = False
                logging.info('************Missing PV Profile ***************')
                sys.exit("Missing PV data")
        else:
            self.pv_exists = False
            logging.info('************Missing PV Profile ***************')
            sys.exit("Missing PV data")
        # --------------------------------------
        #  read capex costs into reference tables
        # --------------------------------------
        self.en_capex = pd.read_csv(self.capexen_file,
                                    dtype={'site_capex': np.float64,
                                           'unit_capex': np.float64,
                                           'site_opex': np.float64,
                                           'unit_opex': np.float64,
                                           })
        self.en_capex.loc[:, ['site_capex', 'unit_capex', 'site_opex', 'unit_opex']] \
            = self.en_capex.loc[:, ['site_capex', 'unit_capex', 'site_opex', 'unit_opex']].fillna(0.0)
        self.en_capex = self.en_capex.set_index('en_capex_id')
        if self.pv_exists:
            self.pv_capex_table = pd.read_csv(self.capexpv_file,
                                              dtype={'pv_capex': np.float64,
                                                     'inverter_cost': np.float64,
                                                     'inverter_life': np.float64,
                                                     })
            self.pv_capex_table = self.pv_capex_table.set_index('pv_cap_id')
            self.pv_capex_table.loc[:, ['pv_capex', 'inverter_cost']] \
                = self.pv_capex_table.loc[:, ['pv_capex', 'inverter_cost']].fillna(0.0)
        # ----------------------------------
        # read battery data into tariff_lookup file
        # ----------------------------------
        self.battery_lookup = pd.read_csv(self.battery_file, index_col='battery_id')
        self.battery_strategies = pd.read_csv(self.battery_strategies_file, index_col='battery_strategy')

        # -------------------
        #  Identify load data
        # -------------------
        if len(self.study_parameters['load_folder'].unique()) == 1:
            self.different_loads = False  # Same load or set of loads for each scenario
        else:
            self.different_loads = True  # Different loads for each scenario

        self.load_path = os.path.join(self.base_path, 'load_profiles',
                                      self.study_parameters.loc[self.study_parameters.index[0], 'load_folder'])
        self.load_list = os.listdir(self.load_path)
        if len(self.load_list) == 0:
            logging.info('***************** Load folder %s is empty *************************', self.load_path)
            sys.exit("Missing load data")
        elif len(self.load_list) == 1:
            self.multiple_loads = False  # single load profile for each scenario
        else:
            self.multiple_loads = True  # multiple load profiles for each scenario - outputs are mean ,std dev, etc.

        # ---------------------------------------------
        # If same loads throughout Study, get them now:
        # ---------------------------------------------
        # self.load_profiles = {}
        self.load_profiles = LoadCollection()
        if not self.different_loads:
            for profile_name in self.load_list:
                load_file = os.path.join(self.load_path, profile_name)
                temp_load = pd.read_csv(load_file,
                                        parse_dates=['timestamp'],
                                        dayfirst=True)
                temp_load = temp_load.set_index('timestamp')
                if 'cp' not in temp_load.columns:
                    temp_load['cp'] = 0
                # self.load_profiles.profiles[profile_name] = temp_load
                self.load_profiles.add_profile_from_df(temp_load, profile_name)

        # Otherwise, get the first load anyway:#@
        # -------------------------------------
        else:
            load_file = os.path.join(self.load_path, self.load_list[0])
            temp_load = pd.read_csv(load_file,
                                    parse_dates=['timestamp'],
                                    dayfirst=True)
            # self.load_profiles.profiles[self.load_list[0]] = temp_load.set_index('timestamp')
            profile_name = self.load_list[0]
            self.load_profiles.add_profile_from_df(temp_load.set_index('timestamp'),profile_name)

        # -----------------------------------------------------------------
        # Use first load profile to initialise timeseries and resident_list
        # -----------------------------------------------------------------
        # Initialise timeseries
        # ---------------------
        # TODO More globals. ts_ng = timeseries not global
        # global ts  # (assume timeseries are all the same for all load profiles)
        self.ts_ng = Timeseries(
            # load=self.load_profiles.profiles[self.load_list[0]],
            load=self.load_profiles.get_profile(self.load_list[0]).to_df(),
            dst_lookup=self.dst_lookup,
            dst_region='nsw')

        # Lists of meters / residents (includes cp)
        # -----------------------------------------
        # This is used for initialisation (and when different_loads = FALSE),
        # but RESIDENT_LIST CAN VARY for each scenario:
        # list of potential child meters - residents + cp
        # temp_list = list(self.load_profiles.profiles[self.load_list[0]].columns.values)
        
        profile_name = self.load_list[0]
        temp_list = self.load_profiles.get_profile(profile_name).get_participant_names()
        
        self.resident_list = []

        for i in temp_list:
            if type(i) == 'str':
                self.resident_list += [i]
            else:
                self.resident_list += [str(i)]
        # ---------------------------------------------------------------
        # Initialise Tariff Look-up table and generate all static tariffs
        # ---------------------------------------------------------------
        parameter_list = self.study_parameters.values.flatten().tolist()

        self.tariff_data = TariffData(
            tariff_lookup_path=self.t_lookupFile,
            output_path=self.output_path,
            parameter_list=parameter_list,
            ts=self.ts_ng)

        self.tariff_data.generateStaticTariffs()
        # -----------------------------
        # Initialise output data frames:
        # -----------------------------
        self.op = pd.DataFrame(index=self.scenario_list)

    def log_study_data(self):
        """Saves study outputs and summary to .csv files."""

        # For ease of handling, 3 csv files are created:
        # results_ has key values for all scenarios, averaged across multiple load profiles
        # customer_results has individual customer bills and total costs
        # results_std_dev has standard deviations of all averaged values
        # idex by scenario:

        self.op.index.name = 'scenario'
        # Separate individual customer data and save as csv
        if not self.different_loads:
            op_customer = self.op[[c for c in self.op.columns if 'cust_' in c and 'cp' not in c]]
            self.op = self.op.drop(op_customer.columns, axis=1)
            op_customer_file = os.path.join(self.output_path, self.name + '_customer_results.csv')
            util.df_to_csv(op_customer, op_customer_file)

        # Separate standard deviations and save as csv
        op_std = self.op[[c for c in self.op.columns if 'std' in c]]
        self.op = self.op.drop(op_std.columns, axis=1)
        op_std_file = os.path.join(self.output_path, self.name + '_results_std_dev.csv')
        util.df_to_csv(op_std, op_std_file)

        # Save remaining results for all scenarios
        op_file = os.path.join(self.output_path, self.name + '_results.csv')
        util.df_to_csv(self.op, op_file)

    def get_scenario_list(self):
        return self.scenario_list

    def run_scenario(self, scenario_name):
        """ This is the main body of script."""
        print("Running Scenario number", scenario_name)
        logging.info("Running Scenario number %i ", scenario_name)
        # Initialise scenario
        scenario = Scenario(scenario_name=scenario_name, study=self, timeseries=self.ts_ng)
        eno = Network(scenario=scenario, study=self, timeseries=self.ts_ng)
        # N.B. in embedded network scenarios, eno is the actual embedded network operator,
        # but in other scenarios, it is a virtual intermediary to organise energy and cash flows
        eno.initialiseAllTariffs(scenario)
        eno.initialiseAllBatteries(scenario)

        # Set up pv profile if allocation not load-dependent
        if scenario.pv_allocation == 'fixed':
            eno.allocatePV(scenario, scenario.pv)

        # if scenario.has_solar_block:
        #     eno.initialiseDailySolarBlockQuotas(scenario)

        # Iterate through all load profiles for this scenario:
        for load_name in scenario.load_list:
            eno.initialise_building_loads(load_name, scenario)
            if scenario.pv_allocation == 'load_dependent':  # ie. for btm_i_c, btm_s and btm_p arrangements
                eno.allocatePV(scenario, scenario.pv)
            # eno.initialiseSolarInstQuotas(scenario)  # depends on load and pv - not implemented. Solar Inst for EN

            # If no battery, calc all internal energy flows statically (i.e. as single df calculation)
            # ----------------------------------------------------------------------------------------
            if not eno.has_central_battery and not eno.any_resident_has_battery:
                eno.calcBuildingStaticEnergyFlows()
            else:
                # If battery, reset then calculate energy flows stepwise:
                # -------------------------------------------------------
                eno.resetAllBatteries(scenario)
                for step in np.arange(0, self.ts_ng.get_num_steps()):
                    eno.calcBuildingDynamicEnergyFlows(step)

            # Energy Flows for retailer (static)
            # -----------------------------------
            # retailer acts like a customer too, buying from DNSP
            # These are the load and generation that it presents to DNSP
            eno.retailer.initialise_customer_load(eno.imports)
            eno.retailer.initialise_customer_pv(eno.exports)
            eno.retailer.calc_static_energy()

            # Summary energy metrics
            # ----------------------lo
            eno.calcEnergyMetrics(scenario)

            # Financial's
            # ----------
            eno.calcAllDemandCharges()
            # per load profile to allow for scenarios where capex allocation depends on load
            eno.allocateAllCapex(scenario)
            # If tariffs are dynamic (e.g block), calculate them stepwise:
            # ------------------------------------------------------------

            scenario.calcFinancials(eno)
            scenario.collate_network_results(eno)
            if scenario.log_timeseries_detailed:
                eno.logTimeseriesDetailed(scenario)
            if scenario.log_timeseries_brief:
                eno.logTimeseriesBrief(scenario)

        # collate / log data for all loads in scenario
        # TODO Work out how to remove this global.
        if self.use_threading is 'True':
            with lock:
                scenario.log_scenario_data()
        else:
            scenario.log_scenario_data()

        logging.info('Completed Scenario %i', scenario_name)
