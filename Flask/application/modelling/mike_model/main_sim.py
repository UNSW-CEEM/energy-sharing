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

# IMPORT Modules
import numpy as np
import logging
import sys
import os
import pdb, traceback
import pandas as pd
import threading
import concurrent.futures
import datetime as dt

# TODO stupid import error but the import works.
# Import Classes
import en_utilities as util
from study import Study


def model_run(base_path, project, study_name, override_output='', use_threading='False'):

    # set up script logging
    py_name = os.path.basename(__file__)
    util.setup_local_logging(base_path, py_name, label=study_name)
    start_time = dt.datetime.now()
    global study

    try:
        # --------------------------------------
        # Initialise and load data for the study
        # --------------------------------------
        logging.info("study_name = %s", study_name)
        logging.info("Thread variable is %s", use_threading)
        study_ng = Study(
            base_path=base_path,
            project=project,
            study_name=study_name,
            dst_region=dst_region,
            override_output=override_output,
            use_threading=use_threading)

        if use_threading == 'True':  # NB use_threading is a string so need to compare with string
            # -------------
            # Use Threading
            # -------------
            logging.info("THREADING")
            global lock
            num_worker_threads = num_threads
            lock = threading.Lock()
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_worker_threads) as x:
                results = list(x.map(run_scenario, study.scenario_list))

        else:
            # WITHOUT Threads (simpler to debug):
            # ----------------------------------
            logging.info("NOT THREADING")
            print("study: ", study)
            print("study.scenario_list: ", study_ng.get_scenario_list())
            for scenario in study_ng.get_scenario_list():
                study_ng.run_scenario(scenario)

        study_ng.log_study_data()

        end_time = dt.datetime.now()
        duration = end_time - start_time
        print("***COMPLETED STUDY ***", study_name)
        logging.info("***COMPLETED STUDY %s ***", study_name)
        logging.info(" ********* Completed %i scenarios in %f **************", len(study_ng.scenario_list),
                     duration.seconds)
        logging.info(" ********* Time per Scenario is  %f **************", duration.seconds / len(study_ng.scenario_list))

    except:
        pass
        logging.exception('\n\n\n Exception !!!!!!')
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)


if __name__ == "__main__":
    # Raise exceptions on warnings - for debugging
    # import warnings
    # warnings.filterwarnings('error', category=UnicodeWarning)

    num_threads = 6
    default_project = 'ww1'  # 'tests'
    default_study = 'W_bldg4en_cust'

    default_use_threading = False

    # Import arguments - allows multi-processing from command line
    opts = {}
    while sys.argv:
        if sys.argv[0][0] == '-':
            opts[sys.argv[0]] = sys.argv[1]
        sys.argv = sys.argv[1:]

    if '-p' in opts:
        project = opts['-p']
    else:
        project = default_project

    if '-s' in opts:
        study = opts['-s']
    else:
        study = default_study

    if '-t' in opts:
        use_threading = opts['-t']
    else:
        use_threading = default_use_threading

    # base_path for all input data
    if '-b' in opts:
        base_path = opts['-b']
    else:
        base_path = os.path.realpath('temp_data_location')

    # daylight savings:
    if '-dst' in opts:
        dst_region = opts['-dst']
    else:
        dst_region = 'nsw'

    # direct hpc output:
    if '-o' in opts:
        override_output = opts['-o']
    else:
        override_output = 'False'

    model_run(
        project=project,
        study_name=study,
        base_path=base_path,
        use_threading=use_threading,
        override_output=override_output)
