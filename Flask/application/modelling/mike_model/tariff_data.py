import os
import pandas as pd
import numpy as np

from ..mike_model import en_utilities as util
import pendulum

class TariffData:
    """Reference resource with time-specific price data for multiple tariffs"""

    def __init__(
            self,
            tariff_lookup_path,
            output_path,
            parameter_list,
            ts,
            dynamic_tariffs):
        """Initialise tariff look-up table."""
        self.dynamic_tariffs = dynamic_tariffs
        self.ts = ts
        
        self.saved_tariff_path = os.path.join(output_path, 'saved_tariffs')
        os.makedirs(self.saved_tariff_path, exist_ok=True)
        # read csv of tariff parameters
        self.lookup = pd.read_csv(tariff_lookup_path, index_col=[0])
        self.all_tariffs = [t for t in self.lookup.index if t in parameter_list]  # list of all tariff ids
        # set up dfs for static import and export tariffs
        self.static_imports = pd.DataFrame(
            index=pd.DatetimeIndex(data=self.ts.get_date_times())
            )
        self.static_exports = pd.DataFrame(index=pd.DatetimeIndex(data=self.ts.get_date_times()))
        self.static_solar_imports = pd.DataFrame(index=pd.DatetimeIndex(data=self.ts.get_date_times()))

        self.tou_rate_list = {'name_1': ['rate_1', 'start_1', 'end_1', 'week_1'],
                              'name_2': ['rate_2', 'start_2', 'end_2', 'week_2'],
                              'name_3': ['rate_3', 'start_3', 'end_3', 'week_3'],
                              'name_4': ['rate_4', 'start_4', 'end_4', 'week_4'],
                              'name_5': ['rate_5', 'start_5', 'end_5', 'week_5'],
                              'name_6': ['rate_6', 'start_6', 'end_6', 'week_6'],
                              'name_7': ['rate_7', 'start_7', 'end_7', 'week_7'],
                              'name_8': ['rate_8', 'start_8', 'end_8', 'week_8'],
                              }

    def generateStaticTariffs(self):
        """ Creates time-based rates for all load-independent tariffs."""

       

        for tid in self.all_tariffs:
            # apply discounts to all tariffs:
            # -------------------------------
            # excluding FiTs and solar tariffs
            if not np.isnan(self.lookup.loc[tid, 'discount']):
                discount = self.lookup.loc[tid, 'discount']
                rates = [c for c in self.lookup.columns if 'rate' in c and not 'fit' in c]
                named_rates = [c for c in rates if
                               not np.isnan(self.lookup.loc[tid, c]) and
                               c.replace('rate', 'name') in self.lookup.columns]
                solar_rates = [c for c in named_rates if
                               'solar' in self.lookup.loc[tid, c.replace('rate', 'name')]
                               or 'Solar' in self.lookup.loc[tid, c.replace('rate', 'name')]]
                discounted_rates = [c for c in rates if c not in solar_rates]
                self.lookup.loc[tid, discounted_rates] = self.lookup.loc[tid, discounted_rates] * (100 - discount) / 100
            # Allocate Flat rate and Zero Tariffs
            # -----------------------------------:
            self.static_imports[tid] = 0  # for zero rate tariff and as initialisation
            self.static_solar_imports[tid] = 0  # for zero rate tariff and as initialisation

            if 'Flat' in self.lookup.loc[tid, 'tariff_type']:
                self.static_imports[tid] = self.lookup.loc[tid, 'flat_rate']
            # Allocate TOU tariffs:
            # --------------------
            # including residual (non-solar) rates for Solar_Block_TOU
            elif 'TOU' in self.lookup.loc[tid, 'tariff_type'] \
                    or 'Solar_Block' in self.lookup.loc[tid, 'tariff_type'] \
                    or 'Solar_Inst' in self.lookup.loc[tid, 'tariff_type']:
                # calculate timeseries TOU tariff based on up to 8 periods (n=1 to 8)
                # volumetric tariff is rate_n, between times start_n and end_n
                # week_n is 'day' for week, 'end' for weekend, 'both' for both
                # NB times stored in csv in form 'h:mm'. Midnight saved as 23:59
                for name, parameter in self.tou_rate_list.items():
                    if not pd.isnull(self.lookup.loc[tid, parameter[1]]):  # parameter[1] is rate_
                        # Returns a pd.DatetimeIndex containing relevant winter days affected by tariff.
                        # Here we are just trying to get 'what are all the days that are both weekends/weekdays, and also winter / summer seasonal?
                        weekday_key = self.lookup.loc[tid, parameter[3]] #either 'day', 'end' or 'both' - needs a refactor. 
                        winter_days_affected = self.ts.get_seasonal_times('winter', weekday_key)
                        winter_days_affected = pd.DatetimeIndex(data=winter_days_affected) #convert array to pd.DatetimeIndex
                        
                        summer_days_affected = self.ts.get_seasonal_times('summer', weekday_key)
                        summer_days_affected = pd.DatetimeIndex(data=summer_days_affected) #convert array to pd.DatetimeIndex
                       
                        if pd.Timestamp(self.lookup.loc[tid, parameter[1]]).time() > pd.Timestamp(
                                self.lookup.loc[tid, parameter[2]]).time():
                            # winter tariff period crosses midnight:
                            winter_period = \
                                (winter_days_affected[
                                    (winter_days_affected.time >= pd.Timestamp(
                                        self.lookup.loc[tid, parameter[1]]).time())  # [1] is start_)
                                    & (winter_days_affected.time <= pd.Timestamp('23:59').time())]).append(
                                    winter_days_affected[
                                        (winter_days_affected.time >= pd.Timestamp('0:00').time())
                                        & (winter_days_affected.time < pd.Timestamp(
                                            self.lookup.loc[tid, parameter[2]]).time())])  # [2] is end_
                        else:
                            # tariff period doesn't cross midnight:
                            winter_period = \
                                winter_days_affected[
                                    (winter_days_affected.time >= pd.Timestamp(
                                        self.lookup.loc[tid, parameter[1]]).time())  # start_)
                                    & (winter_days_affected.time < pd.Timestamp(
                                        self.lookup.loc[tid, parameter[2]]).time())]  # end_

                        if (pd.Timestamp(self.lookup.loc[tid, parameter[1]]) + self.ts.get_dst_reverse_shift()).time() > (
                                pd.Timestamp(
                                        self.lookup.loc[tid, parameter[2]]) + self.ts.get_dst_reverse_shift()).time():
                            # summer tariff period crosses midnight:
                            summer_period = \
                                (summer_days_affected[
                                    (summer_days_affected.time >= (pd.Timestamp(
                                        self.lookup.loc[
                                            tid, parameter[1]]) + self.ts.get_dst_reverse_shift()).time())  # [1] is start_)
                                    & (summer_days_affected.time <= pd.Timestamp('23:59').time())]).append(
                                    summer_days_affected[
                                        (summer_days_affected.time >= pd.Timestamp('0:00').time())
                                        & (summer_days_affected.time < (pd.Timestamp(
                                            self.lookup.loc[
                                                tid, parameter[2]]) + self.ts.get_dst_reverse_shift()).time())])  # [2] is end_
                        else:
                            summer_period = \
                                summer_days_affected[
                                    (summer_days_affected.time >= (pd.Timestamp(
                                        self.lookup.loc[tid, parameter[1]]) + self.ts.get_dst_reverse_shift()).time())  # start_)
                                    & (summer_days_affected.time < (pd.Timestamp(
                                        self.lookup.loc[tid, parameter[2]]) + self.ts.get_dst_reverse_shift()).time())]  # end_
                        period = winter_period.join(summer_period, 'outer').sort_values()
                        if not any(s in self.lookup.loc[tid, name] for s in ['solar', 'Solar']):
                            # Store solar rate and period separately
                            # For non-solar periods and rates only:
                            self.static_imports.loc[period, tid] = self.lookup.loc[tid, parameter[0]]  # rate_
                        else:  # Solar (local) periods and rates only:
                            self.static_solar_imports.loc[period, tid] = self.lookup.loc[tid, parameter[0]]  # rate_
                    pass

            # todo: create timeseries for TOU  FiT Tariffs in the same way
            # (currently only zero or flat rate FiTs)
            if self.lookup.loc[tid, 'fit_type'] == 'Zero_Rate':
                self.static_exports[tid] = 0
            elif self.lookup.loc[tid, 'fit_type'] == 'Flat_Rate':
                self.static_exports[tid] = self.lookup['fit_flat_rate'].fillna(0).loc[tid]
        
        # ==================================
        # DYNAMIC TOU TARIFF IMPLEMENTATION
        # ==================================
        # HOLY GRAIL NUMBER 2
        # These three params (static_imports etc. ) are timeseries' that are queried for the tariff.
        # Two ways to do this, but the lighter touch is to extend this module
        # Such that these three params still exist, but are generated on the fly from supplied params.
        
        self._configure_dynamic_tariffs()
        

        # Save tariffs as csvs
        import_name = os.path.join(self.saved_tariff_path, 'static_import_tariffs.csv')
        solar_name = os.path.join(self.saved_tariff_path, 'static_solar_import_tariffs.csv')
        export_name = os.path.join(self.saved_tariff_path, 'static_export_tariffs.csv')

        util.df_to_csv(self.static_imports, import_name)
        util.df_to_csv(self.static_solar_imports, solar_name)
        util.df_to_csv(self.static_exports, export_name)

        
    def _configure_dynamic_tariffs(self):
        """This is a parser to get the data from the dynamic tariffs UI construction into the dataframe format used in the Mike model. """
        # Loop through each dynamic tariff in the list. 
        for dynamic_tariff in self.dynamic_tariffs:
            print("tariff_data.py/_configure_dynamic_tariffs()", dynamic_tariff)
            # Add they dynamic tariff's static import data
            static_imports = []
            
            for key in self.static_imports.index:
                dt = pendulum.instance(key)
                # Luke's first ever use of the for...else construction.
                for period in dynamic_tariff['static_imports']:
                    if (dt.hour >= period['start_hr']) and (dt.hour < period['end_hr']):
                        static_imports.append(period['price'])
                        break
                else:
                    static_imports.append(0)
            self.static_imports[dynamic_tariff['name']] = static_imports

            # Add they dynamic tariff's static solar import data
            static_solar_imports = []
            for key in self.static_solar_imports.index:
                dt = pendulum.instance(key)
                for period in dynamic_tariff['static_solar_imports']:
                    if (dt.hour >= period['start_hr']) and (dt.hour < period['end_hr']):
                        static_solar_imports.append(period['price'])
                        break
                else:
                    static_solar_imports.append(0)
            self.static_solar_imports[dynamic_tariff['name']] = static_solar_imports

            # Add they dynamic tariff's static export data
            static_exports = []
            for key in self.static_exports.index:
                dt = pendulum.instance(key)
                for period in dynamic_tariff['static_exports']:
                    if (dt.hour >= period['start_hr']) and (dt.hour < period['end_hr']):
                        static_exports.append(period['price'])
                        break
                else:
                    static_exports.append(0)
            self.static_exports[dynamic_tariff['name']] = static_exports

            # print("tariff_data.py/_configure_dynamic_tariffs", self.static_imports.to_string())
            

            # Modify the tariff lookup so that it contains a special tariff type for each custom tariff. 
            self.lookup.loc[dynamic_tariff['name'], 'tariff_type'] = 'custom'
            for parameter in ['daily_fixed_rate']:
                self.lookup.loc[dynamic_tariff['name'], parameter] = dynamic_tariff[parameter]
    
    
