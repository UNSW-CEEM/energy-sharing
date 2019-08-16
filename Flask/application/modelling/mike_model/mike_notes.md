#recovering morePvs functionality from energy sharing model

###15/8/19
###Get model running using `.csv` data 

 `mike_runner2.py` does this. 
 **But** 
 - Can only run a single scenario atm
 - timestamps in load and solar profiles have to be reformatted using `convert_profiles.py`
 -  `solar inst` type tariffs not working, because Luke was working with a version of  `solar_rate_name` may not exist
 `morePVs` where i had removed them. Now attempting to replace the missing section in `Tariff` module. BUT there is an issue
 with datatypes. Luke's `ts.get_seasonal_times` returns a list of dates, whereas i was working with a `DatetimeIndex`
 So, for now, will have to sack these solar tariffs and therefor `btm_p` arrangements
 - Some issues with parameters that aren't needed for particular scenarios, may be passed as `None` objects which is causing issues'


###16/8/19
- Issue with ***file paths***: `folder_routes.py` defines file paths for GUI, particularly for output.
I want to override these with base_path, project and study names from `morePVs2.py`


- Issue with how `cp` is handled. Counted as an additional apartment / customer which affects the financial outcomes for `en`
