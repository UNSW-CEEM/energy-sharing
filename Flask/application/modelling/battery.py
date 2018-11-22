import numpy as np
import pandas as pd
import datetime

class Battery:
    def __init__(self, cap_kWh, cap_kW, cycle_eff):
        """Make note: cycle efficiency must be between zero and one."""
        self.cap_kWh = cap_kWh
        self.cap_kW = cap_kW
        self.cycle_eff = cycle_eff
        self.charge_level_kWh = 0  
        self.num_cycles = 0      

    def charge(self, kWh):
        # Increase battery charge level by the input kWh
        amount_to_charge = min(self.cap_kWh - self.charge_level_kWh, kWh)
        self.charge_level_kWh += amount_to_charge * self.cycle_eff
        return kWh - amount_to_charge

    def discharge(self, kWh_request):
        discharge_amount = min(kWh_request, self.charge_level_kWh)
        self.charge_level_kWh -= discharge_amount
        self.num_cycles += float(discharge_amount) / float(self.cap_kWh)
        return discharge_amount

    def get_num_cycles(self):
        return self.num_cycles

class Central_Battery(Battery):
    def __init__(self, cap_kWh, cap_kW, cycle_eff, ui_battery_discharge_windows_path):
        Battery.__init__(self, cap_kWh, cap_kW, cycle_eff)
        self.ui_battery_discharge_windows_path = ui_battery_discharge_windows_path
        self.discharge_times_data = pd.read_csv(ui_battery_discharge_windows_path)
        # Get pandas series containing all allowed discharge hours
        # Note - end time is NOT inclusive
        # (i.e. if end time is 10 then allowed time period will be up to and including 9)
        self.allowed_discharge_hours = pd.Series()
        for row in self.discharge_times_data.index.values:
            self.start_time = self.discharge_times_data.loc[row,'start_time']
            self.end_time = self.discharge_times_data.loc[row,'end_time']
            allowed_discharge_raw = pd.Series(list(range(self.start_time, self.end_time, 1)))
            self.allowed_discharge_hours = self.allowed_discharge_hours.append(allowed_discharge_raw)
    
    def make_export_decision(self, net_participant_kWh, date_time):
        """Takes amount of available energy (positive = can charge, negative = there is demand on the network). Makes a decision about whether to charge or discharge. 
        Returns positive if discharging, negative if charging."""
        # Case where there is energy available to charge
        if net_participant_kWh >= 0 :
            # Charge - note this returns what ever is left over after charging
            return (net_participant_kWh - self.charge(net_participant_kWh)) * -1
        
        # Case where there is demand on the network
        else :
            # Hours which discharge is allowed (note midnight is 00:00)
            all_hours = pd.Series(list(range(0,24,1)))
            # Filter to only contain allowed discharge hours
            all_hours_subset_allowed = all_hours[all_hours.isin(self.allowed_discharge_hours)]

            # Check whether hour limitation applies
            if date_time.hour in all_hours_subset_allowed.values:
                return self.discharge(abs(net_participant_kWh))
            else:
                return 0.0


if __name__=="__main__":
    my_batt = Central_Battery(10, 5, 0.9, "data/ui_battery_discharge_window_eg.csv")

