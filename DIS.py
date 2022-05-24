import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
import pandas as pd

class Model_DIS:
    def __init__(self, target_inv_sales_ratio, inventory_correction,
                 ex_sales_weight, labor_productivity, wage_rate, int_margin, mark_up,
                 autonomous_consumption, prop_consume_discret_income, prop_consume_wealth,
                 income_expect_weight, loan_rate):
        self.target_inv_sales_ratio = target_inv_sales_ratio
        self.inventory_correction = inventory_correction
        self.ex_sales_weight = ex_sales_weight
        self.labor_productivity = labor_productivity
        self.wage_rate = wage_rate
        self.int_margin = int_margin
        self.mark_up = mark_up
        self.autonomous_consumption = autonomous_consumption
        self.prop_consume_discret_income = prop_consume_discret_income
        self.prop_consume_wealth = prop_consume_wealth
        self.income_expect_weight = income_expect_weight
        self.loan_rate = loan_rate
        self.deposit_rate = loan_rate - int_margin
        self.model_data = pd.DataFrame(columns=['real_output', 'real_inv_target', 'ex_real_inv', 'real_inv', 'ex_real_sales',
                                                'real_sales', 'employment',  'wage_bill', 'unit_cost', 'nominal_inventory', 'nominal_sales', 'price_level',
                                                'norm_hist_unit_cost', 'entrepeneurial_profits', 'loan_demand', 'loan_supply', 'deposits_supplied',
                                                'loan_rate', 'deposit_rate', 'bank_profits', 'nominal_dis_income', 'deposits_held', 'haig_simons_dis_income',
                                                'nominal_consumption', 'real_deposits', 'real_consumption', 'ex_real_hs_dis_income'])
        self.steady_state_solution()


    def steady_state_solution(self):
        steady_state_unit_cost = self.wage_rate / self.labor_productivity
        steady_state_nhuc = (1 + self.target_inv_sales_ratio * self.loan_rate) * steady_state_unit_cost
        steady_state_price = (1 + self.mark_up) * steady_state_nhuc
        steady_haig_simons_dis_income = self.autonomous_consumption / ( 1 - self.prop_consume_discret_income -
                                        self.prop_consume_wealth * self.target_inv_sales_ratio *
                                        (steady_state_unit_cost / steady_state_price))
        ex_real_hs_dis_income = steady_haig_simons_dis_income
        real_consumption = steady_haig_simons_dis_income
        real_sales = steady_haig_simons_dis_income
        real_output = steady_haig_simons_dis_income
        ex_real_sales = steady_haig_simons_dis_income
        employment = steady_haig_simons_dis_income / self.labor_productivity
        real_inv_target = self.target_inv_sales_ratio * real_sales
        ex_real_inv = real_inv_target
        real_inv = real_inv_target
        wage_bill = employment * self.wage_rate
        nominal_inventory = real_inv * steady_state_unit_cost
        nominal_sales = steady_state_price * real_sales
        entrepeneurial_profits = nominal_sales - wage_bill - (self.loan_rate * nominal_inventory)
        loan_demand = nominal_inventory
        loan_supply = loan_demand
        deposits_supplied = loan_supply
        bank_profits = (self.loan_rate * loan_supply) - (self.deposit_rate * deposits_supplied)
        nominal_dis_income = wage_bill + entrepeneurial_profits + bank_profits + (self.deposit_rate * deposits_supplied)
        deposits_held = deposits_supplied
        nominal_consumption = real_consumption * steady_state_price
        real_deposits = deposits_held / steady_state_price
        df_row = {'real_output': real_output,
                  'real_inv_target' : real_inv_target,
                  'ex_real_inv' : ex_real_inv,
                  'real_inv' : real_inv,
                  'ex_real_sales' : ex_real_sales,
                  'real_sales' : real_sales,
                  'employment' : employment,
                  'wage_bill' : wage_bill,
                  'unit_cost' : steady_state_unit_cost,
                  'nominal_inventory' : nominal_inventory,
                  'nominal_sales' : nominal_sales,
                  'price_level' : steady_state_price,
                  'norm_hist_unit_cost' : steady_state_nhuc,
                  'entrepeneurial_profits' : entrepeneurial_profits,
                  'loan_demand' : loan_demand,
                  'loan_supply' : loan_supply,
                  'deposits_supplied' : deposits_supplied,
                  'loan_rate' : self.loan_rate,
                  'deposit_rate' : self.deposit_rate,
                  'bank_profits' : bank_profits,
                  'nominal_dis_income' : nominal_dis_income,
                  'deposits_held' : deposits_held,
                  'haig_simons_dis_income' : steady_haig_simons_dis_income,
                  'nominal_consumption' : nominal_consumption,
                  'real_deposits' : real_deposits,
                  'real_consumption' : real_consumption,
                  'ex_real_hs_dis_income' : ex_real_hs_dis_income}
        self.model_data = self.model_data.append(df_row, ignore_index=True)


    def shock_method(self, target_inv_sales_ratio=0, inventory_correction=0,
                     ex_sales_weight=0, labor_productivity=0, wage_rate=0, int_margin=0, mark_up=0,
                     autonomous_consumption=0, prop_consume_discret_income=0, prop_consume_wealth=0,
                     income_expect_weight=0, loan_rate=0):
        if target_inv_sales_ratio != 0:
            self.target_inv_sales_ratio = target_inv_sales_ratio
        if inventory_correction != 0:
            self.inventory_correction = inventory_correction
        if ex_sales_weight != 0:
            self.ex_sales_weight = ex_sales_weight
        if labor_productivity != 0:
            self.labor_productivity = labor_productivity
        if wage_rate != 0:
            self.wage_rate = wage_rate
        if int_margin != 0:
            self.int_margin = int_margin
        if mark_up != 0:
            self.mark_up = mark_up
        if autonomous_consumption != 0:
            self.autonomous_consumption = autonomous_consumption
        if prop_consume_discret_income != 0:
            self.prop_consume_discret_income = prop_consume_discret_income
        if prop_consume_wealth != 0:
            self.prop_consume_wealth = prop_consume_wealth
        if income_expect_weight != 0:
            self.income_expect_weight = income_expect_weight
        if loan_rate != 0:
            self.loan_rate = loan_rate


    def one_step_solution(self):
        prev_per_hs_dis_income = self.model_data.iloc[-1]['haig_simons_dis_income']
        prev_per_exp_hs_dis_income = self.model_data.iloc[-1]['ex_real_hs_dis_income']
        prev_per_sales = self.model_data.iloc[-1]['real_sales']
        prev_per_exp_sales = self.model_data.iloc[-1]['ex_real_sales']
        prev_loan_rate = self.model_data.iloc[-1]['loan_rate']
        prev_per_loans = self.model_data.iloc[-1]['loan_supply']
        prev_deposit_rate = self.model_data.iloc[-1]['deposit_rate']
        prev_per_deposits = self.model_data.iloc[-1]['deposits_held']
        prev_per_real_deposits = self.model_data.iloc[-1]['real_deposits']
        prev_per_real_inv = self.model_data.iloc[-1]['real_inv']
        prev_unit_cost = self.model_data.iloc[-1]['unit_cost']
        prev_nom_inv = self.model_data.iloc[-1]['nominal_inventory']
        ex_real_hs_dis_income = (self.income_expect_weight * prev_per_hs_dis_income + (1-self.income_expect_weight) * prev_per_exp_hs_dis_income)
        ex_real_sales = self.ex_sales_weight * prev_per_sales + (1 - self.ex_sales_weight) * prev_per_exp_sales
        bank_profits = prev_loan_rate * prev_per_loans - prev_deposit_rate * prev_per_deposits
        real_consumption = self.autonomous_consumption + self.prop_consume_discret_income * ex_real_hs_dis_income + self.prop_consume_wealth * prev_per_real_deposits
        real_sales = real_consumption
        real_inv_target = self.target_inv_sales_ratio * real_sales
        ex_real_inv = prev_per_real_inv + self.inventory_correction * (real_inv_target - prev_per_real_inv)
        real_output = ex_real_sales + ex_real_inv - prev_per_real_inv
        real_inv = prev_per_real_inv + real_output - real_sales
        employment = real_output / self.labor_productivity
        wage_bill = employment * self.wage_rate
        unit_cost = wage_bill / real_output
        nominal_inventory = real_inv * unit_cost
        loan_demand = nominal_inventory
        loan_supply = loan_demand
        deposits_supplied = loan_supply
        norm_hist_unit_cost = (1 - self.target_inv_sales_ratio) * unit_cost + self.target_inv_sales_ratio * (1 + prev_loan_rate) * prev_unit_cost
        price_level = (1 + self.mark_up) * norm_hist_unit_cost
        nominal_sales = real_sales * price_level
        entrepeneurial_profits = nominal_sales - wage_bill + (nominal_inventory - prev_nom_inv) - prev_loan_rate * prev_nom_inv
        nominal_dis_income = wage_bill + entrepeneurial_profits + bank_profits + prev_deposit_rate * prev_per_deposits
        nominal_consumption = real_consumption * price_level
        deposits_held = nominal_dis_income - nominal_consumption + prev_per_deposits
        real_deposits = deposits_held / price_level
        haig_simons_dis_income = real_consumption + real_deposits - prev_per_real_deposits
        df_row = {'real_output': real_output,
                  'real_inv_target' : real_inv_target,
                  'ex_real_inv' : ex_real_inv,
                  'real_inv' : real_inv,
                  'ex_real_sales' : ex_real_sales,
                  'real_sales' : real_sales,
                  'employment' : employment,
                  'wage_bill' : wage_bill,
                  'unit_cost' : unit_cost,
                  'nominal_inventory' : nominal_inventory,
                  'nominal_sales' : nominal_sales,
                  'price_level' : price_level,
                  'norm_hist_unit_cost' : norm_hist_unit_cost,
                  'entrepeneurial_profits' : entrepeneurial_profits,
                  'loan_demand' : loan_demand,
                  'loan_supply' : loan_supply,
                  'deposits_supplied' : deposits_supplied,
                  'loan_rate' : self.loan_rate,
                  'deposit_rate' : self.deposit_rate,
                  'bank_profits' : bank_profits,
                  'nominal_dis_income' : nominal_dis_income,
                  'deposits_held' : deposits_held,
                  'haig_simons_dis_income' : haig_simons_dis_income,
                  'nominal_consumption' : nominal_consumption,
                  'real_deposits' : real_deposits,
                  'real_consumption' : real_consumption,
                  'ex_real_hs_dis_income' : ex_real_hs_dis_income}
        self.model_data = self.model_data.append(df_row, ignore_index=True)


    def iterative_solution(self, time):
        for i in range(time):
            self.one_step_solution()


    def print_model_data(self):
        self.model_data.to_csv('Model_Data')
        print(self.model_data)


inv_target_param = 0.15
inventory_correction_param = 0.25
ex_sales_weight_param = 0.75
labor_productivity_param = 1
wage_rate_param = 0.86
int_margin_param = 0.02
mark_up_param = 0.25
autonomous_consumption_param = 15
prop_consume_dis_income_param = 0.8
prop_consume_wealth_param = 0.1
income_expect_adj_param = 0.75
loan_rate_param = 0.04

x = Model_DIS(inv_target_param, inventory_correction_param, ex_sales_weight_param, labor_productivity_param,
              wage_rate_param, int_margin_param, mark_up_param, autonomous_consumption_param,
              prop_consume_dis_income_param, prop_consume_wealth_param, income_expect_adj_param, loan_rate_param)
x.shock_method(mark_up=0.3)
x.iterative_solution(100)
x.print_model_data()
