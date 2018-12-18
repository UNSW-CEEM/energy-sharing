import os
import csv


class Participants:
    def __init__(self, data_dir):
        self.data_dir = data_dir

        self.participants = []

    def load(self, inputs):
        # Reset the list of participants
        self.participants = []

        # Sort through the UI input arrays and create participants.
        for each in inputs:
            row = each["row_inputs"]
            parameters = {}
            for each_dict in row:
                # print(each_dict, "\n")
                parameters[each_dict["name"]] = (each_dict["value"])
            self.participants.append(Participant(**parameters))

    def load_defaults(self):
        # Reset the list of participants
        self.participants = []

        default_participants_path = os.path.join(self.data_dir, "defaults/participants.csv")

        # Parse through each line in the default csv and create participants.
        with open(default_participants_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.participants.append(Participant(**row))


class Participant:
    def __init__(self,
                 participant_id,
                 participant_type,
                 retail_tariff_type,
                 load_path,
                 solar_path,
                 solar_scaling=None,
                 battery_type=None,
                 network_tariff_type=None,
                 retailer=None,
                 solar_capacity=None):

        self.participant_id = participant_id
        self.participant_type = participant_type
        self.retail_tariff_type = retail_tariff_type

        self.load_path = load_path
        self.solar_path = solar_path

        # Maybe optional parameter
        self.solar_scaling = solar_scaling
        self.battery_type = battery_type
        self.network_tariff_type = network_tariff_type
        self.retailer = retailer
        self.solar_capacity = solar_capacity

        self.print()

    def print(self):
        print("Participant Object Contains: {}, {}, {}".format(
            self.participant_id, self.participant_type, self.solar_scaling))
