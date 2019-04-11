class CentralSolar:
    def __init__(self, folder_routes):
        self.luomi_dir = folder_routes.get_route("luomi_dir")

        self.data_source = None
        self.scaling_factor = None
        self.sharing_algorithm = None
