1. **Data Diagnostics and Pre-processing**
   - Perform a visual correlation analysis between `gdp_per_capita` and `investment_rate` to confirm the presence of the endogenous feedback loop.
   - Transform `gdp_per_capita`, `capital_stock`, `labor_force`, `human_capital`, and `tfp` into natural logarithms.
   - Standardize policy variables (`trade_openness`, `government_expenditure_share`) and mean-center them to facilitate the interpretation of interaction terms.
   - Conduct Levin-Lin-Chu unit root tests on log-transformed series to verify stationarity for dynamic panel estimation.

2. **Baseline Estimation of Investment Elasticity**
   - Specify the structural investment function: $\ln(s_{i,t}) = \gamma_0 + \gamma_1 \ln(Y/L)_{i,t} + \gamma_2 \text{Policy}_{i,t} + \mu_i + \epsilon_{i,t}$.
   - Use a Fixed Effects (FE) estimator to establish a baseline for $\gamma_1$ and account for time-invariant country-specific heterogeneity.
   - Run a simple OLS regression as a benchmark to contrast with the FE and subsequent GMM results, highlighting the impact of endogeneity.

3. **Dynamic Panel GMM for Endogenous Feedback**
   - Implement a System GMM estimator to address the endogeneity of $\ln(Y/L)_{i,t}$.
   - Define the instrument set: use lagged differences of endogenous variables for the level equation and lagged levels of endogenous variables (and predetermined variables like $K$ and $H$) for the difference equation.
   - Use a "collapsed" instrument matrix and limit lag depth (e.g., $t-2$ and beyond) to prevent instrument proliferation.
   - Validate the model using the Hansen J-test for over-identifying restrictions and the Difference-in-Hansen test to verify the validity of the level equations.

4. **Structural Parameter Recovery**
   - Estimate the production function $\ln(Y/L) = \beta_0 + \alpha \ln(K/L) + \beta_H \ln(H) + \ln(A)$ to recover the capital elasticity $\alpha$.
   - Estimate the depreciation rate $\delta$ by regressing the growth rate $\frac{K_{t+1}-K_t}{K_t}$ on the term $(s_t \cdot \frac{Y_t}{K_t})$ using the identity $\frac{K_{t+1}-K_t}{K_t} = s_t(Y_t/K_t) - \delta$.
   - Compare recovered $\alpha$ and $\delta$ against the theoretical DGP values of 0.35 and 0.07.

5. **Policy Moderation Analysis**
   - Estimate the interaction model: $\ln(s_{i,t}) = \gamma_0 + \gamma_1 \ln(Y/L)_{i,t} + \gamma_2 \text{Policy}_{i,t} + \gamma_3 (\ln(Y/L)_{i,t} \times \text{Policy}_{i,t}) + \mu_i + \epsilon_{i,t}$.
   - Instrument the interaction term $(\ln(Y/L) \times \text{Policy})$ by interacting the instruments for $\ln(Y/L)$ with the policy variables.
   - Calculate Variance Inflation Factors (VIF) to ensure that multicollinearity between the interaction term and its components does not inflate standard errors.

6. **Diagnostic and Robustness Testing**
   - Conduct the Arellano-Bond test for AR(2) serial correlation to ensure the validity of the dynamic panel specification.
   - Report the Kleibergen-Paap rk Wald F-statistic to confirm instrument strength.
   - Perform sub-sample analysis (high-income vs. low-income) to test the stability of the investment-income elasticity.

7. **Sensitivity Analysis of Structural Integrity**
   - Systematically vary the lag depth of the instruments to document the trade-off between bias (from endogeneity) and variance (from instrument proliferation).
   - Assess if deviations from theoretical DGP values are attributable to the synthetic measurement noise by comparing GMM performance across different noise-filtered subsets of the data.