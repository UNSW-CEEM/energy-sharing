import pandas as pd

class PVCollectionFactory():
    def empty_collection(self, date_times, labels):
        data = pd.DataFrame(index=pd.DatetimeIndex(data=date_times), columns=labels).fillna(0)
        data.set_index('timestamp', inplace=True)
        return PVCollection(data)
    
    def from_file(self, file_path):
        data = pd.read_csv(file_path, parse_dates=['timestamp'], dayfirst=True)
        data.set_index('timestamp', inplace=True)
        return PVCollection(data)

class PVCollection():
    def __init__(self, pv_df):
        self._data = pv_df

    def get_date_times(self):
        return [x for x in self._data.index]
    
    def scale(self, scaling_factor):
        """Allows scaling of PV data by a given factor. """
        self._data = self._data * scaling_factor
    
    def copy(self):
        return PVCollection(self._data)
    
    def get_num_systems(self):
        return len(self._data.columns)
    
    def get_system_names(self):
        return self._data.columns

    def rename_system(self, old_name, new_name):
        """Changes the name of a system in the PV collection. """
        columns = [x for x in self._data.columns]
        for i in range(len(columns)):
            if columns[i] == old_name:
                columns[i] = new_name
        self._data.columns = pd.Index(data=columns)
    
    def copy_system(self, existing_system_name, new_system_name):
        """Create a new system with the same output as an existing system"""
        self._data[new_system_name] = self._data[existing_system_name]
    
    def scale_system(self,system_name, scaling_factor):
        """Scale the output of a PV system by a scaling factor"""
        self._data[system_name] = self._data[system_name] * scaling_factor
    
    def delete_system(self,system_name):
        """Delete a system from the PV collection"""
        self._data = self._data.drop(system_name, axis=1)
    
    def subtract_system(self,system_name, system_name_to_subtract):
        """Subtracts one system's data from another"""
        # Subtracts one system data from another, in-place. Don't love it. Abstraction-brakey.
        self._data[system_name] = self._data[system_name] - self._data[system_name_to_subtract]
    
    def aggregate_systems(self,new_system_name):
        """Adds all data up, puts into one system called 'total', deletes all others."""
        self._data[new_system_name] = self._data.sum(axis=1)
        self._data = self._data.loc[:, [new_system_name]]
    
    def multiply_by_timeseries(self, system_name, timeseries):
        print("input timeseries is a pandas df here -  and i want to convert away from pandas df - but couldnt call this code before. Refactor now!")
        self._data =  network_load_fractions.multiply(self._data.loc[:, system_name], axis=0)
    
    def get_system_sum(self, system_name):     
        """Return the sum of all the energy produced by one pv system"""   
        return self._data[system_name].sum()
    
    def get_aggregate_sum(self):
        """Return the total of all the energy from all systems, added up."""
        # Yes, sum does need to be called twice - otherwise can get summed across rows first if 1d array only.
        return self._data.sum().sum()
    
    def add_zero_system(self, system_name):
        """Adds a PV system with constant output of zero"""
        self._data = pd.concat([self._data, pd.DataFrame(columns=[system_name])], sort=False).fillna(0)
    
    def get_data(self, system_name):
        """Return a timeseries array of all datapoints of energy produced by the system."""
        return [x for x in self._data[system_name]]
    
    def get_aggregate_data(self):
        """Returns a timeseries array of total aggregate pv output, summed across all systems."""
        return self._data.sum(axis=1)
        