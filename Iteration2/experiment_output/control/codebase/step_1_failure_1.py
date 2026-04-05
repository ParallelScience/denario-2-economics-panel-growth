# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import pandas as pd
import numpy as np
from linearmodels.panel import DynamicPanelModel
from linearmodels.panel.unitroot import levinlinchu
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
    print("--- Levin-Lin-Chu Unit Root Test Results ---")
    for var in ["ln_gdp_per_capita", "ln_capital_stock", "ln_tfp"]:
        llc = levinlinchu(df[var], lags=1)
        print("Variable: " + var + " | P-value: " + str(round(llc.pvalue, 4)))
    df["ln_investment_rate_lag"] = df.groupby("country_id")["ln_investment_rate"].shift(1)
    df_gmm = df.dropna()
    exog = df_gmm[["ln_gdp_per_capita", "trade_openness_std", "government_expenditure_share_std"]]
    endog = df_gmm["ln_investment_rate"]
    mod = DynamicPanelModel(dependent=endog, exog=exog, lags=1, entity_effects=True, time_effects=True)
    res = mod.fit(method="gmm", instruments=exog)
    with open("data/gmm_results.txt", "w") as f:
        f.write(str(res.summary))
    print("\n--- System GMM Estimation Results ---")
    print(res.summary)
    print("\n--- Diagnostic Statistics ---")
    print("Hansen J-test P-value: " + str(round(res.hansen.pvalue, 4)))
    print("Arellano-Bond AR(2) P-value: " + str(round(res.arellano_bond(2).pvalue, 4)))

if __name__ == "__main__":
    run_analysis()