# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import pandas as pd
import numpy as np
import statsmodels.api as sm
import os

def run_analysis():
    data_path = "/home/node/work/projects/economics_v1/data/panel_data.csv"
    df = pd.read_csv(data_path)
    df["country_id"] = df["country"].astype("category").cat.codes
    df = df.set_index(["country_id", "year"])
    log_vars = ["gdp_per_capita", "capital_stock", "labor_force", "human_capital", "tfp"]
    for var in log_vars:
        df["ln_" + var] = np.log(df[var])
    policy_vars = ["trade_openness", "government_expenditure_share"]
    for var in policy_vars:
        df[var + "_std"] = (df[var] - df[var].mean()) / df[var].std()
    df["ln_investment_rate"] = np.log(df["investment_rate"])
    df.to_csv("data/processed_panel.csv")
    df["ln_investment_rate_lag"] = df.groupby("country_id")["ln_investment_rate"].shift(1)
    df_clean = df.dropna()
    exog_vars = ["ln_investment_rate_lag", "ln_gdp_per_capita", "trade_openness_std", "government_expenditure_share_std"]
    exog = sm.add_constant(df_clean[exog_vars])
    endog = df_clean["ln_investment_rate"]
    model = sm.PanelLM(endog, exog, entity_effects=True, time_effects=True)
    res = model.fit()
    with open("data/regression_results.txt", "w") as f:
        f.write(str(res.summary()))
    print("\n--- Fixed Effects Panel Regression Results ---")
    print(res.summary())

if __name__ == "__main__":
    run_analysis()