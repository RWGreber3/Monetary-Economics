import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
import pandas as pd

class Model_DIS_INF:
    def __init__(self, target_inv_sales_ratio, inventory_correction,
                 ex_sales_weight, labor_productivity, int_margin, mark_up,
                 autonomous_consumption, prop_consume_discret_income, prop_consume_wealth,
                 income_expect_weight, real_loan_rate, autonomous_wage_target, labor_productivity_share,
                 wage_adjustment):
        self.target_inv_sales_ratio = target_inv_sales_ratio
        self.inventory_correction = inventory_correction
        self.ex_sales_weight = ex_sales_weight
        self.labor_productivity = labor_productivity
        self.int_margin = int_margin
        self.mark_up = mark_up
        self.autonomous_consumption = autonomous_consumption
        self.prop_consume_discret_income = prop_consume_discret_income
        self.prop_consume_wealth = prop_consume_wealth
        self.income_expect_weight = income_expect_weight
        self.real_loan_rate = real_loan_rate
        self.autonomous_wage_target = autonomous_wage_target
        self.labor_productivity_share = labor_productivity_share
        self.wage_adjustment = wage_adjustment
        self.model_data = pd.DataFrame(columns=['real_output', 'real_inv_target', 'ex_real_inv', 'real_inv', 'ex_real_sales', 'real_sales',
                                                'employment',  'wage_bill', 'unit_cost', 'nominal_inventory', 'nominal_sales', 'entrepeneurial_profits',
                                                'price_level', 'loan_demand', 'loan_supply', 'deposits_supplied', 'deposit_rate', 'bank_profits',
                                                'inflation', 'real_loan_rate', 'loan_rate', 'nominal_dis_income', 'deposits_held', 'haig_simons_dis_income',
                                                'real_dis_income', 'nominal_consumption', 'real_deposits', 'real_consumption', 'ex_real_hs_dis_income',
                                                'real_wage_target', 'wage_rate'])
        #self.steady_state_solution()


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
        prev_wage_rate = self.model_data.iloc[-1]['wage_rate']
        prev_wage_target = self.model_data.iloc[-1]['real_wage_target']
        prev_price_level = self.model_data.iloc[-1]['price_level']
        ex_real_hs_dis_income = (self.income_expect_weight * prev_per_hs_dis_income + (1-self.income_expect_weight) * prev_per_exp_hs_dis_income)
        ex_real_sales = self.ex_sales_weight * prev_per_sales + (1 - self.ex_sales_weight) * prev_per_exp_sales
        real_consumption = self.autonomous_consumption + self.prop_consume_discret_income * ex_real_hs_dis_income + self.prop_consume_wealth * prev_per_real_deposits
        real_sales = real_consumption
        real_inv_target = self.target_inv_sales_ratio * real_sales
        ex_real_inv = prev_per_real_inv + self.inventory_correction * (real_inv_target - prev_per_real_inv)
        real_output = ex_real_sales + ex_real_inv - prev_per_real_inv
        real_inv = prev_per_real_inv + real_output - real_sales
        employment = real_output / self.labor_productivity
        real_wage_target = self.autonomous_wage_target + self.labor_productivity_share * self.labor_productivity
        wage_rate = prev_wage_rate * (1 + self.wage_adjustment * (prev_wage_target - (prev_wage_rate / prev_price_level)))
        wage_bill = employment * wage_rate
        unit_cost = wage_bill / real_output
        nominal_inventory = real_inv * unit_cost
        price_level = (1 + self.mark_up) * (1 + self.real_loan_rate * self.target_inv_sales_ratio) * unit_cost
        loan_demand = nominal_inventory
        loan_supply = loan_demand
        deposits_supplied = loan_supply
        inflation = (unit_cost - prev_unit_cost) / prev_unit_cost
        loan_rate = (1 + inflation) * (1 + self.real_loan_rate) - 1
        nominal_sales = real_sales * price_level
        entrepeneurial_profits = nominal_sales - wage_bill + (nominal_inventory - prev_nom_inv) - prev_loan_rate * prev_nom_inv
        deposit_rate = loan_rate - self.int_margin
        bank_profits = prev_loan_rate * prev_per_loans - prev_deposit_rate * prev_per_deposits
        nominal_dis_income = wage_bill + entrepeneurial_profits + bank_profits + prev_deposit_rate * prev_per_deposits
        nominal_consumption = real_consumption * price_level
        deposits_held = nominal_dis_income - nominal_consumption + prev_per_deposits
        real_deposits = deposits_held / price_level
        haig_simons_dis_income = real_consumption + real_deposits - prev_per_real_deposits
        real_dis_income = nominal_dis_income / price_level
        

