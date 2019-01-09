import os

# Not necessarily happy with these names/system. But can easily be changed later
BASE_DIR_NAME = os.path.join("application", "modelling", "data")
DATA_DIR = os.path.realpath(BASE_DIR_NAME)

LUOMI_DIR_NAME = "luomi"
LUOMI_DEFAULTS_DIR_NAME = "defaults"
LUOMI_INPUT_DIR_NAME = "input"
LUOMI_OUTPUT_DIR_NAME = "output"

MIKE_DIR_NAME = "mike"
MIKE_STUDIES_DIR_NAME = "studies"
MIKE_PROJECT_NAME = "ceem_ui"
MIKE_STUDY_NAME = "ceem_ui_default"
MIKE_MODEL_INPUTS = "inputs"
MIKE_MODEL_OUTPUTS = "outputs"

PROFILES_DIR_NAME = "shared"
LOAD_PROFILES_DIR_NAME = "load"
LOAD_PROFILES_FILE_NAME = "load_profiles.csv"
SOLAR_PROFILES_DIR_NAME = "solar"
SOLAR_PROFILES_FILE_NAME = "solar_profiles.csv"


class FolderRoutes:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.luomi_dir = os.path.join(self.data_dir, LUOMI_DIR_NAME)
        self.luomi_defaults_dir = os.path.join(self.luomi_dir, LUOMI_DEFAULTS_DIR_NAME)
        self.luomi_input_dir = os.path.join(self.luomi_dir, LUOMI_INPUT_DIR_NAME)
        self.luomi_output_dir = os.path.join(self.luomi_dir, LUOMI_OUTPUT_DIR_NAME)

        self.mike_base_dir = os.path.join(self.data_dir, MIKE_DIR_NAME)
        self.mike_studies_dir = os.path.join(
            self.mike_base_dir, MIKE_STUDIES_DIR_NAME)
        self.mike_input_dir = os.path.join(self.mike_studies_dir, MIKE_STUDY_NAME, MIKE_MODEL_INPUTS)
        self.mike_output_dir = os.path.join(self.mike_studies_dir, MIKE_STUDY_NAME, MIKE_MODEL_OUTPUTS)

        # Dealing with the relative paths stuff in Mike's model
        self.mike_project_name = MIKE_PROJECT_NAME
        self.mike_study_name = MIKE_STUDY_NAME

        # The shared data profiles folders.
        self.profiles_dir = os.path.join(self.data_dir, PROFILES_DIR_NAME)
        self.load_profiles_dir = os.path.join(self.profiles_dir, LOAD_PROFILES_DIR_NAME)
        self.load_profiles_path = os.path.join(self.load_profiles_dir, LOAD_PROFILES_FILE_NAME)
        self.solar_profiles_dir = os.path.join(self.profiles_dir, SOLAR_PROFILES_DIR_NAME)
        self.solar_profiles_path = os.path.join(self.solar_profiles_dir, SOLAR_PROFILES_FILE_NAME)

    def get_route(self, route):
        response = False

        for n, r in self.__dict__.items():
            if route is n:
                response = r

        return response
