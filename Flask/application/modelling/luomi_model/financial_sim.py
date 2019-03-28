# Custom modules

# Required 3rd party libraries
import pandas as pd

TIME_PERIOD_LENGTH_MINS = 30


def simulate(time_periods, mynetwork, my_tariffs, results, status_callback=None):
    
    # --------------------------------------------------------------
    # Participant financial calcs
    # --------------------------------------------------------------
    # Status Reporting
    if status_callback:
        status_callback('Calculating Financial Flows: 0%')
        percent_finished = 0
        single_step_percent = 100.0 / float(len(time_periods) * len(mynetwork.get_participants()))


    for p in mynetwork.get_participants():
        # Initialise params used in block tariff calcs.
        total_usage_today = 0
        previous_time = time_periods[0]

        for time in time_periods:
            if status_callback:
                percent_finished += single_step_percent
                status_callback('Calculating Financial Flows: '+str(round(percent_finished))+"%")
            
            retail_tariff_type = p.get_retail_tariff_type()
            network_tariff_type = p.get_network_tariff_type()

            net_export = results.get_net_export(time, p.get_id())
            local_solar_import = results.get_local_solar_import(time, p.get_id())
            participant_central_batt_import = results.get_participant_central_batt_import(time, p.get_id())
            local_solar_sales = results.get_local_solar_sales(time, p.get_id())
            central_batt_solar_sales = results.get_central_batt_solar_sales(time, p.get_id())
            # Left over solar which is exported to the grid. Calculated in energy flows above.
            export_to_grid_solar_sales = results.get_export_to_grid_solar_sales(time, p.get_id())
            # Left over load which requires grid import. Calculated in energy flows above.
            external_grid_import = results.get_external_grid_elec_import(time, p.get_id())

            # Calc resultant financial flows (all except variable charge - this is done below)
            results.set_local_solar_import_charge(time, p.get_id(),  my_tariffs.get_local_solar_import_tariff(time) * local_solar_import)
            results.set_central_batt_import_charge(time, p.get_id(),  my_tariffs.get_central_batt_tariff(time) * participant_central_batt_import)
            results.set_local_solar_sales_revenue(time, p.get_id(),  my_tariffs.get_local_solar_export_tariff(time) * local_solar_sales)
            results.set_central_batt_solar_sales_revenue(time, p.get_id(),  my_tariffs.get_central_batt_buy_tariff(time) * central_batt_solar_sales)
            results.set_export_to_grid_solar_sales_revenue(time, p.get_id(),  my_tariffs.get_retail_solar_tariff(time,retail_tariff_type,8) * export_to_grid_solar_sales)
            results.set_fixed_charge(time, p.get_id(),  my_tariffs.get_fixed_tariff(TIME_PERIOD_LENGTH_MINS,retail_tariff_type))
            
            # Variable charges - apply retail tariffs to external grid import
            # May be worth moving this section of code into util?
            
            # Block tariff ---------------
            # The block tariffs will be applied by counting the volume of energy used within the period and applying the appropriate tariff accordingly
            # if retail_tariff_type == 'Business Anytime':
            if 'Block' in retail_tariff_type:
                block_1_charge, block_2_charge, block_1_volume = my_tariffs.get_variable_retail_tariff(time,'Block')

                # First, calculate the current cumulative energy usage
                # Check whether it's a new day. If the current hour is midnight and the previous hour was 11pm, then it's a new day.
                if time.hour == 0 and previous_time.hour == 23 :
                    # If it's a new day then reset the block counter
                    total_usage_today = 0
                    # Set the previous time equal to current time for next loop.
                    previous_time = time
                else:
                    # Add the grid import during this period to the total usage for the day
                    # NOTE _ we are assuming only grid import applies to the block total
                    total_usage_today += external_grid_import
                
                # If the usage today has not yet exceeded the block max, then use the first block rate, else the second rate.
                if total_usage_today < block_1_volume :
                    variable_tariff = block_1_charge
                else:
                    variable_tariff = block_2_charge

                # Apply the tariff 
                results.set_participant_variable_charge(time, p.get_id(), variable_tariff * external_grid_import)
                
            
            # TOU Tariffs ---------------
            # The TOU tariffs will be applied by using if statements to determine whether peak/shoulder/off-peak
            # if retail_tariff_type == 'Business TOU':
            if 'TOU' in retail_tariff_type:
                peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag = my_tariffs.get_variable_retail_tariff(time,'TOU')

                # If the TOU periods apply all days and not just weekdays then the flag will be zero
                if tou_weekday_only_flag == 0 :
                    # Check for whether it's a peak time
                    if (time.hour > peak_start_time and time.hour <= peak_end_time) or (time.hour > peak_start_time_2 and time.hour <= peak_end_time_2) :
                        variable_tariff = peak_charge
                    # If not, check whether it's shoulder time
                    elif (time.hour > shoulder_start_time and time.hour <= shoulder_end_time) or (time.hour > shoulder_start_time_2 and time.hour <= shoulder_end_time_2) :
                        variable_tariff = shoulder_charge
                    else:
                        variable_tariff = offpeak_charge

                # In the case where TOU periods only apply on weekdays then check for weekdays and apply the same logic as above.
                elif tou_weekday_only_flag == 1 and (time.weekday() >= 0 and time.weekday() <=4) :
                    if (time.hour > peak_start_time and time.hour <= peak_end_time) or (time.hour > peak_start_time_2 and time.hour <= peak_end_time_2) :
                        variable_tariff = peak_charge
                    elif (time.hour > shoulder_start_time and time.hour <= shoulder_end_time) or (time.hour > shoulder_start_time_2 and time.hour <= shoulder_end_time_2) :
                        variable_tariff = shoulder_charge
                    else:
                        variable_tariff = offpeak_charge

                # Else assume it's off-peak time
                else:
                    variable_tariff = offpeak_charge
                # Apply the tariff
                results.set_participant_variable_charge(time, p.get_id(),variable_tariff * external_grid_import )

            # Total bill

            participant_variable_charge = results.get_participant_variable_charge(time, p.get_id())
            local_solar_import_charge = results.get_local_solar_import_charge(time, p.get_id())
            central_batt_import_charge = results.get_central_batt_import_charge(time, p.get_id())
            local_solar_sales_revenue = results.get_local_solar_sales_revenue(time, p.get_id())
            central_batt_solar_sales_revenue = results.get_central_batt_solar_sales_revenue(time, p.get_id())
            export_to_grid_solar_sales_revenue = results.get_export_to_grid_solar_sales_revenue(time, p.get_id())
            fixed_charge = results.get_fixed_charge(time, p.get_id())

            # Add charges and subtract revenue for total bill
            total_bill = participant_variable_charge + local_solar_import_charge + central_batt_import_charge + fixed_charge - local_solar_sales_revenue - central_batt_solar_sales_revenue - export_to_grid_solar_sales_revenue 
            results.set_total_participant_bill(time, p.get_id(), total_bill)

    
    # --------------------------------------------------------------
    # DNSP financial calcs
    # --------------------------------------------------------------  
    if status_callback:
        status_callback('Calculating DNSP Finances:0%')
        percent_finished = 0
        single_step_percent = 100.0 / float(len(time_periods) * len(mynetwork.get_participants()))
    # Initialise df used in demand tariff calcs (stores max demand values)      
    df_participant_max_monthly_demand = pd.DataFrame(0, index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]) 


    for p in mynetwork.get_participants():
        # Initialise params used in demand tariff calcs
        max_demand = 0
        max_demand_time = time_periods[0]
        previous_month = time_periods[0].month

        for time in time_periods:
            # Update callback status
            if status_callback:
                percent_finished += single_step_percent
                status_callback('Calculating DNSP Finances: '+str(round(percent_finished))+"%")       

            # Required energy flows for retailer / DNSP / TNSP calcs
            gross_participant_grid_import = results.get_gross_participant_grid_import(time)
            gross_participant_local_solar_import = results.get_gross_participant_local_solar_import(time)
            gross_participant_central_battery_import = results.get_gross_participant_central_battery_import(time)
            

            # Financial calcs for DNSP
            # Fixed charges revenue is the fixed charge times by the number of customers paying this charge

            results.set_dnsp_grid_import_revenue_fixed(time,  my_tariffs.get_duos_on_grid_import_fixed(TIME_PERIOD_LENGTH_MINS, network_tariff_type) * len(mynetwork.get_participants()))
            results.set_dnsp_local_solar_import_revenue(time,  my_tariffs.get_duos_on_local_solar_import(time) * gross_participant_local_solar_import)
            results.set_dnsp_central_battery_import_revenue(time,  my_tariffs.get_duos_on_central_batt_import(time) * gross_participant_central_battery_import)

            # Variable component - will need to be the sum of each individual participant's dnsp payment because each may be on a different tariff.
            
            network_tariff_type = p.get_network_tariff_type()

            # Left over load which requires grid import. Calculated in energy flows above.
            external_grid_import = results.get_external_grid_elec_import(time, p.get_id())

            # Controlled Load and Flat Tariffs ---------------
            # The controlled load tariffs and the flat tariff will be applied simply as the tariff times by the volume of electricity consumed, so the same calculation is applied.
            # if network_tariff_type == 'Controlled Load 1' or network_tariff_type == 'Controlled Load 2' or network_tariff_type == 'LV Small Business Anytime':
            #     variable_tariff = my_tariffs.get_duos_on_grid_import_variable(time, network_tariff_type)
            #     results.set_participant_duos_payments(time, p.get_id(), variable_tariff * external_grid_import)

            # TOU Tariffs ---------------
            # The TOU tariffs will be applied by using if statements to determine whether peak/shoulder/off-peak
            # if network_tariff_type == 'LV TOU <100MWh' or network_tariff_type == 'LV Business TOU_Interval meter' or network_tariff_type == 'Small Business - Opt in Demand':
            if 'TOU' in network_tariff_type:
                print("Time of Use Land")
                peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag, demand_charge = my_tariffs.get_duos_on_grid_import_variable(time,network_tariff_type)

                # If the TOU periods apply all days and not just weekdays then the flag will be zero
                if tou_weekday_only_flag == 0 :
                    # Check for whether it's a peak time
                    if (time.hour > peak_start_time and time.hour <= peak_end_time) or (time.hour > peak_start_time_2 and time.hour <= peak_end_time_2) :
                        variable_tariff = peak_charge
                    # If not, check whether it's shoulder time
                    elif (time.hour > shoulder_start_time and time.hour <= shoulder_end_time) or (time.hour > shoulder_start_time_2 and time.hour <= shoulder_end_time_2) :
                        variable_tariff = shoulder_charge

                # In the case where TOU periods only apply on weekdays then check for weekdays and apply the same logic as above.
                elif tou_weekday_only_flag == 1 and (time.weekday() >= 0 and time.weekday() <=4) :
                    if (time.hour > peak_start_time and time.hour <= peak_end_time) or (time.hour > peak_start_time_2 and time.hour <= peak_end_time_2) :
                        variable_tariff = peak_charge
                    elif (time.hour > shoulder_start_time and time.hour <= shoulder_end_time) or (time.hour > shoulder_start_time_2 and time.hour <= shoulder_end_time_2) :
                        variable_tariff = shoulder_charge

                # Else assume it's off-peak time
                else:
                    variable_tariff = offpeak_charge
                # Apply the tariff 
                results.set_participant_duos_payments(time, p.get_id(),variable_tariff * external_grid_import )
            
            # Demand tariff includes TOU component which is handled above. In addition, the demand component is calculated for each participant
            # if network_tariff_type == 'Small Business - Opt in Demand' :
            if 'Demand' in network_tariff_type:
                current_month = time.month
                
                # If it's a new month, then print the max demand value to the df at the max demand time, reset the max demand to zero and set the month to the new month.
                if current_month != previous_month:
                    # Print to df in units of power (kVA, assume unity pf)
                    df_participant_max_monthly_demand.loc[max_demand_time, p.get_id()] = max_demand * (60/TIME_PERIOD_LENGTH_MINS)
                    max_demand = 0
                    previous_month = current_month

                # Left over load which requires grid import. Calculated in energy flows above.
                external_grid_import = results.get_external_grid_elec_import(time, p.get_id())
                
                # If the load in this period is greater than the currently recorded max demand then update max demand and max demand time
                if external_grid_import > max_demand :
                    max_demand = external_grid_import
                    max_demand_time = time

                # In the case where there is less than 1 month of data (i.e. start and end months are the same) AND the loop is on the final time period, then print max to df.
                if time_periods[0].month == time_periods[-1].month and time == time_periods[-1] :
                    # Print to df in units of power (kVA, assume unity pf)
                    df_participant_max_monthly_demand.loc[max_demand_time, p.get_id()] = max_demand * (60/TIME_PERIOD_LENGTH_MINS)
        
        # After looping through all time periods for the current participant
        # if network_tariff_type == 'Small Business - Opt in Demand' :
        if 'Demand' in network_tariff_type:
            # Need a separate time loop to calculate demand charges since the max kVA values are entered into the df 'retrospectively'
            for time in time_periods:
                demand_payment = df_participant_max_monthly_demand.loc[time, p.get_id()] * demand_charge
                new_duos_payment = results.get_participant_duos_payments(time, p.get_id()) + demand_payment
                results.set_participant_duos_payments(time, p.get_id(), new_duos_payment)
    
    # Finally, calculate the sum across participants to find the DNSP's variable DUOS revenue. Then calculate the DNSP's total revenue (i.e. including fixed charges etc).
    for time in time_periods:
        grid_import_revenue_variable = sum([results.get_participant_duos_payments(time, participant.get_id()) for participant in mynetwork.get_participants()])
        results.set_dnsp_grid_import_revenue_variable(time, grid_import_revenue_variable)
    # Sum across columns for total dnsp revenue 
    for time in time_periods:
        dnsp_total_revenue = results.get_dnsp_grid_import_revenue_fixed(time) + results.get_dnsp_grid_import_revenue_variable(time) + results.get_dnsp_local_solar_import_revenue(time) + results.get_dnsp_central_battery_import_revenue(time)
        results.set_dnsp_total_revenue(time, dnsp_total_revenue)
    # --------------------------------------------------------------
    # TNSP financial calcs 
    # --------------------------------------------------------------
    if status_callback:
        status_callback('Calculating TNSP Finances:0%')
        percent_finished = 0
        single_step_percent = 100.0 / float(len(time_periods) * len(mynetwork.get_participants()))
    # Initialise df used in demand tariff calcs (stores max demand values)      
    df_participant_max_monthly_demand = pd.DataFrame(0, index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]) 


    for p in mynetwork.get_participants():
        # Initialise params used in demand tariff calcs
        max_demand = 0
        max_demand_time = time_periods[0]
        previous_month = time_periods[0].month

        for time in time_periods:
            # Update callback status
            if status_callback:
                percent_finished += single_step_percent
                status_callback('Calculating TNSP Finances: '+str(round(percent_finished))+"%")       

            # Required energy flows for retailer / DNSP / TNSP calcs
            gross_participant_grid_import = results.get_gross_participant_grid_import(time)
            gross_participant_local_solar_import = results.get_gross_participant_local_solar_import(time)
            gross_participant_central_battery_import = results.get_gross_participant_central_battery_import(time)

            # Financial calcs for TNSP
            # Fixed charges revenue is the fixed charge times by the number of customers paying this charge

            results.set_tnsp_grid_import_revenue_fixed(time, my_tariffs.get_tuos_on_grid_import_fixed(TIME_PERIOD_LENGTH_MINS, network_tariff_type) * len(mynetwork.get_participants()))
            results.set_tnsp_local_solar_import_revenue(time, my_tariffs.get_tuos_on_local_solar_import(time) * gross_participant_local_solar_import)
            results.set_tnsp_central_battery_import_revenue(time, my_tariffs.get_tuos_on_central_batt_import(time) * gross_participant_central_battery_import)
            
            # Variable component - will need to be the sum of each individual participant's tnsp payment because each may be on a different tariff.
            
            network_tariff_type = p.get_network_tariff_type()

            # Left over load which requires grid import. Calculated in energy flows above.
            external_grid_import = results.get_external_grid_elec_import(time, p.get_id())

            # Controlled Load and Flat Tariffs ---------------
            # The controlled load tariffs and the flat tariff will be applied simply as the tariff times by the volume of electricity consumed, so the same calculation is applied.
            # if network_tariff_type == 'Controlled Load 1' or network_tariff_type == 'Controlled Load 2' or network_tariff_type == 'LV Small Business Anytime':
            #     variable_tariff = my_tariffs.get_tuos_on_grid_import_variable(time, network_tariff_type)
            #     results.set_participant_tuos_payments(time, p.get_id(), variable_tariff * external_grid_import)

            # TOU Tariffs ---------------
            # The TOU tariffs will be applied by using if statements to determine whether peak/shoulder/off-peak
            # if network_tariff_type == 'LV TOU <100MWh' or network_tariff_type == 'LV Business TOU_Interval meter' or network_tariff_type == 'Small Business - Opt in Demand':
            if 'TOU' in network_tariff_type:
                peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag, demand_charge = my_tariffs.get_tuos_on_grid_import_variable(time,network_tariff_type)

                # If the TOU periods apply all days and not just weekdays then the flag will be zero
                if tou_weekday_only_flag == 0 :
                    # Check for whether it's a peak time
                    if (time.hour > peak_start_time and time.hour <= peak_end_time) or (time.hour > peak_start_time_2 and time.hour <= peak_end_time_2) :
                        variable_tariff = peak_charge
                    # If not, check whether it's shoulder time
                    elif (time.hour > shoulder_start_time and time.hour <= shoulder_end_time) or (time.hour > shoulder_start_time_2 and time.hour <= shoulder_end_time_2) :
                        variable_tariff = shoulder_charge

                # In the case where TOU periods only apply on weekdays then check for weekdays and apply the same logic as above.
                elif tou_weekday_only_flag == 1 and (time.weekday() >= 0 and time.weekday() <=4) :
                    if (time.hour > peak_start_time and time.hour <= peak_end_time) or (time.hour > peak_start_time_2 and time.hour <= peak_end_time_2) :
                        variable_tariff = peak_charge
                    elif (time.hour > shoulder_start_time and time.hour <= shoulder_end_time) or (time.hour > shoulder_start_time_2 and time.hour <= shoulder_end_time_2) :
                        variable_tariff = shoulder_charge

                # Else assume it's off-peak time
                else:
                    variable_tariff = offpeak_charge
                # Apply the tariff 
                results.set_participant_tuos_payments(time, p.get_id(), variable_tariff * external_grid_import)
            
            # Demand tariff includes TOU component which is handled above. In addition, the demand component is calculated for each participant
            # if network_tariff_type == 'Small Business - Opt in Demand' :
            if 'Demand' in network_tariff_type:
                current_month = time.month
                
                # If it's a new month, then print the max demand value to the df at the max demand time, reset the max demand to zero and set the month to the new month.
                if current_month != previous_month:
                    # Print to df in units of power (kVA, assume unity pf)
                    df_participant_max_monthly_demand.loc[max_demand_time, p.get_id()] = max_demand * (60/TIME_PERIOD_LENGTH_MINS)
                    max_demand = 0
                    previous_month = current_month

                # Left over load which requires grid import. Calculated in energy flows above.
                external_grid_import = results.get_external_grid_elec_import(time, p.get_id())
                
                # If the load in this period is greater than the currently recorded max demand then update max demand and max demand time
                if external_grid_import > max_demand :
                    max_demand = external_grid_import
                    max_demand_time = time

                # In the case where there is less than 1 month of data (i.e. start and end months are the same) AND the loop is on the final time period, then print max to df.
                if time_periods[0].month == time_periods[-1].month and time == time_periods[-1] :
                    # Print to df in units of power (kVA, assume unity pf)
                    df_participant_max_monthly_demand.loc[max_demand_time, p.get_id()] = max_demand * (60/TIME_PERIOD_LENGTH_MINS)
        
        # After looping through all time periods for the current participant
        # if network_tariff_type == 'Small Business - Opt in Demand' :
        if 'Demand' in network_tariff_type:
            # Need a separate time loop to calculate demand charges since the max kVA values are entered into the df 'retrospectively'
            for time in time_periods:
                demand_payment = df_participant_max_monthly_demand.loc[time, p.get_id()] * demand_charge
                new_tuos_payment = results.get_participant_tuos_payments(time, p.get_id())
                results.set_participant_tuos_payments(time, p.get_id(), new_tuos_payment)
    
    # Finally, calculate the sum across participants to find the TNSP's variable TUOS revenue. Then calculate the TNSP's total revenue (i.e. including fixed charges etc).
    for time in time_periods:
        tnsp_grid_import_revenue_variable = sum( [results.get_participant_tuos_payments(time, participant.get_id()) for participant in mynetwork.get_participants()] )
        results.set_tnsp_grid_import_revenue_variable(time, tnsp_grid_import_revenue_variable)
    # Sum across columns for total tnsp revenue 
    for time in time_periods:    
        tnsp_total_revenue = results.get_tnsp_grid_import_revenue_fixed(time) + results.get_tnsp_grid_import_revenue_variable(time) + results.get_tnsp_local_solar_import_revenue(time) + results.get_tnsp_central_battery_import_revenue(time)
        results.set_tnsp_total_revenue(time, tnsp_total_revenue)
    # --------------------------------------------------------------
    # NUOS financial calcs - NOTE this is not paid to a specific entity as NUOS = DUOS + TUOS + green schemes
    # --------------------------------------------------------------
    if status_callback:
        status_callback('Calculating NUOS Finances:0%')
        percent_finished = 0
        single_step_percent = 100.0 / float(len(time_periods) * len(mynetwork.get_participants()))
    # Initialise df used in demand tariff calcs (stores max demand values)      
    df_participant_max_monthly_demand = pd.DataFrame(0, index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]) 


    for p in mynetwork.get_participants():
        # Initialise params used in demand tariff calcs
        max_demand = 0
        max_demand_time = time_periods[0]
        previous_month = time_periods[0].month

        for time in time_periods:
            # Update callback status
            if status_callback:
                percent_finished += single_step_percent
                status_callback('Calculating NUOS Finances: '+str(round(percent_finished))+"%")       

            # Required energy flows for retailer / DNSP / TNSP calcs
            gross_participant_grid_import = results.get_gross_participant_grid_import(time)
            gross_participant_local_solar_import = results.get_gross_participant_local_solar_import(time)
            gross_participant_central_battery_import = results.get_gross_participant_central_battery_import(time)

            # Financial calcs for NUOS
            # Fixed charges revenue is the fixed charge times by the number of customers paying this charge

            results.set_nuos_grid_import_revenue_fixed(time, my_tariffs.get_nuos_on_grid_import_fixed(TIME_PERIOD_LENGTH_MINS, network_tariff_type) * len(mynetwork.get_participants()))
            results.set_nuos_local_solar_import_revenue(time, my_tariffs.get_nuos_on_local_solar_import(time, network_tariff_type) * gross_participant_local_solar_import)
            results.set_nuos_central_battery_import_revenue(time, my_tariffs.get_nuos_on_central_batt_import(time, network_tariff_type) * gross_participant_central_battery_import)

            # Variable component - will need to be the sum of each individual participant's NUOS payment because each may be on a different tariff.
            
            network_tariff_type = p.get_network_tariff_type()

            # Left over load which requires grid import. Calculated in energy flows above.
            external_grid_import = results.get_external_grid_elec_import(time, p.get_id())

            # Controlled Load and Flat Tariffs ---------------
            # The controlled load tariffs and the flat tariff will be applied simply as the tariff times by the volume of electricity consumed, so the same calculation is applied.
            # if network_tariff_type == 'Controlled Load 1' or network_tariff_type == 'Controlled Load 2' or network_tariff_type == 'LV Small Business Anytime':
            #     variable_tariff = my_tariffs.get_nuos_on_grid_import_variable(time, network_tariff_type)
            #     results.set_participant_nuos_payments(time, p.get_id(), variable_tariff * external_grid_import)

            # TOU Tariffs ---------------
            # The TOU tariffs will be applied by using if statements to determine whether peak/shoulder/off-peak
            # if network_tariff_type == 'LV TOU <100MWh' or network_tariff_type == 'LV Business TOU_Interval meter' or network_tariff_type == 'Small Business - Opt in Demand':
            if 'TOU' in network_tariff_type:
                peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag, demand_charge = my_tariffs.get_nuos_on_grid_import_variable(time,network_tariff_type)

                # If the TOU periods apply all days and not just weekdays then the flag will be zero
                if tou_weekday_only_flag == 0 :
                    # Check for whether it's a peak time
                    if (time.hour > peak_start_time and time.hour <= peak_end_time) or (time.hour > peak_start_time_2 and time.hour <= peak_end_time_2) :
                        variable_tariff = peak_charge
                    # If not, check whether it's shoulder time
                    elif (time.hour > shoulder_start_time and time.hour <= shoulder_end_time) or (time.hour > shoulder_start_time_2 and time.hour <= shoulder_end_time_2) :
                        variable_tariff = shoulder_charge

                # In the case where TOU periods only apply on weekdays then check for weekdays and apply the same logic as above.
                elif tou_weekday_only_flag == 1 and (time.weekday() >= 0 and time.weekday() <=4) :
                    if (time.hour > peak_start_time and time.hour <= peak_end_time) or (time.hour > peak_start_time_2 and time.hour <= peak_end_time_2) :
                        variable_tariff = peak_charge
                    elif (time.hour > shoulder_start_time and time.hour <= shoulder_end_time) or (time.hour > shoulder_start_time_2 and time.hour <= shoulder_end_time_2) :
                        variable_tariff = shoulder_charge

                # Else assume it's off-peak time
                else:
                    variable_tariff = offpeak_charge
                # Apply the tariff 
                results.set_participant_nuos_payments(time, p.get_id(), variable_tariff * external_grid_import)
            
            # Demand tariff includes TOU component which is handled above. In addition, the demand component is calculated for each participant
            # if network_tariff_type == 'Small Business - Opt in Demand' :
            if 'Demand' in network_tariff_type:
                current_month = time.month
                
                # If it's a new month, then print the max demand value to the df at the max demand time, reset the max demand to zero and set the month to the new month.
                if current_month != previous_month:
                    # Print to df in units of power (kVA, assume unity pf)
                    df_participant_max_monthly_demand.loc[max_demand_time, p.get_id()] = max_demand * (60/TIME_PERIOD_LENGTH_MINS)
                    max_demand = 0
                    previous_month = current_month

                # Left over load which requires grid import. Calculated in energy flows above.
                external_grid_import = results.get_external_grid_elec_import(time, p.get_id())
                
                # If the load in this period is greater than the currently recorded max demand then update max demand and max demand time
                if external_grid_import > max_demand :
                    max_demand = external_grid_import
                    max_demand_time = time

                # In the case where there is less than 1 month of data (i.e. start and end months are the same) AND the loop is on the final time period, then print max to df.
                if time_periods[0].month == time_periods[-1].month and time == time_periods[-1] :
                    # Print to df in units of power (kVA, assume unity pf)
                    df_participant_max_monthly_demand.loc[max_demand_time, p.get_id()] = max_demand * (60/TIME_PERIOD_LENGTH_MINS)
        
        # After looping through all time periods for the current participant
        # if network_tariff_type == 'Small Business - Opt in Demand' :
        if 'Demand' in network_tariff_type:
            # Need a separate time loop to calculate demand charges since the max kVA values are entered into the df 'retrospectively'
            for time in time_periods:
                demand_payment = df_participant_max_monthly_demand.loc[time, p.get_id()] * demand_charge
                new_nuos_payment = results.get_participant_nuos_payments(time, p.get_id()) + demand_payment
                results.set_participant_nuos_payments(time, p.get_id(), new_nuos_payment)
    
    # Finally, calculate the sum across participants to find the total variable NUOS revenue. Then calculate the total NUOS revenue (i.e. including fixed charges etc).
    nuos_grid_import_revenue_variable = sum( [results.get_participant_nuos_payments(time, participant.get_id()) for participant in mynetwork.get_participants()] )
    results.set_nuos_grid_import_revenue_variable(time, nuos_grid_import_revenue_variable)
    # Sum across columns for total nuos revenue 
    for time in time_periods:    
        nuos_total_revenue = results.get_nuos_grid_import_revenue_fixed(time) + results.get_nuos_grid_import_revenue_variable(time) + results.get_nuos_local_solar_import_revenue(time) + results.get_nuos_central_battery_import_revenue(time)
        results.set_nuos_total_revenue(time, nuos_total_revenue)


    # --------------------------------------------------------------
    # Retailer financial calcs
    # --------------------------------------------------------------
    if status_callback:
        status_callback('Calculating Retail Finances')
    for time in time_periods:
        # print "Financial", time
        # Fixed charges revenue is the fixed charge times by the number of customers paying this charge
        # TODO - check whether .sum() is working as expected! See test file.
       
        
        total_variable = sum([results.get_participant_variable_charge(time, p.get_id()) for p in mynetwork.get_participants()])
        total_fixed = sum([my_tariffs.get_fixed_tariff(TIME_PERIOD_LENGTH_MINS, p.get_retail_tariff_type()) for p in mynetwork.get_participants()])
        total_local_solar = sum([results.get_local_solar_import(time, p.get_id()) * my_tariffs.get_retail_income_on_local_solar_import(time) for p in mynetwork.get_participants()])
        total_fit_payments = sum([results.get_export_to_grid_solar_sales_revenue(time, p.get_id()) for p in mynetwork.get_participants()])

        results.set_retailer_grid_import_revenue_fixed(time, total_fixed)
        results.set_retailer_grid_import_revenue_variable(time, total_variable)
        results.set_retailer_local_solar_import_revenue(time, total_local_solar)
        results.set_retailer_central_battery_import_revenue(time, my_tariffs.get_retail_income_on_central_batt_import(time) * gross_participant_central_battery_import)
        total_retailer_revenue = results.get_retailer_grid_import_revenue_fixed(time) + results.get_retailer_grid_import_revenue_variable(time) + results.get_retailer_local_solar_import_revenue(time) + results.get_retailer_central_battery_import_revenue(time)
        results.set_retailer_total_revenue(time, total_retailer_revenue)
        results.set_retailer_solar_fit_payments(time, total_fit_payments)

        # Central Battery revenue
        # Energy imported by the battery
        battery_import = sum([results.get_central_batt_solar_sales(time, participant.get_id()) for participant in mynetwork.get_participants()])
        # Energy exported by the battery
        # TODO - will need to update thif is the battery can also import from the grid.
        battery_export = sum([results.get_participant_central_batt_import(time, participant.get_id()) for participant in mynetwork.get_participants()])
        # Calculate income for battery which is export(kWh) * export tariff for energy paid by consumer (c/kWh) minus import (kWh) * import tariff for energy paid by battery (c/kWh, includes energy,retail,NUOS)
        central_battery_revenue = battery_export * my_tariffs.get_central_batt_buy_tariff(time) - battery_import * my_tariffs.get_total_central_battery_import_tariff(time)
        results.set_central_battery_revenue(time, central_battery_revenue)


