import csv
import os
from .participant import CSV_Participant


class Network:
    def __init__(self, name):
        self.name = name
        self.participant_list = []
        self.battery_list = []

    def test(self) :
        # print('hello world')
        print(self.name)

    def add_participant(self, participant):
        self.participant_list.append(participant)

    def get_participants(self):
        return self.participant_list
    
    def calc_total_participant_export(self, date_time, interval_min):
        """Calculates the total participant export after local solar is traded."""
        total = 0
        for p in self.participant_list :
            total += p.calc_net_export(date_time, interval_min)
        return total
    
    def add_central_battery(self, battery):
        self.battery_list.append(battery)
    
    def get_batteries(self):
        return self.battery_list

    def add_participants_from_csv(self, data_dir, participant_csv):
        with open(os.path.join(data_dir, participant_csv)) as f:
            reader = csv.DictReader(f, delimiter=",")
            for line in reader: 
                # print line
                participant = CSV_Participant(
                    participant_id=line['participant_id'],
                    participant_type=line['participant_type'],
                    retail_tariff_type=line['retail_tariff_type'],
                    network_tariff_type=line['network_tariff_type'],
                    retailer=line['retailer'],
                    solar_path=os.path.join(data_dir, line['solar_path']),
                    load_path=os.path.join(data_dir, line['load_path']),
                    solar_scaling=float(line['solar_scaling'])
                )
                self.add_participant(participant)

    def add_participants_from_string(self, data_dir, load_path, solar_path, participants_string):
        reader = csv.DictReader(participants_string, delimiter=",")
        for line in reader:
            print("Adding Participant with solar capacity:", float(line['solar_scaling']))
            participant = CSV_Participant(
                participant_id=line['participant_id'],
                participant_type=line['participant_type'],
                retail_tariff_type=line['retail_tariff_type'],
                network_tariff_type=line['network_tariff_type'],
                retailer=line['retailer'],
                solar_path=os.path.join(data_dir,'shared','solar', solar_path),
                load_path=os.path.join(data_dir,'shared', 'load',load_path),
                solar_scaling=float(line['solar_scaling']),
                load_profile=line['load_profile'],
                solar_profile = line['solar_profile']
            )
            self.add_participant(participant)
