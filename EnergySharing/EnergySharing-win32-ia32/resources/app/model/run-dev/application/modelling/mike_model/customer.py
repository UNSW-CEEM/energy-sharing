import numpy as np
import sys

from ..mike_model.tariff import Tariff


class Customer:
    """Can be resident, strata body, or ENO representing aggregation of residents."""

    def __init__(self, name, study, timeseries):
        self.name = name
        self.study = study
        self.ts = timeseries

        self.tariff_data = self.study.tariff_data
        self.en_capex_repayment = 0
        self.en_opex = 0
        self.bat_capex_repayment = 0
        self.exports = np.zeros(self.ts.get_num_steps())
        self.imports = np.zeros(self.ts.get_num_steps())
        # self.local_exports = np.zeros(ts.get_num_steps())  # not used, available for local trading
        self.solar_allocation = np.zeros(self.ts.get_num_steps())  # used for allocation of local generation
        self.local_consumption = np.zeros(self.ts.get_num_steps())
        self.flows = np.zeros(self.ts.get_num_steps())
        self.cash_flows = np.zeros(self.ts.get_num_steps())
        self.import_charge = np.zeros(self.ts.get_num_steps())
        self.local_solar_bill = 0
        self.total_payment = 0

        # TODO My linter wants everything instantiated within the init
        self.load = None
        self.coincidence = None
        self.tariff_id = None
        self.scenario = None
        self.tariff = None
        self.generation = None
        self.demand_charge = None
        self.npv = None
        self.energy_bill = None

    # as 1-d np.array
    def initialise_customer_load(self, customer_load):
        """Set customer load, energy flows and cashflows to zero."""
        self.load = customer_load
        # used for calculating self-consumption and self sufficiency
        self.coincidence = np.zeros(self.ts.get_num_steps())

    def initialise_customer_tariff(self, customer_tariff_id, scenario):
        self.tariff_id = customer_tariff_id
        self.scenario = scenario
        self.tariff = Tariff(tariff_id=self.tariff_id, scenario=scenario)

    def initialise_customer_pv(self, pv_generation):  # 1-D array
        self.generation = pv_generation

    def calc_static_energy(self):
        """Calculate Customer imports and exports for whole time period"""
        self.flows = self.generation - self.load
        self.exports = self.flows.clip(0)
        self.imports = (-1 * self.flows).clip(0)
        # # Calculate local quota here??
        # self.solar_allocation = np.minimum(self.imports, self.local_quota)  # for use of local generation
        # for btm_p and btm_s arrangements:
        self.local_consumption = np.minimum(self.generation, self.load)

    def calc_dynamic_energy(self, step):
        """Calculate Customer imports and exports for single timestep"""
        # Used for scenarios with batteries
        # -------------------------------------------------------------------------------
        # Calculate energy flow without battery, then modify by calling battery.dispatch:
        # -------------------------------------------------------------------------------
        self.flows[step] = self.generation[step] - self.load[step]
        if self.has_battery:
            self.flows[step] = self.battery.dispatch(generation=self.generation[step],
                                                     load=self.load[step],
                                                     step=step)
        else:
            self.flows[step] = self.generation[step] - self.load[step]
        self.exports[step] = self.flows[step].clip(0)
        self.imports[step] = (-1 * self.flows[step]).clip(0)

        # Calculate local quota here??
        # # Solar allocation is for solar_instantaneous tariff
        # self.solar_allocation[step] = np.minimum(self.imports[step], self.local_quota[step])

        # Local Consumption is PV self-consumed by customer (which is charged for in btm_p arrangement)
        self.local_consumption[step] = np.minimum(self.generation[step], self.load[step])

    def calc_demand_charge(self):
        if self.tariff.is_demand:
            max_demand = np.multiply(self.imports, self.tariff.demand_period_array).max() * 2  # convert kWh to kW
            self.demand_charge = max_demand * self.tariff.demand_tariff * self.ts.get_num_days()
            # Use nominal pf to convert to kVA?
            if self.tariff.demand_type == 'kVA':
                self.demand_charge = self.demand_charge / self.tariff.assumed_pf
        else:
            self.demand_charge = 0

    def calc_cash_flow(self):
        """Calculate receipts and payments for customer.

        self.cashflows is net volumetric import & export charge,
        self.energy_bill is total elec bill, ic fixed charges
        self.total_payment includes opex & capex repayments"""

        if any(s in self.tariff.solar_rate_name for s in ['self_con', 'Self_Con', 'sc', 'SC']):
            # IFF solar tariff paid to secondary solar retailer for self-consumed generation
            # and export FiT paid for exported generation
            # NB cost of exported self generation is received from retailer and passed to PV seller, so zero net effect
            # Energy flows treated as if PV is owned by customer
            self.local_solar_bill = (np.multiply(self.local_consumption, self.tariff.solar_import_tariff) + \
                                     np.multiply(self.exports, self.tariff.export_tariff)).sum()
        else:
            self.local_solar_bill = 0.0

        if self.tariff.is_dynamic:
            # ------------------------------------
            # calculate tariffs and costs stepwise
            # ------------------------------------
            for step in np.arange(0, self.ts.get_num_steps()):
                # print(step)
                # --------------------------------------------------------------
                # Solar Block Daily Tariff : Calculate energy used at solar rate
                # --------------------------------------------------------------
                # Fixed daily allocation (set as % of annual generation) charged at solar rate,
                # residual is at underlying, e.g. TOU
                if 'Solar_Block_Daily' in self.tariff.tariff_type:
                    print('Solar_Block_Daily NOT SUPPORTED')
                    sys.exit('Solar_Block_Daily NOT SUPPORTED')
                    # SOLAR BLOCK DAILY REMOVED
                    # steps_today = ts.steps_today(step)
                    # # Cumulative Energy for this day:
                    # cumulative_energy = self.imports[steps_today].sum()
                    # if len(steps_today) <= 1:
                    #     previous_energy = 0
                    # else:
                    #     previous_energy = self.imports[steps_today[:-1]].sum()
                    # # Allocate local solar allocation depending on cumulative energy relative to quota:
                    # if cumulative_energy <= self.daily_local_quota:
                    #     self.solar_allocation[step] = self.imports[step]
                    # elif previous_energy < self.daily_local_quota \
                    #         and cumulative_energy > self.daily_local_quota:
                    #     self.solar_allocation[step] = self.daily_local_quota - previous_energy
                    # else:
                    #     self.solar_allocation[step] = 0
                else:
                    # ---------------------------------------------------------
                    # For Block Tariffs, calc volumetric charges for each block
                    # ---------------------------------------------------------
                    # Block Quarterly Tariff
                    # ----------------------
                    if self.tariff.tariff_type == 'Block_Quarterly':
                        steps_since_reset = np.mod((step - self.tariff.block_billing_start),
                                                   self.tariff.steps_in_block)  # to include step0
                        cumulative_energy = self.imports[
                                            step - steps_since_reset:step + 1].sum()  # NB only adds to step
                        if steps_since_reset == 0:
                            previous_energy = 0
                        else:
                            previous_energy = self.imports[step - steps_since_reset:step].sum()  # NB adds to step-1

                    # Block Daily Tariff
                    # -------------------
                    elif self.tariff.tariff_type == 'Block_Daily':
                        steps_today = self.ts.steps_today(step)
                        cumulative_energy = self.imports[steps_today].sum()
                        if len(steps_today) <= 1:
                            previous_energy = 0
                        else:
                            previous_energy = self.imports[steps_today[:-1]].sum()

                    if cumulative_energy - previous_energy - self.imports[step] > 0.01:
                        print('accumulation error')
                    # All Block Tariffs:
                    # -----------------
                    if cumulative_energy <= self.tariff.high_1:
                        self.import_charge[step] = self.imports[step] * self.tariff.block_rate_1
                    elif previous_energy < self.tariff.high_1 and cumulative_energy <= self.tariff.high_2:
                        self.import_charge[step] = (self.tariff.high_1 - previous_energy) * self.tariff.block_rate_1 + \
                                                   (cumulative_energy - self.tariff.high_1) * self.tariff.block_rate_2
                    elif previous_energy > self.tariff.high_1 and cumulative_energy <= self.tariff.high_2:
                        self.import_charge[step] = self.imports[step] * self.tariff.block_rate_2
                    elif previous_energy < self.tariff.high_2 and cumulative_energy > self.tariff.high_2:
                        self.import_charge[step] = (self.tariff.high_2 - previous_energy) * self.tariff.block_rate_2 + \
                                                   (cumulative_energy - self.tariff.high_2) * self.tariff.block_rate_3
                    elif previous_energy >= self.tariff.high_2:
                        self.import_charge[step] = self.imports[step] * self.tariff.block_rate_3
                    elif previous_energy < self.tariff.high_1 and cumulative_energy > self.tariff.high_2:
                        self.import_charge[step] = (self.tariff.high_1 - previous_energy) * self.tariff.block_rate_1 + \
                                                   (
                                                               self.tariff.high_2 - self.tariff.high_1) * self.tariff.block_rate_2 + \
                                                   (cumulative_energy - self.tariff.high_2) * self.tariff.block_rate_3

        # -------------------------------------------------------------
        #  calculate costs using array for static and underlying tariffs
        # -------------------------------------------------------------
        if self.tariff.tariff_type == 'Solar_Block_Daily' or not self.tariff.is_dynamic:
            self.import_charge = np.multiply((self.imports - self.solar_allocation), self.tariff.import_tariff)
        # For all dynamic and static tariffs:
        # -----------------------------------
        self.cash_flows = self.import_charge \
                          + np.multiply(self.solar_allocation, self.tariff.solar_import_tariff) \
                          - np.multiply(self.exports, self.tariff.export_tariff)
        # - np.multiply(self.local_exports, self.tariff.local_export_tariff) could be added for LET / P2P
        # (These are all 1x17520 Arrays.)

        self.energy_bill = self.cash_flows.sum() + self.tariff.fixed_charge * self.ts.get_num_days() + self.demand_charge

        if self.name == 'retailer':
            self.total_payment = self.energy_bill
        else:
            # capex, opex in $, energy in c (because tariffs in c/kWh)
            self.total_payment = self.energy_bill + \
                                 self.local_solar_bill + \
                                 (self.pv_capex_repayment +
                                  self.en_capex_repayment +
                                  self.en_opex +
                                  self.bat_capex_repayment) * 100
            

        # --------
        # Calc NPV
        # --------
        self.npv = -sum(self.total_payment / (1 + self.scenario.a_rate / 12) ** t
                        for t in np.arange(1, 12 * self.scenario.a_term))