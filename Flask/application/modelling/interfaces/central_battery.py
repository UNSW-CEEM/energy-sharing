import os


class CentralBattery:
    def __init__(self, data_dir):
        self.data_dir = data_dir

        self.capacity = 1
        self.max_discharge = 1
        self.cycle_efficiency = 0.9
        self.dispatch_algorithm = 'tou_arbitrage'
        self.battery_discharge_filepath = self.set_battery_discharge_filepath()

    def load(self, inputs):
        print(inputs)

    def get_params_dict(self):
        params = {
            'cap_kWh': self.capacity,
            'cap_kW': self.max_discharge,
            'cycle_eff': self.cycle_efficiency,
            'ui_battery_discharge_windows_path': self.battery_discharge_filepath
        }
        return params

    def get_capacity(self):
        return self.capacity

    def get_max_discharge(self):
        return self.max_discharge

    def get_cycle_efficiency(self):
        return self.cycle_efficiency

    def get_dispatch_algorithm(self):
        return self.dispatch_algorithm

    def set_battery_discharge_filepath(self):
        battery_discharge_filename = 'ui_battery_discharge_window_eg.csv'
        return os.path.join(self.data_dir, battery_discharge_filename)
