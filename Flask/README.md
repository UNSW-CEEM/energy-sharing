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

Also in relation to the timeseries.days parameter, in the battery model, there were a number of instances that used this as a basis for finding times that were on weekends, weekdays, or 'both', between two times, sometimes over midnight. I have built a function into the Timeseries object that performs this function, and adapted the code to use it. I have some reservations around this code - sort_values() is being called on what looks like a tuple that contains pd.DatetimeIndex - which would suggest to me that the tuple values are being sorted and not the index. This is how it was though. Additionally, a lot of variables are titled like 'charge_period2' but sometimes there is and/or isn't an underscore between the words and the number....maybe this doesn't matter as its just used locally, but I suspect an alternative is some of these if-statements havent been called.

Made a getter for the 'interval' parameter of the timeseries object. Changes to battery.py to handle this (ie use the getter instead of grabbing the variable).

Reminder for luke by luke: when I have internet again, look up https://www.xkcd.com/1883/

Made a getter for dst reverse shift. Might be scope here for writing a conversion function for timezones instead, or using pendulum...but...future problem. 

Changed all references to .pv to the PVCollection object (from a pandas dataframe), which will be considered a collection of PV systems that can be queried for solar data. All access to data, and modifications of data, are carried out through function calls rather than by accessing internal parameters.

Refactored the loads dicts and dataframes, so that they simply use a LoadCollection object (load.py). Removing any reliance on dataframes here. 