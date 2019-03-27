import os
import csv
import io

DUOS_NAME = "duos.csv"
NUOS_NAME = "nuos.csv"
TUOS_NAME = "tuos.csv"
RETAIL_NAME = "retail_tariffs.csv"
UI_TARIFFS_NAME = "ui_tariffs.csv"


class Tariffs:
    def __init__(self, folder_routes):
        self.luomi_defaults_dir = folder_routes.get_route("luomi_defaults_dir")

        # Tariff type specific arrays
        self.duos_tariffs = []
        self.nuos_tariffs = []
        self.tuos_tariffs = []
        self.retail_tariffs = []

    # TODO Get normal load working (from UI_Input)
    def load(self, inputs, debug_print=False):
        # Reset the list of tariffs
        self.reset_all_tariffs()

        # Mappings to make things a little easier
        mapping = {
            'DUOS': {'array': self.duos_tariffs, 'tariff': DuosTariff},
            'TUOS': {'array': self.nuos_tariffs, 'tariff': NuosTariff},
            'NUOS': {'array': self.tuos_tariffs, 'tariff': TuosTariff},
            'Retail': {'array': self.retail_tariffs, 'tariff': RetailTariff}
        }

        # Parse through each line in the UI inputs and create a tariff
        for each in inputs:
            row = each["row_inputs"]
            parameters = {}
            for each_dict in row:
                # print(each_dict, "\n")
                parameters[each_dict["name"]] = (each_dict["value"])
            # print(parameters["tariff_type"], "\n")

            mapped_type = mapping[parameters["tariff_type"]]
            array = mapped_type["array"]
            tariff = mapped_type["tariff"]
            print(parameters["tariff_type"])
            print(parameters)
            array.append(tariff(**parameters))

        if debug_print:
            for each in self.duos_tariffs:
                each.print()

    def load_defaults(self, debug_print=False):
        self.reset_all_tariffs()

        duos_path = os.path.join(self.luomi_defaults_dir, DUOS_NAME)
        nuos_path = os.path.join(self.luomi_defaults_dir, NUOS_NAME)
        tuos_path = os.path.join(self.luomi_defaults_dir, TUOS_NAME)
        retail_path = os.path.join(self.luomi_defaults_dir, RETAIL_NAME)

        mapping = [
            {'path': duos_path, 'array': self.duos_tariffs, 'tariff': DuosTariff},
            {'path': nuos_path, 'array': self.nuos_tariffs, 'tariff': NuosTariff},
            {'path': tuos_path, 'array': self.tuos_tariffs, 'tariff': TuosTariff},
            {'path': retail_path, 'array': self.retail_tariffs, 'tariff': RetailTariff},
        ]

        for each in mapping:
            self.load_tariff_from_csv(**each)

        if debug_print:
            for each in self.duos_tariffs:
                each.print()

    @staticmethod
    def load_tariff_from_csv(path, array, tariff):
        # Parse through each line in the defaults csv and create tariffs.
        with open(path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                array.append(tariff(**row))

    def get_tariffs_dict(self):
        # Create the params dict here. Similar to in central battery
        # TODO Figure out a nice way to do scheme name
        
        duos_string = self.array_to_string_buffer(self.duos_tariffs)
        nuos_string = self.array_to_string_buffer(self.nuos_tariffs)
        tuos_string = self.array_to_string_buffer(self.tuos_tariffs)
        retail_string = self.array_to_string_buffer(self.retail_tariffs)
        # ui_tariff_string = self.array_to_string_buffer(self.duos_tariffs)
        print("TARIFF LOOK AT ME", self.retail_tariffs)
        results = {
            "scheme_name": "Scheme Name",
            "duos_data_path": duos_string,
            "nuos_data_path": nuos_string,
            "tuos_data_path": tuos_string,
            "retail_tariff_data_path": retail_string,
            "ui_tariff_data_path": os.path.join(self.luomi_defaults_dir, UI_TARIFFS_NAME),
        }

        return results

    def reset_all_tariffs(self):
        self.duos_tariffs = []
        self.nuos_tariffs = []
        self.tuos_tariffs = []
        self.retail_tariffs = []

    def print_duos(self):
        for each in self.duos_tariffs:
            self.print_tariff(each)

    def array_to_string_buffer(self, array):
        t_string = io.StringIO()
        header_tariff = array[0]
        t_string.write(self.output_fields(header_tariff))

        for each in array:
            t_string.write(self.output_values(each))

        # This moves the pointer to the start of the file.
        t_string.seek(0)
        return t_string

    @staticmethod
    def print_tariff(tariff, ignore_empty=True):
        label = "Tariff object contains\n"
        lines = []

        for attr, value in tariff.__dict__.items():
            if value is '' and ignore_empty:
                pass
            else:
                x = ":".join([attr, str(value)])
                lines.append(x)

        joined = "\n".join(lines)
        print(label, joined)

    @staticmethod
    def output_values(tariff):
        csv_line = []
        for attr, value in tariff.__dict__.items():
            # print("Attr: ", attr, " Value: ", value)
            csv_line.append(value)

        joined_line = ','.join(csv_line)
        joined_line += "\n"

        return joined_line

    @staticmethod
    def output_fields(tariff):
        csv_line = []
        for attr, value in tariff.__dict__.items():
            csv_line.append(attr)

        joined_line = ','.join(csv_line)
        joined_line += "\n"
        return joined_line


class DuosTariff:
    def __init__(
                self,
                peak_charge,
                shoulder_charge,
                offpeak_charge,
                tariff_type='',
                tariff_name='',
                fit_input='',
                ref = '',
                dnsp = '',
                offer_name='',
                type='',
                daily_charge='',
                flat_charge='',
                block_1_charge='',
                block_2_charge='',
                controlled_load='',
                peak_start_time='',
                peak_end_time='',
                peak_start_time_2='',
                peak_end_time_2='',
                shoulder_start_time='',
                shoulder_end_time='',
                shoulder_start_time_2='',
                shoulder_end_time_2='',
                block_1_volume='',
                block_2_volume='',
                demand='',
                demand_units='',
                tou_weekday_only_flag=''):

        print("========== ==== = = = Creating DUOS Triff - tariff_name:", tariff_name, "offer_name", offer_name, "tariff_type", tariff_type)
        if offer_name == '':
            offer_name = tariff_name


        self.peak_charge = peak_charge
        self.shoulder_charge = shoulder_charge
        self.offpeak_charge = offpeak_charge
        self.tariff_type = tariff_type
        self.tariff_name = tariff_name
        self.fit_input = fit_input
        self.ref = ref
        self.dnsp = dnsp
        self.offer_name = offer_name
        self.type = type
        self.daily_charge = daily_charge
        self.flat_charge = flat_charge
        self.block_1_charge = block_1_charge
        self.block_2_charge = block_2_charge
        self.controlled_load = controlled_load
        self.peak_start_time = peak_start_time
        self.peak_end_time = peak_end_time
        self.peak_start_time = peak_start_time
        self.peak_start_time_2 = peak_start_time_2
        self.peak_end_time_2 = peak_end_time_2
        self.shoulder_start_time = shoulder_start_time
        self.shoulder_end_time = shoulder_end_time
        self.shoulder_start_time_2 = shoulder_start_time_2
        self.shoulder_end_time_2 = shoulder_end_time_2
        self.block_1_volume = block_1_volume
        self.block_2_volume = block_2_volume
        self.demand = demand
        self.demand_units = demand_units
        self.tou_weekday_only_flag = tou_weekday_only_flag


class NuosTariff:
    def __init__(
                self,
                peak_charge,
                shoulder_charge,
                offpeak_charge,
                tariff_type='',
                tariff_name='',
                fit_input='',
                ref = '',
                dnsp = '',
                offer_name='',
                type='',
                daily_charge='',
                flat_charge='',
                block_1_charge='',
                block_2_charge='',
                controlled_load='',
                peak_start_time='',
                peak_end_time='',
                peak_start_time_2='',
                peak_end_time_2='',
                shoulder_start_time='',
                shoulder_end_time='',
                shoulder_start_time_2='',
                shoulder_end_time_2='',
                block_1_volume='',
                block_2_volume='',
                demand='',
                demand_units='',
                tou_weekday_only_flag='',
                local_solar_import='',
                central_battery_import='',
                central_battery_local_solar_import=''):

        

        self.peak_charge = peak_charge
        self.shoulder_charge = shoulder_charge
        self.offpeak_charge = offpeak_charge
        self.tariff_type = tariff_type
        self.tariff_name = tariff_name
        self.fit_input = fit_input
        self.ref = ref
        self.dnsp = dnsp
        self.offer_name = tariff_name
        self.type = type
        self.daily_charge = daily_charge
        self.flat_charge = flat_charge
        self.block_1_charge = block_1_charge
        self.block_2_charge = block_2_charge
        self.controlled_load = controlled_load
        self.peak_start_time = peak_start_time
        self.peak_end_time = peak_end_time
        self.peak_start_time = peak_start_time
        self.peak_start_time_2 = peak_start_time_2
        self.peak_end_time_2 = peak_end_time_2
        self.shoulder_start_time = shoulder_start_time
        self.shoulder_end_time = shoulder_end_time
        self.shoulder_start_time_2 = shoulder_start_time_2
        self.shoulder_end_time_2 = shoulder_end_time_2
        self.block_1_volume = block_1_volume
        self.block_2_volume = block_2_volume
        self.demand = demand
        self.demand_units = demand_units
        self.tou_weekday_only_flag = tou_weekday_only_flag
        self.local_solar_import = local_solar_import
        self.central_battery_import = central_battery_import
        self.central_battery_local_solar_import = central_battery_local_solar_import


class TuosTariff:
    def __init__(
                self,
                peak_charge,
                shoulder_charge,
                offpeak_charge,
                tariff_type='',
                tariff_name='',
                fit_input='',
                ref = '',
                dnsp = '',
                offer_name='',
                type='',
                daily_charge='',
                flat_charge='',
                block_1_charge='',
                block_2_charge='',
                controlled_load='',
                peak_start_time='',
                peak_end_time='',
                peak_start_time_2='',
                peak_end_time_2='',
                shoulder_start_time='',
                shoulder_end_time='',
                shoulder_start_time_2='',
                shoulder_end_time_2='',
                block_1_volume='',
                block_2_volume='',
                demand='',
                demand_units='',
                tou_weekday_only_flag=''):

        self.peak_charge = peak_charge
        self.shoulder_charge = shoulder_charge
        self.offpeak_charge = offpeak_charge
        self.tariff_type = tariff_type
        self.tariff_name = tariff_name
        self.fit_input = fit_input
        self.ref = ref
        self.dnsp = dnsp
        self.offer_name = tariff_name
        self.type = type
        self.daily_charge = daily_charge
        self.flat_charge = flat_charge
        self.block_1_charge = block_1_charge
        self.block_2_charge = block_2_charge
        self.controlled_load = controlled_load
        self.peak_start_time = peak_start_time
        self.peak_end_time = peak_end_time
        self.peak_start_time = peak_start_time
        self.peak_start_time_2 = peak_start_time_2
        self.peak_end_time_2 = peak_end_time_2
        self.shoulder_start_time = shoulder_start_time
        self.shoulder_end_time = shoulder_end_time
        self.shoulder_start_time_2 = shoulder_start_time_2
        self.shoulder_end_time_2 = shoulder_end_time_2
        self.block_1_volume = block_1_volume
        self.block_2_volume = block_2_volume
        self.demand = demand
        self.demand_units = demand_units
        self.tou_weekday_only_flag = tou_weekday_only_flag


class RetailTariff:
    def __init__(self,
                 peak_charge,
                 shoulder_charge,
                 offpeak_charge,
                 tariff_type='',
                 tariff_name='',
                 fit_input='',
                 ref='',
                 retailer='',
                 offer_name='',
                 type='',
                 daily_charge='',
                 flat_charge='',
                 block_1_charge='',
                 block_2_charge='',
                 controlled_load='',
                 peak_start_time='',
                 peak_end_time='',
                 peak_start_time_2='',
                 peak_end_time_2='',
                 shoulder_start_time='',
                 shoulder_end_time='',
                 shoulder_start_time_2='',
                 shoulder_end_time_2='',
                 block_1_volume='',
                 block_2_volume='',
                 demand='',
                 demand_units='',
                 solar_tariff_1='',
                 solar_cap_1='',
                 solar_tariff_2='',
                 tou_weekday_only_flag=''):
        print("Creating Retail Tariff Object:", tariff_name)

        self.peak_charge = peak_charge
        self.shoulder_charge = shoulder_charge
        self.offpeak_charge = offpeak_charge
        self.tariff_type = tariff_type
        self.tariff_name = tariff_name
        self.fit_input = fit_input
        self.ref = ref
        self.retailer = retailer
        self.offer_name = tariff_name
        self.type = type
        self.daily_charge = daily_charge
        self.flat_charge = flat_charge
        self.block_1_charge = block_1_charge
        self.block_2_charge = block_2_charge
        self.controlled_load = controlled_load
        self.peak_start_time = peak_start_time
        self.peak_end_time = peak_end_time
        self.peak_start_time_2 = peak_start_time_2
        self.peak_end_time_2 = peak_end_time_2
        self.shoulder_start_time = shoulder_start_time
        self.shoulder_end_time = shoulder_end_time
        self.shoulder_start_time_2 = shoulder_start_time_2
        self.shoulder_end_time_2 = shoulder_end_time_2
        self.block_1_volume = block_1_volume
        self.block_2_volume = block_2_volume
        self.demand = demand
        self.demand_units = demand_units
        self.solar_tariff_1 = solar_tariff_1
        self.solar_cap_1 = solar_cap_1
        self.solar_tariff_2 = solar_tariff_2
        self.tou_weekday_only_flag = tou_weekday_only_flag

