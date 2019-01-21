import os

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
        sp = SHARED_SOLAR_LOCATION
        lp = SHARED_LOAD_LOCATION

        self.solar_files = [f for f in os.listdir(sp) if os.path.isfile(os.path.join(sp, f))]
        self.load_files = [f for f in os.listdir(lp) if os.path.isfile(os.path.join(lp, f))]


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
