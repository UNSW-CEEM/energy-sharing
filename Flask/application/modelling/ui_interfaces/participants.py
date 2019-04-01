import os
import csv
import io
import pandas as pd

DEFAULT_PARTICIPANTS_NAME = 'participants.csv'
DEFAULT_SOLAR_DATA_NAME = 'solar_data.csv'
DEFAULT_LOAD_DATA_NAME = 'load_data.csv'
DEFAULT_LOAD_PROFILE_NAME = 'load_profiles.csv'
DEFAULT_SOLAR_PROFILE_NAME = 'solar_profiles.csv'


class Participants:
    def __init__(self, folder_routes):
        self.luomi_defaults_dir = folder_routes.get_route("luomi_defaults_dir")
        self.load_profiles_dir = folder_routes.get_route("load_profiles_dir")
        self.solar_profiles_dir = folder_routes.get_route("solar_profiles_dir")

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

            p = Participant(**parameters)
            # p.print()
            self.participants.append(p)

        # After parsing the participants create the input files, solar_data, and load_data.
        self.create_data_files()

    # def add_participant(self, participant):
    #     # print(participant["input_rows"])
    #     parameters = {}
    #     for each in participant["input_rows"]:
    #         print(each["name"])
    #         if each["name"] == "central_solar_data":
    #             print(each["name"])
    #         else:
    #             parameters[each["name"]] = (each["value"])
    #
    #     p = Participant(**parameters)
    #     self.participants.append(p)

    def load_defaults(self):
        # Reset the list of participants
        self.participants = []

        default_participants_path = os.path.join(self.luomi_defaults_dir, DEFAULT_PARTICIPANTS_NAME)

        # Parse through each line in the default csv and create participants.
        with open(default_participants_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.participants.append(Participant(**row))

        # After parsing the participants create the input files, solar_data, and load_data.
        self.create_data_files()

    def get_participants_as_string(self):
        output = io.StringIO()
        output.write(self.participants[0].output_header_fields())
        for each in self.participants:
            output.write(each.output_values())

        output.seek(0)
        return output

    def create_data_files(self):
        # TODO Remove semi hard coding from these paths.
        # ^^^ I think use a selector method in folder_routes that sets a shared path depending on the model selected.
        # Or maybe they will need completely separate methods. Not sure.

        # Set output data file paths
        load_data_file = os.path.join(self.luomi_defaults_dir, DEFAULT_LOAD_DATA_NAME)
        solar_data_file = os.path.join(self.luomi_defaults_dir, DEFAULT_SOLAR_DATA_NAME)

        # Get the paths for input profile data
        load_profiles = os.path.join(self.load_profiles_dir, DEFAULT_LOAD_PROFILE_NAME)
        solar_profiles = os.path.join(self.solar_profiles_dir, DEFAULT_SOLAR_PROFILE_NAME)

        self.csv_combiner(input_path=load_profiles, output_path=load_data_file, solar_profiles=False)
        self.csv_combiner(input_path=solar_profiles, output_path=solar_data_file, solar_profiles=True)

    def csv_combiner(self, input_path, output_path, solar_profiles=True):
        # Make sure output file is empty
        self.clear_csv(output_path)

        # Key to merge the csv's based on their common timestamp column
        common_key = "timestamp"
        all_to_combine = []

        for p in self.participants:
            # If this is combining solar it uses the solar profile keyword and sets the solar file path to the
            # participant object. Otherwise load & load path set.
            if solar_profiles:
                p_profile = p.solar_profile
                p.solar_path = output_path
            else:
                p_profile = p.load_profile
                p.load_path = output_path

            p_id = p.participant_id
            p_data = io.StringIO()

            with open(input_path) as inputs:
                reader = csv.DictReader(inputs)
                # Set the headers to the common key (timestamp) and the desired header (participant_id)
                writer = csv.DictWriter(p_data, fieldnames=[common_key, p_id])
                writer.writeheader()

                for row in reader:
                    # Writes the PROFILE data to the PARTICIPANT_ID header.
                    if common_key in row and p_profile in row:
                        this_row = {common_key: row[common_key], p_id: row[p_profile]}
                        
                        writer.writerow(this_row)

                # Put the pointer back to the start of the file
                p_data.seek(0)

            # Append this csv to the list of csvs all containing an individual participants data
            all_to_combine.append(p_data)

        # Merge all the csvs together using their common key (timestamp)
        a = pd.read_csv(all_to_combine.pop(0))

        for each in all_to_combine:
            b = pd.read_csv(each)
            a = a.merge(b, on=common_key)

        # Finally write combined CSV to the output path
        a.to_csv(output_path, index=False)

    @staticmethod
    def clear_csv(path):
        f = open(path, "w+")
        f.close()


class Participant:
    def __init__(self,
                 participant_id='',
                 participant_type='',
                 retail_tariff_type='',
                 network_tariff_type='LV TOU <100MWh',
                 retailer='ENOVA',
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
