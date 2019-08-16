import json
import sys
import os
import pandas as pd
from application.modelling.ui_interfaces.mike import MikeWrapper

def simple_status_callback(message):
    print("Status", message)


def transfer_df_to_dict(study_parameters, params,scenario_list,load_path, pv_path):

    # Transfer df to dict....
    # ------------------------
    # luke change is that params has only one load and pv source file to be used for all scenarios
    # Go with that for now, taking load  from 1st scenario....
    # So each scenario now has only one network, and each network is the same in terms of load, participants ...
    # Also same solar file for all at this stage, but will change that...
    # Allow specification of load_file or load_folder for legacy data:
    if 'load_file' in study_parameters.columns:
        load_file = study_parameters.loc[scenario_list[0], 'load_file']
    elif 'load_folder' in study_parameters.columns:
        if '.csv' in study_parameters.loc[scenario_list[0], 'load_folder']:
            load_file = study_parameters.loc[scenario_list[0], 'load_folder']
        else:
            load_folder = os.path.join(load_path, study_parameters.loc[scenario_list[0], 'load_folder'])
            load_file = os.listdir(load_folder)[0]
    else:
        print("********* no load specified ******")
        sys.exit("********* no load specified ******")
    params['model_data_sources_mike']['selected_load_file'] = load_file

    # todo !!MR This is for single pv profile file..... need to reintroduce option for scenario-specific pv in scenario._generate_pv_profiles
    if 'pv_filename' not in study_parameters.columns:
        solar_file = ''
    else:
        solar_file = study_parameters.loc[scenario_list[0], 'pv_filename']
    params['model_data_sources_mike']['selected_solar_file'] = solar_file


    # Extract participant identifiers and tariffs from load file headers
    # (Maybe this should happen in Study?)
    # Legacy format has headers in load file as participant ids
    dfload = pd.read_csv(
        os.path.join(load_path,
                     params['model_data_sources_mike']['selected_load_file']),
                    index_col='timestamp')
    print(dfload.columns)
    participant_list = dfload.columns.tolist()
    params["model_participants_mike"] = []
    for participant in participant_list:
        # For now, take tariff information from the first scenario:
        if 'all_residents' in study_parameters.columns:
            tariff = study_parameters.loc[study_parameters.index[0],'all_residents']
        else:
            tariff = study_parameters.loc[study_parameters.index[0],participant]
        # Add tariff to the study tariff list
        params['study_parameters_mike']['tariffs'][participant] = tariff

        # set up participants list
        params["model_participants_mike"].append({
            'row_id': participant_list.index(participant),
             'row_inputs': [
                 {'name': 'participant_id', 'value': participant},
                 {'name': 'retail_tariff_type', 'value': tariff},
                 {'name': 'load_profile', 'value': participant},
                 {'name': 'solar_profile', 'value': participant},
                ]})

    # Transfer scenario parameters from df to dict
    # Only single scenario possible at the moment
    # for s in scenario_list:
    print('Extracting data for first scenario only')
    s= scenario_list[0]
    params['study_parameters_mike']['scenario'] = s
    params['study_parameters_mike']['arrangement'] = study_parameters.loc[s, 'arrangement']
    params['study_parameters_mike']['a_term'] = study_parameters.loc[s, 'a_term']
    params['study_parameters_mike']['a_rate'] = study_parameters.loc[s, 'a_rate']
    if 'en_capex_id' in study_parameters.columns:
        params['study_parameters_mike']['en_capex_id'] = study_parameters.loc[s, 'en_capex_id']

    # Transfer all pv parameters
    if not ('bau' in study_parameters.loc[s, 'arrangement']
            or study_parameters.loc[s, 'arrangement'] == 'en'):
        params['study_parameters_mike']['pv_cap_id'] = study_parameters.loc[s, 'pv_cap_id']

        # TODO MR!! This is per-scenario pv.. not yet implemented
        params['study_parameters_mike']['pv_filename'] = study_parameters.loc[s, 'pv_filename']
        if 'pv_scaleable' in study_parameters.columns:
            params['study_parameters_mike']['pv_scaleable'] = study_parameters.loc[s, 'pv_scaleable']
            if study_parameters.loc[s, 'pv_scaleable'] == True:
                params['study_parameters_mike']['pv_kW_peak'] = study_parameters.loc[s, 'pv_kW_peak']
                if 'pv_capex_scaleable' in study_parameters.columns:
                    params['study_parameters_mike']['pv_capex_scaleable'] = study_parameters.loc[
                        s, 'pv_capex_scaleable']

    # Transfer tariff parameters:
    if 'cp' in study_parameters.columns:
        params['study_parameters_mike']['tariffs']['cp'] = study_parameters.loc[s, 'cp']
    if 'en' in study_parameters.loc[s, 'arrangement']:
        params['study_parameters_mike']['tariffs']['parent'] = study_parameters.fillna('TIDNULL').loc[s, 'parent']
    if 'network_tariff' in study_parameters.columns:
        params['study_parameters_mike']['tariffs']['network_tariff'] = study_parameters.loc[s, 'network_tariff']


    #todo MR!! Allow 'all' and individual customer tariffs  per scenario
    # Transfer cp pointers
    if 'cp' in study_parameters.columns:
        params['study_parameters_mike']['common_property_load_profile'] = 'cp'
        params['study_parameters_mike']['common_property_solar_profile'] = '' # May need to be conditional??

    # Transfer central pv pointer  - check these conditions cover all cases
    #todo MR!!  central pv and bess pointers need option of being per-scenario parameters
    if 'en' in study_parameters.loc[s, 'arrangement']:
        params['study_parameters_mike']['central_solar_profile'] = 'pv'
        #todo MR!! Make central pv pointer consistent with legacy and future cases


    # Transfer individual battery parameters
    # todo MR!!  Battery parameters need option of being per-scenario parameters
    bess_owners = [c.split('_')[0] for c in study_parameters.columns if '_battery_id' in c]
    for bess_owner  in bess_owners:
        id = bess_owner + '_battery_id'
        strat = bess_owner + '_battery_strategy'
        cap = bess_owner + '_battery_capacity_kWh'
        for p in [id,strat,cap]:
            params['study_parameters_mike'][p] = study_parameters.loc[s, p]

    return params



