import os
import csv


# May change this to a helper module with no class. Just functions
class ResultParsers:
    def __init__(self, folder_routes):
        self.luomi_dir = folder_routes.get_route("luomi_dir")

        self.luomi_output_dir = folder_routes.get_route("luomi_output_dir")

    def temp_parser(self, battery_capacity):
        energy_flows_path = os.path.join(
            self.luomi_output_dir,
            ("df_network_energy_flows" + str(battery_capacity) + ".csv")
        )

        total_participant_bill_path = os.path.join(
            self.luomi_output_dir,
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
        rev_participant = self.parse_revenue_participants(total_participant_bill)

        results = {
            "energy_flows": energy_flows_data,
            "total_participant_bill": tpb,
            "revenue_participant": rev_participant,
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

    @staticmethod
    def parse_revenue_participants(data):
        timestamps = []
        data_points = {}

        for each in data:
            # print(each)
            for key, value in each.items():
                if key == "":
                    timestamps.append(value)
                else:
                    if key not in data_points:
                        data_points[key] = []
                        data_points[key].append(value)
                    else:
                        data_points[key].append(value)

        # print("\n|\nTimestamps:", timestamps)
        # print("\n|\nData Points:", data_points)

        return {"timestamps": timestamps, "data_points": data_points}
