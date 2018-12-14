''' A new all in one version of model_data_parser, model_parameters, and model_runner

# This module will contain
    - A ModelInterface object which will init using another DefaultInputs object/function
    (for things that will come from the UI) and a DefaultSetup object/function (for directories, etc)

    - A load method that will take in a UI parameters JSON object and over write the appropriate
    fields of the default object/function return. If something is incorrect we will most likely use
    the default so the model can run but also return a sensible error to the UI so that in can be changed.
    Or run anyway with the default values for those fields.

    - A run method for linking the data in the ModelInterface object to the model

    - Some custom parse methods for turning the model results back into easy to use data.
'''

from .network import Network
from .tariffs import Tariffs

import os


class ModelInterface:
    def __init__(self):
        self.inputs = default_inputs()

        self.status = None

        self.battery_discharge_path = None
        self.data_dir = None
        self.output_dir = None
        self.network = None
        self.central_battery = None
        self.participants_csv = None
        self.tariff_paths = {}
        self.tariffs = None
        self.time_periods = None

        self.results = None

    def load(self, ui_inputs):
        # Will overwrite input parameters etc starting here. And Setup parameters.
        # May change the structure of defaults and over rides etc. Will most likely make further
        # Functions to handle each aspect of the input as well as a default object stored locally.
        load_functions = [
            self.load_network,
            self.load_data_dir,
            self.load_output_dir,
            self.load_participants,
            self.load_battery_discharge,
            self.load_tariffs,
        ]

        for each in load_functions:
            each(ui_inputs)

    # <-------------- HERE ARE SOME LOAD FUNCTIONS ---------------->
    def load_network(self, ui_inputs):
        key = "network_name"
        if key in ui_inputs.keys():
            self.inputs[key] = ui_inputs[key]
        # TODO Address below.
        # I think this should be created later. Should only be an overwrite function
        self.network = Network(self.inputs[key])

    def load_data_dir(self, ui_inputs):
        key = "data_dir"
        if key in ui_inputs:
            self.inputs[key] = ui_inputs[key]
        self.data_dir = os.path.realpath(self.inputs[key])

    def load_output_dir(self, ui_inputs):
        key = "output_dir"
        if key in ui_inputs:
            self.inputs[key] = ui_inputs[key]
        self.output_dir = os.path.realpath(self.inputs[key])

    def load_participants(self, ui_inputs):
        key = "model_participants"
        if key in ui_inputs and len(ui_inputs[key]) > 0:
            # Do some logic about parsing the participants
            # TODO Sort out this creation of a participants CSV from the ui input.
            # print(ui_inputs[key])
            pass
        # Else use the default CSV
        self.participants_csv = self.inputs["participants_csv"]

    def load_battery_discharge(self, ui_inputs):
        key = "battery_discharge_file"
        if key in ui_inputs:
            self.inputs[key] = ui_inputs[key]
        self.battery_discharge_path = os.path.join(self.data_dir, self.inputs[key])

    # TODO This whole load_tariffs system needs a rethink at some point. Very hacky right now.
    def load_tariffs(self, ui_inputs):
        key = "model_tariffs"

        # This just handles the fact the UI has a slightly different name than the existing Model.
        # This may need to change later.
        key_mappings = {
            'Retail': 'retail_tariff_data_path',
            'DUOS': 'duos_data_path',
            'TUOS': 'tuos_data_path',
            'NUOS': 'nuos_data_path',
            'Peer to Peer': 'p2p_data_path',
        }

        # Create default tariff paths
        for each in self.inputs[key]:
            if each["name"] is "scheme_name":
                self.tariff_paths[each["name"]] = each["value"]
            else:
                # Slightly hacky naming here.. means we can just use **self.tariff_paths in the tariff object
                # constructor. Which maps the key/values to the expected parameters
                self.tariff_paths[(each["name"] + "_data_path")] = os.path.join(self.data_dir, each["value"])

        if key in ui_inputs and len(ui_inputs[key]) > 0:
            # Create tariff files
            for each in ui_inputs[key]:
                # Get the "Tariff Type" value from the UI data
                key = each["row_inputs"][0]["value"]
                # Can use it's corrosponding model name from the key_mappings object
                # print(key_mappings[key])
                result = tariff_parser(each)

                if result:
                    self.tariff_paths[key_mappings[key]] = result

        # After creating the custom tariff files we need to ensure the paths are also updated.
        print(self.tariff_paths)

    def run(self, status_callback):
        # Create necessary objects
        self.create_network()
        self.create_tariffs()

        # Run the model

    # <-------------- HERE ARE SOME CREATE (RUN) FUNCTIONS ---------------->
    def create_network(self):
        pass

    def create_tariffs(self):
        # This expands our paths dict into our Tariff object parameters. Verrrrrry niiiiiice.
        self.tariffs = Tariffs(**self.tariff_paths)

    def parse(self):
        # A one stop function to call all the parsing functions.

        # Open up the appropriate results CSV
        tpb_file = {}
        # Call the relevant parser.
        tpb = parse_total_participants_bill(tpb_file)

        # Package up the result.
        result = {
            "total_participants_bill": tpb
        }

        return result


