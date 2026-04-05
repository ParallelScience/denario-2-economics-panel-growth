1. **Data Preprocessing and Stationarity Assessment**
   - Transform all level variables (`gdp_per_capita`, `capital_stock`, `labor_force`, `human_capital`, `tfp`) into natural logarithms.
   - Compute growth rates for key variables and first-difference the investment rate to assess integration properties.
   - Conduct panel unit root tests (e.g., Levin-Lin-Chu) to confirm stationarity.
   - Standardize policy variables (`trade_openness`, `government_expenditure_share`) into z-scores to facilitate interpretation of interaction effects.

2. **Baseline Growth Accounting Decomposition**
   - Implement the Solow-Swan framework using structural parameters ($\alpha = 0.35$).
   - Calculate TFP growth as the Solow residual: $\Delta \ln(A) = \Delta \ln(Y/L) - 0.35 \Delta \ln(K/L) - 0.65 \Delta \ln(H)$.
   - Visualize cross-country TFP dispersion to establish baseline productivity heterogeneity.

3. **Estimation of Endogenous Investment Elasticity**
   - Specify a dynamic panel model where $s_{i,t}$ is a function of lagged `gdp_per_capita`.
   - Apply System GMM to address endogeneity, treating `gdp_per_capita` as endogenous.
   - Use a "collapsed" instrument matrix and limit lag depth to prevent instrument proliferation and overfitting.

4. **Dynamic Panel Specification for Transition Speed**
   - Define the transition equation: $\Delta \ln(K_{i,t}) = \beta_0 + \beta_1 \ln(K_{i,t-1}) + \beta_2 s_{i,t} + \gamma X_{i,t} + \mu_i + \epsilon_{i,t}$.
   - Ensure the model accounts for the structural depreciation rate (0.07) by interpreting $\beta_1$ as the net convergence rate.
   - Treat $s_{i,t}$ as endogenous due to the simultaneous feedback loop with $Y_t$ and $K_t$.

5. **Interaction Analysis for Policy Moderators**
   - Mean-center policy variables before creating interaction terms with $s_{i,t}$ to reduce multicollinearity.
   - Include main effects for all interacted variables to avoid omitted variable bias.
   - Estimate the model: $\Delta \ln(K_{i,t}) = \dots + \delta_1 (s_{i,t} \times \text{Trade}_{centered}) + \delta_2 (s_{i,t} \times \text{GovExp}_{centered}) + \dots$.

6. **Model Diagnostics and Robustness Checks**
   - Perform the Hansen J-test for over-identifying restrictions and the Arellano-Bond test for AR(2) serial correlation.
   - Report the Kleibergen-Paap rk Wald F-statistic to check for weak instrument bias.
   - Compare estimated coefficients against the theoretical structural parameters ($\alpha=0.35, \delta=0.07$) to validate recovery of the DGP.

7. **Quantification of Transition Velocity**
   - Calculate the "half-life" of convergence for each country based on $\beta_1$.
   - Derive the "implied" steady-state capital stock from the estimated model and compare it against the theoretical steady-state derived from the structural parameters.
   - Simulate the impact of a one-standard-deviation change in policy variables on the predicted path of capital deepening to visualize shifts in growth trajectories.