import os
import csv


# May change this to a helper module with no class. Just functions
class ResultParsers:
    def __init__(self, data_dir):
        self.data_dir = data_dir

        self.output_dir = os.path.join(self.data_dir, 'output')

    def temp_parser(self, battery_capacity):
        energy_flows_path = os.path.join(
            self.output_dir,
            ("df_network_energy_flows" + str(battery_capacity) + ".csv")
        )

        total_participant_bill_path = os.path.join(
            self.output_dir,
            ("df_total_participant_bill" + str(battery_capacity) + ".csv")
        )
        energy_flows_data = []
        total_participant_bill = []

        with open(energy_flows_path) as fileOne:
            reader = csv.DictReader(fileOne)
            for row in reader:
                energy_flows_data.append(row)

        with open(total_participant_bill_path) as fileTwo:
            reader = csv.DictReader(fileTwo)
            for row in reader:
                total_participant_bill.append(row)

        tpb = self.parse_total_participants_bill(total_participant_bill)

        results = {
            "energy_flows": energy_flows_data,
            "total_participant_bill": tpb
        }

        return results

    @staticmethod
    def parse_total_participants_bill(tpb):
        # Takes in the TPB data and returns it in a more manageable structure.
        data_points = {}

        for each in tpb:
            for key, value in each.items():
                # print("Key:", key, " Value: ", value, "\n")
                if key == "":
                    pass
                else:
                    if key not in data_points:
                        data_points[key] = 0
                    else:
                        data_points[key] += float(value)

        return data_points
