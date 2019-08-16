#recovering morePvs functionality from energy sharing model

###15/8/19
###Get model running using `.csv` data 

 `mike_runner2.py` does this. 
 **But** 
 - Can only run a single scenario atm
 - [X] timestamps in load and solar profiles have to be reformatted using `convert_profiles.py`
- []  `solar inst` type tariffs not working, because Luke was working with a version of  `solar_rate_name` may not exist
 `morePVs` where i had removed them. Now attempting to replace the missing section in `Tariff` module. BUT there is an issue
 with datatypes. Luke's `ts.get_seasonal_times` returns a list of dates, whereas i was working with a `DatetimeIndex`
 So, for now, will have to sack these solar tariffs and therefor `btm_p` arrangements
- [] Some issues with parameters that aren't needed for particular scenarios, may be passed as `None` objects which is causing issues'


###16/8/19
- [] Issue with ***file paths***: `folder_routes.py` defines file paths for GUI, particularly for output.
I want to override these with base_path, project and study names from `morePVs2.py`.

***CAN I JUST SET A flag `override_folders`??***


- [] Issue with how `cp` is handled. Was counted as an additional apartment / customer which affected the 
financial outcomes for `en`. Now right # of participants but still wrong answer


- [X] Issue with all scenarios without PV (`bau`, `en`, etc.):
   - [X] `mike.find_time_periods` loads solar file. called from `mike.load_data_sources` Need flag for solar
   - [X] `new_sim.__init` same issue
   
- [X] `study.__init__` can't find `central_solar_profile` and `shared_solar_profile` parameters. Now made conditional
    (Need to clarify what the difference is ffs)

 -[X] `study.__init__` 'locate pv data` made conditional to avoid false error for arrangements without pv
 
 -[X] Error in `pv.py` : `PVCollectionFactory.empty_collection`:
  Changed to `data.index.name= 'timestamp'`
  
  -[X] `scenario._generate_pv_profiles`  key error `cp`  Make 'cp' conditional on whether it exists
  -[X] `scenario.__init__` line 101 `parent` key error. Fill `parent` and `network` tariffs with `TIDNULL`
  -[X] `pv_cap_id`
  
  -[] Issue:`bau` scenario now running BUT outputs are wrong:
        - customer bills and totals are correct, but `cp` bill is much lower, 
        - also retailer receipt and total bulding cost;
        - retailler bill less but by smaller amount
        - `import_kWh` is less by `4828.14` (Total cp load is `4828.154428`). Coincidence!!
  *Or is this related to difference between `customers` (inc `cp`) and `residents`?*
  
  -[X] Added `+ ['cp']` and `+ 1` to lists of residents twhere appropriate in `network.py`
  BUT hmmmm...... Now creates issues when calling `study.get_solar_profiles` and others because `cp` doesn't have a profile
  ##Is `cp` a _participant or not??
  
  