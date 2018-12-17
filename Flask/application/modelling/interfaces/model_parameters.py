from .central_battery import CentralBattery
from .central_solar import CentralSolar

import os


class ModelParameters:
    def __init__(self):
        # Model setup parameters
        self.model_type = 'luomi'
        self.network_name = 'Default_Network'
        self.network_type = 'embedded_network'
        self.data_dir = os.path.realpath('application/modelling/data')
        self.input_dir = None
        self.output_dir = None

        # Model setup objects
        self.participants = None
        self.tariffs = None
        self.finances = None
        self.central_battery = CentralBattery(self.data_dir)
        self.central_solar = CentralSolar(self.data_dir)

    def load(self, ui_inputs):
        load_functions = [
            self.load_network_name,
            self.load_network_type,
            self.load_central_battery
        ]

        for each in load_functions:
            each(ui_inputs)

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
            self.central_battery.load(ui_inputs[key])

    def print(self):
        print("Model Type: ", self.model_type)
