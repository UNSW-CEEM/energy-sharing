import io
import numpy as np
import pandas as pd
from . import util


class Participant: 
    # Need to update to have both network and retail tariffs as inputs
    def __init__(self, participant_id, participant_type, retail_tariff_type, network_tariff_type,retailer):
        self.participant_id = participant_id
        self.participant_type = participant_type
        self.retail_tariff_type = retail_tariff_type
        self.network_tariff_type = network_tariff_type
        self.retailer = retailer
    
    def print_attributes(self):
        print(self.participant_type, self.retail_tariff_type, self.network_tariff_type, self.retailer)

    # TODO - make this work
    def calc_net_export(self, date_time, interval_min):
        return np.random.uniform(-10, 10)

    def get_id(self):
        return self.participant_id

    def get_retail_tariff_type(self):
        return self.retail_tariff_type

    def get_network_tariff_type(self):
        return self.network_tariff_type


class CSV_Participant(Participant):
    def __init__(self, participant_id, participant_type, retail_tariff_type, network_tariff_type, retailer, solar_path, load_path, solar_capacity):
        Participant.__init__(self, participant_id, participant_type, retail_tariff_type, network_tariff_type, retailer)
        self.solar_path = solar_path
        self.load_path = load_path
        solar_data = pd.read_csv(solar_path, index_col='timestamp', parse_dates=True, date_parser=util.date_parser)
        load_data = pd.read_csv(load_path, index_col='timestamp', parse_dates=False, date_parser=util.date_parser)
        # Delete all cols not relevant to this participant
        self.load_data = load_data[participant_id]
        self.solar_data = solar_data[participant_id]
        # Apply capacity to solar data
        self.solar_data = self.solar_data * solar_capacity
        # print solar_data
        
    def calc_net_export(self, date_time, interval_min):
        solar_data = float(self.solar_data.loc[date_time])
        load_data = float(self.load_data.loc[date_time])
        net_export = solar_data - load_data
        return net_export


