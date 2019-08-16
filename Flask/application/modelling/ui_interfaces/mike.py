# UI Input parsing modules
from .central_battery import CentralBattery as Ui_Central_Battery
from .central_solar import CentralSolar as Ui_Central_Solar
from .tariffs import Tariffs as Ui_Tariffs
from .participants import Participants as Ui_Participants
from .result_parsers import ResultParsers as Ui_Results_Parsers
from application.folder_routes import FolderRoutes as FolderRoutes
# from .csv_helpers import create_csvs

# Luomi Modules
from ..luomi_model.network import Network as Luomi_Network
from ..luomi_model.battery import Central_Battery as Luomi_Central_Battery
from ..luomi_model.tariffs import Tariffs as Luomi_Tariffs
from ..luomi_model.results import Results
from ..luomi_model import energy_sim, financial_sim, util

# Mike Modules
from ..mike_model.new_sim import NewSim

import os
import datetime
import pandas as pd
import pendulum
import json


class MikeWrapper:
    def __init__(self):
        
        # Folder Routes
        self.folder_routes = FolderRoutes()

        # Model setup parameters
        self.model_type = 'mike'
        self.network_name = 'Default_Network'
        self.network_type = 'embedded_network'
        self.data_dir = self.folder_routes.get_route('data_dir')

        # UI Interface objects
        self.ui_participants = Ui_Participants(self.folder_routes)
        self.ui_tariffs = None
        self.ui_finances = None
        self.ui_central_battery = Ui_Central_Battery(self.folder_routes)
        self.ui_central_solar = Ui_Central_Solar(self.folder_routes)
        self.ui_results_parser = Ui_Results_Parsers(self.folder_routes)

        # Model Objects
        self.model_network = None
        self.model_central_battery = None
        self.model_tariffs = None
        self.model_time_periods = None
        self.model_results = None

        # Mike Model Objects
        self.mike_model = None

        # Legacy Stuff.
        self.time_periods = None

        self.ui_inputs = None

    def load(self, ui_inputs):
        load_functions = [
            self.load_model_selection,
            self.load_network_name,
            self.load_central_services,
            self.load_tariffs,
            self.load_participants,
            self.load_data_sources,
            self.load_study_parameters,
        ]

        for each in load_functions:
            each(ui_inputs)
        self.ui_inputs = ui_inputs

    def load_model_selection(self, ui_inputs):
        if 'model_selection' in ui_inputs:
            inputs = ui_inputs['model_selection']
            self.model_type = inputs['model_type'] if 'model_type' in inputs else None
            self.network_type = inputs['network_type'] if 'network_type' in inputs else None

    def load_network_name(self, ui_inputs):
        key = "network_name"
        if key in ui_inputs:
            self.network_name = ui_inputs[key]

    def load_central_services(self, ui_inputs):
        key = "central_services"
        if key in ui_inputs:
            print(ui_inputs[key])
            self.ui_central_battery.load(ui_inputs[key])

    def load_tariffs(self, ui_inputs):
        # print("mike.py/load_tariffs()", ui_inputs['model_tariffs_mike'])
        self.ui_tariffs = ui_inputs['model_tariffs_mike']
        # self.ui_tariffs = [
        #     {
        #         'name':'user_interface',
        #         'daily_fixed_rate': 1,
        #         'static_imports':[
        #             {
        #                 'start_hr':7,
        #                 'end_hr':10,
        #                 'price':0.3
        #             },
        #             {
        #                 'start_hr':10,
        #                 'end_hr':15,
        #                 'price':0.5
        #             },
        #             {
        #                 'start_hr':15,
        #                 'end_hr':18,
        #                 'price':0.3
        #             },
        #         ],
        #         'static_solar_imports':[],
        #         'static_exports':[]
        #     }
        # ]

    def load_study_parameters(self, ui_inputs):
        if 'study_parameters_mike' in ui_inputs:
            self.study_parameters = ui_inputs['study_parameters_mike']
        # self.study_parameters = {
        #     'scenario': 1,
        #     'arrangement':'en_pv',
        #     'pv_cap_id': 'W_max_yield',
        #     'pv_capex_scaleable':False,
            
        #     'en_capex_id':'capex_med',
        #     'a_term':20,
        #     'a_rate':0.06,
        #     'pv_scaleable':False,
        #     'pv_kW_peak':'',
        #     'notes':'',
        #     'tariffs':{
        #         'cp':'TIDNULL',
        #         'all_residents':'STC_20',
        #         'parent': 'EA305_TOU12',
        #         'network_tariff':'EA305',
        #     }
        # }

    def load_participants(self, ui_inputs):
        ui_participants = {}
        if "model_participants_mike" in ui_inputs:
            for row in ui_inputs["model_participants_mike"]:
                row_selections = {}
                for row_input in row['row_inputs']:
                    if row_input['name'] == 'participant_id':
                        row_selections['participant_id'] = row_input['value']
                    if row_input['name'] == 'retail_tariff_type':
                        row_selections['tariff'] = row_input['value']
                    if row_input['name'] == 'load_profile':
                        row_selections['load'] = row_input['value']
                    if row_input['name'] == 'solar_profile':
                        row_selections['solar'] = row_input['value']
                
                ui_participants[row_selections['participant_id']] = row_selections
        # print("mike.py/load_participants()",ui_participants)
        self.ui_participants = ui_participants
        # self.ui_participants = {
        #     'Participant 1':{
        #         'load':'profile_1',
        #         'solar':'profile_1',
        #         'tariff':'user_interface',
        #     },
        #     'Participant 2':{
        #         'load':'profile_1',
        #         'solar':'profile_1',
        #         'tariff':'STC_20',
        #     },
        # }

    def load_data_sources(self, ui_inputs):
        
        if "model_data_sources_mike" in ui_inputs:
            self.solar_filename = ui_inputs['model_data_sources_mike']['selected_solar_file']
            self.load_filename = ui_inputs['model_data_sources_mike']['selected_load_file']

            # If bau or en, no solar file needed
            if ui_inputs['study_parameters_mike']['arrangement'] in ['en','bau']:
                self.solar_skiprows = 0
                self.load_skiprows = 0
            else:
                # This code figures out where the datasets need to be chopped such that they match.
                start, end = self.find_time_periods(self.solar_filename, self.load_filename)
                self.solar_skiprows = self.find_skiprows(
                    os.path.join(self.folder_routes.solar_profiles_dir, self.solar_filename),
                    start,
                    end
                )

                self.load_skiprows = self.find_skiprows(
                    os.path.join(self.folder_routes.load_profiles_dir, self.load_filename),
                    start,
                    end
                )

            # self.time_periods = util.generate_dates_in_range(start, end, 30)

    def print(self):
        print("Model Type: ", self.model_type)

    def create_objects(self):
        
        # Create the main Study object
        self.mike_model = NewSim(
            self.folder_routes, 
            self.ui_participants, 
            self.ui_tariffs, 
            self.study_parameters, 
            self.solar_filename, 
            self.load_filename,
            self.solar_skiprows,
            self.load_skiprows)
       

    def run(self, status):
        print("mike.py/run()", "Attempting Mike Model Run")
        status("Running Mike Simulation")
        self.mike_model.run()

        print("mike.py/run()", "Finished Running Mike Model")
        status("Finished Running Model. Parsing Results")
        parsed_results = self.ui_results_parser.mike_temp_parser()


        print("mike.py/run()", "Finished Parsing Results")
        status("Finished Parsing Results")
        return parsed_results

    # Might move this later.
    def find_time_periods(self, solar_filename, load_filename):

        s_file_path = os.path.join(self.folder_routes.solar_profiles_dir, solar_filename)
        l_file_path = os.path.join(self.folder_routes.load_profiles_dir, load_filename)

        s_df = pd.read_csv(s_file_path)
        l_df = pd.read_csv(l_file_path)

        s_start_string = str(s_df.head(1)["timestamp"].values[0])
        s_start = pd.datetime.strptime(s_start_string, '%d/%m/%Y %H:%M')

        l_start_string = str(l_df.head(1)["timestamp"].values[0])
        l_start = pd.datetime.strptime(l_start_string, '%d/%m/%Y %H:%M')

        s_end_string = str(s_df.tail(1)["timestamp"].values[0])
        s_end = pd.datetime.strptime(s_end_string, '%d/%m/%Y %H:%M')

        l_end_string = str(l_df.tail(1)["timestamp"].values[0])
        l_end = pd.datetime.strptime(l_end_string, '%d/%m/%Y %H:%M')

        return max(s_start, l_start), min(s_end, l_end)
    

    def find_skiprows(self, path, start, end):
        """
        This generates a skiprows array that can be passed to a pd.read_csv function.
        Given two datetimes, it searches through the dataset and determines arrays of rows to skip.
        These can be passed to pd.read_csv (ie. pd.read_csv(path, skiprows=skiprows)) and results in loading the constrained period. 
        """
        df = pd.read_csv(path)
        start_idx = 0
        end_idx = 0
        for index, row in df.iterrows():
            dt = pd.datetime.strptime(row['timestamp'], '%d/%m/%Y %H:%M')
            #print(index, row['timestamp'])
            if dt.isoformat() == start.isoformat():
                start_idx = index + 1
            if dt.isoformat() == end.isoformat():
                end_idx = index+2
        final_index = df.shape[0] + 1
        

        skiprows = list(range(1,start_idx))+list(range(end_idx,final_index))
        # trimmed_df = pd.read_csv(path, skiprows=skiprows)
        # print(trimmed_df)

        return skiprows
            


