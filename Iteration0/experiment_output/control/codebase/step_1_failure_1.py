# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os

def process_economics_data():
    input_path = "/home/node/work/projects/economics_v1/data/panel_data.csv"
    df = pd.read_csv(input_path)
    df = df.sort_values(['country', 'year'])
    log_vars = ['gdp_per_capita', 'capital_stock', 'labor_force', 'human_capital', 'tfp']
    for var in log_vars:
        df['ln_' + var] = np.log(df[var])
    for var in ['trade_openness', 'government_expenditure_share']:
        df[var + '_z'] = (df[var] - df[var].mean()) / df[var].std()
    for var in log_vars:
        df['dln_' + var] = df.groupby('country')['ln_' + var].diff()
    df['dln_y_l'] = df['dln_gdp_per_capita']
    df['dln_k_l'] = df['dln_capital_stock'] - df['dln_labor_force']
    df['dln_h'] = df['dln_human_capital']
    df['solow_tfp_growth'] = df['dln_y_l'] - 0.35 * df['dln_k_l'] - 0.65 * df['dln_h']
    corr_matrix = df[['ln_gdp_per_capita', 'ln_capital_stock', 'ln_labor_force', 'ln_human_capital', 'ln_tfp']].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix of Primary Variables")
    plt.tight_layout()
    timestamp = int(time.time())
    heatmap_path = os.path.join("data", "correlation_heatmap_1_" + str(timestamp) + ".png")
    plt.savefig(heatmap_path, dpi=300)
    print("Correlation heatmap saved to " + heatmap_path)
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='year', y='tfp', hue='country', legend=False, alpha=0.3)
    plt.title("Cross-Country TFP Dispersion (1990-2019)")
    plt.xlabel("Year")
    plt.ylabel("TFP Index")
    plt.tight_layout()
    tfp_plot_path = os.path.join("data", "tfp_dispersion_1_" + str(timestamp) + ".png")
    plt.savefig(tfp_plot_path, dpi=300)
    print("TFP dispersion plot saved to " + tfp_plot_path)
    df.to_csv(os.path.join("data", "processed_panel_data.csv"), index=False)
    print("Processed data saved to data/processed_panel_data.csv")
    print("\nSummary Statistics of Key Variables:")
    print(df[['ln_gdp_per_capita', 'ln_capital_stock', 'solow_tfp_growth']].describe())

if __name__ == '__main__':
    process_economics_data()