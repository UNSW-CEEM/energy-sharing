import os
import csv


class Tariffs:
    def __init__(self, data_dir):
        self.data_dir = data_dir

        self.tariffs = []

    def load(self, inputs):
        # Reset the list of tariffs
        self.tariffs = []

        # Parse through each line in the UI inputs and create a tariff
        for each in inputs:
            row = each["row_inputs"]
            parameters = {}
            for each_dict in row:
                # print(each_dict, "\n")
                parameters[each_dict["name"]] = (each_dict["value"])
            # print(parameters, "\n")
            self.tariffs.append(Tariff(**parameters))

    def load_defaults(self):
        self.tariffs = []

        default_tariffs_path = os.path.join(self.data_dir, "defaults/duos.csv")

        # Parse through each line in the defaults csv and create tariffs.
        with open(default_tariffs_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.tariffs.append(Tariff(**row))


# TODO Confirm these.
class Tariff:
    def __init__(
                self,
                peak_charge,
                shoulder_charge,
                offpeak_charge,
                tariff_type=None,
                tariff_name=None,
                fit_input=None,
                Ref = None,
                dnsp = None,
                offer_name=None,
                type=None,
                daily_charge=None,
                flat_charge=None,
                block_1_charge=None,
                block_2_charge=None,
                controlled_load=None,
                peak_start_time=None,
                peak_end_time=None,
                peak_start_time_2=None,
                peak_end_time_2=None,
                shoulder_start_time=None,
                shoulder_end_time=None,
                shoulder_start_time_2=None,
                shoulder_end_time_2=None,
                block_1_volume=None,
                block_2_volume=None,
                demand=None,
                demand_units=None,
                tou_weekday_only_flag=None):

        self.tariff_type = tariff_type
        self.tariff_name = tariff_name
        self.fit_input = fit_input
        self.peak_charge = peak_charge
        self.shoulder_charge = shoulder_charge
        self.offpeak_charge = offpeak_charge

        self.print()

    def print(self):
        print("Tariff Object Contains: {}, {}, {}".format(self.tariff_type, self.tariff_name, self.peak_charge))

'''
Ref,dnsp,offer_name,type,
daily_charge,flat_charge,peak_charge,shoulder_charge,
offpeak_charge,block_1_charge,block_2_charge,controlled_load,
peak_start_time,peak_end_time,peak_start_time_2,peak_end_time_2,
shoulder_start_time,shoulder_end_time,shoulder_start_time_2,shoulder_end_time_2,
block_1_volume,block_2_volume,demand,demand_units,
tou_weekday_only_flag

Fields from the UI...

Tariff Type,tariff_name,fit_input,peak_price,shoulder_price,off_peak_price
'''