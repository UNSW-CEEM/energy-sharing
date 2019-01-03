import os

BASE_DIR_NAME = os.path.join("application", "modelling", "data")
DATA_DIR = os.path.realpath(BASE_DIR_NAME)

LUOMI_DIR_NAME = "luomi"
LUOMI_DEFAULTS_DIR_NAME = "defaults"
LUOMI_INPUT_DIR_NAME = "input"
LUOMI_OUTPUT_DIR_NAME = "output"

MIKE_DIR_NAME = "mike"


class FolderRoutes:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.luomi_dir = os.path.join(self.data_dir, LUOMI_DIR_NAME)
        self.luomi_defaults_dir = os.path.join(self.luomi_dir, LUOMI_DEFAULTS_DIR_NAME)
        self.luomi_input_dir = os.path.join(self.luomi_dir, LUOMI_INPUT_DIR_NAME)
        self.luomi_output_dir = os.path.join(self.luomi_dir, LUOMI_OUTPUT_DIR_NAME)

        self.mike_base_dir = os.path.join(self.data_dir, MIKE_DIR_NAME)

    def get_route(self, route):
        response = False

        for n, r in self.__dict__.items():
            if route is n:
                response = r

        return response
