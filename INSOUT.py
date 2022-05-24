import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
import pandas as pd

class Model_INSOUT:
    def __init__(self,
                 labor_productivity = 1,
                 sales_expectation_adj = .5,
                 base_inventory_sales_target = 0.3612,
                 inventory_sales_adjustment = 3,
                 inventory_correction_factor = 0.5,
                 mark_up = 0.1,
                 autonomous_consumption = 0,
                 prop_consume_income = 0.95,
                 prop_consume_wealth = 0.05,
                 cash_for_consumption = 0.1,
                 expected_income_adj = 0.5,
                 long_bond_rate = 0.027,
                 bill_rate = 0.023,
                 real_govt_expenditure = 25,
                 checking_reserve_req = 0.1,
                 saving_reserve_req = 0.1,
                 min_bank_liq = 0.02,
                 max_bank_liq = 0.04,
                 deposit_to_bill_rate_sens = 0.9,
                 loan_rate_to_profit_sens = 0.02,
                 deposit_rate_to_liq_sens = 0.0002,
                 min_bank_pm = 0.002,
                 max_bank_pm = 0.005,
                 tax_rate = 0.25,
                 lambda1 = [1, 0, 0, 0, 0, 0],
                 lambda2 = [0.52245, 20, 40, -20, -20, -0.06],
                 lambda3 = [0.47311, 40, -20, 40, -20, -0.06],
                 lambda4 = [0.17515, 20, -20, -20, 40, -0.06],
                 omega = [-0.32549, 1, 1.5],
                 omega3 = 0.1,
                 full_employment = 133.28):
        self.labor_productivity = labor_productivity
        self.sales_expectation_adj = sales_expectation_adj
        self.base_inventory_sales_target = base_inventory_sales_target
        self.inventory_sales_adjustment = inventory_sales_adjustment
        self.inventory_correction_factor = inventory_correction_factor
        self.mark_up = mark_up
        self.autonomous_consumption = autonomous_consumption
        self.prop_consume_income = prop_consume_income
        self.prop_consume_wealth = prop_consume_wealth
        self.cash_for_consumption = cash_for_consumption
        self.expected_income_adj = expected_income_adj
        self.long_bond_rate = long_bond_rate
        self.bill_rate = bill_rate
        self.real_govt_expenditure = real_govt_expenditure
        self.checking_reserve_req = checking_reserve_req
        self.saving_reserve_req = saving_reserve_req
        self.min_bank_liq = min_bank_liq
        self.max_bank_liq = max_bank_liq
        self.deposit_to_bill_rate_sens = deposit_to_bill_rate_sens
        self.loan_rate_to_profit_sens = loan_rate_to_profit_sens
        self.deposit_rate_to_liq_sens = deposit_rate_to_liq_sens
        self.min_bank_pm = min_bank_pm
        self.max_bank_pm = max_bank_pm
        self.tax_rate = tax_rate
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.lambda3 = lambda3
        self.lambda4 = lambda4
        self.omega = omega
        self.omega3 = omega3
        self.full_employment = full_employment
        self.model_data = pd.DataFrame(columns=['real_output', 'employment', 'wage_bill', 'unit_cost', 'exp_sales',
                                                'real_inv_target', 'inv_sales_target', 'real_loan_rate', 'ex_real_inv',
                                                'price_level', 'normal_hist_unit_cost', 'real_sales', 'nominal_sales',
                                                'real_inv', 'inv_sales_ratio', 'nominal_inv', 'loan_demand',
                                                'entrepreneurial_profits', 'inflation_rate', 'nominal_dis_income',
                                                'capital_gains', 'nominal_hs_dis_income', 'total_profit',
                                                'nominal_wealth', 'wealth_less_cash', 'real_dis_income',
                                                'real_hs_income', 'real_wealth', 'real_consumption',
                                                'expected_regular_income', 'nominal_consumption',
                                                'nominal_exp_reg_income', 'exp_wealth', 'household_demand_cash',
                                                'exp_wealth_less_cash', 'check_dep_demand', 'save_dep_demand',
                                                'bill_demand', 'bond_demand', 'cash_held', 'bils_held_house',
                                                'bonds_held_house', 'not_check_held', 'check_held', 'check_neg',
                                                'savings_held', 'z2', 'taxes', 'nominal_gov_spend', 'pub_sec_borrow',
                                                'bill_supply', 'bond_supply', 'bond_price', 'bond_rate', 'hpm_supply',
                                                'cash_held_banks', 'bills_held_cb', 'bill_rate', 'advances_supply',
                                                'advance_rate', 'cb_profit', 'cash_supplied_house', 'check_supply',
                                                'saving_supply', 'loan_supply', 'bank_reserves',
                                                'not_bank_bs_constraint', 'not_bank_liquidity_ratio', 'advance_demand',
                                                'z4', 'bank_balance_sheet_con', 'bank_liq_ratio', 'deposit_rate',
                                                'delta_dep_rate', 'z4_2', 'z5', 'bank_profit', 'loan_rate',
                                                'delta_loan_rate', 'z6', 'z7', 'bank_profit_margin', 'real_wage_target',
                                                'wage_rate', 'nominal_output'])




