import pandas as pd


class Timeseries:
    """DateTimeIndex & related parameters used throughout."""

    def __init__(self,
                 load,
                 dst_lookup,
                 dst_region
                 ):
        self._date_times = load.index
        
        # Set up weekdays and weekends
        self._days = {
            'day': self._date_times[self._date_times.weekday.isin([0, 1, 2, 3, 4])],
            'end': self._date_times[self._date_times.weekday.isin([5, 6])],
            'both': self._date_times}
        

        # Set up summer and winter periods for daylight savings:
        
        self._seasonal_time = {
            'winter': self._date_times[0:0],
            'summer': self._date_times[0:0]
        }

        start_label = dst_region + '_start'
        end_label = dst_region + '_end'

        for year in self._date_times.year.drop_duplicates().tolist():
            dst_start = pd.Timestamp(dst_lookup.loc[year, start_label])
            dst_end = pd.Timestamp(dst_lookup.loc[year, end_label])
            tsy = self._date_times[self._date_times.year == year]
            if dst_start < dst_end:
                self._seasonal_time['winter'] = \
                    self._seasonal_time['winter'].join(tsy[(tsy >= pd.Timestamp('1/01/' + str(year) + ' 00:00:00'))
                                                          & (tsy < dst_start)], 'outer').join(
                        tsy[(tsy >= dst_end)
                            & (tsy < pd.Timestamp('31/12/' + str(year) + ' 23:59:59'))], 'outer')
                self._seasonal_time['summer'] = \
                    self._seasonal_time['summer'].join(tsy[(tsy >= dst_start)
                                                          & (tsy < dst_end)], 'outer')
            else:
                self._seasonal_time['summer'] = \
                    self._seasonal_time['summer'].join(tsy[(tsy >= pd.Timestamp('1/01/' + str(year) + ' 00:00:00'))
                                                          & (tsy < dst_end)], 'outer').join(
                        tsy[(tsy >= dst_start)
                            & (tsy < pd.Timestamp('31/12/' + str(year) + ' 23:59:59'))], 'outer')
                self._seasonal_time['winter'] = \
                    self._seasonal_time['winter'].join(tsy[(tsy >= dst_end)
                                                          & (tsy < dst_start)], 'outer')
        pass

    def steps_today(self, this_step):
        """Returns list of earlier time steps with same day as today"""
        step_ts = pd.Series(self._date_times)
        today = step_ts[this_step].date()
        steps_today = step_ts.loc[step_ts.dt.date == today].index.tolist()
        steps_so_far_today = [s for s in steps_today if s <= this_step]
        return steps_so_far_today
    
    def get_num_steps(self):
        return len(self._date_times)
    
    def get_date_times(self):
        return [dt for dt in self._date_times]
    
    def get_seasonal_times(self, season, weekday='both'):
        """
            Takes a season key, either 'summer' or 'winter
            Takes a weekday key, either 'both' or 'weekday' or 'weekend'
            Returns the times in the timeseries that are in the given season, for weekdays, weekends, or both. 
        """
        if weekday == 'weekend':
            weekday = 'end'
        if weekday == 'weekday':
            weekday = 'day'
        return [x for x in self._days[weekday].join(self._seasonal_time[season], how='inner')]
    
    def get_times_between(self, start_time, end_time, weekday):
        """
            Takes a start_time and an end_time (time objects w/ tzinfo=None)
            Plus an optional weekday tag  - 'weekend' 'weekday' 'both'
            Returns all date_times in the timeseries that are between these two times. 
        """
        if weekday == 'weekend':
            weekday = 'end'
        if weekday == 'weekday':
            weekday = 'day'

        times = self._days[weekday][(self._days[weekday].time >= start_time) & (self._days[weekday].time < end_time)]
        return [time for time in times]
    
    def get_interval(self):
        """Returns number of seconds in each interval of the timeseries"""
        return pd.to_timedelta(pd.tseries.frequencies.to_offset(pd.infer_freq(self._date_times))).total_seconds()
    
    def get_num_days(self):
        return int(len(self._date_times) * self.get_interval() / (24 * 60 * 60))
    
    def get_dst_reverse_shift(self):
        # NB This is negative because it is applied to tariff period start and end times,
        # rather than to timestamp steps
        # https://www.xkcd.com/1883/
        return pd.DateOffset(hours=-1)
