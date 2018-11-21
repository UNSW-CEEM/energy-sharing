import os
import glob
import pandas as pd
from os import listdir
from os.path import isfile, join
import csv
from collections import OrderedDict

def concatenate(input_directory="/mnt/c/Users/Emily/Documents/Test",outfile="concatenated.csv"):
    # os.chdir(input_directory)
    # fileList=glob.glob("*.csv")
    dfList=[]
    # for filename in fileList:
    #     print(filename)
    #     df=pandas.read_csv(filename,header=True)
    #     dfList.append(df)
    files = [f for f in listdir(input_directory) if isfile(join(input_directory, f))]
    print(files)
    output = OrderedDict()
    participant_names = []

    for file in files:
        file_path = input_directory+"/"+file
        # Open the file
        with open(file_path) as f:
            # Create a csv reader object
            reader = csv.DictReader(f)
            # Python dict to store our output
            
            # Loop through every line of the csv file
            for line in reader:
                # Get the date as a string
                date = line['date_time']
                # If the date is not in our output object, add it and add the relevant data.
                output[date] = {} if not date in output else output[date]
                # Update the line in our output object with the SGSC data
                output[date].update(line)
                
                # Building a list of participant names
                del line['date_time']
                for key in line:
                    if key not in participant_names:
                        participant_names.append(key)
    print(participant_names)
    participant_names.insert(0, 'date_time')
    with open(outfile, "w") as f:
        writer = csv.DictWriter(f, participant_names)

        writer.writeheader()
        for date in output:
            writer.writerow(output[date])
        




concatenate()
