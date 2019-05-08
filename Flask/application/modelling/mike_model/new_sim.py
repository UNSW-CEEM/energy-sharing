# morePVs Copyright (C) 2018 Mike B Roberts
# multi-occupancy residential electricity with PV and storage model
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version. # This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details. You should have received a copy of the GNU General Public License along with this program. If not,
# see <http://www.gnu.org/licenses/>.
# Contact: m.roberts@unsw.edu.au

# Remaking a module to interact with the script.

import os
from ..mike_model.study import Study

# Need base_path, project study_name, override_output, use_threading


class NewSim:
    def __init__(self, folder_routes):
        base_path = folder_routes.get_route("mike_base_dir")
        self.project = folder_routes.get_route("mike_project_name")
        self.study_name = folder_routes.get_route("mike_study_name")

        # pv_path = os.path.join(base_path, 'pv_profiles', 'ceem_ui_default.csv')
        # load_path = os.path.join(base_path, 'load_profiles', 'ceem_ui_default','ceem_ui_default.csv')

        pv_path = os.path.join(folder_routes.get_route("data_dir"), 'shared','solar', 'solar_profiles_6.csv')
        load_path = os.path.join(folder_routes.get_route("data_dir"), 'shared','load', 'load_profiles_6.csv')

        print("new_sim.py/NewSim()/__init__", "Base Directory", base_path)
        print("new_sim.py/NewSim()/__init__", "Project Directory", self.project)
        print("new_sim.py/NewSim()/__init__", "PV Path", pv_path)
        print("new_sim.py/NewSim()/__init__", "Load Path", load_path)
        print("new_sim.py/NewSim()/__init__", "Study Name", self.study_name)
        
        # print("\n\n It be working", self.base_dir, "\n", self.project, self.study_name)
        
        self.study = Study(base_path, self.project, self.study_name, pv_path, load_path)
        print("new_sim.py/NewSim()/__init__", "NewSim Created")

    def run(self):
        for scenario in self.study.get_scenario_list():
            self.study.run_scenario(scenario)
