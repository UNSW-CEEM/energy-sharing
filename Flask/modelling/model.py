
# Custom modules
from network import Network
from participant import Participant, CSV_Participant
from battery import Battery, Central_Battery
from tariffs import Tariffs
import util
from results import Results
import energy_sim
import financial_sim

# Required 3rd party libraries
import datetime
import pandas as pd
import numpy as np
import pprint
import csv
import os




def run_en(scenario= None, status_callback=None, data_dir='data'):

    # Create a network
    mynetwork = Network('Byron')

    # Create participants

    participant_1 = CSV_Participant('participant_1','solar', 'Business TOU', 'LV TOU <100MWh','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),0)
    participant_2 = CSV_Participant('participant_2','solar', 'Business TOU', 'LV TOU <100MWh','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),0)
    participant_3 = CSV_Participant('participant_3','solar', 'Business TOU', 'LV TOU <100MWh','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),0)
    participant_4 = CSV_Participant('participant_4','solar', 'Business TOU', 'LV TOU <100MWh','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),26)
    participant_5 = CSV_Participant('participant_5','solar', 'Business TOU', 'LV TOU <100MWh','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),0)
    participant_6 = CSV_Participant('participant_6','solar', 'Business TOU', 'LV TOU <100MWh','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),14.8)
    participant_7 = CSV_Participant('participant_7','solar', 'Business TOU', 'LV TOU <100MWh','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),0)
    participant_8 = CSV_Participant('participant_8','solar', 'Business TOU', 'LV TOU <100MWh','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),27.5)
    participant_9 = CSV_Participant('participant_9','solar', 'Business Anytime', 'LV Small Business Anytime','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),3)
    participant_10 = CSV_Participant('participant_10','solar', 'Business Anytime', 'LV Small Business Anytime','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),0)
    participant_11 = CSV_Participant('participant_11','solar', 'Business Anytime', 'LV Small Business Anytime','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),0)

    # participant_1 = Participant('building_1','solar','Business TOU','LV TOU <100MWh', 'ENOVA')
    # participant_2 = Participant('building_2','load','Business TOU','Small Business - Opt in Demand', 'ENOVA')
    # participant_3 = Participant('building_3','load','Business TOU','Small Business - Opt in Demand', 'ENOVA')


    # Add participants to network
    mynetwork.add_participant(participant_1)
    mynetwork.add_participant(participant_2)
    mynetwork.add_participant(participant_3)
    mynetwork.add_participant(participant_4)
    mynetwork.add_participant(participant_5)
    mynetwork.add_participant(participant_6)
    mynetwork.add_participant(participant_7)
    mynetwork.add_participant(participant_8)
    mynetwork.add_participant(participant_9)
    mynetwork.add_participant(participant_10)
    mynetwork.add_participant(participant_11)
   

    # Add a central battery
    # See if the user has configured a battery capacity - if not, just use 1 MWh
    capacity = scenario['battery_capacity'] if 'battery_capacity' in scenario else 1
    # Create the battery object.
    battery_1 = Central_Battery(capacity, capacity, 0.99, os.path.join(data_dir,"ui_battery_discharge_window_eg.csv"))
    # Add the battery to the network.
    mynetwork.add_central_battery(battery_1)

    # Add tariffs
    # my_tariffs = Tariffs('Test',os.path.join(data_dir,"retail_tariffs.csv"),os.path.join(data_dir,"duos.csv",)"test")
    my_tariffs = Tariffs('Test',os.path.join(data_dir,"retail_tariffs.csv"),os.path.join(data_dir,"duos.csv"),os.path.join(data_dir,"tuos.csv"), os.path.join(data_dir,"nuos.csv"), os.path.join(data_dir,"ui_tariffs_eg.csv"))
    # Generate a list of time periods in half hour increments
    start = datetime.datetime(year=2017,month=2,day=26,hour=4)
    end =  datetime.datetime(year=2017,month=2,day=26,hour=23)
    # end =  datetime.datetime(year=2017,month=4,day=30,hour=23)
    time_periods = util.generate_dates_in_range(start, end, 30)

    # Create a results object to store the results of the simulations
    results = Results(time_periods, [p.get_id() for p in mynetwork.get_participants()])
    # Perform energy simulations and store the results in our results object.
    energy_sim.simulate(time_periods, mynetwork, my_tariffs, results, status_callback)
    # Perform financial calculations based on the energy sim and store the results in our results object.
    financial_sim.simulate(time_periods, mynetwork, my_tariffs, results, status_callback)

    return results


def run_en_csv(output_dir, data_dir, scenario=None, status_callback=None):
    if status_callback:
        status_callback('Running EN CSV')

    result = run_en(scenario, status_callback=status_callback, data_dir=data_dir)
    print "Writing to CSV"
    if status_callback:
        status_callback('Writing Output to CSV Files')
    battery_capacity = str(scenario['battery_capacity']) if 'battery_capacity' in scenario else ""
    result.to_csv(output_dir, info_tag=battery_capacity)
   
    if status_callback:
        status_callback('Finished')



# Start here! :)

if __name__ == "__main__":
    print "Running Simulation: ",0.001, "kWh"
    run_en_csv('output', 'data', {'battery_capacity':0.001})
    # for battery_capacity in range(5,35,5):
    #     print "Running Simulation: ",battery_capacity, "kWh"
    #     run_en_csv('output', 'data', {'battery_capacity':battery_capacity})
