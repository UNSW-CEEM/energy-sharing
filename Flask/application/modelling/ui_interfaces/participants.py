import os
import csv
import io

DEFAULT_PARTICIPANTS_NAME = 'participants.csv'
DEFAULT_SOLAR_NAME = 'solar_data.csv'
DEFAULT_LOAD_NAME = 'load_data.csv'


class Participants:
    def __init__(self, folder_routes):
        self.luomi_defaults_dir = folder_routes.get_route("luomi_defaults_dir")

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
                parameters["solar_path"] = os.path.join(self.luomi_defaults_dir, DEFAULT_SOLAR_NAME)
            if parameters["load_path"] is '':
                parameters["load_path"] = os.path.join(self.luomi_defaults_dir, DEFAULT_LOAD_NAME)

            p = Participant(**parameters)
            # p.print()
            self.participants.append(p)

    def load_defaults(self):
        # Reset the list of participants
        self.participants = []

        default_participants_path = os.path.join(self.luomi_defaults_dir, DEFAULT_PARTICIPANTS_NAME)

        # Parse through each line in the default csv and create participants.
        with open(default_participants_path) as file:
            reader = csv.DictReader(file)
            for row in reader:

                # TODO Think of a better way to handle this.
                # I don't want to have hardcoded paths in the csv. Which means having to use
                # OS to create the path somewhere. Here seems best for now.
                row["solar_path"] = os.path.join(self.luomi_defaults_dir, row["solar_path"])
                row["load_path"] = os.path.join(self.luomi_defaults_dir, row["load_path"])

                self.participants.append(Participant(**row))

    def get_participants_as_string(self):
        output = io.StringIO()
        output.write(self.participants[0].output_header_fields())
        for each in self.participants:
            output.write(each.output_values())

        output.seek(0)
        return output


class Participant:
    def __init__(self,
                 participant_id='',
                 participant_type='',
                 retail_tariff_type='',
                 network_tariff_type='',
                 retailer='',
                 solar_path='',
                 load_path='',
                 solar_capacity=0,
                 solar_scaling='',
                 battery_type=''
                 ):

        # Ordering important here since I use __dict__.items() to spit out these.
        self.participant_id = participant_id
        self.participant_type = participant_type
        self.retail_tariff_type = retail_tariff_type
        self.network_tariff_type = network_tariff_type
        self.retailer = retailer
        self.solar_path = solar_path
        self.load_path = load_path
        self.solar_capacity = solar_capacity
        self.solar_scaling = solar_scaling
        self.battery_type = battery_type

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
