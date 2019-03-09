

class LoadProfile():
    """A load profile contains loads """
    def __init__(self, name):
        self.name = name
        self._data = None
    
    def from_df(self,load_df):
        self._data = load_df.copy()
        return self
    
    def to_df(self):
        """Returns a dataframe indexed on timestamps, with participant names as column headers."""
        return self._data
    
    def get_participant_names(self):
        return [name for name in self._data.columns.values]

class LoadCollection():
    def __init__(self):
        self.profiles = {}
    
    def add_profile_from_df(self, profile_df, profile_name):
        """Add a load to the load collection"""
        print("Adding load profile from dataframe. Load name: ", profile_name)
        # print(profile_df)
        self.profiles[profile_name] = LoadProfile(profile_name).from_df(profile_df)
    
    def get_profile(self, profile_name):
        """Returns a LoadProfile object with the corresponding name"""
        print("Getting", profile_name)
        print([key for key in self.profiles])
        print(self.profiles[profile_name])
        return self.profiles[profile_name]
