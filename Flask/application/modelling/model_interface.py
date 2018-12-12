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


class ModelInterface:
    def __init__(self):
        self.inputs = default_inputs()
        self.setup = default_setup()

    def load(self, ui_inputs):
        # Will overwrite input parameters etc starting here. And Setup parameters.
        # May change the structure of defaults and over rides etc. Will most likely make further
        # Functions to handle each aspect of the input as well as a default object stored locally.
        pass

    def run(self, status_callback):
        # Should be reasonably simple and somewhat akin to the model runner. I want to pull as much
        # bespoke stuff as possible out of the function.
        pass

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
        'model_tariffs':
            [
                {'name': 'scheme_name', 'value': 'Test'},
                {'name': 'retail_tariff_file', 'value': 'retail_tariffs.csv'},
                {'name': 'duos_file', 'value': 'duos.csv'},
                {'name': 'tuos_file', 'value': 'tuos.csv'},
                {'name': 'nuos_file', 'value': 'nuos.csv'},
                {'name': 'ui_tariff_file', 'value': 'ui_tariffs_eg.csv'}
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


def default_setup():
    # A default setup representation.
    result = {
        'default_network_name': 'Default_Test_Network',
        'default_data_dir': 'application/modelling/data',
        'default_output_dir': 'application/modelling/test_output',
        'default_participants_csv': 'participant_meta_data.csv',
        'default_battery_discharge_file': 'ui_battery_discharge_window_eg.csv',
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
