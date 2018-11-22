from .network import Network
from .battery import Battery, Central_Battery
from .tariffs import Tariffs
from . import util
from .results import Results
from . import energy_sim
from . import financial_sim

import datetime
import os


class ModelRunner:
    def __init__(self):
        output_dir = 'test_output'
        data_dir = 'data'
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
