import os
class FileService():

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

    def valid_file(self, filename):
        return True

    def save(self, file):
        print("FILE_SERVICE: Saving", file)
        file.save(os.path.join('uploads', file.filename))
        print("Successfully saved")