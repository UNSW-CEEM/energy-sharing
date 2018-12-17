# This will provide a layer of abstraction between the format of the frontend data object and the format
# required by the back end. Design changes on either side of this layer should only need to be changed here.


class ModelParameters:
    def __init__(self, ui_parameters):
        self.ui_parameters = ui_parameters

        self.data = self.default_data()

        # self.parse_all()

    def parse_all(self):
        self.parse_basics()
        self.parse_battery()
        # self.parse_participants()
        # self.parse_solar()
        # self.parse_tariffs()

    def parse_basics(self):
        self.data.network_name = self.ui_parameters["network_name"]
        self.data.data_dir = self.ui_parameters["data_dir"]
        self.data.output_dir = self.ui_parameters["output_dir"]
        self.data.participants_csv = self.ui_parameters["participants_csv"]
        self.data.battery_discharge_file = self.ui_parameters["battery_discharge_file"]

    def parse_battery(self):
        try:
            battery_params = self.ui_parameters["central_battery"]
            for each in battery_params:
                if each["value"] is "":
                    # TODO implement a default parameters object to set these values.
                    pass
                else:
                    self.data["central_battery"][each["name"]] = each["value"]

        except:
            print("Bad Battery Parameters")

    def parse_financing(self):
        pass

    # Don't think this is needed as Data simply shows the files available.
    def parse_model(self):
        pass

    def parse_solar(self):
        try:
            solar_params = self.data.ui_parameters["central_solar"]
            for each in solar_params:
                self.data.central_solar[each["name"]] = each["value"]

        except:
            print("Bad Solar Parameters")

    def parse_tariffs(self):
        try:
            tariff_params = self.ui_parameters["model_tariffs"]
            for each in tariff_params:
                self.tariffs[each["name"]] = each["value"]

        except:
            print("Bad Tariff Parameters")

    def parse_participants(self):
        try:
            part_params = self.ui_parameters["model_participants"]
            print(part_params)

        except:
            print("Error with participants")

    def default_data(self):
        data = {
            'network_name': 'Byron',
            'data_dir': 'application/modelling/data',
            'output_dir': 'application/modelling/test_output',
            'participants_csv': 'participant_meta_data.csv',
            'battery_discharge_file': 'ui_battery_discharge_window_eg.csv',

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

        return data
