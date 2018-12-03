# This will provide a layer of abstraction between the format of the frontend data object and the format
# required by the back end. Design changes on either side of this layer should only need to be changed here.


class ModelParameters:
    def __init__(self, ui_parameters):
        self.ui_parameters = ui_parameters

        self.network_name = None
        self.data_dir = None
        self.output_dir = None
        self.participants_csv = None
        self.battery_discharge_file = None
        self.tariffs = {
            "scheme_name": None,
            "retail_tariff_file": None,
            "duos_file": None,
            "tuos_file": None,
            "nuos_file": None,
            "ui_tariff_file": None,
        }
        self.central_battery = {
            "capacity": 0.01,
            "max_discharge": 0.01,
            "cycle_efficiency": 0.95,
            "dispatch_algorithm": None
        }
        self.central_solar = None

        self.parse_basics()
        self.parse_battery()
        self.parse_tariffs()

    def parse_basics(self):
        self.network_name = self.ui_parameters["network_name"]
        self.data_dir = self.ui_parameters["data_dir"]
        self.output_dir = self.ui_parameters["output_dir"]
        self.participants_csv = self.ui_parameters["participants_csv"]
        self.battery_discharge_file = self.ui_parameters["battery_discharge_file"]

    def parse_battery(self):
        try:
            battery_params = self.ui_parameters["central_battery"]
            for each in battery_params:
                self.central_battery[each["name"]] = each["value"]

        except:
            print("Bad Battery Parameters")

    def parse_financing(self):
        pass

    def parse_model(self):
        pass

    def parse_solar(self):
        pass

    def parse_tariffs(self):
        try:
            tariff_params = self.ui_parameters["tariffs"]
            for each in tariff_params:
                self.tariffs[each["name"]] = each["value"]

        except:
            print("Bad Tariff Parameters")


''' {
    'network_name': 'Byron',
    'data_dir': 'application/modelling/data',
    'output_dir': 'application/modelling/test_output',
    'participants_csv': 'participant_meta_data.csv',
    'battery_discharge_file': 'ui_battery_discharge_window_eg.csv',

    'tariffs':
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
    'model_tariffs':
        [
            {'row_id': 0, 'row_inputs':
                [
                    {'value': 'TUOS'},
                    {'value': '1'},
                    {'value': '2'},
                    {'value': '3'},
                    {'value': '4'}
                ]
            },
            {'row_id': 1, 'row_inputs':
                [
                    {'value': 'NUOS'},
                    {'value': '5'},
                    {'value': '6'},
                    {'value': '7'},
                    {'value': '8'}
                ]
            }
        ],
    'undefined':
        [
            {'name': 'data_source', 'value': 'ABC'},
            {'name': 'scaling_factor', 'value': '2'},
            {'name': 'sharing_algorithm', 'value': 'ABC'}
        ],
    'central_battery':
        [
            {'name': 'capacity', 'value': '1'},
            {'name': 'max_discharge', 'value': '1'},
            {'name': 'cycle_efficiency', 'value': '1'},
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
'''
