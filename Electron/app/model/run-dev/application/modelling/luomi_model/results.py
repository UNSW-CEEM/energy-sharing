import pandas as pd
import os


class Results:
    def __init__(self, time_periods, participant_ids):
        # Make empty df to store energy calcs

        print(type(participant_ids))
        print(time_periods)
        self.energy_output = {
            "df_net_export" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            "df_network_energy_flows" : pd.DataFrame(0,index = time_periods, columns=['net_participant_export', 'central_battery_export', 'unallocated_local_solar', 'unallocated_central_battery_load','gross_participant_grid_import','gross_participant_local_solar_import','gross_participant_central_battery_import']),
            "df_local_solar_import" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            "df_participant_central_batt_import" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            "df_local_solar_sales" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            "df_central_batt_solar_sales" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            "df_export_to_grid_solar_sales" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            "df_external_grid_elec_import": pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids])
            }

        self.financial_output = {
            "df_participant_variable_charge" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            "df_local_solar_import_charge" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            "df_central_batt_import_charge" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            "df_local_solar_sales_revenue" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            "df_central_batt_solar_sales_revenue" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            "df_export_to_grid_solar_sales_revenue" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            "df_fixed_charge" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            "df_total_participant_bill" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            # The df_participant_duos_payments df contains the amount paid by each participant in DUOS charges. This is summed to find the DNSP variable revenue from grid import
            "df_participant_duos_payments": pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            "df_participant_tuos_payments": pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            # Where nuos = duos + tuos + green scheme stuff
            "df_participant_nuos_payments": pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
            "df_dnsp_revenue" : pd.DataFrame(0,index = time_periods, columns=['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue','total_revenue']),
            "df_tnsp_revenue" : pd.DataFrame(0,index = time_periods, columns=['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue','total_revenue']),
            "df_nuos_revenue" : pd.DataFrame(0,index = time_periods, columns=['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue','total_revenue']),
            "df_retailer_revenue" : pd.DataFrame(0,index = time_periods, columns=['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue','total_revenue']),
            "df_retailer_fit_payments" : pd.DataFrame(0,index = time_periods, columns=['solar_fit_payments',]),
            "df_central_battery_revenue" : pd.DataFrame(0,index = time_periods, columns=['central_battery_revenue'])
            }

    def to_csv(self, output_dir, info_tag):
        info_tag = str(info_tag)
        for label in self.financial_output:
            print(label)
            self.financial_output[label].to_csv(path_or_buf=os.path.join(output_dir, label+info_tag+".csv"))
        for label in self.energy_output:
            print(label)
            self.energy_output[label].to_csv(path_or_buf=os.path.join(output_dir, label+info_tag+".csv"))


    def to_dict(self):

        new_financial_output = {}
        for key in self.financial_output:
            new_financial_output[key]=[]
            for date, row in self.financial_output[key].T.iteritems():
                row_dict = {'dt_str':str(date)}
                for col_header in self.financial_output[key]:
                    row_dict[col_header] = float(row[col_header]) if not pd.isnull(row[col_header]) else 0
                new_financial_output[key].append(row_dict)
                    # print col_header+": "+str(row[col_header])


        new_energy_output = {}
        for key in self.energy_output:
            new_energy_output[key]=[]
            for date, row in self.energy_output[key].T.iteritems():
                row_dict = {'dt_str':str(date)}
                for col_header in self.energy_output[key]:
                    row_dict[col_header] = float(row[col_header]) if not pd.isnull(row[col_header]) else 0

                    # print col_header+": "+str(row[col_header])
                new_energy_output[key].append(row_dict)

        return {'financial_output':new_financial_output, 'energy_output': new_energy_output}

    def set_net_export(self, time, participant_id, value):
        self.energy_output['df_net_export'].loc[time,participant_id] = value

    def get_net_export(self, time, participant_id):
        return self.energy_output['df_net_export'].loc[time,participant_id]

    # NOTE there was a typo here where we werent setting it to participant id but the actual participant object. might have been causing an issue.
    # If differences come out in results, I'd suggest this might have been a cause
    # To test that, try passing the participant object in the participant id spot and see if it makes a difference.
    def set_local_solar_import(self, time, participant_id, value):
        self.energy_output["df_local_solar_import"].loc[time, participant_id] = value
    def get_local_solar_import(self, time, participant_id):
        return self.energy_output["df_local_solar_import"].loc[time, participant_id]

    # NOTE there was a typo here where we werent setting it to participant id but the actual participant object. might have been causing an issue.
    # If differences come out in results, I'd suggest this might have been a cause
    # To test that, try passing the participant object in the participant id spot and see if it makes a difference.
    def set_participant_central_batt_import(self, time, participant_id, value):
        self.energy_output["df_participant_central_batt_import"].loc[time, participant_id] = value
    def get_participant_central_batt_import(self, time, participant_id):
        return self.energy_output["df_participant_central_batt_import"].loc[time, participant_id]

    # NOTE there was a typo here where we werent setting it to participant id but the actual participant object. might have been causing an issue.
    # If differences come out in results, I'd suggest this might have been a cause
    # To test that, try passing the participant object in the participant id spot and see if it makes a difference.
    def set_local_solar_sales(self, time, participant_id, value):
        self.energy_output["df_local_solar_sales"].loc[time, participant_id] = value
    def get_local_solar_sales(self, time, participant_id):
        return self.energy_output["df_local_solar_sales"].loc[time, participant_id]

    # NOTE there was a typo here where we werent setting it to participant id but the actual participant object. might have been causing an issue.
    # If differences come out in results, I'd suggest this might have been a cause
    # To test that, try passing the participant object in the participant id spot and see if it makes a difference.
    def set_central_batt_solar_sales(self, time, participant_id, value):
        self.energy_output["df_central_batt_solar_sales"].loc[time, participant_id] = value
    def get_central_batt_solar_sales(self, time, participant_id):
        return self.energy_output["df_central_batt_solar_sales"].loc[time, participant_id]

    def set_export_to_grid_solar_sales(self, time, participant_id, value):
        self.energy_output["df_export_to_grid_solar_sales"].loc[time,participant_id] = value
    def get_export_to_grid_solar_sales(self, time, participant_id,):
        return self.energy_output["df_export_to_grid_solar_sales"].loc[time,participant_id]

    def set_external_grid_elec_import(self, time, participant_id, value):
        self.energy_output["df_external_grid_elec_import"].loc[time,participant_id] = value
    def get_external_grid_elec_import(self, time, participant_id):
        return self.energy_output["df_external_grid_elec_import"].loc[time,participant_id]


    # 'Network Energy Flows'
    def set_net_participant_export(self, time, value):
        self.energy_output['df_network_energy_flows'].loc[time, 'net_participant_export'] = value

    def get_net_participant_export(self, time):
        return self.energy_output['df_network_energy_flows'].loc[time, 'net_participant_export']

    def set_central_battery_export(self, time, value):
        self.energy_output['df_network_energy_flows'].loc[time, 'central_battery_export'] = value

    def get_central_battery_export(self, time):
        return self.energy_output['df_network_energy_flows'].loc[time, 'central_battery_export']

    # TODO I think this should be labelled import, as our convention is normally subject -> action with the action as positive.
    def set_net_network_export(self, time, value):
        self.energy_output['df_network_energy_flows'].loc[time, 'net_network_export'] = value

    def set_unallocated_local_solar(self, time, value):
        self.energy_output["df_network_energy_flows"].loc[time, 'unallocated_local_solar'] = value

    def set_unallocated_central_battery_load(self, time, value):
        self.energy_output["df_network_energy_flows"].loc[time, 'unallocated_central_battery_load'] = value

    def set_gross_participant_grid_import(self, time, value):
        self.energy_output["df_network_energy_flows"].loc[time, 'gross_participant_grid_import'] = value

    def get_gross_participant_grid_import(self, time):
        return self.energy_output["df_network_energy_flows"].loc[time, 'gross_participant_grid_import']

    def set_gross_participant_local_solar_import(self, time, value):
        self.energy_output["df_network_energy_flows"].loc[time, 'gross_participant_local_solar_import'] = value

    def get_gross_participant_local_solar_import(self, time):
        return self.energy_output["df_network_energy_flows"].loc[time, 'gross_participant_local_solar_import']

    def set_gross_participant_central_battery_import(self, time, value):
        self.energy_output["df_network_energy_flows"].loc[time, 'gross_participant_central_battery_import'] = value

    def get_gross_participant_central_battery_import(self, time):
        return self.energy_output["df_network_energy_flows"].loc[time, 'gross_participant_central_battery_import']





    # Financial Results
    def set_participant_variable_charge(self, time, participant_id, value):
        self.financial_output["df_participant_variable_charge"].loc[time, participant_id] = value
    def get_participant_variable_charge(self, time, participant_id):
        return self.financial_output["df_participant_variable_charge"].loc[time, participant_id]

    def set_local_solar_import_charge(self, time, participant_id, value):
        self.financial_output["df_local_solar_import_charge"].loc[time,participant_id] = value
    def get_local_solar_import_charge(self, time, participant_id):
        return self.financial_output["df_local_solar_import_charge"].loc[time,participant_id]

    def set_central_batt_import_charge(self, time, participant_id, value):
        self.financial_output["df_central_batt_import_charge"].loc[time,participant_id] = value
    def get_central_batt_import_charge(self, time, participant_id):
        return self.financial_output["df_central_batt_import_charge"].loc[time,participant_id]

    def set_local_solar_sales_revenue(self, time, participant_id, value):
        self.financial_output["df_local_solar_sales_revenue"].loc[time,participant_id] = value
    def get_local_solar_sales_revenue(self, time, participant_id):
        return self.financial_output["df_local_solar_sales_revenue"].loc[time,participant_id]

    def set_central_batt_solar_sales_revenue(self, time, participant_id, value):
        self.financial_output["df_central_batt_solar_sales_revenue"].loc[time,participant_id] = value
    def get_central_batt_solar_sales_revenue(self, time, participant_id):
        return self.financial_output["df_central_batt_solar_sales_revenue"].loc[time,participant_id]

    def set_export_to_grid_solar_sales_revenue(self, time, participant_id, value):
        self.financial_output["df_export_to_grid_solar_sales_revenue"].loc[time,participant_id] = value
    def get_export_to_grid_solar_sales_revenue(self, time, participant_id):
        return self.financial_output["df_export_to_grid_solar_sales_revenue"].loc[time,participant_id]

    def set_fixed_charge(self, time, participant_id, value):
        self.financial_output["df_fixed_charge"].loc[time,participant_id] = value
    def get_fixed_charge(self, time, participant_id):
        return self.financial_output["df_fixed_charge"].loc[time,participant_id]

    def set_total_participant_bill(self, time, participant_id, value):
        self.financial_output["df_total_participant_bill"].loc[time,participant_id] = value
    def get_total_participant_bill(self, time, participant_id):
        return self.financial_output["df_total_participant_bill"].loc[time,participant_id]

    def set_participant_duos_payments(self, time, participant_id, value):
        self.financial_output["df_participant_duos_payments"].loc[time,participant_id] = value
    def get_participant_duos_payments(self, time, participant_id):
        return self.financial_output["df_participant_duos_payments"].loc[time,participant_id]

    def set_participant_tuos_payments(self, time, participant_id, value):
        self.financial_output["df_participant_tuos_payments"].loc[time,participant_id] = value
    def get_participant_tuos_payments(self, time, participant_id):
        return self.financial_output["df_participant_tuos_payments"].loc[time,participant_id]

    def set_participant_nuos_payments(self, time, participant_id, value):
        self.financial_output["df_participant_nuos_payments"].loc[time,participant_id] = value
    def get_participant_nuos_payments(self, time, participant_id):
        return self.financial_output["df_participant_nuos_payments"].loc[time,participant_id]

    def set_central_battery_revenue(self, time, value):
        self.financial_output["df_central_battery_revenue"].loc[time,'central_battery_revenue'] = value
    def get_central_battery_revenue(self, time):
        return self.financial_output["df_central_battery_revenue"].loc[time,'central_battery_revenue']

    # DNSP Revenues

    def set_dnsp_grid_import_revenue_fixed(self, time, value):
        self.financial_output["df_dnsp_revenue"].loc[time,'grid_import_revenue_fixed'] = value
    def get_dnsp_grid_import_revenue_fixed(self, time):
        return self.financial_output["df_dnsp_revenue"].loc[time,'grid_import_revenue_fixed']

    def set_dnsp_grid_import_revenue_variable(self, time, value):
        self.financial_output["df_dnsp_revenue"].loc[time,'grid_import_revenue_variable'] = value
    def get_dnsp_grid_import_revenue_variable(self, time):
        return self.financial_output["df_dnsp_revenue"].loc[time,'grid_import_revenue_variable']

    def set_dnsp_local_solar_import_revenue(self, time, value):
        self.financial_output["df_dnsp_revenue"].loc[time,'local_solar_import_revenue'] = value
    def get_dnsp_local_solar_import_revenue(self, time):
        return self.financial_output["df_dnsp_revenue"].loc[time,'local_solar_import_revenue']

    def set_dnsp_central_battery_import_revenue(self, time, value):
        self.financial_output["df_dnsp_revenue"].loc[time,'central_battery_import_revenue'] = value
    def get_dnsp_central_battery_import_revenue(self, time):
        return self.financial_output["df_dnsp_revenue"].loc[time,'central_battery_import_revenue']

    def set_dnsp_total_revenue(self, time, value):
        self.financial_output["df_dnsp_revenue"].loc[time,'total_revenue'] = value
    def get_dnsp_total_revenue(self, time):
        return self.financial_output["df_dnsp_revenue"].loc[time,'total_revenue']


    # TNSP Revenues

    def set_tnsp_grid_import_revenue_fixed(self, time, value):
        self.financial_output["df_tnsp_revenue"].loc[time,'grid_import_revenue_fixed'] = value
    def get_tnsp_grid_import_revenue_fixed(self, time):
        return self.financial_output["df_tnsp_revenue"].loc[time,'grid_import_revenue_fixed']

    def set_tnsp_grid_import_revenue_variable(self, time, value):
        self.financial_output["df_tnsp_revenue"].loc[time,'grid_import_revenue_variable'] = value
    def get_tnsp_grid_import_revenue_variable(self, time):
        return self.financial_output["df_tnsp_revenue"].loc[time,'grid_import_revenue_variable']

    def set_tnsp_local_solar_import_revenue(self, time, value):
        self.financial_output["df_tnsp_revenue"].loc[time,'local_solar_import_revenue'] = value
    def get_tnsp_local_solar_import_revenue(self, time):
        return self.financial_output["df_tnsp_revenue"].loc[time,'local_solar_import_revenue']

    def set_tnsp_central_battery_import_revenue(self, time, value):
        self.financial_output["df_tnsp_revenue"].loc[time,'central_battery_import_revenue'] = value
    def get_tnsp_central_battery_import_revenue(self, time):
        return self.financial_output["df_tnsp_revenue"].loc[time,'central_battery_import_revenue']

    def set_tnsp_total_revenue(self, time, value):
        self.financial_output["df_tnsp_revenue"].loc[time,'total_revenue'] = value
    def get_tnsp_total_revenue(self, time):
        return self.financial_output["df_tnsp_revenue"].loc[time,'total_revenue']


