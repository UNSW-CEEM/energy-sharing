import os
import csv
import pandas as pd

SHARED_SOLAR_LOCATION = os.path.realpath(os.path.join(
    'application', 'modelling', 'data', 'shared', 'solar'))
SHARED_LOAD_LOCATION = os.path.realpath(os.path.join(
    'application', 'modelling', 'data', 'shared', 'load'))
SHARED_PARTICIPANTS_CONFIG_LOCATION = os.path.realpath(os.path.join(
    'application', 'modelling', 'data', 'shared', 'ui_participants'))
SHARED_TARIFFS_CONFIG_LOCATION = os.path.realpath(os.path.join(
    'application', 'modelling', 'data', 'shared', 'ui_tariffs'))
SHARED_FINANCING_CONFIG_LOCATION = os.path.realpath(os.path.join(
    'application', 'modelling', 'data', 'shared', 'ui_financing'))


class FileService:

    # Checks that a file is valid.
    def valid_file(self, filename):
        pass
    
    # Given a file, saves it (internally)
    def save(self, file):
        pass

    # Given a filename, retrieves a standard python file object.
    def get(self, filename):
        pass


class OSFileService(FileService):
    def __init__(self):

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

        self.solar_files = [f for f in os.listdir(self.solar_path) if os.path.isfile(os.path.join(self.solar_path, f))]
        self.load_files = [f for f in os.listdir(self.load_path) if os.path.isfile(os.path.join(self.load_path, f))]
        self.p_config_files = [f for f in os.listdir(self.p_config_path)
                               if os.path.isfile(os.path.join(self.p_config_path, f))]

    def valid_file(self, filename):
        return True

    def save(self, file):
        print("FILE_SERVICE: Saving", file)
        file.save(os.path.join('uploads', file.filename))
        print("Successfully saved")

    def list_solar_files(self):
        return self.solar_files

    def list_load_files(self):
        return self.load_files

    def list_solar_profiles(self, filename):

        solar_profiles = list(pd.read_csv(os.path.join(self.solar_path, filename)))
        if solar_profiles[0] == 'timestamp':
            solar_profiles.pop(0)

        return solar_profiles

    def list_load_profiles(self, filename):

        load_profiles = list(pd.read_csv(os.path.join(self.load_path, filename)))
        if load_profiles[0] == 'timestamp':
            load_profiles.pop(0)

        return load_profiles

    def save_config(self, page_name, file_name, data):
        table_data = data["data"]
        table_headers = []

        for each in table_data[0]["row_inputs"]:
            table_headers.append(each)

        file_path = os.path.join(self.config_paths[page_name], file_name)
        self.clear_csv(file_path)

        with open(file_path, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=table_headers)
            writer.writeheader()

            for each in table_data:
                row = each["row_inputs"]
                writer.writerow(row)

            return True

    def load_config(self, page_name, filename):
        file_path = os.path.join(self.config_paths[page_name], filename)

        results = []

        if os.path.isfile(file_path):
            with open(file_path) as file:
                reader = csv.DictReader(file)
                counter = 0
                for row in reader:
                    results.append({'row_id': counter, 'row_inputs': row})

        return self.result_channels[page_name], results

    @staticmethod
    def clear_csv(path):
        f = open(path, "w+")
        f.close()
