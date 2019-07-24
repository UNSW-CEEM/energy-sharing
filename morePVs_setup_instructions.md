#morePVs model
morePVs Copyright (C) 2018 Mike B Roberts

multi-occupancy residential electricity with PV and storage model

*This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
Contact: m.roberts@unsw.edu.au*

###Setup Instructions

All input parameters for each study are contained or referenced in `study_xxxxxxx.csv` file.

`scenario` :    Scenario identifier (integer)

`output_type`:
This column lists output formats required, applied to the whole study, not individual scenarios.
All other parameters are given *per scenario* i.e. per line of `.csv` file.



---
PV:
---
Name of pv file - 1 year's output within `DATA_EN_3\pv_profiles`

For `en` or `cp` arrangement, pv file has single column, must be 'cp'

For `btm_i` : btm individual:  en has column for each unit, or if not, single 'cp' or 'total' column that is split equally

For `btm_i_c` : en has column for each unit and cp. Or, single column: cp gets share according to load share; units get equal share of remainder

For Shared btm inc cp:  `btm_s_c` A single `total` or 'cp' column that is split according to instantaneous load between all units AND cp

For Shared btm Units only:`btm_s_u` single `total` or 'cp' column that is split according to instantaneous load between all units EXCLUDING cp

`btm_p_c` and `btm_p_u` are similar, but generation is paid for under a ppa to a solar retailer
For en_external scenario: `cp tariff != TIDNULL`

Scaleable PV:
-------------
filename of 1kWp PV output is `pv_filename` column

`pv_scaleable = TRUE`

`pv_kW_peak` = value to scaleby, eg 50 for 50kWp
If `pv_capex_scaleable` is `True` or absent (ie default setting = `True`),  `pv_cap_id` refers to a scaleable capex scenario with capex and repayments also scaled by `pv_kW_peak` (NB - use of this should be restricted to system sizes with equal $/kWp capex).

if `pv_capex_scaleable` is `False` then `pv_cap_id` has absolute capex values


-----
LOADS
-----
`load_folder` contains the name of sub-folder within `base_path\load_profiles` that contains the load profile(s)
Can be a single file or multiple files for multiple iterations
Load files contain: 
    `timestamp` (first column) in format `d/mm/yyyy h:mm`
    30 minute timestamps assumed. Up to 1 year (17520) but can be less.
    customer load columns (in kWh)
    `'cp'` (optional) common property load (kWh)
    __NB: timestamp refers to *start* of time period__

i.e `1/01/2013 00:00`  timestamp is attached to the period 00:00 - 00:30.

this is to align with the PV output files produced by NREL SAM. It is likely that interval data will need adjusting to align with this.

If there are multiple loads for each scenario, they must all have the same list of customers within the folder,
BUT each scenario *can* have different number of residents, etc.

-----
CAPEX
-----
capex scenarios for en and pv are included in reference file
amortization a_term (years) and a_rate (%) are included in study_....csv file
a_rate is decimal e.g. `0.06` NOT `6%` or `6`
NB if `capex_en_lookup` has duplicate `capex id`s, it all goes to cock. (read_csv retrns series instead of single value).

`pv_capex` is full system cost (*including inverter cost * ), after rebates and including GST
`inverter_cost` is only required if `inverter_life` > amortization period

N.B. Different `pv_capex_id` ids required for individual systems (`btm_i_u` and `btm_i_c`)
to allow for higher $/W costs for smaller systems:

-------
TARIFFS
-------
If all_residents has a tariff, it applies to all households (not cp) either internally for en arrangement or externally for bau btm etc.
If all_residents tariff is not given, each houshold can have its own tariff code
'Static tariffs' are calculated independent of energy flows; 'dynamic' tariffs calculated for each timestep dependent on network status 
(e.g. cumulative load, pv generation, battery state). Dynamic tariffs are identified by having `Block` or `Dynamic` in the the `tariff_type`

'cp' tariff:
-----------
In `en` scenarios, If ENO  is the  strata body, `cp tariff = TIDNULL`,
		If ENO is not the strata  cp tariff is what strata pays ENO for cp load

## Daylight Savings

All load and generation profiles are given in local standard time (no DST)

If the tariff is adjusted for DST (i.e. periods applied to DST-shifted times) then in `study_.....csv` file :

Set `dst = NSW`  (e.g.)

 __NB__ Default is `nsw`

__NB__ `dst` must be the same for the whole study

Then `dst_lookup.csv` has start and end timestamps (`nsw_start` and `nsw_end` ) for  each year.
NB Timestamps given as local standard time (e.g 2am for start and end)


Discount
--------
% discount applied to fixed and volumetric charges

