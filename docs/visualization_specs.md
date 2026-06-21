# Phase 8: Visualization Specifications

This document outlines the design specifications for the dashboards to be built in Tableau, Power BI, and Streamlit.

## 1. Executive Dashboard (Power BI / Tableau)
**Target Audience**: C-Level Executives, High-Level Policymakers
**Layout Structure**:
- **Top Row (KPIs)**: Global GDP, Total CO2 Emissions, Average Temperature Anomaly, Global Population.
- **Center Left**: Time-series line chart showing historical and forecasted Temperature Anomaly vs CO2 Emissions (2020-2050).
- **Center Right**: Donut chart showing Global Energy Mix (Renewable vs Fossil Fuels).
- **Bottom**: Scenario selector (Optimistic, Realistic, Worst-Case) that dynamically updates the charts.

## 2. Country Comparison Dashboard
**Target Audience**: Analysts, Researchers
**Layout Structure**:
- **Top**: Dropdowns to select Country A and Country B.
- **Main View**: Side-by-side radar charts comparing: GDP per capita, CO2 per capita, Renewable Energy %, Life Expectancy.
- **Bottom**: Bar charts showing total emissions breakdown by sector for each selected country.

## 3. Climate Dashboard
**Target Audience**: Environmental Scientists, Climate NGOs
**Layout Structure**:
- **Full Screen Map**: A global choropleth map color-coded by Temperature Anomaly or CO2 per capita.
- **Interactive Element**: Clicking a country reveals a tooltip with historical emission trends and a timeline of their net-zero pledges.

## 4. Economic Dashboard
**Target Audience**: Economists, Investors
**Layout Structure**:
- **Scatter Plot**: GDP vs CO2 Emissions (The "Kuznets Curve" visualization).
- **Trend Lines**: FDI Inflows vs Renewable Energy Capacity additions.

## 5. Forecast Dashboard (Streamlit)
**Target Audience**: Data Scientists, Technical Users
**Features**:
- Built in Python using Streamlit and Plotly.
- Users can adjust parameters (e.g., "Increase Global Carbon Tax by $X", "Boost Africa Renewable Investment by Y%") and see the real-time impact on the ARIMA/LSTM forecast models.
- Code resides in `src/dashboard/app.py`.
