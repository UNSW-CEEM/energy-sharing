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


def create_study_csv():
    pass


# This is a copied "study" csv
'''       n   nn n
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