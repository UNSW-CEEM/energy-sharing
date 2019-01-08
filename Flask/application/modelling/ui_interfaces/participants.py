import os
import csv
import io
import pandas as pd

DEFAULT_PARTICIPANTS_NAME = 'participants.csv'
DEFAULT_SOLAR_DATA_NAME = 'solar_data.csv'
DEFAULT_LOAD_DATA_NAME = 'load_data.csv'
DEFAULT_LOAD_PROFILE_NAME = 'load_profiles.csv'


class Participants:
    def __init__(self, folder_routes):
        self.luomi_defaults_dir = folder_routes.get_route("luomi_defaults_dir")
        self.load_profiles_dir = folder_routes.get_route("load_profiles_dir")

        self.participants = []

    def load(self, inputs):
        # Reset the list of participants
        self.participants = []

        # Parse through the UI input arrays and create participants.
        for each in inputs:
            row = each["row_inputs"]
            parameters = {}
            for each_dict in row:
                # print(each_dict, "\n")
                parameters[each_dict["name"]] = (each_dict["value"])

            # TODO I think this will be temporary
            if parameters["solar_path"] is '':
                parameters["solar_path"] = os.path.join(self.luomi_defaults_dir, DEFAULT_SOLAR_DATA_NAME)
            if parameters["load_path"] is '':
                parameters["load_path"] = os.path.join(self.luomi_defaults_dir, DEFAULT_LOAD_DATA_NAME)

            p = Participant(**parameters)
            # p.print()
            self.participants.append(p)

        self.create_load_data()

    def load_defaults(self):
        # Reset the list of participants
        self.participants = []

        default_participants_path = os.path.join(self.luomi_defaults_dir, DEFAULT_PARTICIPANTS_NAME)

        # Parse through each line in the default csv and create participants.
        with open(default_participants_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.participants.append(Participant(**row))

        self.create_load_data()

    def get_participants_as_string(self):
        output = io.StringIO()
        output.write(self.participants[0].output_header_fields())
        for each in self.participants:
            output.write(each.output_values())

        output.seek(0)
        return output

    # TODO this function could be improved maybe.
    def get_load_profiles(self):
        d = []
        for each in self.participants:
            d.append({each.participant_id: each.load_path})

        return d

    def create_load_data(self):
        # Find the final load csv and clear it
        final_loads = os.path.join(self.luomi_defaults_dir, DEFAULT_LOAD_DATA_NAME)
        self.clear_csv(final_loads)

        # Get the path to the profiles data
        load_profiles = os.path.join(self.load_profiles_dir, DEFAULT_LOAD_PROFILE_NAME)

        # Column to merge everything upon
        profile_index = "timestamp"
        all_profiles = []

        for each in self.participants:
            this_profile = each.solar_profile
            this_participant = each.participant_id
            each.solar_path = os.path.realpath(os.path.join(self.luomi_defaults_dir, "solar_data.csv"))
            each.load_path = final_loads

            to_join = io.StringIO()

            with open(load_profiles) as file:
                reader = csv.DictReader(file)
                writer = csv.DictWriter(to_join, fieldnames=[profile_index, this_participant])
                writer.writeheader()
                for row in reader:
                    this_row = {profile_index: row[profile_index], this_participant: row[this_profile]}
                    writer.writerow(this_row)

                to_join.seek(0)

            all_profiles.append(to_join)

        a = pd.read_csv(all_profiles.pop(0))

        for each in all_profiles:
            b = pd.read_csv(each)
            a = a.merge(b, on=profile_index)

        a.to_csv(final_loads, index=False)
        # return a

    @staticmethod
    def clear_csv(path):
        f = open(path, "w+")
        f.close()


class Participant:
    def __init__(self,
                 participant_id='',
                 participant_type='',
                 retail_tariff_type='',
                 network_tariff_type='',
                 retailer='',
                 solar_profile='',
                 load_profile='',
                 solar_capacity=0,
                 solar_scaling='',
                 battery_type='',
                 ):

        # Ordering important here since I use __dict__.items() to spit out these.
        self.participant_id = participant_id
        self.participant_type = participant_type
        self.retail_tariff_type = retail_tariff_type
        self.network_tariff_type = network_tariff_type
        self.retailer = retailer
        self.solar_profile = solar_profile
        self.load_profile = load_profile
        self.solar_capacity = solar_capacity
        self.solar_scaling = solar_scaling
        self.battery_type = battery_type

        # Trial
        self.solar_path = None
        self.load_path = None

    def print(self):
        label = "Participant Object Contains:\n"

        lines = []
        for attr, value in self.__dict__.items():
            x = ":".join([attr, str(value)])
            lines.append(x)

        joined = "\n".join(lines)

        print(label, joined)

    # I think this could maybe be just done using __repr__
    def output_values(self):
        csv_line = []
        for attr, value in self.__dict__.items():
            # print("Key values in this participant: ", attr, value)
            csv_line.append(str(value))

        joined_line = ",".join(csv_line)
        joined_line += "\n"
        return joined_line

    def output_header_fields(self):
        csv_line = []
        for attr, value in self.__dict__.items():
            # print("Key values in this participant: ", attr, value)
            csv_line.append(attr)

        joined_line = ",".join(csv_line)
        joined_line += "\n"
        return joined_line
