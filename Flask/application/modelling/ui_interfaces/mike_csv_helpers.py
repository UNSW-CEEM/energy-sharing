import os
import io
import csv


# UI Input Parsing modules (I don't think these are needed...)
from .central_battery import CentralBattery as Ui_Central_Battery
from .central_solar import CentralSolar as Ui_Central_Solar
from .tariffs import Tariffs as Ui_Tariffs
from .participants import Participants as Ui_Participants
from .result_parsers import ResultParsers as Ui_Results_Parsers
from .folder_routes import FolderRoutes as FolderRoutes


def create_csvs(participants, tariffs, finances, central_battery, central_solar, folder_routes):
    scenario_name = "default"
    participant_string = participants.get_participants_as_string()
    create_load_profile_csv(participants)


def create_load_profile_csv(participants):
    # Get the participant_id:load_data_paths from the participant object
    load_data_paths = participants.get_name_load_dict()

    participant_list = create_participants_list(load_data_paths)

    # Create a header array
    csv_header = participant_list.copy()
    csv_header.insert(0, "timestamp")
    print("CSV HEADER: ", csv_header)
    print("DATA PATHS: ", load_data_paths)

    # Create data arrays
    data = []

    for each in participant_list:
        path = load_data_paths[each]

        this_data = []
        with open(path) as this_data_file:
            reader = csv.DictReader(this_data_file)
            for row in reader:
                this_data.append(row)

        # print(this_data)

    final = []


def create_participants_list(load_data_paths):
    # Create a list of all the participant_ids
    participant_ids = []

    for key in load_data_paths:
        participant_ids.append(key)

    return participant_ids


def create_study_csv():
    pass


# This is a copied "study" csv
'''
scenario,
pv_filename,
load_folder,
arrangement,
pv_cap_id,
pv_capex_scaleable,
cp,
all_residents,
parent,
network_tariff,
en_capex_id,
a_term,
a_rate,
pv_scaleable,
pv_kW_peak,notes
'''


# This is a copied "load_profile" csv
'''
timestamp,
W01,W02,W03,W04,W05,W06,W07,W08,W09,W10,
W11,W12,W13,W14,W15,W16,W17,W18,W19,W20,
W21,W22,W23,W24,W25,W27,W28,W29,cp,W26_A,
W30_A,W31_A,W32_A,W33_A,W34_A,W35_A,W36_A,
W37_A,W38_A,W39_A,W40_A,W41_A,W42_A,W43_A,
W44_A,W45_A,W46_A,W47_A,W48_A,W49_A,W50_A,
W51_A,W52_A,W53_A,W54_A,W55_A,W56_A,W57_A,
W58_A,W59_A,W60_A,W61_A,W62_A,W63_A,W64_A,
W65_A,W66_A,W67_A,W68_A,W69_A,W70_A,W71_A,W72_A
'''