def dummy_status_callback(message):
    # my_status = "Status: " + message
    print(message)

# run with pipenv run python -m 
if __name__ == "__main__":

    p = Parameters()
    p.load_defaults()
    p.model_type = 'mike'
    p.create_objects()
    results = p.run(dummy_status_callback)
    

    # Make sure the outputs haven't changed
    expected_str = '{"total_participant_bill": {"cust_total$_W01": "1621.2177776059468", "cust_total$_W02": "1244.0590245491867", "cust_total$_W03": "1539.6694190048577", "cust_total$_W04": "1277.1697100222532", "cust_total$_W05": "1853.411473722031", "cust_total$_W06": "2396.2379833677064", "cust_total$_W07": "1313.16320065428", "cust_total$_W08": "1283.4072823120578", "cust_total$_W09": "1499.2408409905686", "cust_total$_W10": "982.6049788473111", "cust_total$_W11": "1085.8358211744755", "cust_total$_W12": "1295.751001512609", "cust_total$_W13": "1838.2146786638402", "cust_total$_W14": "1601.2267053592711", "cust_total$_W15": "2702.1448412286354", "cust_total$_W16": "1448.966625086649", "cust_total$_W17": "953.3447564128355", "cust_total$_W18": "438.4070266636045", "cust_total$_W19": "951.4354996833379", "cust_total$_W20": "1409.3640737357866", "cust_total$_W21": "2306.4447092180576", "cust_total$_W22": "1029.9172118963688", "cust_total$_W23": "964.3471644411289", "cust_total$_W24": "777.2908544895467", "cust_total$_W25": "918.9360406439156", "cust_total$_W26_A": "1364.9269853278454", "cust_total$_W27": "1528.00265447888", "cust_total$_W28": "1585.6029413094134", "cust_total$_W29": "1853.581098165551", "cust_total$_W30_A": "1364.9269853278454", "cust_total$_W31_A": "1364.9269853278454", "cust_total$_W32_A": "1364.9269853278454", "cust_total$_W33_A": "1364.9269853278454", "cust_total$_W34_A": "1364.9269853278454", "cust_total$_W35_A": "1364.9269853278454", "cust_total$_W36_A": "1364.9269853278454", "cust_total$_W37_A": "1364.9269853278454", "cust_total$_W38_A": "1364.9269853278454", "cust_total$_W39_A": "1364.9269853278454", "cust_total$_W40_A": "1364.9269853278454", "cust_total$_W41_A": "1364.9269853278454", "cust_total$_W42_A": "1364.9269853278454", "cust_total$_W43_A": "1364.9269853278454", "cust_total$_W44_A": "1364.9269853278454", "cust_total$_W45_A": "1364.9269853278454", "cust_total$_W46_A": "1364.9269853278454", "cust_total$_W47_A": "1364.9269853278454", "cust_total$_W48_A": "1364.9269853278454", "cust_total$_W49_A": "1364.9269853278454", "cust_total$_W50_A": "1364.9269853278454", "cust_total$_W51_A": "1364.9269853278454", "cust_total$_W52_A": "1364.9269853278454", "cust_total$_W53_A": "1364.9269853278454", "cust_total$_W54_A": "1364.9269853278454", "cust_total$_W55_A": "1364.9269853278454", "cust_total$_W56_A": "1364.9269853278454", "cust_total$_W57_A": "1364.9269853278454", "cust_total$_W58_A": "1364.9269853278454", "cust_total$_W59_A": "1364.9269853278454", "cust_total$_W60_A": "1364.9269853278454", "cust_total$_W61_A": "1364.9269853278454", "cust_total$_W62_A": "1364.9269853278454", "cust_total$_W63_A": "1364.9269853278454", "cust_total$_W64_A": "1364.9269853278454", "cust_total$_W65_A": "1364.9269853278454", "cust_total$_W66_A": "1364.9269853278454", "cust_total$_W67_A": "1364.9269853278454", "cust_total$_W68_A": "1364.9269853278454", "cust_total$_W69_A": "1364.9269853278454", "cust_total$_W70_A": "1364.9269853278454", "cust_total$_W71_A": "1364.9269853278454", "cust_total$_W72_A": "1364.9269853278454", "cust_total$_cp": "0.0"}, "revenue_participant": false, "revenue_retailer": false, "energy_gencon": false, "energy_cc": false}'
    expected = json.loads(expected_str)
    success = True
    for customer in results['total_participant_bill']:
        if results['total_participant_bill'][customer] != expected['total_participant_bill'][customer]:
            success = False
            print(customer,"expected", expected['total_participant_bill'][customer],"got",results['total_participant_bill'][customer])
            break
        
    if success:
        print("!!!!!!!!!!!!!!!!! Test Passed !!!!!!!!!!!!!!!!!!")
    else:
        print("<<<<<<<<<<<<<<<<<<< Test Failed >>>>>>>>>>>>>>>>>>>>>")
