import pandas as pd


class Timeseries:
    """DateTimeIndex & related parameters used throughout."""

    def __init__(self,
                 load,
                 dst_lookup,
                 dst_region
                 ):
        self.timeseries = load.index
        
        self.interval = \
            pd.to_timedelta(
                pd.tseries.frequencies.to_offset(
                    pd.infer_freq(self.timeseries)
                )).total_seconds()
        self.num_days = int(len(self.timeseries) * self.interval / (24 * 60 * 60))
        # Set up weekdays and weekends
        self.days = {
            'day': self.timeseries[self.timeseries.weekday.isin([0, 1, 2, 3, 4])],
            'end': self.timeseries[self.timeseries.weekday.isin([5, 6])],
            'both': self.timeseries}
        self.step_ts = pd.Series(self.timeseries)

        # Set up summer and winter periods for daylight savings:
        # NB This is negative because it is applied to tariff period start and end times,
        # rather than to timestamp steps
        # https://www.xkcd.com/1883/
        self.dst_reverse_shift = pd.DateOffset(hours=-1)
        self.seasonal_time = {
            'winter': self.timeseries[0:0],
            'summer': self.timeseries[0:0]
        }

        start_label = dst_region + '_start'
        end_label = dst_region + '_end'

        for year in self.timeseries.year.drop_duplicates().tolist():
            dst_start = pd.Timestamp(dst_lookup.loc[year, start_label])
            dst_end = pd.Timestamp(dst_lookup.loc[year, end_label])
            tsy = self.timeseries[self.timeseries.year == year]
            if dst_start < dst_end:
                self.seasonal_time['winter'] = \
                    self.seasonal_time['winter'].join(tsy[(tsy >= pd.Timestamp('1/01/' + str(year) + ' 00:00:00'))
                                                          & (tsy < dst_start)], 'outer').join(
                        tsy[(tsy >= dst_end)
                            & (tsy < pd.Timestamp('31/12/' + str(year) + ' 23:59:59'))], 'outer')
                self.seasonal_time['summer'] = \
                    self.seasonal_time['summer'].join(tsy[(tsy >= dst_start)
                                                          & (tsy < dst_end)], 'outer')
            else:
                self.seasonal_time['summer'] = \
                    self.seasonal_time['summer'].join(tsy[(tsy >= pd.Timestamp('1/01/' + str(year) + ' 00:00:00'))
                                                          & (tsy < dst_end)], 'outer').join(
                        tsy[(tsy >= dst_start)
                            & (tsy < pd.Timestamp('31/12/' + str(year) + ' 23:59:59'))], 'outer')
                self.seasonal_time['winter'] = \
                    self.seasonal_time['winter'].join(tsy[(tsy >= dst_end)
                                                          & (tsy < dst_start)], 'outer')
        pass

    def steps_today(self, this_step):
        """Returns list of earlier time steps with same day as today"""

        today = self.step_ts[this_step].date()
        steps_today = self.step_ts.loc[self.step_ts.dt.date == today].index.tolist()
        steps_so_far_today = [s for s in steps_today if s <= this_step]
        return steps_so_far_today
    
    def get_num_steps(self):
        return len(self.timeseries)
