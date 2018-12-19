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
        setters = {
            'capacity': self.set_capacity,
            'max_discharge': self.set_max_discharge,
            'cycle_efficiency': self.set_cycle_efficiency,
            'dispatch_algorithm': self.set_dispatch_algorithm,
        }
        for each in inputs:
            setters[each["name"]](each["value"])

        # print(self.capacity, self.max_discharge, self.cycle_efficiency)

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

    def set_battery_discharge_filepath(self, value=None):
        file_name = 'ui_battery_discharge_window_eg.csv'
        if value is not None:
            file_name = value
        return os.path.join(self.data_dir, file_name)

    def set_capacity(self, value):
        if value is not '':
            self.capacity = value

    def set_cycle_efficiency(self, value):
        if value is not '':
            self.cycle_efficiency = value

    def set_dispatch_algorithm(self, value):
        if value is not '':
            self.dispatch_algorithm = value

    def set_max_discharge(self, value):
        if value is not '':
            self.max_discharge = value
