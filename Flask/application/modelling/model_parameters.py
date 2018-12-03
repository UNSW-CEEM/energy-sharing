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


