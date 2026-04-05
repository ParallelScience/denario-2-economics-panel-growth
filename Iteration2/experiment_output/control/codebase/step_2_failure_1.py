# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import time

def run_step_2():
    data_dir = "data/"
    df = pd.read_csv(os.path.join(data_dir, "processed_panel.csv"))
    df = df.set_index(["country_id", "year"])

    def objective(delta):
        k_next = df.groupby("country_id")["capital_stock"].shift(-1)
        k_curr = df["capital_stock"]
        y_curr = df["gdp"]
        s_curr = df["investment_rate"]
        pred_k_next = (1 - delta) * k_curr + s_curr * y_curr
        mask = k_next.notna()
        return np.sum((k_next[mask] - pred_k_next[mask])**2)

    res = minimize(objective, x0=[0.07], bounds=[(0.03, 0.15)])
    delta_est = res.x[0]
    
    print("Estimated Depreciation Rate (delta): " + str(round(delta_est, 4)))

    df["k_star"] = (df["investment_rate"] * df["gdp"]) / delta_est
    df["dist_to_ss"] = np.log(df["k_star"]) - np.log(df["capital_stock"])
    df["delta_ln_k"] = df.groupby("country_id")["capital_stock"].apply(lambda x: np.log(x).diff().shift(-1))

    df_clean = df.dropna(subset=["dist_to_ss", "delta_ln_k", "trade_openness_std", "government_expenditure_share_std"])
    
    exog = df_clean[["dist_to_ss", "trade_openness_std", "government_expenditure_share_std"]].copy()
    exog["inter_trade"] = exog["dist_to_ss"] * exog["trade_openness_std"]
    exog["inter_gov"] = exog["dist_to_ss"] * exog["government_expenditure_share_std"]
    exog = sm.add_constant(exog)
    
    model = sm.OLS(df_clean["delta_ln_k"], exog)
    results = model.fit(cov_type="cluster", cov_kwds={"groups": df_clean.index.get_level_values("country_id")})
    
    print("\n--- Moderated Transition Model Results ---")
    print(results.summary())

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    for i, var in enumerate(["trade_openness_std", "government_expenditure_share_std"]):
        pcts = [df_clean[var].quantile(0.25), df_clean[var].quantile(0.5), df_clean[var].quantile(0.75)]
        labels = ["25th Pct", "50th Pct", "75th Pct"]
        
        for p, l in zip(pcts, labels):
            beta_dist = results.params["dist_to_ss"]
            beta_inter = results.params["inter_trade"] if "trade" in var else results.params["inter_gov"]
            marginal_effect = beta_dist + beta_inter * p
            axes[i].bar(l, marginal_effect, alpha=0.7)
            
        axes[i].set_title("Marginal Effect of Distance to SS: " + var)
        axes[i].set_ylabel("Effect on Capital Growth")
        axes[i].grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    timestamp = int(time.time())
    plot_path = os.path.join(data_dir, "transition_analysis_1_" + str(timestamp) + ".png")
    plt.savefig(plot_path, dpi=300)
    print("\nPlot saved to " + plot_path)

if __name__ == "__main__":
    run_step_2()