Block Tariffs
-------------
Tariff type: `block_daily`has upto three rates for daily usage. Parameters are:
`block_rate_1`,`high_1`,`block_rate_2`,`high_2`,`block_rate_3`. `high_1` and `high_2` are daily thresholds in kWh. If `high_1` is provided, `block_rate_2` is required.

Tariff type: `block_quarterly` as above but quarterly thresholds, also in kWh. 1st Quarter starts at start of time period. 

		
Solar Tariffs
-------------
`STS_xx`  Solar TOU Tariff based on peak, shoulder and off-peak solar periods with rates at xx% discount from EASO TOU rates
`STC_xx`  Solar TOU Combined tariff based on EASO TOU periods, with additional off-peak solar period and xx% off EASO TOU rates

***SOLAR BLOCK TARIFF NOT IMPLEMENTED - NEEDS REDESIGN***
`SBTd_xx_yy_zz` Solar block TOU tariff (daily):
Based on TOU with `xx%` discount and each customer having a fixed daily quota of solar energy (charged at zz c/kWh) , based on total annual generation during solar period (single solar period is defined in `tariff_lookup.csv` as constant all year, and the script handles DST shift)
cp allocated a fixed % (`cp_solar_allocation` given as decimal (`0.yy`)in `tariff_lookup.csv`) and 
the remainder shared equally between units.
`tariff_type` = `Solar_Block_Daily`
- daily quota applied to solar tariff
If residents have `Solar_Block_daily` and strata body is ENO, CP must have a `Solar_Block_Daily_Null` with same period and allocation but zero rates

         
`SIT_xx` Solar Instantaneous TOU tariff : 
                Based on TOU with `xx%` discount and each customer having a quota of solar energy, based on % of instantaneous generation at that timestamp after cp load has been satisfied. 
                Intended for use with `btm_s` arrangements (e.g. Allum)
				This is **not** a block tariff. 
				`local_import` is calculated statically, 
				Currently doesn't allow for individual battery.

`tariff_type` = `Solar_Instantaneous`
- generation allocated according to load and charged at `solar_rate`,
- with underlying (`Flat_Rate` or `TOU`) tariff for grid consumption.

If `name_x` is `solar_sc`:
    solar tariff applied within solar period but only to self-consumed solar generation. Export is passed through at FiT rate
Solar rate must have details for solar period (even if it is `00:00` to `23:59`)

For `btm_p` arrangements, .....
e.g. Allume:
`tariff_type` = `Solar_Inst_SC_only`
- solar instantaneous tariff (`solar_sc`)applied only to self-consumed solar,
- exported solar charged at FiT rate, so passed through
- Tariff is a combination of retailer tariff and solar tariff paid to third party
    - i.e. underlying (`Flat_Rate` or `TOU`) tariff for grid consumption.

for `btm_s` (eg `upfront`). btm capex and opex are treated as en capex and opex
and shared between customers. PV is treated as if owned individually,
with instantaneous generation allocated equally



##Other EN Tariffs

`CostPlus_xx`   Based on bills paid at parent tariff + xx%. Fixed costs (and CP?) shared evenly; Volumetric costs shared by usage; 
                How best to deal with demand charges? 


`parent` tariff
---------------
Tariff paid at the parent meter for `en` arrangement. 
For Non EN scenarios (bau, btm, cp_only, etc.), parent tariff must be `TIDNULL`, while cp tariff is paid by strata.

-------
BATTERY
-------
__For central Battery__
In `study_xxxxxxx.csv` file, battery is identified by `central_battery_id` and battery control strategy by `central_battery_strategy` 
If `central_battery_id` and `central_battery_strategy` are in the headers, then both must be supplied; 
If `central_battery_id` and `central_battery_strategy` are NOT BOTH in the headers, then battery is not included.

__For Individual Batteries__
Batteries are identified by `x_battery_id` and battery control strategy by `x_battery_strategy` 
    where `x = customer id` from load file

*OR* `all_battery_id` and `all_battery_strategy` for all *households* having the same battery arrangement, plus `cp_battery_id` and `cp_battery_stratagey` (this overrides individual settings).

N.B. (all `_id`s require `_strategy` too.)

| Arrangement                                                  | Battery Set-up                                             |
| ------------------------------------------------------------ | ---------------------------------------------------------- |
| `bau`                                                        | No battery, by definition                                  |
| `bau_bat` -  no pv, individual bats                          | `all_battery_id`  (or multiple `x_bat....`)`cp_battery_id` |
| `en` or `en_pv`  - with central battery                      | `central_battery_id`                                       |
| *This isn't allowed currently:*<br />`en` or `en_pv` with individual batteries | `all_battery_id`  (or multiple `x_bat....`)`cp_battery_id` |
|                                                              |                                                            |
| `en...` with central *and* individual ??                     | `central_` and `all_` and `cp_` ??                         |
| `cp_only` - cp bat only                                 | `cp_battery_id`                                       |
| `btm_i_c`  `btm_i_u`- only ind batteries                     | `all_battery_id`  (or multiple `x_bat....`)`cp_battery_id` |
| `btm_s_c`  `btm_s_u` - only ind batteries                    | `all_battery_id`  (or multiple `x_bat....`)`cp_battery_id` |
|                                                              |                                                            |


