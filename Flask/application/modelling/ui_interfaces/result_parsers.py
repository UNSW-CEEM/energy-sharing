import os
import csv


# May change this to a helper module with no class. Just functions
class ResultParsers:
    def __init__(self, folder_routes):
        self.luomi_dir = folder_routes.get_route("luomi_dir")
        self.luomi_output_dir = folder_routes.get_route("luomi_output_dir")

        self.mike_output_dir = folder_routes.get_route("mike_output_dir")
        self.mike_output_file_path = os.path.join(
            self.mike_output_dir, "ceem_ui_default", "scenarios", "ceem_ui_default_001.csv"
        )

    def mike_temp_parser(self):
        row_data = []

        # All info on one line.
        with open(self.mike_output_file_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                row_data.append(row)

        customer_bills = {}
        customer_solar_bills = {}
        customer_totals = {}
        scenario_info = {}

        for row in row_data:
            for key, value in row.items():
                if "cust_bill" in key:
                    customer_bills[key] = value
                elif "cust_solar" in key:
                    customer_solar_bills[key] = value
                elif "cust_total" in key:
                    customer_totals[key] = value
                else:
                    scenario_info[key] = value

        tpb = self.mike_parse_tpb(customer_totals)
        rev_participant = False
        revenue_retailer = False
        energy_gencon = False
        energy_cc = False

        results = {
            "total_participant_bill": tpb,
            "revenue_participant": rev_participant,
            "revenue_retailer": revenue_retailer,
            "energy_gencon": energy_gencon,
            "energy_cc": energy_cc,
        }

        return results

    @staticmethod
    def mike_parse_tpb(data):
        for each in data:
            # print(each, data[each])
            pass

        return data

    def luomi_temp_parser(self, battery_capacity):
        energy_flows_path = os.path.join(
            self.luomi_output_dir,
            ("df_network_energy_flows" + str(battery_capacity) + ".csv")
        )

        total_participant_bill_path = os.path.join(
            self.luomi_output_dir,
            ("df_total_participant_bill" + str(battery_capacity) + ".csv")
        )

        retailer_revenue_path = os.path.join(
            self.luomi_output_dir,
            ("df_retailer_revenue" + str(battery_capacity) + ".csv")
        )

        energy_gencon_path = os.path.join(
            self.luomi_output_dir,
            ("df_net_export" + str(battery_capacity) + ".csv")
        )

        energy_cc_path = os.path.join(
            self.luomi_output_dir,
            ("df_net_export" + str(battery_capacity) + ".csv")
        )

        energy_flows_data = []
        total_participant_bill = []
        retailer_revenue_data = []
        energy_gencon_data = []
        energy_cc_data = []

        with open(energy_flows_path) as fileOne:
            reader = csv.DictReader(fileOne)
            for row in reader:
                energy_flows_data.append(row)

        with open(total_participant_bill_path) as fileTwo:
            reader = csv.DictReader(fileTwo)
            for row in reader:
                total_participant_bill.append(row)

        with open(retailer_revenue_path) as fileThree:
            reader = csv.DictReader(fileThree)
            for row in reader:
                retailer_revenue_data.append(row)

        with open(energy_gencon_path) as fileFour:
            reader = csv.DictReader(fileFour)
            for row in reader:
                energy_gencon_data.append(row)

        with open(energy_cc_path) as fileFive:
            reader = csv.DictReader(fileFive)
            for row in reader:
                energy_cc_data.append(row)

        tpb = self.parse_total_participants_bill(total_participant_bill)
        rev_participant = self.parse_revenue_participants(total_participant_bill)
        revenue_retailer = self.parse_revenue_retailer(retailer_revenue_data)
        energy_gencon = self.parse_energy_gen_con(energy_gencon_data)
        energy_cc = self.parse_energy_cc(energy_cc_data)

        results = {
            "energy_flows": energy_flows_data,
            "total_participant_bill": tpb,
            "revenue_participant": rev_participant,
            "revenue_retailer": revenue_retailer,
            "energy_gencon": energy_gencon,
            "energy_cc": energy_cc,
        }

        return results

    # 1 TPB - Total Participants Bill
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
                        if value != "":
                            data_points[key] += float(value)

        return data_points

    # 2 EnergyGenCon - Half hourly energy Generation/Consumption for each participant
    def parse_energy_gen_con(self, data):
        return self.general_parser(data)

    # 3 RevParticipant - Half hourly revenue for each participant
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

        return {"timestamps": timestamps, "data_points": data_points}

    # 4 RevRCC - Half-hourly revenue for retailer, central_battery, central_solar
    @staticmethod
    def parse_revenue_retailer(data):
        timestamps = []
        data_points = {}

        for each in data:
            for key, value in each.items():
                if key == "":
                    timestamps.append(value)
                else:
                    if key not in data_points:
                        data_points[key] = []
                        data_points[key].append(value)
                    else:
                        data_points[key].append(value)

        return {"timestamps": timestamps, "data_points": data_points}

    # 5 EnergyCC - half-hourly central battery charge, central solar generation
    def parse_energy_cc(self, data):
        return self.general_parser(data)

    # This is useful for several different parsers. Call if appropriate.
    @staticmethod
    def general_parser(data):
        timestamps = []
        data_points = {}

        for each in data:
            for key, value in each.items():
                if key == "":
                    timestamps.append(value)
                else:
                    if key not in data_points:
                        data_points[key] = []
                        data_points[key].append(value)
                    else:
                        data_points[key].append(value)

        return {"timestamps": timestamps, "data_points": data_points}
