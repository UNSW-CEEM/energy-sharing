import os
import logging
import sys
import pandas as pd
import numpy as np


class Battery:
    # adapted from original script by Luke Marshall
    def __init__(self,
                 scenario,
                 battery_id,
                 battery_strategy,
                 battery_capacity):

        self.battery_id = battery_id
        self.scenario = scenario
        self.study = scenario.get_study()
        self.ts = scenario.get_timeseries()

        if battery_id not in self.study.battery_lookup.index:
            logging.info("battery-id %s is not in battery_lookup.csv :", battery_id)
            sys.exit("battery-id %s is not in battery_lookup.csv :", battery_id)
        else:
            # Load battery parameters from battery_lookup
            # -------------------------------------------
            self.capacity_kWh = self.study.battery_lookup.loc[battery_id, 'capacity_kWh']
            self.max_charge_kW = self.study.battery_lookup.loc[battery_id, 'max_charge_kW']
            self.efficiency_cycle = self.study.battery_lookup.loc[battery_id, 'efficiency_cycle']
            if self.efficiency_cycle > 1.0:
                logging.info('***************Exception!!! Battery Efficiency must be < 1.0*******')
                print('***************Exception!!! Battery Efficiency must be < 1.0*******')
                sys.exit("Battery Efficiency > 1")
            self.maxDOD = self.study.battery_lookup.loc[battery_id, 'maxDOD']
            self.maxSOC = self.study.battery_lookup.loc[battery_id, 'maxSOC']
            if self.maxDOD + self.maxSOC <= 1.0:
                logging.info('***************Exception!!! Battery maxSOC + maxDOD >= 1.0 *******')
                print('***************Exception!!! Battery maxSOC + maxDOD <= 1.0*******')
                sys.exit("Battery maxDOD + maxSOC  <= 1")
            self.battery_cost = self.study.battery_lookup.loc[battery_id, 'battery_cost']
            self.battery_inv_cost = self.study.battery_lookup.loc[battery_id, 'battery_inv_cost']
            if np.isnan(self.study.battery_lookup.loc[battery_id, 'life_bat_inv']):
                self.life_bat_inv = scenario.a_term
            else:
                self.life_bat_inv = self.study.battery_lookup.loc[battery_id, 'life_bat_inv']
            self.battery_life_years = self.study.battery_lookup.loc[battery_id, 'battery_life_years']
            self.max_cycles = self.study.battery_lookup.loc[battery_id, 'max_cycles']

            # Scalable Battery
            # ----------------
            # details in `battery_lookup` are for 1kWh and this is scaled by capacity in `study_parameters`
            if any(word in self.battery_id for word in ['scale', 'scalable']):
                self.capacity_kWh = self.capacity_kWh * battery_capacity
                self.max_charge_kW = self.max_charge_kW * battery_capacity

            # Use default values if missing:
            # ------------------------------
            if pd.isnull(self.max_charge_kW):
                self.max_charge_kW = self.capacity_kWh * 0.5
            if pd.isnull(self.maxDOD):
                self.maxDOD = 0.8
            if pd.isnull(self.maxSOC):
                self.maxSOC = 1.0
            if pd.isnull(self.efficiency_cycle):
                self.efficiency_cycle = 0.95
            if pd.isnull(self.max_cycles):
                self.max_cycles = 2000
            if pd.isnull(self.battery_cost):
                self.battery_cost = 0.0
            if pd.isnull(self.battery_inv_cost):
                self.battery_inv_cost = 0.0

            # Define battery charging and discharging strategy
            # ------------------------------------------------
            # strategy that prioritises using PV to charg over onsite load:
            if 'prioritise_battery' in self.study.battery_strategies.columns:
                self.prioritise_battery = self.study.battery_strategies.fillna(False).loc[
                    battery_strategy, 'prioritise_battery']
            else:
                self.prioritise_battery = False

            # Strategy with different summer / winter charge and discharge periods (DST):
            if 'seasonal_strategy' not in self.study.battery_strategies.columns:
                seasonal_strategy = False
            else:
                seasonal_strategy = self.study.battery_strategies.fillna(False).loc[battery_strategy, 'seasonal_strategy']

            # peak_demand strategy only discharges when net export >= peak_demand_percentage of annual peak load
            if 'peak_demand_percentage' not in self.study.battery_strategies.columns:
                self.peak_demand_percentage = 0
            else:
                self.peak_demand_percentage = self.study.battery_strategies.fillna(0).loc[
                    battery_strategy, 'peak_demand_percentage']

            # Set up restricted discharge period(s) and additional charge period(s)
            # ---------------------------------------------------------------------
            discharge_start1 = self.study.battery_strategies.loc[battery_strategy, 'discharge_start1']
            discharge_end1 = self.study.battery_strategies.loc[battery_strategy, 'discharge_end1']
            discharge_day1 = self.study.battery_strategies.loc[battery_strategy, 'discharge_day1']
            discharge_start2 = self.study.battery_strategies.loc[battery_strategy, 'discharge_start2']
            discharge_end2 = self.study.battery_strategies.loc[battery_strategy, 'discharge_end2']
            discharge_day2 = self.study.battery_strategies.loc[battery_strategy, 'discharge_day2']
            charge_start1 = self.study.battery_strategies.loc[battery_strategy, 'charge_start1']
            charge_end1 = self.study.battery_strategies.loc[battery_strategy, 'charge_end1']
            charge_day1 = self.study.battery_strategies.loc[battery_strategy, 'charge_day1']
            charge_start2 = self.study.battery_strategies.loc[battery_strategy, 'charge_start2']
            charge_end2 = self.study.battery_strategies.loc[battery_strategy, 'charge_end2']
            charge_day2 = self.study.battery_strategies.loc[battery_strategy, 'charge_day2']

            # Calculate discharge and grid-charge period(s):
            # ----------------------------------------------
            # If battery strategy is seasonal, add an hour to summer charge and discharge periods
            
            if seasonal_strategy:
                # If battery strategy is seasonal, add an hour to summer charge and discharge periods
                # discharge_1
                if pd.isnull(discharge_start1):
                    summer_period = pd.DatetimeIndex([])
                    winter_period = pd.DatetimeIndex([])
                elif pd.Timestamp(discharge_start1) > pd.Timestamp(discharge_end1):
                    # winter period crosses midnight
                    weekday_key = discharge_day1
                    winter_days_affected = self.ts.get_seasonal_times('winter', weekday_key)
                    winter_days_affected = pd.DatetimeIndex(data = winter_days_affected)
                    winter_period = \
                        winter_days_affected[
                            (winter_days_affected.time >= pd.Timestamp(discharge_start1).time()) & (
                                    winter_days_affected.time <= pd.Timestamp('23:59').time())].append(
                            winter_days_affected[(winter_days_affected.time >= pd.Timestamp('0:00').time()) & (
                                    winter_days_affected.time < pd.Timestamp(discharge_end1).time())]).sort_values()
                    # summer period crosses midnight
                    summer_days_affected = self.ts.get_seasonal_times('summer', weekday_key)
                    summer_days_affected = pd.DatetimeIndex(data = summer_days_affected)
                   
                    summer_period = \
                        summer_days_affected[
                            (summer_days_affected.time >= (
                                        pd.Timestamp(discharge_start1) + self.ts.dst_reverse_shift).time()) & (
                                    summer_days_affected.time <= pd.Timestamp('23:59').time())].append(
                            summer_days_affected[(summer_days_affected.time >= pd.Timestamp('0:00').time()) & (
                                    summer_days_affected.time < (
                                        pd.Timestamp(discharge_end1) + self.ts.dst_reverse_shift).time())]).sort_values()
                else:
                    # winter_period doesn't cross midnight
                    weekday_key = discharge_day1
                    winter_days_affected = self.ts.get_seasonal_times('winter', weekday_key)
                    winter_days_affected = pd.DatetimeIndex(data = winter_days_affected)
                    
                    winter_period = \
                        winter_days_affected[(winter_days_affected.time >= pd.Timestamp(discharge_start1).time())
                                             & (winter_days_affected.time < pd.Timestamp(discharge_end1).time())]
                    # summer_period doesn't cross midnight
                    summer_days_affected = self.ts.get_seasonal_times('summer', weekday_key)
                    summer_days_affected = pd.DatetimeIndex(data=summer_days_affected)
                    
                    summer_period = \
                        summer_days_affected[(summer_days_affected.time >= (
                                    pd.Timestamp(discharge_start1) + self.ts.dst_reverse_shift).time())
                                             & (summer_days_affected.time < (
                                    pd.Timestamp(discharge_end1) + self.ts.dst_reverse_shift).time())]
                discharge_period1 = winter_period.join(summer_period, 'outer').sort_values()

                # discharge_2
                if pd.isnull(discharge_start2):
                    summer_period = pd.DatetimeIndex([])
                    winter_period = pd.DatetimeIndex([])
                elif pd.Timestamp(discharge_start2) > pd.Timestamp(discharge_end2):
                    # winter period crosses midnight
                    weekday_key = discharge_day2
                    winter_days_affected = self.ts.get_seasonal_times('winter', weekday_key)
                    winter_days_affected = pd.DatetimeIndex(data = winter_days_affected)
                    
                    winter_period = \
                        winter_days_affected[
                            (winter_days_affected.time >= pd.Timestamp(discharge_start2).time()) & (
                                    winter_days_affected.time <= pd.Timestamp('23:59').time())].append(
                            winter_days_affected[(winter_days_affected.time >= pd.Timestamp('0:00').time()) & (
                                    winter_days_affected.time < pd.Timestamp(discharge_end2).time())]).sort_values()
                    # summer period crosses midnight
                    summer_days_affected = self.ts.get_seasonal_times('summer', weekday_key)
                    summer_days_affected = pd.DatetimeIndex(data=summer_days_affected)
                    
                    summer_period = \
                        summer_days_affected[
                            (summer_days_affected.time >= (
                                        pd.Timestamp(discharge_start2) + self.ts.dst_reverse_shift).time()) & (
                                    summer_days_affected.time <= pd.Timestamp('23:59').time())].append(
                            summer_days_affected[(summer_days_affected.time >= pd.Timestamp('0:00').time()) & (
                                    summer_days_affected.time < (
                                        pd.Timestamp(discharge_end2) + self.ts.dst_reverse_shift).time())]).sort_values()
                else:
                    # winter_period doesn't cross midnight
                    weekday_key = discharge_day2
                    winter_days_affected = self.ts.get_seasonal_times('winter', weekday_key)
                    winter_days_affected = pd.DatetimeIndex(data = winter_days_affected)
                    
                    winter_period = \
                        winter_days_affected[(winter_days_affected.time >= pd.Timestamp(discharge_start2).time())
                                             & (winter_days_affected.time < pd.Timestamp(discharge_end2).time())]
                    # summer_period doesn't cross midnight
                    summer_days_affected = self.ts.get_seasonal_times('summer', weekday_key)
                    summer_days_affected = pd.DatetimeIndex(data=summer_days_affected)
                    
                    summer_period = \
                        summer_days_affected[(summer_days_affected.time >= (
                                    pd.Timestamp(discharge_start2) + self.ts.dst_reverse_shift).time())
                                             & (summer_days_affected.time < (
                                    pd.Timestamp(discharge_end2) + self.ts.dst_reverse_shift).time())]
                discharge_period2 = winter_period.join(summer_period, 'outer').sort_values()

                # charge_1
                if pd.isnull(charge_start1):
                    summer_period = pd.DatetimeIndex([])
                    winter_period = pd.DatetimeIndex([])
                elif pd.Timestamp(charge_start1) > pd.Timestamp(charge_end1):
                    # winter period crosses midnight
                    weekday_key = charge_day1
                    winter_days_affected = self.ts.get_seasonal_times('winter', weekday_key)
                    winter_days_affected = pd.DatetimeIndex(data = winter_days_affected)
                    
                    winter_period = \
                        winter_days_affected[
                            (winter_days_affected.time >= pd.Timestamp(charge_start1).time()) & (
                                    winter_days_affected.time <= pd.Timestamp('23:59').time())].append(
                            winter_days_affected[(winter_days_affected.time >= pd.Timestamp('0:00').time()) & (
                                    winter_days_affected.time < pd.Timestamp(charge_end1).time())]).sort_values()
                    # summer period crosses midnight
                    summer_days_affected = self.ts.get_seasonal_times('summer', weekday_key)
                    summer_days_affected = pd.DatetimeIndex(data=summer_days_affected)
                    
                    summer_period = \
                        summer_days_affected[
                            (summer_days_affected.time >= (
                                        pd.Timestamp(charge_start1) + self.ts.dst_reverse_shift).time()) & (
                                    summer_days_affected.time <= pd.Timestamp('23:59').time())].append(
                            summer_days_affected[(summer_days_affected.time >= pd.Timestamp('0:00').time()) & (
                                    summer_days_affected.time < (
                                        pd.Timestamp(charge_end1) + self.ts.dst_reverse_shift).time())]).sort_values()
                else:
                    # winter_period doesn't cross midnight
                    weekday_key = charge_day1
                    winter_days_affected = self.ts.get_seasonal_times('winter', weekday_key)
                    winter_days_affected = pd.DatetimeIndex(data = winter_days_affected)
                    
                    winter_period = \
                        winter_days_affected[(winter_days_affected.time >= pd.Timestamp(charge_start1).time())
                                             & (winter_days_affected.time < pd.Timestamp(charge_end1).time())]
                    # summer_period doesn't cross midnight
                    summer_days_affected = self.ts.get_seasonal_times('summer', weekday_key)
                    summer_days_affected = pd.DatetimeIndex(data=summer_days_affected)

                    summer_period = \
                        summer_days_affected[
                            (summer_days_affected.time >= (pd.Timestamp(charge_start1) + self.ts.dst_reverse_shift).time())
                            & (summer_days_affected.time < (pd.Timestamp(charge_end1) + self.ts.dst_reverse_shift).time())]
                charge_period1 = winter_period.join(summer_period, 'outer').sort_values()

                # charge_2
                if pd.isnull(charge_start2):
                    summer_period = pd.DatetimeIndex([])
                    winter_period = pd.DatetimeIndex([])
                elif pd.Timestamp(charge_start2) > pd.Timestamp(charge_end2):
                    # winter period crosses midnight
                    weekday_key = charge_day2
                    winter_days_affected = self.ts.get_seasonal_times('winter', weekday_key)
                    winter_days_affected = pd.DatetimeIndex(data = winter_days_affected)
                    
                    winter_period = \
                        winter_days_affected[
                            (winter_days_affected.time >= pd.Timestamp(charge_start2).time()) & (
                                    winter_days_affected.time <= pd.Timestamp('23:59').time())].append(
                            winter_days_affected[(winter_days_affected.time >= pd.Timestamp('0:00').time()) & (
                                    winter_days_affected.time < pd.Timestamp(charge_end2).time())]).sort_values()
                    # summer period crosses midnight
                    summer_days_affected = self.ts.get_seasonal_times('summer', weekday_key)
                    summer_days_affected = pd.DatetimeIndex(data=summer_days_affected)
                    
                    summer_period = \
                        summer_days_affected[
                            (summer_days_affected.time >= (
                                        pd.Timestamp(charge_start2) + self.ts.dst_reverse_shift).time()) & (
                                    summer_days_affected.time <= pd.Timestamp('23:59').time())].append(
                            summer_days_affected[(summer_days_affected.time >= pd.Timestamp('0:00').time()) & (
                                    summer_days_affected.time < (
                                        pd.Timestamp(charge_end2) + self.ts.dst_reverse_shift).time())]).sort_values()
                else:
                    # winter_period doesn't cross midnight
                    weekday_key = charge_day2
                    winter_days_affected = self.ts.get_seasonal_times('winter', weekday_key)
                    winter_days_affected = pd.DatetimeIndex(data = winter_days_affected)
                    
                    winter_period = \
                        winter_days_affected[(winter_days_affected.time >= pd.Timestamp(charge_start2).time())
                                             & (winter_days_affected.time < pd.Timestamp(charge_end2).time())]
                    # summer_period doesn't cross midnight
                    summer_days_affected = self.ts.get_seasonal_times('summer', weekday_key)
                    summer_days_affected = pd.DatetimeIndex(data=summer_days_affected)
                    summer_period = \
                        summer_days_affected[
                            (summer_days_affected.time >= (pd.Timestamp(charge_start2) + self.ts.dst_reverse_shift).time())
                            & (summer_days_affected.time < (pd.Timestamp(charge_end2) + self.ts.dst_reverse_shift).time())]
                charge_period2 = winter_period.join(summer_period, 'outer').sort_values()

            else:
                # If non-seasonal battery , use same periods for whole year:
                # discharge_1
                if pd.isnull(discharge_start1):
                    discharge_period1 = pd.DatetimeIndex([])
                elif pd.Timestamp(discharge_start1) > pd.Timestamp(discharge_end1):
                    weekday_key = discharge_day1
                    discharge_period1 = (
                        self.ts.days[weekday_key][(self.ts.days[weekday_key].time >= pd.Timestamp(discharge_start1).time()) & (
                                self.ts.days[weekday_key].time <= pd.Timestamp('23:59').time())].append(
                            self.ts.days[weekday_key][(self.ts.days[weekday_key].time >= pd.Timestamp('0:00').time()) & (
                                    self.ts.days[weekday_key].time < pd.Timestamp(discharge_end1).time())])).sort_values()
                else:
                    weekday_key = discharge_day1
                    discharge_period1 = \
                        self.ts.days[weekday_key][(self.ts.days[weekday_key].time >= pd.Timestamp(discharge_start1).time())
                                                & (self.ts.days[weekday_key].time < pd.Timestamp(discharge_end1).time())]
                # discharge_2
                if pd.isnull(discharge_start2):
                    discharge_period2 = pd.DatetimeIndex([])
                elif pd.Timestamp(discharge_start2) > pd.Timestamp(discharge_end2):
                    weekday_key = discharge_day2
                    discharge_period2 = (
                        self.ts.days[weekday_key][
                            (self.ts.days[weekday_key].time >= pd.Timestamp(discharge_start2).time()) & (
                                    self.ts.days[weekday_key].time <= pd.Timestamp('23:59').time())].append(
                            self.ts.days[weekday_key][(self.ts.days[weekday_key].time >= pd.Timestamp('0:00').time()) & (
                                    self.ts.days[weekday_key].time < pd.Timestamp(discharge_end2).time())])).sort_values()
                else:
                    weekday_key = discharge_day2
                    discharge_period2 = \
                        self.ts.days[weekday_key][(self.ts.days[weekday_key].time >= pd.Timestamp(discharge_start2).time())
                                                & (self.ts.days[weekday_key].time < pd.Timestamp(discharge_end2).time())]
                # charge_1
                if pd.isnull(charge_start1):
                    charge_period1 = pd.DatetimeIndex([])
                elif pd.Timestamp(charge_start1) > pd.Timestamp(charge_end1):
                    weekday_key = charge_day1
                    charge_period1 = (
                        self.ts.days[weekday_key][(self.ts.days[weekday_key].time >= pd.Timestamp(charge_start1).time()) & (
                                self.ts.days[weekday_key].time <= pd.Timestamp('23:59').time())].append(
                            self.ts.days[weekday_key][(self.ts.days[weekday_key].time >= pd.Timestamp('0:00').time()) & (
                                    self.ts.days[weekday_key].time < pd.Timestamp(charge_end1).time())])).sort_values()
                else:
                    weekday_key = charge_day1
                    charge_period1 = \
                        self.ts.days[weekday_key][(self.ts.days[weekday_key].time >= pd.Timestamp(charge_start1).time())
                                             & (self.ts.days[weekday_key].time < pd.Timestamp(charge_end1).time())]
                # charge_2
                if pd.isnull(charge_start2):
                    charge_period2 = pd.DatetimeIndex([])
                elif pd.Timestamp(charge_start2) > pd.Timestamp(charge_end2):
                    weekday_key = charge_day2
                    charge_period2 = (
                        self.ts.days[weekday_key][(self.ts.days[weekday_key].time >= pd.Timestamp(charge_start2).time()) & (
                                self.ts.days[weekday_key].time <= pd.Timestamp('23:59').time())].append(
                            self.ts.days[weekday_key][(self.ts.days[weekday_key].time >= pd.Timestamp('0:00').time()) & (
                                    self.ts.days[weekday_key].time < pd.Timestamp(charge_end2).time())])).sort_values()
                else:
                    weekday_key = charge_day2
                    charge_period2 = \
                        self.ts.days[weekday_key][(self.ts.days[weekday_key].time >= pd.Timestamp(charge_start2).time())
                                             & (self.ts.days[weekday_key].time < pd.Timestamp(charge_end2).time())]

            # Combine multiple charge and discharge periods:
            # ---------------------------------------------
            self.discharge_period = discharge_period1.join(discharge_period2, how='outer')
            if len(self.discharge_period) == 0:
                self.discharge_period = pd.DatetimeIndex(data=self.ts.get_date_times())  # if no discharge period set, discharge any time
            self.charge_period = charge_period1.join(charge_period2, how='outer')

            # discharge period as array for calculating peak demand
            # -----------------------------------------------------
            s = pd.Series(0, index=pd.DatetimeIndex(self.ts.get_date_times()))
            s[self.discharge_period] = 1
            self.discharge_period_array = np.array(s)

            # Calculate charge and discharge rates
            # ------------------------------------
            self.charge_rate_kW = self.max_charge_kW
            if 'charge_c_rate' in self.study.battery_strategies.columns:
                if not pd.isnull(self.study.battery_strategies.loc[battery_strategy, 'charge_c_rate']):
                    self.charge_rate_kW = min(self.max_charge_kW, self.study.battery_strategies.loc[
                        battery_strategy, 'charge_c_rate'] * self.capacity_kWh)

            self.discharge_rate_kW = self.max_charge_kW
            if 'discharge_c_rate' in self.study.battery_strategies.columns:
                if not pd.isnull(self.study.battery_strategies.loc[battery_strategy, 'discharge_c_rate']):
                    self.discharge_rate_kW = min(self.max_charge_kW, self.study.battery_strategies.loc[
                        battery_strategy, 'discharge_c_rate'] * self.capacity_kWh)

            # Initialise remaining battery variables
            # --------------------------------------
            self.initial_SOC = 0.5  # BATTERY STARTS AT 50% SOC
            self.charge_level_kWh = self.capacity_kWh * self.initial_SOC
            self.number_cycles = 0
            self.SOH = 100  # State of health
            # Max charge / discharge rate is accepted / delivered energy
            self.max_timestep_delivered = self.discharge_rate_kW * self.ts.interval / 3600
            self.max_timestep_accepted = self.charge_rate_kW * self.ts.interval / 3600
            self.cumulative_losses = 0
            self.net_discharge = np.zeros(
                self.ts.num_steps)  # this is +ve for discharge, -ve for charge. Used for SC and SS calcs

            # Assume losses are all in charging part of cycle:
            # This works if energy capacity is actually "useful discharge capacity"
            # see discussion here: https://electronics.stackexchange.com/questions/379778/how-to-estimate-li-ion-battery-soc/379793?noredirect=1#comment921865_379793
            self.efficiency_charge = self.efficiency_cycle
            self.efficiency_discharge = 1

            # Initialise SOC log
            # ------------------
            self.SOC_log = np.zeros(self.ts.num_steps)

    def reset(self,
              annual_load):  # annual road as np.array
        self.charge_level_kWh = self.capacity_kWh * self.initial_SOC
        self.number_cycles = 0
        self.SOH = 100
        self.SOC_log = np.zeros(self.ts.num_steps)
        self.cumulative_losses = 0
        self.net_discharge = np.zeros(self.ts.num_steps)
        annual_peak_load = np.multiply(annual_load, self.discharge_period_array).max()
        self.peak_demand_threshold = annual_peak_load * self.peak_demand_percentage / 100

    def charge(self, desired_charge):
        amount_to_charge = min((self.capacity_kWh * self.maxSOC - self.charge_level_kWh),
                               self.max_timestep_accepted * self.efficiency_charge,
                               desired_charge * self.efficiency_charge)
        self.charge_level_kWh += amount_to_charge
        energy_accepted = amount_to_charge / self.efficiency_charge
        if amount_to_charge > 0:
            self.number_cycles += 0.5 * amount_to_charge / (self.capacity_kWh * (self.maxSOC - 1 + self.maxDOD))
        self.net_discharge_for_ts = - energy_accepted
        self.cumulative_losses += energy_accepted * (1 - self.efficiency_charge)

        return desired_charge - energy_accepted  # returns unstored portion of energy

    def discharge(self, desired_discharge):
        if self.charge_level_kWh > self.capacity_kWh * (1 - self.maxDOD):
            amount_to_discharge = min(desired_discharge / self.efficiency_discharge,
                                      (self.charge_level_kWh - self.capacity_kWh * (1 - self.maxDOD)),
                                      self.max_timestep_delivered / self.efficiency_discharge)
            self.charge_level_kWh -= amount_to_discharge
            self.number_cycles += 0.5 * amount_to_discharge / (self.capacity_kWh * (self.maxSOC - 1 + self.maxDOD))
        else:
            amount_to_discharge = 0

        energy_delivered = amount_to_discharge * self.efficiency_discharge  # Unneccessary step if losses are all in charge cycle
        self.cumulative_losses += amount_to_discharge * (1 - self.efficiency_discharge)
        self.net_discharge_for_ts = energy_delivered
        return energy_delivered  # returns delivered energy

    def dispatch(self, generation, load, step):
        """Determines charge and discharge of battery at timestep."""
        self.net_discharge_for_ts = 0.0  # reset
        # -------------------------------
        # Make battery control decisions:
        # -------------------------------

        if not self.prioritise_battery:
            # A) Strategy to maximise SC :
            # ---------------------------
            # 1) meet onsite load first:
            # --------------------------
            available_kWh = generation - load
            # 2) Use excess PV to charge
            # --------------------------
            if available_kWh > 0:
                available_kWh = \
                    self.charge(available_kWh)
            # 3) Discharge if needed to meet load, within discharge period
            # ------------------------------------------------------------
            if available_kWh < -self.peak_demand_threshold and self.ts.get_date_times()[step] in self.discharge_period:
                available_kWh += \
                    self.discharge(-available_kWh)
            # 4) Charge from grid in additional charge period:
            # ------------------------------------------------
            if available_kWh <= 0 and self.ts.get_date_times()[step] in self.charge_period:
                available_kWh -= (self.max_timestep_accepted -
                                  self.charge(self.max_timestep_accepted))

        else:
            # B) Strategy to reduce peak demand (apply PV to charge first)
            # -----------------------------------------------------------
            # Within discharge period:
            if self.ts.get_date_times()[step] in self.discharge_period:
                # 1) Apply PV to load
                # -------------------
                available_kWh = generation - load
                # 2) Discharge battery to meet residual load
                # ------------------------------------------
                if available_kWh < -self.peak_demand_threshold:
                    available_kWh += self.discharge(-available_kWh)
                # 3) or use excess PV to charge battery:
                # --------------------------------------
                elif available_kWh > 0:
                    available_kWh = \
                        self.charge(available_kWh)
            else:  # outside discharge period
                # 1) Use PV to charge battery:
                # ----------------------------
                if generation > 0:
                    generation = self.charge(generation)
                # 2) use excess PV to meet load
                available_kWh = generation - load
                # If in grid-charging period, charge from grid
                if available_kWh <= 0 and self.ts.get_date_times()[step] in self.charge_period:
                    available_kWh -= (self.max_timestep_accepted -
                                      self.charge(self.max_timestep_accepted))

        # For monitoring purposes, log battery SOC:
        # -----------------------------------------
        if self.capacity_kWh > 0:
            self.SOC_log[step] = self.charge_level_kWh / self.capacity_kWh * 100

        self.SOH = 100 - (self.number_cycles / self.max_cycles) * 100

        # For SS and SC calcs, log net discharge:
        # ---------------------------------------
        self.net_discharge[step] = self.net_discharge_for_ts

        return available_kWh

    def calcBatCapex(self):
        """Calculates capex for battery"""

        # ---------------------------------------
        # 1) Use 'battery_capex_per_kWh' and scale
        # ---------------------------------------
        # If 'battery_capex_per_kWh' is in the parameter file, it overrides capex info in battery_lookup
        if self.scenario.battery_capex_per_kWh > 0:
            self.battery_cost = self.scenario.battery_capex_per_kWh * self.capacity_kWh
            bat_inv_capex = 0
            # --------------------------------------------
        # 2) Use 'battery_cost' and 'battery_inv_cost'
        # --------------------------------------------
        else:
            # Use capex parameters in battery_lookup.csv :
            # Battery capex includes inverter replacement if amortization period > inverter lifetime
            if self.life_bat_inv < self.scenario.a_term:
                bat_inv_capex = int((float(self.scenario.a_term) / self.life_bat_inv) - 0.001) * self.battery_inv_cost
            else:
                bat_inv_capex = self.battery_inv_cost
        # ---------------------------------------------------------------------
        # For 1) or 2) replace battery (or combined battery-inverter) as needed:
        # ----------------------------------------------------------------------
        # Battery capex includes battery replacement if it exceeds max_cycles
        # or battery_life_years (whichever is sooner) within amortization period

        if np.isnan(self.max_cycles):
            self.max_cycles = 100000
        if np.isnan(self.battery_life_years):
            self.battery_life_years = 1000
        if self.battery_life_years == 0:
            self.battery_life_years = 1000

        if self.number_cycles > 0:
            cycle_life = self.max_cycles / self.number_cycles
        else:
            cycle_life = 1000  # years to reach cycle lifetime
        actual_lifetime = np.min([cycle_life, self.battery_life_years])
        if float(self.scenario.a_term) > actual_lifetime:
            number_batteries = int(float(self.scenario.a_term) / actual_lifetime - 0.01) + 1
            bat_capex = number_batteries * self.battery_cost
        else:
            bat_capex = self.battery_cost
        tot_capex = bat_inv_capex + bat_capex
        return tot_capex