### Battery Characteristics

All battery technical data is kept in `reference\battery_lookup.csv`
`battery_id`  - identifier unique to battery characteristics 
`capacity_kWh`      - Single capacity figure: Useful discharge energy
`efficiency_cycle`  - for charge and discharge (MAX = 1.0)  (default `0.95`)
`charge_kW` - for charge and discharge. Max charge rate constrained by inverter power and/or max ~0.8C for charging. Defaults to `0.5C`
`maxDOD` (default `0.8`
`maxSOC` (default `0.9`)
`max_cycles`(default `2000`)

`battery_cost`: Installed battery cost __*excluding*__ inverter (if inverter cost is given) , including GST
`battery_inv_cost` : Installed cost of battery inverter, inc GST (If = zero, inverter and battery treated as single unit).

N.B. If `battery_capex_per_kWh` is given in the `study_` parameter file, it overrides capital costs given in `battery_lookup.csv`

`life_bat_inv` : lifetime of battery inverter (years)) (Defaults to capital amortization period `a_term` )

__Scalable Battery__

If `battery_id` includes `scale` and `x.....battery_capacity_kWh` is in the `study....csv` file (for x = `central` or `cp` or `all` or `customer_id`) this capacity is used to scale the capacity and `max_charge_kW` in the `battery_lookup.csv` file

### Battery Control Strategies
kept in `reference/battery_control_strategies`

__Discharge periods:__

`discharge_start1` and `discharge_end1` (optional) Discharge *only* allowed between these hours 
or these hours: `discharge_start2` and `discharge_end2` . If there is no period, specified, battery is discharged whenever load > generation.

`discharge_day1` , `discharge_day2`	= `week`, `end` or `both` : days to discharge 

__Charge Periods:__

Battery is charged whenever generation > load, 

*plus* Optional additional grid-charging periods (`charge_start1` to `charge_end1`), 

(`charge_start2` to`charge_end2 `)

If there is no charge period specified, battery is never charged from grid.

 `charge_day1` and `charge_day2` 	= `week`, `end` or `both` : days to charge from grid 

If `seasonal_strategy = True` then the model shifts all charge and discharge periods an hour EARLIER in summer. If `False` then winter and summer periods are the same.

__Charge / Discharge Rate__:

`charge_c_rate` and `discharge_c_rate` given in `battery_control_strategies.csv` as C-rate fraction of capacity to charge / discharge in 1 hour. 
e.g 0.5C takes 2 hours to charge / discharge

i.e. charging power = `battery.charge_c_rate` * `battery.capacity_kWh`

If omitted, charge and discharge rate default to `max_charge_kW` in `battery_lookup.csv`

__Priority Charging__

If `prioritise_battery` is `True`: PV generation is applied to charge battery *before* applying to net load.

__Peak demand Strategy__

If `peak_demand_percentage` is present (0 <= x <=100), it is applied as a percentage
to the maximum 30-minute demand in the timeseries to calculate a `peak_demand_threshold`.
Battery is discharged *only* if net import is above this threshold *and* timestep is within `discharge_period`. Default is `0` - i.e. discharge is regardless of load value.
i.e. to discharge battery to meet peak demand, regardless of time, `discharge_period` should be set to 24 hours.







------------
OUTPUT TYPES
------------
Column `output_type` in `'study_...csv` 

| `output_types`       |                                                      | Fields                                                       |
| -------------------- | ---------------------------------------------------- | ------------------------------------------------------------ |
| `log_timeseries_brief` | timeseries `.csv` for each scenario and load profile | ` total load  `,` total building import`, `sum_of_customer_imports` |
| `log_timeseries_detailed` | timeseries `.csv` for each scenario and load profile | ` total load  `,` total building import`, `total building export`,`total generation`,`battery saved charge`, etc. |


the following are no longer functional:

| -------------------- | ---------------------------------------------------- | 
| `csv_total_vs_type`  | Summary `.csv`                                       | `scenario_label`,`load_folder`, `arrangement`, `number_of_households`,`total$_building_costs_mean`,`cp_ratio_mean`,`pv_ratio_mean` |
| `csv_total_vs_bat`   | summary `.csv`                                       | `scenario_label`,`load_folder`, `arrangement`, `number_of_households`,`total$_building_costs_mean`,`self-consumption_mean`,`pv_ratio_mean`, `battery_id` `battery_strategy` |
|                      |                                                      |                                                              |
|                      |                                                      |                                                              |