def default_inputs():
    # A default input representation.
    result = {
        'network_name': 'Default_Network',
        'data_dir': 'application/modelling/data',
        'output_dir': 'application/modelling/test_output',
        'participants_csv': 'participant_meta_data.csv',
        'battery_discharge_file': 'ui_battery_discharge_window_eg.csv',

        'model_tariffs':
            [
                {'name': 'scheme_name', 'value': 'Test'},
                {'name': 'retail_tariff', 'value': 'retail_tariffs.csv'},
                {'name': 'duos', 'value': 'duos.csv'},
                {'name': 'tuos', 'value': 'tuos.csv'},
                {'name': 'nuos', 'value': 'nuos.csv'},
                {'name': 'ui_tariff', 'value': 'ui_tariffs_eg.csv'}
            ],

        'model_data':
            [
                {'name': 'solar_data_source', 'value': ''},
                {'name': 'load_data_source', 'value': ''}
            ],

        'model_selection':
            [
                {'name': 'simulation', 'value': 'Sim 1'},
                {'name': 'network_type', 'value': 'ABC'}
            ],

        'model_participants':
            [
                {'row_id': 0, 'row_inputs':
                    [
                        {'name': 'participant_id', 'value': 'Participant 0'},
                        {'name': 'participant_type', 'value': 'PV'},
                        {'name': 'tariff_type', 'value': 'Tariff 2'},
                        {'name': 'load_data', 'value': 'Load_From_Flask_1.csv'},
                        {'name': 'solar_data', 'value': 'Solar_From_Flask_1.csv'},
                        {'name': 'solar_scaling', 'value': '2'},
                        {'name': 'battery_type', 'value': 'Battery Option 2'}
                    ]
                 },
                {'row_id': 1, 'row_inputs':
                    [
                        {'name': 'participant_id', 'value': 'Participant 1'},
                        {'name': 'participant_type', 'value': 'PV & Load'},
                        {'name': 'tariff_type', 'value': 'AGL TOU 1'},
                        {'name': 'load_data', 'value': 'Load_From_Flask_2.csv'},
                        {'name': 'solar_data', 'value': 'Solar_From_Flask_2.csv'},
                        {'name': 'solar_scaling', 'value': '1'},
                        {'name': 'battery_type', 'value': 'Battery Option 1'}
                    ]
                 }
            ],

        'central_solar':
            [
                {'name': 'data_source', 'value': 'ABC'},
                {'name': 'scaling_factor', 'value': '2'},
                {'name': 'sharing_algorithm', 'value': 'ABC'}
            ],

        'central_battery':
            [
                {'name': 'capacity', 'value': '0.01'},
                {'name': 'max_discharge', 'value': '0.01'},
                {'name': 'cycle_efficiency', 'value': '0.8'},
                {'name': 'dispatch_algorithm', 'value': 'ABC'}
            ],

        'model_financing':
            [
                {'row_id': 0, 'row_inputs':
                    [
                        {'name': 'component', 'value': 'Yes'},
                        {'name': 'capex', 'value': '100'},
                        {'name': 'capex_payer', 'value': 'Option 1'},
                        {'name': 'discount_rate', 'value': '5'},
                        {'name': 'amortization', 'value': '10'},
                        {'name': 'opex', 'value': '15'},
                        {'name': 'opex_payer', 'value': 'Option Two'}
                    ]
                 }
            ]
    }

    return result


def parse_total_participants_bill(tpb):
    # Takes in the TPB data and returns it in a more manageable structure.
    data_points = {}

    for each in tpb:
        for key, value in each.items():
            # print("Key:", key, " Value: ", value, "\n")
            if key == "":
                pass
            else:
                if key not in data_points:
                    data_points[key] = 0
                else:
                    data_points[key] += float(value)

    return data_points


def tariff_parser(tariff):
    result = False

    # Insert some logic creating a CSV for the tariff, and if successful return the path.

    return result
