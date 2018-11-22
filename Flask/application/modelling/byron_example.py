# =====================================================
# Imports - these are external bits of code that we use to make the model run properly.
# =====================================================

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

#  ==================
# PROGRAM STARTS HERE
#  ==================

# Directories where input and output data lives.
output_dir = 'byron_output'
data_dir = 'data'

# Create a network - this stores information on the electricity network we want to model.
my_network = Network('Byron')

# Load the participants from a csv
my_network.add_participants_from_csv(data_dir, "participant_meta_data.csv")

# Create a central battery.
battery_capacity = 0.001
central_battery = Central_Battery(
    cap_kWh=battery_capacity, cap_kW=battery_capacity, cycle_eff=0.99,
    ui_battery_discharge_windows_path=os.path.join(data_dir,"ui_battery_discharge_window_eg.csv"))
# Add the battery to the network.
my_network.add_central_battery(central_battery)

# Create a 'tariffs' object that stores information and logic about different tariffs.
my_tariffs = Tariffs('Test',os.path.join(data_dir,"retail_tariffs.csv"),os.path.join(data_dir,"duos.csv"),os.path.join(data_dir,"tuos.csv"), os.path.join(data_dir,"nuos.csv"), os.path.join(data_dir,"ui_tariffs_eg.csv"))

# Define the start and end times of the simulation.
start = datetime.datetime(year=2017,month=2,day=26,hour=4)
end =  datetime.datetime(year=2017,month=2,day=26,hour=23)
# this is an end time very near the start, good for testing code because we don't do many calculations.
# end =  datetime.datetime(year=2017,month=4,day=30,hour=23)
# #this is the total end time for all the data in the byron model

# Generate a list of time periods in half hour increments, on which to run the simulation.
# These must be included in the input time series.
time_periods = util.generate_dates_in_range(start, end, 30)
# Create a results object to store the results of the simulations
results = Results(time_periods, [p.get_id() for p in my_network.get_participants()])
# Perform energy simulations and store the results in our results object.
energy_sim.simulate(time_periods, my_network, my_tariffs, results)
# Perform financial calculations based on the energy sim and store the results in our results object.
financial_sim.simulate(time_periods, my_network, my_tariffs, results)
# Print to CSV files
results.to_csv(output_dir, info_tag=battery_capacity)



