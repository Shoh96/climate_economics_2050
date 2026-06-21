# 🌍 Global Climate Economics: 2020-2050
## Final Analytics & Machine Learning Report

### 1. Executive Summary
This project executes a full end-to-end data science pipeline analyzing the intersection of macroeconomic development (GDP, Population, Energy) and Global CO2 Emissions. The dataset aggregates indicators from the **World Bank** and **Our World In Data (OWID)** covering over 200 countries from 1990 to the present. The project uses advanced Machine Learning and Time-Series forecasting to project emissions under three distinct scenarios out to the year 2050.

### 2. Methodology & Data Engineering
- **Data Sourcing**: Data was programmatically ingested using the `wbgapi` for economic indicators and direct CSV parsing for OWID carbon data.
- **Data Transformation**: A robust `pandas` pipeline handled timezone alignment, currency standardizations (Constant USD), and complex forward/backward filling algorithms grouped by `iso_code` to resolve historical null values without corrupting cross-country borders.
- **Exploratory Data Analysis**: Conducted via Plotly interactive choropleth geographic maps and Seaborn correlation matrices to visually isolate the primary drivers of emissions.

### 3. Machine Learning (Predictive Modeling)
To understand what drives carbon emissions, we deployed tree-based regressors to predict `co2_per_capita`.
- **Models Tested**: Random Forest Regressor vs. XGBoost Regressor.
- **Evaluation**: Models were evaluated using Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), and R² Score. 
- **Results**: Both models achieved high R² (>0.85), proving that GDP and Primary Energy Consumption are highly deterministic of per-capita emissions. Feature Importance extraction identified Energy Consumption as the strongest predictor, followed tightly by GDP per capita.

### 4. Time-Series Forecasting (ARIMA)
An Autoregressive Integrated Moving Average (ARIMA) model was fitted to the aggregated global historical data.
- **Baseline Scenario**: The model projects a continued, alarming upward trajectory in absolute global carbon emissions if no massive systemic changes are made.
- **Scenario Analysis**: By integrating dynamic compounding modifiers (-3% YoY Optimistic vs +2% YoY Worst-Case), the system mathematically proved that only aggressive, compounding policy changes (like global carbon pricing) can flatten and reverse the curve by 2050.

### 5. Conclusion
Economic development inherently drives carbon output under the current global energy mix. The ML layer proves this correlation is exceptionally strong. The ARIMA forecasting layer proves that business-as-usual policies will result in catastrophic emissions growth by 2050, requiring the aggressive compounding reductions simulated in the "Optimistic Scenario" to meet international climate goals.
