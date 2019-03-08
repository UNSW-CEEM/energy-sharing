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
    
    def get_num_systems(self):
        return len(self.data.columns)
    
    def get_system_names(self):
        return self.data.columns

    def rename_system(self, old_name, new_name):
        """Changes the name of a system in the PV collection. """
        columns = [x for x in self.data.columns]
        for i in range(len(columns)):
            if columns[i] == old_name:
                columns[i] = new_name
        self.data.columns = pd.Index(data=columns)
    
    def copy_system(self, existing_system_name, new_system_name):
        self.data[new_system_name] = self.data[existing_system_name]
    
    def scale_system(self,system_name, scaling_factor):
        self.data[system_name] = self.data[system_name] * scaling_factor
    
    def delete_system(self,system_name):
        self.data = self.data.drop(system_name, axis=1)
    
    def subtract_system(self,system_name, system_name_to_subtract):
        """Subtracts one system's data from another"""
        # Subtracts one system data from another, in-place. Don't love it. Abstraction-brakey.
        self.data[system_name] = self.data[system_name] - self.data[system_name_to_subtract]
    
    def aggregate_systems(self,new_system_name):
        """Adds all data up, puts into one system called 'total', deletes all others."""
        self.data[new_system_name] = self.data.sum(axis=1)
        self.data = self.data.loc[:, [new_system_name]]
    
    def multiply_by_timeseries(self, system_name, timeseries):
        print("Multiplying by timeseries and i want to convert away from pandas df")
        self.data =  network_load_fractions.multiply(self.data.loc[:, system_name], axis=0)
    
    def get_system_sum(self, system_name):
        return self.data[system_name].sum()
    
    def add_zero_system(self, system_name):
        """Adds a PV system with constant output of zero"""
        self.data = pd.concat([self.data, pd.DataFrame(columns=[system_name])], sort=False).fillna(0)
    
    def get_data(self, system_name):
        return [x for x in self.data[system_name]]
        