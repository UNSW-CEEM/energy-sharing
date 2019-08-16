# -----------------------------------------------------------------------------------------
# # This section replaced from earlier implementation as Solar Inst tariffs are still required:
# # SOLAR BLOCK TARIFF IMPLEMENTATION INCORRECT but code below also used for solar instantaneous
# # # NB solar block tariff period is NOT adjusted for DST
# if tariff_id in scenario.solar_list:
#     for name, parameter in self.study.tariff_data.tou_rate_list.items():
#         if not pd.isnull(self.study.tariff_data.lookup.loc[tariff_id, name]):
#             if any(s in self.study.tariff_data.lookup.loc[tariff_id, name] for s in ['solar', 'Solar']):
#                 self.solar_rate_name = self.study.tariff_data.lookup.loc[tariff_id, name]
#                 winter_days_affected = self.ts._days[scenario.tariff_lookup.loc[tariff_id, parameter[3]]].join(
#                     # [3] is week_
#                     self.ts.get_seasonal_times('winter'), 'inner')
#                 summer_days_affected = self.ts._days[scenario.tariff_lookup.loc[tariff_id, parameter[3]]].join(
#                     # [3] is week_
#                     self.ts.get_seasonal_times('summer'), 'inner')
#
#                 if pd.Timestamp(scenario.tariff_lookup.loc[tariff_id, parameter[1]]).time() > \
#                         pd.Timestamp(scenario.tariff_lookup.loc[tariff_id, parameter[2]]).time():
#                     # winter tariff period crosses midnight:
#                     winter_period = \
#                         winter_days_affected[
#                             (winter_days_affected.time >= pd.Timestamp(
#                                 scenario.tariff_lookup.loc[tariff_id, parameter[1]]).time())  # [1] is start
#                             & (winter_days_affected.time < pd.Timestamp('23:59').time())].append(
#                             winter_days_affected[
#                                 (winter_days_affected.time >= pd.Timestamp('0:00').time())
#                                 & (winter_days_affected.time < pd.Timestamp(
#                                     scenario.tariff_lookup.loc[
#                                         tariff_id, parameter[2]]).time())])  # [2] is end_
#                 else:
#                     # winter tariff period doesn't cross midnight:
#                     winter_period = \
#                         winter_days_affected[
#                             (winter_days_affected.time >= pd.Timestamp(
#                                 scenario.tariff_lookup.loc[tariff_id, parameter[1]]).time())  # [1] is start
#                             & (winter_days_affected.time < pd.Timestamp(
#                                 scenario.tariff_lookup.loc[tariff_id, parameter[2]]).time())]  # [2] is end_
#
#                 if (pd.Timestamp(scenario.tariff_lookup.loc[tariff_id, parameter[1]])).time() > \
#                         (pd.Timestamp(scenario.tariff_lookup.loc[tariff_id, parameter[2]])).time():
#                     # summer tariff period crosses midnight:
#                     summer_period = \
#                         summer_days_affected[
#                             (summer_days_affected.time >= (pd.Timestamp(
#                                 scenario.tariff_lookup.loc[
#                                     tariff_id, parameter[1]])).time())  # [1] is start
#                             & (summer_days_affected.time < pd.Timestamp('23:59').time())].append(
#                             # [2] is end_
#                             summer_days_affected[
#                                 (summer_days_affected.time >= pd.Timestamp('0:00').time())  # [1] is start
#                                 & (summer_days_affected.time < (pd.Timestamp(
#                                     scenario.tariff_lookup.loc[
#                                         tariff_id, parameter[2]])).time())])  # [2] is end_
#                 else:
#                     # summer tariff period doesn't cross midnight:
#                     summer_period = \
#                         summer_days_affected[
#                             (summer_days_affected.time >= (pd.Timestamp(
#                                 scenario.tariff_lookup.loc[
#                                     tariff_id, parameter[1]])).time())  # [1] is start
#                             & (summer_days_affected.time < (pd.Timestamp(
#                                 scenario.tariff_lookup.loc[
#                                     tariff_id, parameter[2]])).time())]  # [2] is end_
#
#                 # solar_period, solar_rate and solar_cp_allocation are for solar block tariffs:
#                 # ie fixed quotas with dynamic load-dependent calculation
#                 self.solar_period = winter_period.join(summer_period, 'outer').sort_values()
#                 self.solar_rate = scenario.tariff_lookup.loc[tariff_id, parameter[0]]  # rate_
#                 self.solar_cp_allocation = scenario.tariff_lookup['solar_cp_allocation'].fillna(0).loc[
#                     tariff_id]  # % of total solar generation allocated to cp
#     # Solar import tariff is static TOU tariff for instantaneous solar quota
#     self.solar_import_tariff = (scenario.static_solar_imports[tariff_id]).values
#     # -----------------------------------------------------------------------------------------
