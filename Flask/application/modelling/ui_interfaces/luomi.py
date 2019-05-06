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


import os
import datetime
import pandas as pd
import pendulum
import json


class LuomiWrapper:
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
        self.ui_tariffs = ui_inputs['tariffs'] #This just grabs the new tariffs object from the ui inputs

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
        
        
        self.model_network = Luomi_Network(self.network_name)

        # Need to add participants into model
        
        participants_string = self.ui_participants.get_participants_as_string()
        
        self.model_network.add_participants_from_string(self.data_dir, self.ui_inputs['model_data_sources']['selected_load_file'], self.ui_inputs['model_data_sources']['selected_solar_file'], participants_string)

        # Create a central battery from the ui_central_battery.
        self.model_central_battery = Luomi_Central_Battery(**self.ui_central_battery.get_params_dict())
        # Add the central battery to the network
        self.model_network.add_central_battery(self.model_central_battery)
        
        # tariffs_dict = self.ui_tariffs.get_tariffs_dict()
        
        # self.model_tariffs = Luomi_Tariffs(**tariffs_dict)

        self.model_tariffs = Luomi_Tariffs(self.ui_tariffs)
        
        print("parameters.py/create_luomi_objects","Made LUOMI Objects without error")

    
    def run(self, status):
        info_tag = ""
        # print("RUN_LUOMI_TIME_PERIODS", self.time_periods)
        self.model_results = Results(self.time_periods, [p.get_id() for p in self.model_network.get_participants()])
        energy_sim.simulate(self.time_periods, self.model_network, self.model_tariffs, self.model_results, status)
        financial_sim.simulate(self.time_periods, self.model_network, self.model_tariffs, self.model_results, status)
        self.model_results.to_csv(self.luomi_output_dir, info_tag=info_tag)

        parsed_results = self.ui_results_parser.luomi_temp_parser(info_tag)
        
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
