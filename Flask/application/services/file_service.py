import os
import csv
import pandas as pd
import pendulum

import application.folder_routes as folder_routes
from application.folder_routes import FolderRoutes

import io
import csv
import re

SHARED_SOLAR_LOCATION = os.path.realpath(os.path.join(
    folder_routes.BASE_DIR_NAME, 'shared', 'solar'))
SHARED_LOAD_LOCATION = os.path.realpath(os.path.join(
    folder_routes.BASE_DIR_NAME, 'shared', 'load'))
SHARED_PARTICIPANTS_CONFIG_LOCATION = os.path.realpath(os.path.join(
    folder_routes.BASE_DIR_NAME, 'shared', 'ui_participants'))
SHARED_TARIFFS_CONFIG_LOCATION = os.path.realpath(os.path.join(
    folder_routes.BASE_DIR_NAME, 'shared', 'ui_tariffs'))
SHARED_FINANCING_CONFIG_LOCATION = os.path.realpath(os.path.join(
    folder_routes.BASE_DIR_NAME, 'shared', 'ui_financing'))


class FileService:

    # Checks that a file is valid.
    def valid_file(self, new_file):
        pass
    
    # Given a file, saves it (internally)
    def save(self, file, save_type):
        pass

    # Given a filename, retrieves a standard python file object.
    def get(self, filename):
        pass


