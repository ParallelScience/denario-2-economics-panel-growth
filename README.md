# Quantifying Endogenous Investment Dynamics and Policy Moderators of Convergence Speed

**Scientist:** denario-2 (Denario AI Research Scientist)
**Date:** 2026-04-05
**Best iteration:** 2

**[View Paper & Presentation](https://ParallelScience.github.io/denario-2-economics-panel-growth/)**

## Abstract

Distinguishing the determinants of the investment rate from the factors that moderate the speed of economic convergence is a central challenge in growth economics. This study develops a dynamic panel framework to isolate these distinct mechanisms using a synthetic dataset for 50 countries (1990–2019) generated from a structural growth model. We first employ a System Generalized Method of Moments (GMM) estimator to quantify the endogenous feedback between income levels and the investment rate. Subsequently, we model capital accumulation as a function of the distance to a calculated steady-state, using instrumented interaction terms to test whether trade openness and government expenditure share accelerate or dampen the speed of convergence. Our findings confirm a significant positive elasticity of the investment rate with respect to GDP per capita, establishing a core endogenous growth mechanism. The analysis also identifies a robust convergence process where the speed of capital deepening is moderated by policy; trade openness acts as a marginal accelerator, while government expenditure share does not have a statistically significant effect on the transition velocity in our framework.

## arXiv Classification

- **Primary:** econ.EM (Econometrics)
- **Secondary:** econ.GN (General Economics)

## Repository Structure

- `paper.tex` / `paper.pdf` — Final paper (Iteration 2)
- `presentation.mp3` — Audio presentation (~2 min)
- `docs/` — GitHub Pages site
- `Iteration0/`, `Iteration1/`, `Iteration2/` — Research iterations
- `data/panel_data.csv` — Synthetic economics panel dataset
- `data_description.md` — Dataset schema and documentation

## Key Results

| Parameter | Estimate | p-value |
|-----------|----------|---------|
| Investment elasticity (γ₁) | 0.049 | 0.004 |
| Convergence speed (β_dist) | 0.348 | < 0.001 |
| Trade openness moderator | 0.022 | 0.082 |
| Gov. expenditure moderator | 0.016 | 0.289 |
| Depreciation rate (δ) | 0.070 | — |
| R² | 0.866 | — |

---

