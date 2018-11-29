def parse_total_participants_bill(tpb):
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
