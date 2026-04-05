1. **Data Pre-processing and Stationarity Diagnostics**
   - Log-transform all level variables (`gdp_per_capita`, `capital_stock`, `labor_force`, `human_capital`, `tfp`) to linearize the Cobb-Douglas production function.
   - Perform Levin-Lin-Chu (LLC) unit root tests on all log-transformed series. If non-stationarity is detected, proceed with first-differencing for the dynamic panel estimation.
   - Standardize and mean-center policy variables (`trade_openness`, `government_expenditure_share`) to ensure interaction terms are interpretable and to mitigate multicollinearity.

2. **System GMM Specification for Endogenous Investment**
   - Implement a System GMM estimator (combining Arellano-Bond difference and Blundell-Bond level equations) to model the investment rate: $\ln(s_{i,t}) = \gamma_0 + \gamma_1 \ln(s_{i,t-1}) + \gamma_2 \ln(Y/L)_{i,t} + \gamma_3 \text{Policy}_{i,t} + \mu_i + \epsilon_{i,t}$.
   - Treat policy variables as exogenous/predetermined to preserve degrees of freedom.
   - Apply the "collapse" option to the instrument matrix and limit lag depth (e.g., $t-2$ to $t-4$) to prevent instrument proliferation.

3. **Joint Estimation of Structural Parameters**
   - Estimate the production function and capital accumulation equation as a system. Use residuals from the production function estimation as a proxy for unobserved TFP ($A$) to maintain consistency.
   - Define the system: (1) $\ln(Y/L)_{i,t} = \beta_0 + 0.35 \ln(K/L)_{i,t} + 0.65 \ln(H)_{i,t} + \ln(A)_{i,t}$ and (2) $\Delta \ln(K)_{i,t} = \ln(s_{i,t} \cdot (Y_{i,t}/K_{i,t}) + (1-\delta))$.
   - Estimate $\delta$ as a parameter within a constrained optimization framework (range 0.03–0.15) to ensure it remains economically realistic.

4. **Steady-State Calculation and Transition Gap**
   - Calculate the target steady-state capital stock ($K^*_{i,t}$) using the predicted investment rate ($\hat{s}_{i,t}$) derived from the GMM model in Step 2 and the estimated depreciation rate $\delta$.
   - Define the "distance to steady-state" as $D_{i,t} = \ln(K^*_{i,t}) - \ln(K_{i,t})$, ensuring this metric is purged of raw measurement noise.

5. **Instrumented Policy Moderation Analysis**
   - Estimate the moderated transition model: $\Delta \ln(K_{i,t}) = \beta_0 + \beta_1 D_{i,t} + \beta_2 (D_{i,t} \times \text{Policy}_{i,t}) + \mu_i + \epsilon_{i,t}$.
   - Instrument the interaction term $(D_{i,t} \times \text{Policy}_{i,t})$ by interacting the instruments used for $D_{i,t}$ with the policy variables.
   - Calculate the marginal effect of $D_{i,t}$ on capital growth at the 25th, 50th, and 75th percentiles of the policy variables to interpret the acceleration/dampening effects.

6. **Model Validation and Diagnostic Testing**
   - Perform the Arellano-Bond test for AR(2) serial correlation.
   - Conduct the Hansen J-test for over-identifying restrictions and the "Difference-in-Hansen" test to specifically validate the additional moment conditions introduced by the level equations in the System GMM.
   - Calculate the Kleibergen-Paap rk Wald F-statistic to confirm instrument strength.

7. **Robustness and Stability Analysis**
   - Perform sub-sample analysis (high-income vs. low-income groups) to verify if the investment-income elasticity and policy moderation effects ($\beta_2$) are stable.
   - Systematically vary the lag depth of instruments to assess the sensitivity of structural parameter estimates, ensuring the significance of $\beta_2$ holds across different specifications.