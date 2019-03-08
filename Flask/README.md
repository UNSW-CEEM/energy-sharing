There is a bug in current versions of pipenv, that the default pip is an in-development version, with a bug. 
See here for a workaround:https://github.com/pypa/pipenv/issues/2871
In short:

pip install pipenv
pipenv run pip install pip==18.0
pipenv install



# Questions

1. line 152 of parameters.py in create_mike_objects() - whats create_csvs() doing? doesnt look like this function does much. 

# Mike Model Changes

The Timeseries object used to have a 'timeseries' parameter, which was a pd.DatetimeIndex() object. 
I've deleted this, changed it to .ts internally, and changed all references to use a getter function get_date_times() which returns an array of datetimes - previous calls that used .timeseries will now have to cast this list back to a pd.Datetimeindex with pd.DatetimeIndex(data=ts.get_date_times())

In the tariff data, there were a number of references to the timeseries.days parameter, which returned lists of datetimes that were either weekends or weekdays. Specifically, this was used to find weekends, weekdays or 'both' that were either in summer or winter, for tariff purposes. I've abstracted this functionality out into the get_seasonal_times() function, which takes a season label and a weekday label. 