# 🌍 Global Climate Economics: 2020-2050

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![XGBoost](https://img.shields.io/badge/Machine_Learning-XGBoost-orange.svg)
![ARIMA](https://img.shields.io/badge/Forecasting-ARIMA-green.svg)

## 📖 Overview
**Climate Economics 2050** is an end-to-end Data Science and Machine Learning project that analyzes the macroeconomic drivers of global carbon emissions. By synthesizing over three decades of data from the **World Bank** and **Our World in Data (OWID)**, this project trains predictive models (Random Forest, XGBoost) and leverages Time-Series forecasting (ARIMA) to project global emissions out to the year 2050.

The project culminates in a fully interactive Streamlit dashboard allowing users to manipulate simulated climate policies (like Carbon Taxes and Renewable Investments) to visualize their compounding effects on the 2050 forecast.

---

## 🏗️ Architecture & Features
1. **Automated Data Engineering**: `src/data/ingestion.py` programmatically pulls, cleans, and merges API data from the World Bank with direct CSV downloads from OWID.
2. **Exploratory Data Analysis**: Generates interactive geographic choropleth maps and correlation heatmaps to visualize the dataset.
3. **Machine Learning Pipeline**: Trains and pits regression models against each other to dynamically determine the most mathematically significant drivers of emissions.
4. **Time-Series Forecasting**: Uses Autoregressive Integrated Moving Average (ARIMA) to predict future trends.
5. **Interactive Dashboard**: A robust Streamlit frontend to interact with the models.

---

## 🚀 Getting Started

### Option 1: Local Installation (Python Environment)
1. **Clone the repository** and navigate to the root directory.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Data Ingestion Pipeline** (Required to generate the local dataset):
   ```bash
   python src/data/ingestion.py
   ```
4. **Launch the Dashboard**:
   ```bash
   streamlit run src/dashboard/app.py
   ```
5. **Explore Notebooks**: Open `jupyter notebook` and navigate to the `notebooks/` directory to interact with the underlying code.

### Option 2: Docker Deployment
To run the entire dashboard inside an isolated container:
```bash
docker build -t climate-economics-2050 .
docker run -p 8501:8501 climate-economics-2050
```
Then navigate to `http://localhost:8501` in your browser.

---

## 📁 Repository Structure
```text
climate_economics_2050/
├── data/
│   └── processed/          # Generated global datasets
├── docs/                   # Final Reports & Impact Analyses
├── notebooks/
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_advanced_analytics_and_ml.ipynb
│   └── 04_time_series_forecasting.ipynb
├── src/
│   ├── dashboard/
│   │   └── app.py          # Streamlit UI
│   └── data/
│       └── ingestion.py    # Automated ETL pipeline
├── Dockerfile              # Containerization
└── requirements.txt        # Dependencies
```

---

## 🔬 Core Insights
- **The Decoupling Challenge**: The XGBoost Feature Importance extraction mathematically proved that Primary Energy Consumption is the #1 driver of carbon emissions, fundamentally tied to GDP.
- **The 2050 Forecast**: Without aggressive, compounding year-over-year policy interventions, business-as-usual trajectories forecast a continued, severe rise in global carbon output by 2050.

*Designed for publication, academic presentation, and executive decision-making.*
