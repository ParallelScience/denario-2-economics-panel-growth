# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from linearmodels.panel import PanelOLS
import time
import os

def run_analysis():
    data_path = "/home/node/work/projects/economics_v1/data/panel_data.csv"
    df = pd.read_csv(data_path)
    desc_stats = df.describe().loc[['mean', 'std', 'min', 'max']]
    print("Descriptive Statistics:\n", desc_stats)
    timestamp = int(time.time())
    plt.figure(figsize=(10, 6))
    plt.scatter(df['gdp_per_capita'], df['investment_rate'], alpha=0.5, s=10)
    plt.title("Correlation: GDP per Capita vs Investment Rate")
    plt.xlabel("GDP per Capita")
    plt.ylabel("Investment Rate")
    plt.grid(True)
    plot_path = os.path.join("data", "corr_plot_" + str(timestamp) + ".png")
    plt.savefig(plot_path, dpi=300)
    print("Correlation plot saved to " + plot_path)
    log_vars = ['gdp_per_capita', 'capital_stock', 'labor_force', 'human_capital', 'tfp']
    for var in log_vars:
        df['ln_' + var] = np.log(df[var])
    policy_vars = ['trade_openness', 'government_expenditure_share']
    for var in policy_vars:
        df[var + '_std'] = (df[var] - df[var].mean()) / df[var].std()
    print("\nLevin-Lin-Chu (ADF proxy) Unit Root Test Results:")
    for var in ['ln_gdp_per_capita', 'ln_capital_stock', 'ln_human_capital']:
        result = adfuller(df[var].dropna())
        print(var + " p-value: " + str(result[1]))
    df = df.set_index(['country', 'year'])
    exog = sm.add_constant(df[['ln_gdp_per_capita', 'trade_openness_std', 'government_expenditure_share_std']])
    endog = np.log(df['investment_rate'])
    ols_model = sm.OLS(endog, exog).fit()
    print("\nOLS Regression Summary:")
    print(ols_model.summary())
    fe_model = PanelOLS(endog, exog, entity_effects=True).fit()
    print("\nFixed Effects Regression Summary:")
    print(fe_model.summary)
    with open(os.path.join("data", "ols_summary_" + str(timestamp) + ".txt"), "w") as f:
        f.write(str(ols_model.summary()))
    with open(os.path.join("data", "fe_summary_" + str(timestamp) + ".txt"), "w") as f:
        f.write(str(fe_model.summary))
    print("\nRegression summaries saved to data/ folder.")

if __name__ == '__main__':
    run_analysis()