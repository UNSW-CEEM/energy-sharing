
# Custom modules
from .network import Network
from .participant import Participant, CSV_Participant
from .battery import Battery, Central_Battery
from .tariffs import Tariffs
from . import util
from .results import Results


# Required 3rd party libraries
import datetime
import pandas as pd
import numpy as np
import pprint
import csv
import os


def simulate(time_periods, mynetwork, my_tariffs, results, status_callback=None):

    if status_callback:
        status_callback('Performing Energy Calculations: 0%')
        percent_finished = 0
        single_step_percent = 100.0 / float(len(time_periods))
        
    for time in time_periods:
        if status_callback:
            percent_finished += single_step_percent
            status_callback('Performing Energy Calculations: '+str(round(percent_finished))+"%")
        # print "Energy",time
        # Calc each participant in/out kWh
        for p in mynetwork.get_participants():
            results.set_net_export(time, p.get_id(), p.calc_net_export(time, 30))

        
        # Calc exces solar sharing / sales
        net_participant_export =  mynetwork.calc_total_participant_export(time, 30)
        results.set_net_participant_export(time, net_participant_export)
        
        # Calc central battery in/out kWh
        central_battery_export = sum(b.make_export_decision(net_participant_export, time) for b in mynetwork.get_batteries())
        # central_battery_export = sum(b.make_export_decision(net_participant_export) for b in mynetwork.get_batteries())

        results.set_central_battery_export(time, central_battery_export)

        # Calc network in/out kWh
        results.set_net_network_export(time, net_participant_export + central_battery_export)

        # Run local solar allocation algorithm
        # Initialise an empty df with column name net_export
        participants_list_sorted = pd.DataFrame(columns=['net_export'])
        # Add net export data for participants with load
        for p in mynetwork.get_participants():
            # Get data point from df_net_export df
            net_export = results.get_net_export(time, p.get_id())
            # If there is load (i.e. export < 0 ) add to list
            if net_export < 0 :
                participants_list_sorted.loc[p.get_id(), 'net_export'] = net_export
        # Sort list of participants with load
        participants_list_sorted = participants_list_sorted.sort_values('net_export')

        # Calculate total solar available in this time period
        available_batt = max(central_battery_export,0)
        available_solar = 0
        for participant in mynetwork.get_participants():
            net_export = results.get_net_export(time, participant.get_id())
            if net_export > 0 :
                available_solar += net_export
        
        
        # If there exist participants with load then allocate solar
        if len(participants_list_sorted) != 0 :
            # Calculate solar allocation - assume even split between participants with load
            num_remaining_participants = len(participants_list_sorted)
            solar_allocation = float(available_solar) / float(num_remaining_participants)
            battery_allocation = float(available_batt) / float(num_remaining_participants)

            # Initialise for use in second if statement
            reject_solar = 0

            # For each participant with load, find how much of their allocated solar is consumed and calculate the leftover ('reject solar')
            for p in participants_list_sorted.index.values :
                if solar_allocation > 0:
                    # Allocating solar 
                    local_solar_import = min(abs(solar_allocation), abs(participants_list_sorted.loc[p, 'net_export']))
                    results.set_local_solar_import(time, p, local_solar_import)
                    # Find reject solar
                    reject_solar = solar_allocation - local_solar_import
                    # Find new available solar (based on what was used)
                    available_solar -= local_solar_import
                    # Decrement the number of remaining participants
                    num_remaining_participants -= 1
                    # Calculate the new solar allocation
                    solar_allocation = float(available_solar) / float(num_remaining_participants) if num_remaining_participants > 0 else 0
                # If the sale doesn't happen, then these things should be zero
                else :
                    reject_solar = 0
                    local_solar_import = 0

                # Allocate battery export when there is battery export and all solar has been used by this participant
                if battery_allocation > 0 and reject_solar <= 0 :
                    participant_net_export = participants_list_sorted.loc[p,'net_export']
                    participant_central_batt_import = min(abs(battery_allocation), abs(participant_net_export) - abs(local_solar_import))
                    results.set_participant_central_batt_import(time, p, participant_central_batt_import)
                    available_batt -= participant_central_batt_import
                    battery_allocation = float(available_batt) / float(num_remaining_participants) if num_remaining_participants > 0 else 0

                    
        # Save any solar left over after the allocation process to df_network_energy_flows
        results.set_unallocated_local_solar(time, available_solar)

        # Run local load allocation algorithm (aka solar sales)
        # Initialise an empty df with column name net export
        solar_sales_participant_list = pd.DataFrame(columns = ['net_export'])
        # Add net export data for participants with generation
        for p in mynetwork.get_participants():
            # Get data point from df_net_export df
            net_export = results.get_net_export(time, p.get_id())
            # If there is generation (i.e. export > 0 ) add to list
            if net_export > 0 :
                solar_sales_participant_list.loc[p.get_id(), 'net_export'] = net_export
        # Sort list of participants with load
        solar_sales_participant_list = solar_sales_participant_list.sort_values('net_export')

        # Calculate total load available in this time period
        # TODO - central battery
        available_load = 0
        available_batt_charging_load = abs(min(central_battery_export,0))

        #     # NOTE available load is positive
        #     if net_export < 0 :
        #         available_load += abs(net_export)

        for participant in mynetwork.get_participants():
            net_export = results.get_net_export(time, participant.get_id())
            # NOTE available load is positive
            if net_export < 0 :
                available_load += abs(net_export)

        # If there exists participant with solar, allocate load
        if len(solar_sales_participant_list) != 0 :
            num_remaining_participants = len(solar_sales_participant_list)
            load_allocation = float(available_load) / float(num_remaining_participants)
            batt_charging_allocation = float(available_batt_charging_load) / float(num_remaining_participants)

            for p in solar_sales_participant_list.index.values :
                if load_allocation > 0:
                    participant_solar_sale = min(abs(load_allocation), abs(solar_sales_participant_list.loc[p,'net_export']))
                    results.set_local_solar_sales(time, p, participant_solar_sale)
                    reject_load = load_allocation - participant_solar_sale
                    available_load -= participant_solar_sale
                    num_remaining_participants -= 1
                    load_allocation = float(available_load) / float(num_remaining_participants) if num_remaining_participants > 0 else 0
                # If the sale doesn't happen, then these things should be zero
                else :
                    reject_load = 0
                    participant_solar_sale = 0

                if available_batt_charging_load > 0 and reject_load <= 0 :
                    participant_solar_sale = min(abs(batt_charging_allocation), abs(solar_sales_participant_list.loc[p,'net_export']) - abs(participant_solar_sale))
                    results.set_central_batt_solar_sales(time, p, participant_solar_sale)
                    available_batt_charging_load -= participant_solar_sale
                    batt_charging_allocation = float(available_batt_charging_load) / float(num_remaining_participants) if num_remaining_participants > 0 else 0



        # Grid impacts for each customer. Import from grid and solar export to grid.
        for p in mynetwork.get_participants():
            # First, solar export to grid
            net_export = results.get_net_export(time, p.get_id())
            local_solar_sales = results.get_local_solar_sales(time, p.get_id())
            central_battery_solar_sales = results.get_central_batt_solar_sales(time, p.get_id())
            # Calc and save to df
            export_to_grid_solar_sales = max(0,net_export) - max(0,local_solar_sales) - max(0,central_battery_solar_sales)
            results.set_export_to_grid_solar_sales(time, p.get_id(), export_to_grid_solar_sales)
            # Then, electricity import from grid
            local_solar_import = results.get_local_solar_import(time, p.get_id())
            participant_central_batt_import = results.get_participant_central_batt_import(time, p.get_id())
            # Left over load which requires grid import. Calc and save to df.
            external_grid_import = abs(min(net_export,0)) - abs(max(0,local_solar_import)) - abs(max(0,participant_central_batt_import))
            results.set_external_grid_elec_import(time, p.get_id(), external_grid_import)

        # Save any battery load left over after the allocation process to df_network_energy_flows
        results.set_unallocated_central_battery_load(time, available_batt_charging_load)
        
        # For the financial calcs for retailer/NSPs, calculate the gross grid import - i.e. how much did all the participants import during this time interval (only considers import - discards export). Also local solar and central battery import.
        results.set_gross_participant_grid_import(time, abs(min(results.get_net_participant_export(time),0)))
        results.set_gross_participant_local_solar_import(time, max( sum([results.get_local_solar_import(time, participant.get_id()) for participant in mynetwork.get_participants() ]) ,0))
        results.set_gross_participant_central_battery_import(time, max( sum( [results.get_participant_central_batt_import(time, participant.get_id()) for participant in mynetwork.get_participants()] ),0))


