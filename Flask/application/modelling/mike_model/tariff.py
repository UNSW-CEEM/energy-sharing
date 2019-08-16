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
            raise Exception(msg)

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
            weekday_key = scenario.tariff_lookup.loc[tariff_id, 'demand_week']
            winter_days_affected = self.ts.get_seasonal_times('winter', weekday_key)
            winter_days_affected = pd.DatetimeIndex(data = winter_days_affected)

            summer_days_affected = self.ts.get_seasonal_times('summer', weekday_key)
            summer_days_affected = pd.DatetimeIndex(data = summer_days_affected)
            
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

            if (pd.Timestamp(scenario.tariff_lookup.loc[tariff_id, 'demand_start']) + self.ts.get_dst_reverse_shift()).time() > \
                    (pd.Timestamp(self.study.tariff_data.lookup.loc[tariff_id, 'demand_end']) + self.ts.get_dst_reverse_shift()).time():
                # summer period crosses midnight
                summer_period = \
                    summer_days_affected[
                        (summer_days_affected.time >= (pd.Timestamp(
                            scenario.tariff_lookup.loc[tariff_id, 'demand_start']) + self.ts.get_dst_reverse_shift()).time())
                        & (summer_days_affected.time < pd.Timestamp('23:59').time())].append(
                        summer_days_affected[
                            (summer_days_affected.time >= pd.Timestamp('0:00').time())
                            & (summer_days_affected.time < (pd.Timestamp(
                                self.study.tariff_data.lookup.loc[tariff_id, 'demand_end']) + self.ts.get_dst_reverse_shift()).time())])
            else:
                summer_period = \
                    summer_days_affected[
                        (summer_days_affected.time >= (pd.Timestamp(
                            scenario.tariff_lookup.loc[tariff_id, 'demand_start']) + self.ts.get_dst_reverse_shift()).time())
                        & (summer_days_affected.time < (pd.Timestamp(
                            self.study.tariff_data.lookup.loc[tariff_id, 'demand_end']) + self.ts.get_dst_reverse_shift()).time())]
            self.demand_period = winter_period.join(summer_period, 'outer').sort_values()

            s = pd.Series(0, index=pd.DatetimeIndex(data=self.ts.get_date_times()))
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

        # Get solar tariff data:
        # SOLAR BLOCK TARIFF IMPLEMENTATION INCORRECT - REMOVED
        # # NB solar block tariff period is NOT adjusted for DST
        if tariff_id in scenario.solar_list:
            # Solar import tariff is static TOU tariff for instantaneous solar quota
            self.solar_import_tariff = (scenario.static_solar_imports[tariff_id]).values







            pass
        else:
            self.solar_import_tariff = np.zeros(self.ts.get_num_steps())
            self.solar_rate_name = ''
        # -----------------------------
        # All volumetric import tariffs
        # -----------------------------
        # initialise to zero if dynamically calculated, e.g block tariff,
        # otherwise copy from scenario
        if tariff_id not in scenario.dynamic_list:
            self.import_tariff = (scenario.static_imports[tariff_id]).values
        else:
            self.import_tariff = np.zeros(self.ts.get_num_steps())
        
        # self._print_tariff(tariff_id)
    
    def _print_tariff(self, tariff_id):
        print("======")
        print("TARIFF: ", tariff_id)
        for attr, value in self.__dict__.items():
            print(attr, value)
        print("======")
