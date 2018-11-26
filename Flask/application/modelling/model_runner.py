# from mongoengine import Document, StringField

from .network import Network
from .battery import Battery, Central_Battery
from .tariffs import Tariffs
from .import util
from .results import Results
from . import energy_sim
from . import financial_sim

import datetime
import os


class ModelRunner:
    def __init__(self):
        output_dir = 'application/modelling/test_output'
        data_dir = os.path.realpath('application/modelling/data')
        my_network = Network('Byron')
        my_network.add_participants_from_csv(data_dir, "participant_meta_data.csv")

        battery_capacity = 0.001
        central_battery = Central_Battery(
            cap_kWh=battery_capacity,
            cap_kW=battery_capacity,
            cycle_eff=0.99,
            ui_battery_discharge_windows_path=os.path.join(data_dir, "ui_battery_discharge_window_eg.csv")
        )

        my_network.add_central_battery(central_battery)

        my_tariffs = Tariffs(
            'Test',
            os.path.join(data_dir, "retail_tariffs.csv"),
            os.path.join(data_dir, "duos.csv"),
            os.path.join(data_dir, "tuos.csv"),
            os.path.join(data_dir, "nuos.csv"),
            os.path.join(data_dir, "ui_tariffs_eg.csv")
        )

        start = datetime.datetime(year=2017, month=2, day=26, hour=4)
        end = datetime.datetime(year=2017, month=2, day=26, hour=23)

        time_periods = util.generate_dates_in_range(start, end, 30)

        results = Results(time_periods, [p.get_id() for p in my_network.get_participants()])

        energy_sim.simulate(time_periods, my_network, my_tariffs, results)

        financial_sim.simulate(time_periods, my_network, my_tariffs, results)

        results.to_csv(output_dir, info_tag=battery_capacity)


class ModelRunnerBeta:
    def __init__(self):

        self.output_dir = None
        self.data_dir = None
        self.my_network = None
        self.central_battery = None
        self.my_tariffs = None
        self.time_periods = None
        self.results = None

        self.params = None

        params = {
            "network_name": "Byron",
            "data_dir": "application/modelling/data",
            "output_dir": "application/modelling/test_output",
            "participants_csv": "participant_meta_data.csv",
            "battery_capacity": 0.001,
            "cycle_efficiency": 0.99,
            "battery_discharge_file": "ui_battery_discharge_window_eg.csv",
            "tariffs": {
                "scheme_name": "Test",
                "retail_tariff_file": "retail_tariffs.csv",
                "duos_file": "duos.csv",
                "tuos_file": "tuos.csv",
                "nuos_file": "nuos.csv",
                "ui_tariff_file": "ui_tariffs_eg.csv",
            }
        }

    def load_parameters(self, model_parameters):
        self.params = model_parameters

        # Create Network object and set directories
        self.my_network = Network(model_parameters['network_name'])
        self.data_dir = os.path.realpath(self.params['data_dir'])
        self.output_dir = os.path.realpath(self.params['output_dir'])

        self.my_network.add_participants_from_csv(self.data_dir, self.params["participants_csv"])
        self.central_battery = Central_Battery(
            cap_kWh=self.params["battery_capacity"],
            cap_kW=self.params["battery_capacity"],
            cycle_eff=self.params["cycle_efficiency"],
            ui_battery_discharge_windows_path=os.path.join(self.data_dir, self.params["battery_discharge_file"])
        )

        self.my_network.add_central_battery(self.central_battery)

        self.my_tariffs = Tariffs(
            self.params["tariffs"]["scheme_name"],
            os.path.join(self.data_dir, self.params["tariffs"]["retail_tariff_file"]),
            os.path.join(self.data_dir, self.params["tariffs"]["duos_file"]),
            os.path.join(self.data_dir, self.params["tariffs"]["tuos_file"]),
            os.path.join(self.data_dir, self.params["tariffs"]["nuos_file"]),
            os.path.join(self.data_dir, self.params["tariffs"]["ui_tariff_file"])
        )

        start = datetime.datetime(year=2017, month=2, day=26, hour=4)
        end = datetime.datetime(year=2017, month=2, day=26, hour=23)

        self.time_periods = util.generate_dates_in_range(start, end, 30)

    def run(self):
        self.results = Results(self.time_periods, [p.get_id() for p in self.my_network.get_participants()])

        energy_sim.simulate(self.time_periods, self.my_network, self.my_tariffs, self.results)

        financial_sim.simulate(self.time_periods, self.my_network, self.my_tariffs, self.results)

        self.results.to_csv(self.output_dir, info_tag=self.params["battery_capacity"])
