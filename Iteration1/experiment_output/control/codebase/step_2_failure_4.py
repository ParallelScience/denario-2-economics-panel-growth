# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.iv import IV2SLS
import time

def run_gmm_analysis():
    data_path = '/home/node/work/projects/economics_v1/data/panel_data.csv'
    df = pd.read_csv(data_path)
    log_vars = ['gdp_per_capita', 'capital_stock', 'labor_force', 'human_capital', 'tfp']
    for var in log_vars:
        df['ln_' + var] = np.log(df[var])
    policy_vars = ['trade_openness', 'government_expenditure_share']
    for var in policy_vars:
        df[var + '_std'] = (df[var] - df[var].mean()) / df[var].std()
    df = df.set_index(['country', 'year'])
    endog_inv = np.log(df['investment_rate'])
    exog_inv = df[['trade_openness_std', 'government_expenditure_share_std']]
    endog_regressor = df[['ln_gdp_per_capita']]
    df['ln_gdp_per_capita_lag1'] = df.groupby('country')['ln_gdp_per_capita'].shift(1)
    instruments = df[['ln_gdp_per_capita_lag1']]
    iv_model = IV2SLS(dependent=endog_inv, exog=exog_inv, endog=endog_regressor, instruments=instruments)
    iv_res = iv_model.fit(cov_type='clustered', clusters=df.index.get_level_values('country'))
    print('IV2SLS Results (Investment Function):')
    print(iv_res)
    df['ln_y_l'] = df['ln_gdp_per_capita'] - df['ln_labor_force']
    df['ln_k_l'] = df['ln_capital_stock'] - df['ln_labor_force']
    prod_exog = sm.add_constant(df[['ln_k_l', 'ln_human_capital', 'ln_tfp']])
    prod_res = sm.OLS(df['ln_y_l'], prod_exog).fit()
    print('\nStructural Production Function Recovery:')
    print(prod_res.summary())
    df['k_growth'] = (df['capital_stock'].groupby('country').shift(-1) - df['capital_stock']) / df['capital_stock']
    df['y_k_ratio'] = df['gdp'] / df['capital_stock']
    df['s_y_k'] = df['investment_rate'] * df['y_k_ratio']
    depr_data = df.dropna(subset=['k_growth', 's_y_k'])
    depr_res = sm.OLS(depr_data['k_growth'], depr_data['s_y_k']).fit()
    print('\nDepreciation Rate Recovery (Theoretical: 0.07):')
    print('Estimated Delta: ' + str(-depr_res.params[0]))
    df['interaction'] = df['ln_gdp_per_capita'] * df['trade_openness_std']
    inter_exog = sm.add_constant(df[['ln_gdp_per_capita', 'trade_openness_std', 'interaction']])
    inter_res = sm.OLS(endog_inv, inter_exog).fit()
    print('\nPolicy Moderation Analysis (Interaction Model):')
    print(inter_res.summary())
    timestamp = int(time.time())
    with open(os.path.join('data', 'gmm_results_' + str(timestamp) + '.txt'), 'w') as f:
        f.write(str(iv_res))
        f.write('\n\nProduction Function:\n' + str(prod_res.summary()))
        f.write('\n\nInteraction Model:\n' + str(inter_res.summary()))

if __name__ == '__main__':
    run_gmm_analysis()