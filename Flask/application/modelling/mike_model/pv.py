import pandas as pd

class PVCollectionFactory():
    def empty_collection(self, date_times, labels):
        data = pd.DataFrame(index=pd.DatetimeIndex(data=date_times), columns=labels).fillna(0)
        return PVCollection(data)
    
    def from_file(self, file_path):
        data = pd.read_csv(file_path, parse_dates=['timestamp'], dayfirst=True)
        return PVCollection(data)

class PVCollection():
    def __init__(self, pv_df):
        self.data = pv_df
    
    def scale(self, scaling_factor):
        """Allows scaling of PV data by a given factor. """
        self.data = self.data * scaling_factor
    
    def copy(self):
        return PVCollection(self.data)
