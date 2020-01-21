import numpy as np
import pandas as pd
import datetime
import io


class Tariffs():

    def __init__(self, tariff_config_dict):
        self.config = tariff_config_dict
        print("What you're looking for", self.config['retail']['daily_charge'])
    
    def get_variable_retail_tariff(self, date_time, retail_tariff_type):
        # Get data from df
        
        peak_charge	= float(self.config['retail']['peak_tariff'])
        shoulder_charge	= float(self.config['retail']['shoulder_tariff'])
        offpeak_charge = float(self.config['retail']['off_peak_tariff'])
        block_1_charge = float(self.config['retail']['block_1_tariff'])
        block_2_charge = float(self.config['retail']['block_2_tariff'])
        
        peak_start_time = float(self.config['tou_times'][1])
        peak_end_time = float(self.config['tou_times'][2])
        peak_start_time_2 = float(self.config['tou_times'][1])  # Making these the same - just going to have one peak for the moment but leaving the option for 2.
        peak_end_time_2 = float(self.config['tou_times'][2])
        shoulder_start_time = float(self.config['tou_times'][0])
        shoulder_end_time = float(self.config['tou_times'][1])
        shoulder_start_time_2 = float(self.config['tou_times'][2])
        shoulder_end_time_2 = float(self.config['tou_times'][3])
        block_1_volume = float(self.config['retail']['block_1_volume'])
        block_2_volume = float(self.config['retail']['block_2_volume'])
        
        tou_weekday_only_flag = False

        if retail_tariff_type == 'Block':
            variable_tariff = (block_1_charge, block_2_charge, block_1_volume)
        elif retail_tariff_type == 'TOU':
            variable_tariff = (peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag)
        else:
            raise ValueError('Retail tariff type not known:'+str(retail_tariff_type))

        return variable_tariff

    def get_local_solar_import_tariff(self, date_time):
        """
            The amount which the Participant pays for local solar they consume.
        """
        local_solar_import_tariff = float(self.config['local_solar']['energy']) + float(self.config['local_solar']['retail']) + float(self.config['local_solar']['duos']) + float(self.config['local_solar']['tuos'])
        return local_solar_import_tariff
    

    def get_local_solar_export_tariff(self, date_time):
        """Input in UI. 
        Is the amount which the Participant is paid for local solar they generate."""
        local_solar_export_tariff = float(self.config['local_solar']['energy'])
        return local_solar_export_tariff


    def get_central_batt_tariff(self,date_time):
        """This is the tariff paid by the battery to the solar owner when importing solar. It should ONLY include energy and is what the participant RECEIVES."""
        """Input in UI"""
        return float(self.config['central_battery']['local_solar_import_energy'])

    def get_central_batt_buy_tariff(self,date_time):
        """This is the tariff paid by the participant to the battery when consuming battery export electricity."""
        """Input in UI"""
        participant_central_battery_import_tariff = float(self.config['central_battery']['energy']) + float(self.config['central_battery']['retail']) + float(self.config['central_battery']['duos']) + float(self.config['central_battery']['tuos']) + float(self.config['central_battery']['nuos']) + float(self.config['central_battery']['profit'])
        # print(self.config['central_battery'])
        # print("energy", self.config['central_battery']['energy'])
        # print("retail", self.config['central_battery']['retail'])
        # print("duos", self.config['central_battery']['duos'])
        # print("tuos", self.config['central_battery']['tuos'])
        # print("nuos", self.config['central_battery']['nuos'])
        # print("profit", self.config['central_battery']['profit'])
        
        # print(participant_central_battery_import_tariff)
        return participant_central_battery_import_tariff

    def get_retail_solar_tariff(self,date_time, retail_tariff_type, solar_capacity):
        """Solar FiT component from retail tariff data."""
        return float(self.config['feed_in_tariff']['energy'])

    def get_fixed_tariff(self, fixed_period_minutes, retail_tariff_type):
        """Fixed tariff component from retail tariff data. Returns fixed value expressed per fixed period minutes (input)."""
        # print(self.config['retail']['daily_charge'], type(self.config['retail']['daily_charge']))
        fixed_tariff = float(self.config['retail']['daily_charge']) * (float(fixed_period_minutes)/float(60*24))
        return fixed_tariff

    # Things the network is paid (fixed DUOS charges, variable DUOS charges, local solar DUOS charges, central battery DUOS charges)
    # Apply to amounts consumer each time period then sum for total network income
    def get_duos_on_grid_import_fixed(self,fixed_period_minutes, duos_tariff_type):

        fixed_tariff = float(self.config['duos']['daily_charge']) * (float(fixed_period_minutes)/float(60*24))
        return fixed_tariff

    def get_duos_on_grid_import_variable(self,date_time, duos_tariff_type):
        """Variable tariff component from DUOS tariff data."""
        # Get data from df
        
        peak_charge	= float(self.config['duos']['peak_tariff'])
        shoulder_charge	= float(self.config['duos']['shoulder_tariff'])
        offpeak_charge = float(self.config['duos']['off_peak_tariff'])
        peak_start_time	= float(self.config['tou_times'][1])
        peak_end_time = float(self.config['tou_times'][2])
        peak_start_time_2 = float(self.config['tou_times'][1]) #Making these the same - just going to have one peak for the moment but leaving the option for 2. 
        peak_end_time_2	= float(self.config['tou_times'][2])
        shoulder_start_time	= float(self.config['tou_times'][0])
        shoulder_end_time = float(self.config['tou_times'][1])
        shoulder_start_time_2 = float(self.config['tou_times'][2])
        shoulder_end_time_2	= float(self.config['tou_times'][3])
        demand_charge = float(self.config['duos']['demand_charge'])
        tou_weekday_only_flag = float(self.config['duos']['tou_weekday_only'])

       
        # Note, demand charge included in returned values to make calculations in main.py nicer to work with (avoid repeating TOU calcs for demand charge case)
        
        variable_tariff = (peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag, demand_charge)
        
       
        return variable_tariff

 

    def get_duos_on_local_solar_import(self,date_time):
        """From UI"""
        return float(self.config['local_solar']['duos'])
        

    def get_duos_on_central_batt_import(self,date_time):
        """This is the DUOS paid by the customer when consuming battery export."""
        return float(self.config['central_battery']['duos'])

    def get_duos_on_central_batt_solar_import(self,date_time):
        """This is the DUOS paid by the battery when importing local solar."""
        return float(self.config['central_battery']['local_solar_import_duos'])

    # Transmission use of service charges - will presumably be zero for local solar and battery import
    def get_tuos_on_grid_import_fixed(self,fixed_period_minutes, tuos_tariff_type):
        fixed_tariff = float(self.config['tuos']['daily_charge']) * (float(fixed_period_minutes)/float(60*24))
        return fixed_tariff

    def get_tuos_on_grid_import_variable(self,date_time, tuos_tariff_type):    
        """Variable tariff component from TUOS tariff data."""
        # Get data from df
       
        peak_charge	= float(self.config['tuos']['peak_tariff'])
        shoulder_charge	= float(self.config['tuos']['shoulder_tariff'])
        offpeak_charge = float(self.config['tuos']['off_peak_tariff'])
        peak_start_time	= float(self.config['tou_times'][1])
        peak_end_time = float(self.config['tou_times'][2])
        peak_start_time_2 = float(self.config['tou_times'][1]) #Making these the same - just going to have one peak for the moment but leaving the option for 2. 
        peak_end_time_2	= float(self.config['tou_times'][2])
        shoulder_start_time	= float(self.config['tou_times'][0])
        shoulder_end_time = float(self.config['tou_times'][1])
        shoulder_start_time_2 = float(self.config['tou_times'][2])
        shoulder_end_time_2	= float(self.config['tou_times'][3])
        demand_charge = float(self.config['tuos']['daily_charge'])
        tou_weekday_only_flag = float(self.config['tuos']['tou_weekday_only'])

        # Note, demand charge included in returned values to make calculations in main.py nicer to work with (avoid repeating TOU calcs for demand charge case)
        variable_tariff = (peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag, demand_charge)
        
        return variable_tariff

    # TODO - should this be zero?
    def get_tuos_on_local_solar_import(self,date_time):
        return float(self.config['local_solar']['tuos'])

    # TODO - should this be zero?
    def get_tuos_on_central_batt_import(self,date_time):
        """This is the TUOS paid by the customer when consuming battery export."""
        return float(self.config['central_battery']['tuos'])
    
    # TODO - should this be zero?
    def get_tuos_on_central_batt_solar_import(self,date_time):
        """This is the TUOS paid by the battery when importing local solar."""
        return float(self.config['central_battery']['local_solar_import_tuos'])

    # Network use of service charges (TUOS + DUOS + green schemes and friends) - will presumably be zero for local solar and battery import
    def get_nuos_on_grid_import_fixed(self,fixed_period_minutes, nuos_tariff_type):
        # print("!!!!!!!!!!!!!!!!!!!!!!!")
        # print(self.nuos_tariff_data)
        # print("!!!!!!!!!!!!!!!!!!!!!!!")
        fixed_tariff = float(self.config['nuos']['daily_charge']) * (float(fixed_period_minutes)/float(60*24))
        return fixed_tariff

    def get_nuos_on_grid_import_variable(self,date_time, nuos_tariff_type):
        """Variable tariff component from NUOS tariff data."""
        # Get data from df
        
        peak_charge	= float(self.config['nuos']['peak_tariff'])
        shoulder_charge	= float(self.config['nuos']['shoulder_tariff'])
        offpeak_charge = float(self.config['nuos']['off_peak_tariff'])

        peak_start_time	= float(self.config['tou_times'][1])
        peak_end_time = float(self.config['tou_times'][2])
        peak_start_time_2 = float(self.config['tou_times'][1]) #Making these the same - just going to have one peak for the moment but leaving the option for 2. 
        peak_end_time_2	= float(self.config['tou_times'][2])
        shoulder_start_time	= float(self.config['tou_times'][0])
        shoulder_end_time = float(self.config['tou_times'][1])
        shoulder_start_time_2 = float(self.config['tou_times'][2])
        shoulder_end_time_2	= float(self.config['tou_times'][3])
        
        demand_charge = float(self.config['nuos']['demand_charge'])
        tou_weekday_only_flag = float(self.config['nuos']['tou_weekday_only'])

        # Note, demand charge included in returned values to make calculations in main.py nicer to work with (avoid repeating TOU calcs for demand charge case)
        variable_tariff = (peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag, demand_charge)
        
        return variable_tariff 


    def get_nuos_on_local_solar_import(self,date_time, nuos_tariff_type):
        return float(self.config['local_solar']['tuos'])

    def get_nuos_on_central_batt_import(self,date_time, nuos_tariff_type):
        """This is the NUOS paid by the customer when consuming battery export."""
        return float(self.config['central_battery']['nuos'])
    
    def get_nuos_on_central_batt_solar_import(self,date_time, nuos_tariff_type):
        """This is the NUOS paid by the battery when importing local solar."""
        return float(self.config['central_battery']['local_solar_import_nuos'])


    # Things the retailer is paid (fixed retail charges, variable retail charges, local solar retail charges, central battery retail charges)
    def get_retail_income_on_local_solar_import(self,date_time):
        return float(self.config['local_solar']['retail'])

    def get_retail_income_on_central_batt_import(self,date_time):
        """This is the retailer charge paid by the customer when consuming battery export."""
        return float(self.config['central_battery']['retail'])

    def get_retail_income_on_central_batt_solar_import(self,date_time):
        """This is the retailer charge paid by the battery when importing local solar."""
        return float(self.config['central_battery']['local_solar_import_retail'])

    # Total battery import tariff (i.e. what the battery has to pay when importing energy) Includes energy payment + NUOS payment + retail payment
    def get_total_central_battery_import_tariff(self, date_time):
        """What the battery pays when importing energy"""
        total_battery_import_tariff = self.get_central_batt_tariff(date_time) + self.get_duos_on_central_batt_solar_import(date_time) + self.get_tuos_on_central_batt_solar_import(date_time) + self.get_retail_income_on_central_batt_solar_import(date_time)
        return total_battery_import_tariff

# test_tariff = Tariffs('test_scheme',"data/retail_tariffs.csv","data/duos.csv","test", "data/ui_tariffs_eg.csv")
# test_tariff.get_total_central_battery_import_tariff('a')
# test_tariff.get_central_batt_buy_tariff('a')
# print(test_tariff.get_variable_retail_tariff(30,'Business TOU'))
