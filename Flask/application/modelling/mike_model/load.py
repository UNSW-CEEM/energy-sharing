

class LoadCollection():
    def __init__(self):
        self.profiles = {}
    
    
    
    def add_profile_from_df(self, load_df, profile_name):
        """Add a load to the load collection"""
        print("Adding load profile from dataframe. Load name: ", profile_name)
        # print(load_df)
        self.profiles[profile_name] = load_df.copy()
        
