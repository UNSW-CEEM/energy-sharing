# Useful stuff

import datetime
import pendulum
import pandas as pd


def generate_dates_in_range(start_dt, end_dt, interval_minutes):
    """Return list of dates between start and end."""
    start_dt = start_dt.replace(second = 0, microsecond = 0)
    
    date_time_list = []
    current = start_dt
    
    while current < end_dt :
        dt_str = pendulum.instance(current).format('D/MM/YYYY H:mm')
        date_time_list.append(current)
        current = current + datetime.timedelta(minutes = interval_minutes)

    return date_time_list

def date_parser(date_string):
    # print("parsing", date_string)
    # return pendulum.from_format(date_string, ('%d/%m/%Y %H:%M'))
    return pd.datetime.strptime(date_string, '%d/%m/%Y %H:%M')
    # return pendulum.from_format(date_string, ('DD/MM/YYYY HH:mm'))