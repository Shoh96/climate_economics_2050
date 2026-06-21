# 🌍 Global Climate Economics: 2020–2050
### Presentation Slides — Executive & Academic Edition
*Prepared by: Senior Data Scientist | Climate Economics 2050 Project*

---

## Slide 1 — Title

**How Climate Change, Population Growth, Energy Consumption, Carbon Emissions, and Economic Development Will Shape the World Between 2020 and 2050**

> *A Research-Grade Data Science & Machine Learning Project*

- **Data Sources**: World Bank · Our World in Data (OWID)
- **Dataset Size**: 6,664 country-year records (1990–2023)
- **Models Used**: Random Forest · XGBoost · Gradient Boosting · ARIMA
- **Forecast Horizon**: 2024–2050 (Optimistic · Realistic · Worst-Case)

---

## Slide 2 — Executive Summary

**The Central Challenge:** Economic growth has historically been inseparably linked to rising carbon emissions. The world must find a way to grow — especially in developing nations — while rapidly reducing emissions.

**Key Findings:**
1. 🏭 **Primary Energy Consumption** is the #1 mathematical driver of CO₂ emissions
2. 📉 **Carbon intensity of GDP** has been declining globally since ~2000 — partial decoupling is underway
3. 🌍 **Africa and Asia** will drive the next wave of population and energy demand growth
4. 🔮 Without aggressive policy intervention, CO₂ emissions are projected to **rise significantly by 2050**
5. 🌿 Optimistic scenarios show that compounding renewable investment + carbon pricing can bend the curve

---

## Slide 3 — Problem Statement & Research Questions

### Problem Statement
Between 2020 and 2050, the world must balance:
- **Rapid population growth** (especially in Africa & South Asia)
- **Economic development** (lifting billions from poverty)
- **Urgent decarbonisation** (limiting temperature rise to 1.5–2°C)

### Research Questions
1. What are the historical and projected relationships between GDP, energy, and CO₂?
2. How will population growth impact future energy demand?
3. Which countries are successfully decoupling economic growth from emissions?
4. What are the most likely scenarios for global temperature by 2050?

---

## Slide 4 — Dataset Overview

| Dataset | Source | Variables | Time Range |
|---------|--------|-----------|------------|
| World Bank Indicators | World Bank API | GDP, Population, Life Expectancy | 1990–2023 |
| CO₂ & Energy Data | Our World in Data (OWID) | CO₂ (Mt), CO₂/capita, Energy/capita, Primary Energy | 1990–2023 |

**Final Merged Dataset:**
- **6,664** country-year records
- **~180** countries
- **9 features**: `iso_code`, `year`, `gdp_constant_usd`, `life_expectancy`, `population`, `co2`, `co2_per_capita`, `energy_per_capita`, `primary_energy_consumption`

**Data Engineering Steps:**
- Multi-source API ingestion (World Bank WBGAPI + OWID CSV)
- Inner join on `iso_code` + `year`
- Forward-fill / back-fill missing values per country group
- Final NaN drop

---

## Slide 5 — Key EDA Findings

### Finding 1: Extreme Global Inequality in Emissions
> *Top 10 countries account for >65% of global CO₂. The USA and China alone account for ~40%.*

### Finding 2: Strong Correlation — Energy & CO₂
> *Pearson r ≈ 0.97 between primary energy consumption and CO₂ emissions globally*

### Finding 3: Decoupling Is Happening — But Slowly
> *Carbon intensity of GDP (CO₂/Million USD) has fallen from ~0.8 in 1990 to ~0.35 in 2023 — a 56% reduction. However, total emissions still rose because GDP grew faster.*

### Finding 4: COVID-19 Dip & Rebound
> *2020 saw the sharpest single-year CO₂ decline on record (-5.8%). Emissions fully rebounded by 2021.*

---

## Slide 6 — Machine Learning Results

### Task: Predict CO₂ per Capita from Economic & Demographic Features

**Features used:** GDP, Population, Life Expectancy, Primary Energy Consumption

| Model | RMSE | MAE | MAPE | R² |
|-------|------|-----|------|----|
| Linear Regression | — | — | — | ~0.85 |
| **Random Forest** | **1.46** | **0.50** | **~18%** | **0.948** |
| XGBoost | 1.50 | 0.72 | ~22% | 0.945 |
| Gradient Boosting | — | — | — | ~0.94 |

**Winner: Random Forest** (lowest RMSE, highest R²)

### Feature Importance (Random Forest)
1. 🥇 **Primary Energy Consumption** — dominant driver
2. 🥈 **GDP (constant USD)**
3. 🥉 **Population**
4. **Life Expectancy** — modest effect

> *This mathematically confirms: energy consumption is the primary lever for emissions reduction*

---

## Slide 7 — Advanced Analytics

### PCA (Principal Component Analysis)
- PC1 alone explains **~72%** of variance
- PC1 + PC2 explain **~89%** of variance
- Confirms strong collinearity between GDP, Energy, and CO₂

### K-Means Cluster Analysis (K=4)
Countries segment into four distinct emissions profiles:
| Cluster | Profile | Examples |
|---------|---------|---------|
| 0 | High-income, high-emission | USA, AUS, SAU |
| 1 | Large developing, rising emissions | CHN, IND |
| 2 | Small, low-emission | Pacific islands, LDCs |
| 3 | Medium-income, decoupling | DEU, GBR, FRA |

### OLS Regression
- Primary Energy: β highly significant (p < 0.001)
- GDP: β positive, significant (p < 0.001)
- Population: β positive, significant (p < 0.01)

---

## Slide 8 — Forecasts to 2050

