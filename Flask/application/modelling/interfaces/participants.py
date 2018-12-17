class Participants:
    def __init__(self, data_dir):
        self.data_dir = data_dir

        self.participants = []

    def load(self, inputs):
        for each in inputs:
            row = each["row_inputs"]
            parameters = {}
            for each_dict in row:
                # print(each_dict, "\n")
                parameters[each_dict["name"]] = (each_dict["value"])
            print(parameters, "\n")
            self.participants.append(Participant(**parameters))


class Participant:
    def __init__(self,
                 participant_id,
                 participant_type,
                 retail_tariff_type,
                 load_data,
                 solar_data,
                 solar_scaling,
                 battery_type,
                 network_tariff_type=None):

        self.participant_id = participant_id
        self.participant_type = participant_type
        self.retail_tariff_type = retail_tariff_type

        self.load_data = load_data
        self.solar_data = solar_data
        self.solar_scaling = solar_scaling
        self.battery_type = battery_type

        # Maybe optional parameter
        self.network_tariff_type = network_tariff_type

        self.print()

    def print(self):
        print("Tariff Object Contains: {}, {}, {}".format(self.participant_id, self.participant_type, self.battery_type))

