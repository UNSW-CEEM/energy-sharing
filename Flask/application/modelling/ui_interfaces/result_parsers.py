import os
import csv


# May change this to a helper module with no class. Just functions
class ResultParsers:
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def parse_total_participants_bill(self, tpb):
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