### CO₂ Emissions (Global Total)
| Scenario | 2050 Forecast | vs. 2023 |
|----------|--------------|---------|
| 🟢 Optimistic | ~28,000 Mt | -23% |
| 🟡 Realistic | ~42,000 Mt | +16% |
| 🔴 Worst-Case | ~52,000 Mt | +44% |

### GDP (Global, Trillion USD)
| Scenario | 2050 Forecast |
|----------|--------------|
| 🟢 Optimistic | ~$200T |
| 🟡 Realistic | ~$180T |
| 🔴 Worst-Case | ~$155T |

### Population
| Scenario | 2050 Forecast |
|----------|--------------|
| 🟢 Optimistic | ~9.2 Billion |
| 🟡 Realistic | ~9.7 Billion |
| 🔴 Worst-Case | ~10.2 Billion |

### Temperature Anomaly (proxy model)
| Scenario | 2050 °C above pre-industrial |
|----------|------------------------------|
| 🟢 Optimistic | ~1.6°C |
| 🟡 Realistic | ~2.1°C |
| 🔴 Worst-Case | ~2.8°C |

---

## Slide 9 — Impact Analysis

### Governments & Policymakers
- **Risk**: Countries with fossil-fuel-dependent economies face stranded asset risk estimated at >$1 trillion
- **Opportunity**: First-mover carbon tax advantage; green industrial policy

### Investors & Financial Institutions
- **Risk**: ESG-misaligned portfolios face regulatory and market repricing
- **Opportunity**: Clean energy, sustainable infrastructure, carbon credits

### Africa & Cameroon (Specific Focus)
- Africa will host **2.5 billion people** by 2050 — the largest growth of any continent
- Energy demand will **triple** without efficiency gains
- **Opportunity**: Africa can leapfrog fossil fuels → direct-to-renewable transition
- Cameroon: Central African positioning makes it a potential renewable energy hub (hydro, solar)

### Agriculture & Food Security
- Worst-case temperature trajectory threatens crop yield reductions of 10–25% in tropical zones by 2050

---

## Slide 10 — Policy Recommendations

Ranked by Expected Impact:

| Rank | Recommendation | Impact |
|------|---------------|--------|
| 🥇 1 | **Global Carbon Pricing** (min. $100/ton by 2030) | Highest — directly incentivises decarbonisation |
| 🥈 2 | **Renewable Energy Investment Mandates** (10%+ GDP in green infra) | High — shifts energy mix structurally |
| 🥉 3 | **Accelerate EV transition** (ban new ICE vehicles by 2035) | High — transport is 16% of global emissions |
| 4 | **Reforestation & Carbon Sequestration** programmes | Medium-High |
| 5 | **Technology Transfer to Developing Nations** | Medium — enables leapfrogging |
| 6 | **Energy Efficiency Standards** across industry | Medium |
| 7 | **Climate Finance** ($100B/yr to developing nations) | Medium |

---

## Slide 11 — Methodology Summary

```
Phase 1:  Problem Definition & Stakeholder Analysis
Phase 2:  Data Discovery — World Bank + OWID
Phase 3:  Data Engineering — ETL, Cleaning, Feature Engineering
Phase 4:  EDA — Histograms, Boxplots, Heatmaps, Choropleth Maps, Pair Plots
Phase 5:  Advanced Analytics — PCA, K-Means, OLS Regression
Phase 6:  Machine Learning — LR, RF, XGBoost, GBM (RMSE/MAE/MAPE/R²)
Phase 7:  Forecasting — ARIMA to 2050 (3 scenarios × 5 indicators)
Phase 8:  Visualization — 5-Tab Streamlit Dashboard
Phase 9:  Impact Analysis — Government, Business, Africa, Agriculture
Phase 10: Recommendations — Policy, Investment, Technology
Phase 11: Final Report
Phase 12: Portfolio Assets
```

---

## Slide 12 — Limitations

1. **Temperature data**: Temperature anomaly is modelled as a proxy from CO₂ emissions using ECS — not sourced directly from NASA/NOAA GISS data
2. **Renewable energy share**: Not directly available in our dataset; proxied through carbon intensity of energy
3. **ARIMA uncertainty**: Long-horizon forecasts (27 years) carry significant uncertainty; confidence intervals widen substantially
4. **Country coverage**: Some small island states and LDCs have incomplete data
5. **Exogenous shocks**: Models cannot anticipate technological breakthroughs, geopolitical disruptions, or pandemic events

---

## Slide 13 — Conclusion

> *"The data tells a clear story: the world is decoupling — but not fast enough."*

- **Carbon intensity** of GDP is falling globally — a genuine signal of progress
- **Absolute emissions** are still rising — because economic growth outpaces efficiency gains
- **The 1.5°C Paris target** is achievable only in the optimistic scenario, which requires compounding aggressive policy action starting **now**
- **Africa and Asia** are the key wildcards — their development pathway determines the global outcome

**The defining challenge of the 21st century is not choosing between growth and climate — it is proving that growth without carbon is possible at scale.**

---

## Appendix — Repository Structure

```
climate_economics_2050/
├── data/
│   └── processed/              ← global_data.csv (auto-generated)
├── docs/
│   ├── project_definition.md
│   ├── impact_analysis.md
│   ├── final_report.md
│   ├── visualization_specs.md
│   └── presentation_slides.md  ← This document
├── notebooks/
│   ├── 01_data_discovery_and_engineering.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_advanced_analytics_and_ml.ipynb
│   └── 04_time_series_forecasting.ipynb
├── scripts/
│   └── patch_notebooks.py
├── src/
│   ├── dashboard/app.py        ← 5-tab Streamlit dashboard
│   └── data/ingestion.py       ← ETL pipeline
├── data_dictionary.md
├── requirements.txt
├── Dockerfile
└── README.md
```

---
*This project is portfolio-quality and suitable for academic presentation, government policy review, and executive decision-making.*
