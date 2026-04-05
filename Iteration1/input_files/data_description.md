## Economics Panel Dataset: Cross-Country Growth Dynamics (1990–2019)

### Overview
A synthetic balanced panel dataset covering **50 countries** over **30 years** (1990–2019), totalling 1,500 observations. The data is generated from a structural Cobb-Douglas growth model with realistic noise, making it suitable for empirical macroeconomics and growth economics research.

### Data File
`/home/node/work/projects/economics_v1/data/panel_data.csv`

### Variables

| Variable | Description | Units |
|---|---|---|
| `country` | Country identifier (C00–C49) | categorical |
| `year` | Year | 1990–2019 |
| `gdp` | Total GDP | index |
| `gdp_per_capita` | GDP per capita (Y/L) | index |
| `capital_stock` | Physical capital stock (K) | index |
| `labor_force` | Labor force size (L) | index |
| `human_capital` | Human capital index (H) | index |
| `tfp` | Total Factor Productivity (A) | index |
| `investment_rate` | Gross investment as share of GDP (s) | fraction |
| `government_expenditure_share` | Government spending as share of GDP | fraction |
| `trade_openness` | Trade (imports + exports) as share of GDP | fraction |
| `inflation` | Annual inflation rate | fraction |
| `population_growth` | Annual labor force growth rate | fraction |

### Structural Model (Data Generating Process)
The data is generated from a **Cobb-Douglas production function**:

```
Y = A * K^0.35 * (H * L)^0.65
```

- Capital accumulation: `K_{t+1} = (1 - 0.07) * K_t + s_t * Y_t`
- TFP growth: `log(A_{t+1}/A_t) ~ N(0.012, 0.02^2)` (global trend + country noise)
- Human capital accumulation: `log(H_{t+1}/H_t) ~ N(0.015, 0.01^2)`
- Investment rate (s) is endogenous to GDP per capita level
- Country fixed effects in initial TFP (productivity heterogeneity across countries)

### Research Opportunities
- **Growth accounting**: Decompose GDP growth into contributions from K, L, H, and TFP
- **Convergence analysis**: Test for beta- and sigma-convergence across countries
- **Panel regression**: Estimate production function parameters using fixed effects or GMM
- **TFP dynamics**: Analyze cross-country TFP dispersion and catch-up dynamics
- **Policy channels**: Assess the role of trade openness, government spending, and investment on growth
- **Human capital**: Quantify the returns to human capital accumulation

### Notes
- All country identifiers are synthetic (no mapping to real countries)
- The investment rate is mildly endogenous (correlated with income level)
- Measurement noise added to all variables to mimic real-world data imperfections