def main(base_path,project,study_name, override_output = ''):
    with open('mike_params_null.json') as params_file:
        params = json.load(params_file)
        print(params)
        # Load data from .csv files but...
        # keeping (for the moment) default, redundant, UI-specific and Luke additions from .json file
        # Copying data aquisition scripts from original morePVs....
        # So open `study_...csv` and import into params dict:

        # Identify `study....csv` file with input parameters for all scenarios in study
        # Some of these paths may have changed...?
        project_path = os.path.join(base_path, 'mike','studies', project)
        input_path = os.path.join(project_path, 'inputs')
        study_filename = 'study_' + study_name + '.csv'
        study_file = os.path.join(input_path, study_filename)
        # Load and Pv profiles are now in shared folder:
        #todo: MR?? Maybe add an option for shared or mike as source folder?
        load_path = os.path.join(base_path,'shared','load')
        pv_path = os.path.join(base_path,'shared','solar')

        # read csv into df (it's what i know...)
        # ---------------------------------------
        study_parameters = pd.read_csv(study_file)
        study_parameters.set_index('scenario', inplace=True)
        scenario_list = [s for s in study_parameters.index if not pd.isnull(s)]

        params = transfer_df_to_dict(study_parameters, params, scenario_list, load_path, pv_path)
        #params = get_participants_from_load(load_path, params)
        print(params)


        wrapper = MikeWrapper()
        wrapper.load(params)
        wrapper.create_objects()
        results = wrapper.run(simple_status_callback)
        print(results)
        wrapper.mike_model.study.log_study_data()



if __name__ == "__main__":
    # -------------------------------------------------------
    # Set up defaults here: base_path, project and study name
    # --------------------------------------------------------
    default_base_path = '.\\application\\modelling\\data'
    #default_base_path = 'C:\\Users\\z5044992\\OneDrive - UNSW\\python\\en\\DATA_EN_5'  #(Mike's PC)
    #default_base_path = '/Users/mikeroberts/OneDrive - UNSW/python/en/DATA_EN_5'  #(Mike's Mac)
    default_project = 'ww1'
    default_study = 'C_bldg2_163'
    # Import arguments - allows multi-processing from command line
    # ------------------------------------------------------------
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
    # base_path for all input data
    if '-b' in opts:
        base_path = opts['-b']
    else:
        base_path = default_base_path

    # daylight savings:
    if '-dst' in opts:
        dst_region = opts['-dst']
    else:
        dst_region = 'nsw'
    # direct hpc output:
    # (for use on unsw hpc facility)
    if '-o' in opts:
        override_output = opts['-o']
    else:
        override_output = 'False'


    main(project=project,
         study_name=study,
         base_path=base_path,
         override_output=override_output)
