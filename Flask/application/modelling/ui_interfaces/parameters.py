# UI Input parsing modules
from .central_battery import CentralBattery as Ui_Central_Battery
from .central_solar import CentralSolar as Ui_Central_Solar
from .tariffs import Tariffs as Ui_Tariffs
from .participants import Participants as Ui_Participants
from .result_parsers import ResultParsers as Ui_Results_Parsers
from application.folder_routes import FolderRoutes as FolderRoutes
from .csv_helpers import create_csvs

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


class Parameters:
    def __init__(self):
        # Folder Routes
        self.folder_routes = FolderRoutes()

        # Model setup parameters
        self.model_type = 'luomi'
        self.network_name = 'Default_Network'
        self.network_type = 'embedded_network'
        self.data_dir = self.folder_routes.get_route('data_dir')
        self.luomi_defaults_dir = self.folder_routes.get_route("luomi_defaults_dir")
        self.luomi_input_dir = self.folder_routes.get_route("luomi_input_dir")
        self.luomi_output_dir = self.folder_routes.get_route("luomi_output_dir")

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

    def load_defaults(self):
        # Populate default participants from the CSV.
        self.ui_tariffs.load_defaults()
        self.ui_participants.load_defaults()

        # This is temporary.
        start = datetime.datetime(year=2017, month=2, day=26, hour=10)
        end = datetime.datetime(year=2017, month=2, day=26, hour=12)
        self.time_periods = util.generate_dates_in_range(start, end, 30)

    def load_model_selection(self, ui_inputs):
        key = "model_selection"
        if key in ui_inputs:
            model_array = ui_inputs[key]
            for each in model_array:
                if each["name"] == "model_type":
                    self.model_type = each["value"]
                elif each["name"] == "network_type":
                    self.network_type = each["value"]

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
        key = "model_tariffs"
        if key in ui_inputs:
            self.ui_tariffs.load(ui_inputs[key])

    def load_participants(self, ui_inputs):
        key = "model_participants"
        if key in ui_inputs:
            self.ui_participants.load(ui_inputs[key])

    def load_data_sources(self, ui_inputs):
        key = "model_data_sources"
        if key in ui_inputs:
            start, end = self.find_time_periods(ui_inputs[key])
            self.time_periods = util.generate_dates_in_range(start, end, 30)

    # def load_central_solar(self, ui_inputs):
    #     key = "model_solar"
    #     if key in ui_inputs:
    #         print("Called load_central_solar")
    #         # self.ui_participants.add_participant(ui_inputs[key])

    def print(self):
        print("Model Type: ", self.model_type)

    def create_objects(self):
        if self.model_type == 'mike':
            self.create_mike_objects()
        else:
            self.create_luomi_objects()

    def create_luomi_objects(self):
        self.model_network = Luomi_Network(self.network_name)

        # Need to add participants into model
        participants_string = self.ui_participants.get_participants_as_string()
        self.model_network.add_participants_from_string(self.data_dir, participants_string)

        # Create a central battery from the ui_central_battery.
        self.model_central_battery = Luomi_Central_Battery(**self.ui_central_battery.get_params_dict())
        # Add the central battery to the network
        self.model_network.add_central_battery(self.model_central_battery)
        tariffs_dict = self.ui_tariffs.get_tariffs_dict()

        # print(tariffs_dict)
        self.model_tariffs = Luomi_Tariffs(**tariffs_dict)

        print("Made LUOMI Objects without error")

    def create_mike_objects(self):
        # Create the main Study object
        self.mike_model = NewSim(self.folder_routes)
        # Create the CSV's from the standard objects.
        create_csvs(self.ui_participants,
                    self.ui_tariffs,
                    self.ui_finances,
                    self.ui_central_battery,
                    self.ui_central_solar,
                    self.folder_routes)

    def run(self, status):
        if self.model_type == 'mike':
            return self.run_mike_model(status)
        else:
            return self.run_luomi_model(status)

    def run_luomi_model(self, status):
        bc = self.ui_central_battery.get_capacity()
        print("RUN_LUOMI_TIME_PERIODS", self.time_periods)
        self.model_results = Results(self.time_periods, [p.get_id() for p in self.model_network.get_participants()])
        energy_sim.simulate(self.time_periods, self.model_network, self.model_tariffs, self.model_results, status)
        financial_sim.simulate(self.time_periods, self.model_network, self.model_tariffs, self.model_results, status)
        self.model_results.to_csv(self.luomi_output_dir, info_tag=bc)

        parsed_results = self.ui_results_parser.luomi_temp_parser(bc)

        return parsed_results

    def run_mike_model(self, status):
        status("Attempting Mike Model")
        if self.mike_model:
            self.mike_model.run()

        parsed_results = self.ui_results_parser.mike_temp_parser()
        status("Mike Model Complete - See Folder")
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