# NUOS Revenues

    def set_nuos_grid_import_revenue_fixed(self, time, value):
        self.financial_output["df_nuos_revenue"].loc[time,'grid_import_revenue_fixed'] = value
    def get_nuos_grid_import_revenue_fixed(self, time):
        return self.financial_output["df_nuos_revenue"].loc[time,'grid_import_revenue_fixed']

    def set_nuos_grid_import_revenue_variable(self, time, value):
        self.financial_output["df_nuos_revenue"].loc[time,'grid_import_revenue_variable'] = value
    def get_nuos_grid_import_revenue_variable(self, time):
        return self.financial_output["df_nuos_revenue"].loc[time,'grid_import_revenue_variable']

    def set_nuos_local_solar_import_revenue(self, time, value):
        self.financial_output["df_nuos_revenue"].loc[time,'local_solar_import_revenue'] = value
    def get_nuos_local_solar_import_revenue(self, time):
        return self.financial_output["df_nuos_revenue"].loc[time,'local_solar_import_revenue']

    def set_nuos_central_battery_import_revenue(self, time, value):
        self.financial_output["df_nuos_revenue"].loc[time,'central_battery_import_revenue'] = value
    def get_nuos_central_battery_import_revenue(self, time):
        return self.financial_output["df_nuos_revenue"].loc[time,'central_battery_import_revenue']

    def set_nuos_total_revenue(self, time, value):
        self.financial_output["df_nuos_revenue"].loc[time,'total_revenue'] = value
    def get_nuos_total_revenue(self, time):
        return self.financial_output["df_nuos_revenue"].loc[time,'total_revenue']