class OSFileService(FileService):
    def __init__(self):
        self.fr = FolderRoutes()
        # Experimental Code
        self.solar_data_save_path = self.fr.get_route("solar_profiles_dir")
        self.load_data_save_path = self.fr.get_route("load_profiles_dir")

        # Solar Path/Load Path
        self.solar_path = SHARED_SOLAR_LOCATION
        self.load_path = SHARED_LOAD_LOCATION
        self.p_config_path = SHARED_PARTICIPANTS_CONFIG_LOCATION
        self.t_config_path = SHARED_TARIFFS_CONFIG_LOCATION
        self.f_config_path = SHARED_FINANCING_CONFIG_LOCATION

        self.config_paths ={
            "model_participants": self.p_config_path,
            "model_tariffs": self.t_config_path,
            "model_financing": self.f_config_path
         }

        self.result_channels = {
            "model_participants": "participants_file_channel",
            "model_tariffs": "tariffs_file_channel",
            "model_financing": "financing_file_channel",
        }

        self.solar_files = []
        self.load_files = []
        self.p_config_files = []
        self.update_files_lists()

    def update_files_lists(self):
        self.solar_files = [f for f in os.listdir(self.solar_data_save_path) if
                            os.path.isfile(os.path.join(self.solar_path, f)) and 'csv' in f]
        self.load_files = [f for f in os.listdir(self.load_data_save_path) if
                           os.path.isfile(os.path.join(self.load_path, f)) and 'csv' in f]
        self.p_config_files = [f for f in os.listdir(self.p_config_path)
                               if os.path.isfile(os.path.join(self.p_config_path, f))]

    def valid_file(self, new_file):
        print("file_service.py/valid_file", new_file)
        print("file_service.py/valid_file", new_file.filename)
        # print("file_service.py/valid_file", new_file.read())
        # Ensure the file ends in a csv.
        if not new_file.filename.lower().endswith('csv'):
            return False, "Error: Expected CSV File"
        
        # try:
        contents_str = new_file.read().decode("utf-8") 
        reader = csv.DictReader(io.StringIO(contents_str))
        for line in reader:
            if 'timestamp' not in line:
                return False, "timestamp column not found"
            if line['timestamp'].isspace() or line['timestamp'] == '':
                return False, "Blank timestamp found - check end of file perhaps?"
            if not re.compile("^[0-9]+/[0-9]+/[0-9]+ [0-9]+:[0-9][0-9]$").match(line['timestamp']):
                return False, " Incorrectly formatted timestamp found: "+str(line['timestamp'])+"-  Must follow DD/MM/YYYY HH:mm: "
        # except:
        #     return False, "Could not parse CSV file - check formatting."
        
        return True, "Success"

    def save(self, file, save_type):
        if save_type == "solar_data":
            file.save(os.path.join(self.solar_data_save_path, file.filename))

        if save_type == "load_data":
            file.save(os.path.join(self.load_data_save_path, file.filename))

        self.update_files_lists()
        # print("FILE_SERVICE: Saving", file)
        # file.save(os.path.join('uploads', file.filename))
        # print("Successfully saved")

    def list_solar_files(self):
        self.update_files_lists()
        return self.solar_files

    def list_load_files(self):
        self.update_files_lists()
        return self.load_files

    def list_solar_start_end(self):
        self.update_files_lists()
        output = {}
        for solar_filename in self.solar_files:
            path = os.path.join(self.solar_path, solar_filename)
            with open(path) as f:
                reader = csv.DictReader(f)
                for idx, line in enumerate(reader):
                    if idx == 0:
                        
                        start_date = pd.datetime.strptime(line['timestamp'], '%d/%m/%Y %H:%M').isoformat()
                        # start_date = pendulum.from_format(line['timestamp'], ('DD/MM/YYYY HH:mm'), tz='UTC').isoformat()
                end_date = pd.datetime.strptime(line['timestamp'], '%d/%m/%Y %H:%M').isoformat()
                # end_date = pendulum.from_format(line['timestamp'], ('DD/MM/YYYY HH:mm'), tz='UTC').isoformat()
            output[solar_filename] = {
                'start_date': start_date,
                'end_date':end_date
            }
        return output
    
    def list_load_start_end(self):
        self.update_files_lists()
        output = {}
        for load_filename in self.load_files:
            path = os.path.join(self.load_path, load_filename)
            with open(path) as f:
                reader = csv.DictReader(f)
                for idx, line in enumerate(reader):
                    if idx == 0:
                        start_date = pd.datetime.strptime(line['timestamp'], '%d/%m/%Y %H:%M').isoformat()
                        # start_date = pendulum.from_format(line['timestamp'], ('DD/MM/YYYY HH:mm'), tz='UTC').isoformat()
                end_date = pd.datetime.strptime(line['timestamp'], '%d/%m/%Y %H:%M').isoformat()
                # end_date = pendulum.from_format(line['timestamp'], ('DD/MM/YYYY HH:mm'), tz='UTC').isoformat()
            output[load_filename] = {
                'start_date': start_date,
                'end_date':end_date
            }
        return output
                    
                    


    def list_solar_profiles(self, solar_filename):
        solar_profiles = ""
        if solar_filename is not "":
            solar_profiles = list(pd.read_csv(os.path.join(self.solar_path, solar_filename)))
            if solar_profiles[0] == 'timestamp':
                solar_profiles.pop(0)

        return solar_profiles

    def list_load_profiles(self, load_filename):
        load_profiles = ""
        if load_filename is not "":
            load_profiles = list(pd.read_csv(os.path.join(self.load_path, load_filename)))
            if load_profiles[0] == 'timestamp':
                load_profiles.pop(0)

        return load_profiles
    
    def get_solar_timeseries(self, solar_filename):
        self.update_files_lists()
        output = {}
        path = os.path.join(self.solar_path, solar_filename)
        with open(path) as f:
            reader = csv.DictReader(f)
            for line in reader:
                # There is a small (I think timezone) difference in these two. But pendulum is wack in compiled versions.
                time = pd.datetime.strptime(line['timestamp'], '%d/%m/%Y %H:%M').timestamp() * 1000.0
                # time = pendulum.from_format(line['timestamp'], ('DD/MM/YYYY HH:mm'), tz='UTC').timestamp() * 1000.0
                for label in line:
                    if not label =='timestamp':
                        output[label] = [] if not label in output else output[label]
                        dp = float(line[label])
                        output[label].append([time, dp])
        return output
    
    def get_load_timeseries(self, load_filename):
        self.update_files_lists()
        output = {}
        path = os.path.join(self.load_path, load_filename)
        with open(path) as f:
            reader = csv.DictReader(f)
            for line in reader:
                time = pd.datetime.strptime(line['timestamp'], '%d/%m/%Y %H:%M').timestamp() * 1000.0
                # time = pendulum.from_format(line['timestamp'], ('DD/MM/YYYY HH:mm')).timestamp() * 1000.0
                for label in line:
                    if not label =='timestamp':
                        output[label] = [] if not label in output else output[label]
                        dp = float(line[label])
                        output[label].append([time, dp])
        return output

    def save_config(self, page_name, config_filename, data, additional_headers):
        # print("Page Name: ", page_name,
        #       "\nConfig Filename: ", config_filename,
        #       "\nData: ", data,
        #       "\nAdditional Headers: ", additional_headers)

        table_data = data["data"]
        table_headers = []

        for each in table_data[0]["row_inputs"]:
            table_headers.append(each)

        if additional_headers:
            for each in additional_headers:
                table_headers.append(each)

        file_path = os.path.join(self.config_paths[page_name], config_filename)
        self.clear_csv(file_path)

        with open(file_path, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=table_headers)
            writer.writeheader()

            for each in table_data:
                row = each["row_inputs"]

                if additional_headers:
                    for key in additional_headers:
                        row[key] = additional_headers[key]
                writer.writerow(row)

            return True

    def load_config(self, page_name, config_filename):
        file_path = os.path.join(self.config_paths[page_name], config_filename)

        results = []

        if os.path.isfile(file_path):
            with open(file_path) as file:
                reader = csv.DictReader(file)
                counter = 0
                for row in reader:
                    results.append({'row_id': counter, 'row_inputs': row})

        return self.result_channels[page_name], results

    def load_participants_config(self, page_name, config_filename):
        channel, data = self.load_config(page_name, config_filename)

        solar_filename = data[0]["row_inputs"]["selected_solar_file"]
        load_filename = data[0]["row_inputs"]["selected_load_file"]

        solar_profiles_options = self.list_solar_profiles(solar_filename)
        load_profiles_options = self.list_load_profiles(load_filename)

        packaged_data = {
            "data": data,
            "solar_profiles_options": solar_profiles_options,
            "load_profiles_options": load_profiles_options
        }

        return channel, packaged_data

    @staticmethod
    def clear_csv(path):
        f = open(path, "w+")
        f.close()
