import sys
import numpy as np
import pandas as pd


class Tariff:
    def __init__(self,
                 tariff_id,
                 scenario):

        self.study = scenario.get_study()
        self.ts = scenario.get_timeseries()

        """Create time-based rates for single specific tariff."""
        if tariff_id not in scenario.tariff_lookup.index:
            msg = '******Exception: Tariff ' + tariff_id + ' is not in tariff_lookup.csv'
            exit(msg)

        # ------------------------------
        # Export Tariff and Fixed Charge
        # ------------------------------
        self.export_tariff = (scenario.static_exports[tariff_id]).values  # NB assumes FiTs are fixed
        self.fixed_charge = scenario.tariff_lookup.loc[tariff_id, 'daily_fixed_rate']
        # Add in Metering Service Charge for network and combined tariffs:
        self.tariff_type = scenario.tariff_lookup.loc[tariff_id, 'tariff_type']
        self.fixed_charge += \
            scenario.tariff_lookup['metering_sc_non_cap'].fillna(0).loc[tariff_id]
        # scenario.tariff_lookup['metering_sc_cap'].fillna(0).loc[tariff_id]
        # NB Capital component of MSC does not apply as meter capital costs included in en_capex

        # Dynamic (Block) Tariff
        # ----------------------
        if tariff_id in scenario.dynamic_list:
            self.is_dynamic = True
            self.block_rate_1 = scenario.tariff_lookup.loc[tariff_id, 'block_rate_1']
            self.block_rate_2 = scenario.tariff_lookup.loc[tariff_id, 'block_rate_2']
            self.block_rate_3 = scenario.tariff_lookup.loc[tariff_id, 'block_rate_3']
            self.high_1 = scenario.tariff_lookup.loc[tariff_id, 'high_1']
            self.high_2 = scenario.tariff_lookup.loc[tariff_id, 'high_2']
            if self.high_1 > 0 and not self.block_rate_2 > 0:
                sys.exit('missing block tariff data')
            if self.high_2 > 0 and not self.block_rate_3 > 0:
                sys.exit('missing block tariff data')

            if self.tariff_type == 'Block_Quarterly':
                self.block_billing_start = 0  # timestep to start cumulative energy calc
                self.steps_in_block = 4380  # quarterly half-hour steps
        else:
            self.is_dynamic = False
        # -------------
        # Demand Tariff
        # -------------
        if tariff_id in scenario.demand_list:
            self.is_demand = True
            self.demand_type = scenario.tariff_lookup.loc[tariff_id, 'demand_type']
            # Demand period is weekday or weekend between demand_start and demand_end
            # with dst applied to start and end times during summer
            # Assume that demand_end > demand_start
            # (ie period does not cross midnight but can be 00:00 to 23:59)
            winter_days_affected = self.ts.days[scenario.tariff_lookup.loc[tariff_id, 'demand_week']].join(
                self.ts.seasonal_time['winter'], 'inner')
            summer_days_affected = self.ts.days[scenario.tariff_lookup.loc[tariff_id, 'demand_week']].join(
                self.ts.seasonal_time['summer'], 'inner')
            if pd.Timestamp(scenario.tariff_lookup.loc[tariff_id, 'demand_start']).time() > \
                    pd.Timestamp(self.study.tariff_data.lookup.loc[tariff_id, 'demand_end']).time():
                # winter period crosses midnight
                winter_period = \
                    winter_days_affected[
                        (winter_days_affected.time >= pd.Timestamp(
                            scenario.tariff_lookup.loc[tariff_id, 'demand_start']).time())
                        & (winter_days_affected.time < pd.Timestamp('23:59').time())].append(
                        winter_days_affected[
                            (winter_days_affected.time >= pd.Timestamp('0:00').time())
                            & (winter_days_affected.time < pd.Timestamp(
                                self.study.tariff_data.lookup.loc[tariff_id, 'demand_end']).time())])
            else:
                winter_period = \
                    winter_days_affected[
                        (winter_days_affected.time >= pd.Timestamp(
                            scenario.tariff_lookup.loc[tariff_id, 'demand_start']).time())
                        & (winter_days_affected.time < pd.Timestamp(
                            self.study.tariff_data.lookup.loc[tariff_id, 'demand_end']).time())]

            if (pd.Timestamp(scenario.tariff_lookup.loc[tariff_id, 'demand_start']) + self.ts.dst_reverse_shift).time() > \
                    (pd.Timestamp(self.study.tariff_data.lookup.loc[tariff_id, 'demand_end']) + self.ts.dst_reverse_shift).time():
                # summer period crosses midnight
                summer_period = \
                    summer_days_affected[
                        (summer_days_affected.time >= (pd.Timestamp(
                            scenario.tariff_lookup.loc[tariff_id, 'demand_start']) + self.ts.dst_reverse_shift).time())
                        & (summer_days_affected.time < pd.Timestamp('23:59').time())].append(
                        summer_days_affected[
                            (summer_days_affected.time >= pd.Timestamp('0:00').time())
                            & (summer_days_affected.time < (pd.Timestamp(
                                self.study.tariff_data.lookup.loc[tariff_id, 'demand_end']) + self.ts.dst_reverse_shift).time())])
            else:
                summer_period = \
                    summer_days_affected[
                        (summer_days_affected.time >= (pd.Timestamp(
                            scenario.tariff_lookup.loc[tariff_id, 'demand_start']) + self.ts.dst_reverse_shift).time())
                        & (summer_days_affected.time < (pd.Timestamp(
                            self.study.tariff_data.lookup.loc[tariff_id, 'demand_end']) + self.ts.dst_reverse_shift).time())]
            self.demand_period = winter_period.join(summer_period, 'outer').sort_values()

            s = pd.Series(0, index=self.ts.timeseries)
            s[self.demand_period] = 1
            self.demand_period_array = np.array(s)
            self.assumed_pf = 1.0  ##   For kVA demand charges, What is good assumption for this????
            self.demand_tariff = scenario.tariff_lookup.loc[tariff_id, 'demand_tariff']
        else:
            self.is_demand = False
        # ------------------------------------------------------
        # Solar tariff periods and rates (block or instantaneous)
        # ------------------------------------------------------
        if tariff_id in scenario.solar_inst_list:
            self.is_solar_inst = True
        else:
            self.is_solar_inst = False

        # # Get solar tariff data:
        # SOLAR BLOCK TARIFF IMPLEMENTATION INCORRECT - REMOVED
        # # NB solar block tariff period is NOT adjusted for DST
        if tariff_id in scenario.solar_list:
            #     for name, parameter in study.tariff_data.tou_rate_list.items():
            #         if not pd.isnull(study.tariff_data.lookup.loc[tariff_id, name]):
            #             if any(s in study.tariff_data.lookup.loc[tariff_id, name] for s in ['solar','Solar']):
            #                 self.solar_rate_name = study.tariff_data.lookup.loc[tariff_id, name]
            #                 winter_days_affected = ts.days[scenario.tariff_lookup.loc[tariff_id, parameter[3]]].join(  # [3] is week_
            #                     ts.seasonal_time['winter'], 'inner')
            #                 summer_days_affected = ts.days[scenario.tariff_lookup.loc[tariff_id, parameter[3]]].join(  # [3] is week_
            #                     ts.seasonal_time['summer'], 'inner')
            #
            #                 if pd.Timestamp(scenario.tariff_lookup.loc[tariff_id, parameter[1]]).time() > \
            #                         pd.Timestamp(scenario.tariff_lookup.loc[tariff_id, parameter[2]]).time():
            #                     # winter tariff period crosses midnight:
            #                     winter_period = \
            #                         winter_days_affected[
            #                             (winter_days_affected.time >= pd.Timestamp(
            #                                 scenario.tariff_lookup.loc[tariff_id, parameter[1]]).time())  # [1] is start
            #                             & (winter_days_affected.time < pd.Timestamp('23:59').time())].append(
            #                         winter_days_affected[
            #                                 (winter_days_affected.time >= pd.Timestamp('0:00').time())
            #                             & (winter_days_affected.time < pd.Timestamp(
            #                                 scenario.tariff_lookup.loc[tariff_id, parameter[2]]).time())])  # [2] is end_
            #                 else:
            #                     # winter tariff period doesn't cross midnight:
            #                     winter_period = \
            #                         winter_days_affected[
            #                             (winter_days_affected.time >= pd.Timestamp(
            #                                 scenario.tariff_lookup.loc[tariff_id, parameter[1]]).time())  # [1] is start
            #                             & (winter_days_affected.time < pd.Timestamp(
            #                                 scenario.tariff_lookup.loc[tariff_id, parameter[2]]).time())]  # [2] is end_
            #
            #                 if (pd.Timestamp(scenario.tariff_lookup.loc[tariff_id, parameter[1]]) ).time() > \
            #                         (pd.Timestamp(scenario.tariff_lookup.loc[tariff_id, parameter[2]]) ).time():
            #                     # summer tariff period crosses midnight:
            #                     summer_period = \
            #                         summer_days_affected[
            #                             (summer_days_affected.time >= (pd.Timestamp(
            #                                 scenario.tariff_lookup.loc[
            #                                     tariff_id, parameter[1]])).time())  # [1] is start
            #                             & (summer_days_affected.time < pd.Timestamp('23:59').time())].append(  # [2] is end_
            #                         summer_days_affected[
            #                             (summer_days_affected.time >= pd.Timestamp('0:00').time())  # [1] is start
            #                             & (summer_days_affected.time < (pd.Timestamp(
            #                                 scenario.tariff_lookup.loc[
            #                                     tariff_id, parameter[2]]) ).time())])  # [2] is end_
            #                 else:
            #                     # summer tariff period doesn't cross midnight:
            #                     summer_period = \
            #                     summer_days_affected[
            #                         (summer_days_affected.time >= (pd.Timestamp(
            #                             scenario.tariff_lookup.loc[tariff_id, parameter[1]]) ).time())  # [1] is start
            #                         & (summer_days_affected.time < (pd.Timestamp(
            #                             scenario.tariff_lookup.loc[tariff_id, parameter[2]])).time())]  # [2] is end_
            #
            #                 # solar_period, solar_rate and solar_cp_allocation are for solar block tariffs:
            #                 # ie fixed quotas with dynamic load-dependent calculation
            #                 self.solar_period = winter_period.join(summer_period, 'outer').sort_values()
            #                 self.solar_rate = scenario.tariff_lookup.loc[tariff_id, parameter[0]]  # rate_
            #                 self.solar_cp_allocation = scenario.tariff_lookup['solar_cp_allocation'].fillna(0).loc[tariff_id] # % of total solar generation allocated to cp
            # Solar import tariff is static TOU tariff for instantaneous solar quota
            self.solar_import_tariff = (scenario.static_solar_imports[tariff_id]).values
            pass
        else:
            self.solar_import_tariff = np.zeros(self.ts.num_steps)
            self.solar_rate_name = ''
        # -----------------------------
        # All volumetric import tariffs
        # -----------------------------
        # initialise to zero if dynamically calculated, e.g block tariff,
        # otherwise copy from scenario
        if tariff_id not in scenario.dynamic_list:
            self.import_tariff = (scenario.static_imports[tariff_id]).values
        else:
            self.import_tariff = np.zeros(self.ts.num_steps)
