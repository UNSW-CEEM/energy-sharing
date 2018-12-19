# UI Input parsing modules
from .central_battery import CentralBattery as ui_central_battery
from .central_solar import CentralSolar as ui_central_solar
from .tariffs import Tariffs as ui_tariffs
from .participants import Participants as ui_participants
from .result_parsers import ResultParsers as ui_results_parsers

# Model Modules
from ..network import Network as Model_Network
from ..battery import Central_Battery as model_central_battery
from ..tariffs import Tariffs as model_tariffs
from .. import util
from ..results import Results
from .. import energy_sim
from .. import financial_sim

import os


class Parameters:
    def __init__(self):
        # Model setup parameters
        self.model_type = 'luomi'
        self.network_name = 'Default_Network'
        self.network_type = 'embedded_network'
        self.data_dir = os.path.realpath('application/modelling/data')
        self.input_dir = os.path.join(self.data_dir, "input")
        self.output_dir = os.path.join(self.data_dir, "output")

        # UI Interface objects
        self.ui_participants = ui_participants(self.data_dir)
        self.ui_tariffs = ui_tariffs(self.data_dir)
        self.ui_finances = None
        self.ui_central_battery = ui_central_battery(self.data_dir)
        self.ui_central_solar = ui_central_solar(self.data_dir)
        self.ui_results_parser = ui_results_parsers(self.data_dir)

        # Model Objects
        self.model_network = None
        self.model_central_battery = None
        self.model_tariffs = None
        self.model_time_periods = None

    def load(self, ui_inputs):
        load_functions = [
            self.load_network_name,
            self.load_network_type,
            self.load_central_battery,
            self.load_tariffs,
            self.load_participants,
        ]

        for each in load_functions:
            each(ui_inputs)

    def load_defaults(self):
        # Populate default participants from the CSV.
        self.ui_tariffs.load_defaults()
        self.ui_participants.load_defaults()

    def load_network_name(self, ui_inputs):
        key = "network_name"
        if key in ui_inputs:
            self.network_name = ui_inputs[key]

    def load_network_type(self, ui_inputs):
        key = "network_type"
        if key in ui_inputs:
            self.network_type = ui_inputs[key]

    def load_central_battery(self, ui_inputs):
        key = "central_battery"
        if key in ui_inputs:
            self.ui_central_battery.load(ui_inputs[key])

    def load_tariffs(self, ui_inputs):
        key = "model_tariffs"
        if key in ui_inputs:
            self.ui_tariffs.load(ui_inputs[key])

    def load_participants(self, ui_inputs):
        key = "model_participants"
        if key in ui_inputs:
            self.ui_participants.load(ui_inputs[key])

    def print(self):
        print("Model Type: ", self.model_type)

    def create_objects(self):
        if self.model_type is 'mike':
            self.create_mike_objects()
        else:
            self.create_luomi_objects()

    def create_luomi_objects(self):
        self.model_network = Model_Network(self.network_name)
        # Need to add participants into model

        self.model_central_battery = None
        print("Made LUOMI Objects without error")

    def create_mike_objects(self):
        pass
