import os
class FileService():

    def valid_file(self, filename):
        pass
    
    def save(self, file):
        pass
    
    def get(self, filename):
        pass


class OSFileService(FileService):

    def valid_file(self, filename):
        return True

    def save(self, file):
        print("FILE_SERVICE: Saving", file)
        file.save(os.path.join('uploads', file.filename))
        print("Successfully saved")