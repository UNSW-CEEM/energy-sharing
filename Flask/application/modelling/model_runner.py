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
import csv


class ModelRunner:
    def __init__(self):

        self.output_dir = None
        self.data_dir = None
        self.my_network = None
        self.central_battery = None
        self.my_tariffs = None
        self.time_periods = None
        self.results = None

        self.params = None

    def load_parameters(self, model_parameters):
        self.params = model_parameters

        # Create Network object and set directories
        self.my_network = Network(model_parameters['network_name'])
        self.data_dir = os.path.realpath(self.params['data_dir'])
        self.output_dir = os.path.realpath(self.params['output_dir'])

        self.my_network.add_participants_from_csv(self.data_dir, self.params["participants_csv"])
        self.central_battery = Central_Battery(
            cap_kWh=float(self.params["central_battery"][0]["value"]),
            cap_kW=float(self.params["central_battery"][1]["value"]),
            cycle_eff=float(self.params["central_battery"][2]["value"]),
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
        end = datetime.datetime(year=2017, month=2, day=26, hour=8)

        self.time_periods = util.generate_dates_in_range(start, end, 30)

    def run(self):
        self.results = Results(self.time_periods, [p.get_id() for p in self.my_network.get_participants()])

        energy_sim.simulate(self.time_periods, self.my_network, self.my_tariffs, self.results)

        financial_sim.simulate(self.time_periods, self.my_network, self.my_tariffs, self.results)

        self.results.to_csv(self.output_dir, info_tag=self.params["central_battery"][0]["value"])

        return self.temp_return_data()

    def temp_return_data(self):
        energy_flows_path = os.path.join(
            self.output_dir,
            ("df_network_energy_flows" + self.params["central_battery"][0]["value"] + ".csv")
        )

        total_participant_bill_path = os.path.join(
            self.output_dir,
            ("df_total_participant_bill" + self.params["central_battery"][0]["value"] + ".csv")
        )
        energy_flows_data = []
        total_participant_bill = []

        with open(energy_flows_path) as fileOne:
            reader = csv.DictReader(fileOne)
            for row in reader:
                energy_flows_data.append(row)

        with open(total_participant_bill_path) as fileTwo:
            reader = csv.DictReader(fileTwo)
            for row in reader:
                total_participant_bill.append(row)

        results = {
            "energy_flows": energy_flows_data,
            "total_participant_bill": total_participant_bill
        }

        return results
