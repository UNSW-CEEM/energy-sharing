

class LoadCollection():
    def __init__(self):
        self.loads = {}
    
    def add_load_from_df(self, load_obj):
        """Add a load to the load collection"""
