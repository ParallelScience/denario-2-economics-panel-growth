# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import time
from linearmodels.panel import DynamicPanelGMM

def run_dynamic_analysis():
    df = pd.read_csv("data/processed_panel_data.csv")
    df = df.set_index(['country', 'year'])
    df['ln_K_lag'] = df.groupby('country')['ln_capital_stock'].shift(1)
    df['dln_K'] = df['ln_capital_stock'] - df['ln_K_lag']
    df['s_trade'] = df['investment_rate'] * df['trade_openness_z']
    df['s_gov'] = df['investment_rate'] * df['government_expenditure_share_z']
    exog = df[['ln_K_lag', 'investment_rate', 's_trade', 's_gov']]
    endog = df['dln_K']
    mod = DynamicPanelGMM(endog, exog=exog, entity_effects=True, time_effects=False, drop_first=True)
    res = mod.fit(cov_type='robust')
    print("--- GMM Estimation Results ---")
    print(res.summary)
    beta_1 = res.params['ln_K_lag']
    half_life = -np.log(2) / np.log(1 + beta_1)
    print("\n--- Convergence Diagnostics ---")
    print("Implied Half-life of convergence: " + str(round(half_life, 2)) + " years")
    print("Hansen J-test p-value: " + str(round(res.hansen.pvalue, 4)))
    print("Arellano-Bond AR(2) p-value: " + str(round(res.arellano_bond2.pvalue, 4)))
    years = np.arange(20)
    k_path_high = [1.0]
    k_path_low = [1.0]
    for _ in years[1:]:
        k_path_high.append(k_path_high[-1] * (1 + beta_1 * np.log(k_path_high[-1]) + 0.25 * 1.0 + 0.05 * 1.0))
        k_path_low.append(k_path_low[-1] * (1 + beta_1 * np.log(k_path_low[-1]) + 0.25 * 1.0 - 0.05 * 1.0))
    plt.figure(figsize=(10, 6))
    plt.plot(years, k_path_high, label='High Trade Openness (+1 SD)')
    plt.plot(years, k_path_low, label='Low Trade Openness (-1 SD)')
    plt.title("Simulated Capital Stock Trajectory")
    plt.xlabel("Years")
    plt.ylabel("Relative Capital Stock")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    timestamp = int(time.time())
    plot_path = os.path.join("data", "policy_impact_plot_" + str(timestamp) + ".png")
    plt.savefig(plot_path, dpi=300)
    print("Policy impact plot saved to " + plot_path)

if __name__ == '__main__':
    run_dynamic_analysis()