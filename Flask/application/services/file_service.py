import os
import csv
import pandas as pd

SHARED_SOLAR_LOCATION = os.path.realpath(os.path.join(
    'application', 'modelling', 'data', 'shared', 'solar'))
SHARED_LOAD_LOCATION = os.path.realpath(os.path.join(
    'application', 'modelling', 'data', 'shared', 'load'))


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
        self.sp = SHARED_SOLAR_LOCATION
        self.lp = SHARED_LOAD_LOCATION

        self.solar_files = [f for f in os.listdir(self.sp) if os.path.isfile(os.path.join(self.sp, f))]
        self.load_files = [f for f in os.listdir(self.lp) if os.path.isfile(os.path.join(self.lp, f))]

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

        solar_profiles = list(pd.read_csv(os.path.join(self.sp, filename)))
        if solar_profiles[0] == 'timestamp':
            solar_profiles.pop(0)

        return solar_profiles

    def list_load_profiles(self, filename):

        load_profiles = list(pd.read_csv(os.path.join(self.lp, filename)))
        if load_profiles[0] == 'timestamp':
            load_profiles.pop(0)

        return load_profiles