# Retailer Revenues

    def set_retailer_grid_import_revenue_fixed(self, time, value):
        self.financial_output["df_retailer_revenue"].loc[time,'grid_import_revenue_fixed'] = value
    def get_retailer_grid_import_revenue_fixed(self, time):
        return self.financial_output["df_retailer_revenue"].loc[time,'grid_import_revenue_fixed']

    def set_retailer_grid_import_revenue_variable(self, time, value):
        self.financial_output["df_retailer_revenue"].loc[time,'grid_import_revenue_variable'] = value
    def get_retailer_grid_import_revenue_variable(self, time):
        return self.financial_output["df_retailer_revenue"].loc[time,'grid_import_revenue_variable']

    def set_retailer_local_solar_import_revenue(self, time, value):
        self.financial_output["df_retailer_revenue"].loc[time,'local_solar_import_revenue'] = value
    def get_retailer_local_solar_import_revenue(self, time):
        return self.financial_output["df_retailer_revenue"].loc[time,'local_solar_import_revenue']

    def set_retailer_central_battery_import_revenue(self, time, value):
        self.financial_output["df_retailer_revenue"].loc[time,'central_battery_import_revenue'] = value
    def get_retailer_central_battery_import_revenue(self, time):
        return self.financial_output["df_retailer_revenue"].loc[time,'central_battery_import_revenue']

    def set_retailer_total_revenue(self, time, value):
        self.financial_output["df_retailer_revenue"].loc[time,'total_revenue'] = value
    def get_retailer_total_revenue(self, time):
        return self.financial_output["df_retailer_revenue"].loc[time,'total_revenue']

    def set_retailer_solar_fit_payments(self, time, value):
        self.financial_output["df_retailer_fit_payments"].loc[time,'solar_fit_payments'] = value
    def get_retailer_solar_fit_payments(self, time):
        return self.financial_output["df_retailer_fit_payments"].loc[time,'solar_fit_payments']




