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
        self.ui_tariffs = Ui_Tariffs(self.folder_routes)
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
        # key = "model_tariffs"
        # if key in ui_inputs:
        #     self.ui_tariffs.load(ui_inputs[key])
        
        self.ui_tariffs = ui_inputs['model_tariffs_mike'] if 'model_tariffs_mike' in ui_inputs else None #This just grabs the new tariffs object from the ui inputs

    def load_participants(self, ui_inputs):
        key = "model_participants"
        if key in ui_inputs:
            self.ui_participants.load(ui_inputs[key])

    def load_data_sources(self, ui_inputs):
        key = "model_data_sources"
        if key in ui_inputs:
            start, end = self.find_time_periods(ui_inputs[key])
            self.time_periods = util.generate_dates_in_range(start, end, 30)

    def print(self):
        print("Model Type: ", self.model_type)

    def create_objects(self):
        
        # Create the main Study object
        self.mike_model = NewSim(self.folder_routes)
       

    def run(self, status):
        print("mike.py/run()", "Attempting Mike Model Run")
        status("Attempting to run Mike Model")
        self.mike_model.run()

        print("mike.py/run()", "Finished Running Mike Model")
        status("Finished Running Mike Model. Parsing Results")
        parsed_results = self.ui_results_parser.mike_temp_parser()


        print("mike.py/run()", "Finished Parsing Results")
        status("Finished Parsing Results")
        return parsed_results

    # Might move this later.
    def find_time_periods(self, frontend_data):

        s_path = self.folder_routes.solar_profiles_dir
        l_path = self.folder_routes.load_profiles_dir

        s_file_path = os.path.join(s_path, frontend_data["selected_solar_file"])
        l_file_path = os.path.join(l_path, frontend_data["selected_load_file"])

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
