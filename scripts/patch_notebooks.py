"""
Script to append missing EDA cells to notebook 02_exploratory_data_analysis.ipynb
Run: python scripts/patch_notebooks.py
"""
import json, os

PROJ = os.path.join(os.path.dirname(__file__), '..')

# ─── Cells to append to notebook 02 ────────────────────────────────────────
NEW_CELLS_02 = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Boxplots — Distribution by Variable\n",
            "Boxplots reveal the spread, median, and outliers for each key numeric indicator across all countries and years."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "numeric_cols = ['co2', 'co2_per_capita', 'gdp_constant_usd', 'population', 'primary_energy_consumption', 'energy_per_capita']\n",
            "col_labels   = ['CO₂ (Mt)', 'CO₂/capita (t)', 'GDP (USD)', 'Population', 'Primary Energy (TWh)', 'Energy/capita (kWh)']\n",
            "\n",
            "fig, axes = plt.subplots(2, 3, figsize=(16, 8))\n",
            "axes = axes.flatten()\n",
            "\n",
            "for i, (col, label) in enumerate(zip(numeric_cols, col_labels)):\n",
            "    # Log-transform to handle extreme skew\n",
            "    data = np.log1p(df[col].dropna())\n",
            "    axes[i].boxplot(data, vert=True, patch_artist=True,\n",
            "                    boxprops=dict(facecolor='#2980b9', color='white'),\n",
            "                    medianprops=dict(color='#f39c12', linewidth=2),\n",
            "                    whiskerprops=dict(color='white'),\n",
            "                    capprops=dict(color='white'),\n",
            "                    flierprops=dict(markerfacecolor='#e74c3c', marker='o', markersize=3, alpha=0.4))\n",
            "    axes[i].set_title(f'{label} (log scale)', fontsize=11, fontweight='bold')\n",
            "    axes[i].set_ylabel('log(1 + value)')\n",
            "    axes[i].grid(True, alpha=0.3)\n",
            "\n",
            "plt.suptitle('Boxplots of Key Indicators (log-transformed to handle skew)', fontsize=14, fontweight='bold')\n",
            "plt.tight_layout()\n",
            "plt.show()\n",
            "print('Interpretation: Most variables show strong positive skew — a small number of large economies/emitters dominate the global totals.')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Pair Plot — Feature Relationships\n",
            "A pair plot reveals pairwise correlations between all numeric features simultaneously."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Sample to keep pair plot manageable\n",
            "sample = df[numeric_cols].dropna().sample(min(2000, len(df)), random_state=42)\n",
            "\n",
            "pair_fig = sns.pairplot(\n",
            "    sample,\n",
            "    vars=numeric_cols,\n",
            "    diag_kind='kde',\n",
            "    plot_kws=dict(alpha=0.3, s=10, color='#2980b9'),\n",
            "    diag_kws=dict(color='#2ecc71', fill=True),\n",
            ")\n",
            "pair_fig.figure.suptitle('Pair Plot — All Numeric Features', y=1.01, fontsize=13, fontweight='bold')\n",
            "plt.tight_layout()\n",
            "plt.show()\n",
            "print('Key finding: Strong linear correlations exist between CO₂, Energy, and GDP — confirming the decoupling challenge.')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 7. Global Time-Series Trends (1990–present)\n",
            "We aggregate all countries to global totals and visualize the trend for each indicator over time."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "global_ts = df.groupby('year')[['co2', 'gdp_constant_usd', 'population', 'primary_energy_consumption']].sum()\n",
            "\n",
            "fig, axes = plt.subplots(2, 2, figsize=(14, 9))\n",
            "\n",
            "plot_configs = [\n",
            "    ('co2',                      'Global CO₂ Emissions (Mt)',         '#e74c3c'),\n",
            "    ('gdp_constant_usd',         'Global GDP (constant USD)',          '#2ecc71'),\n",
            "    ('population',               'Global Population',                  '#3498db'),\n",
            "    ('primary_energy_consumption','Global Primary Energy (TWh)',       '#f39c12'),\n",
            "]\n",
            "\n",
            "for ax, (col, label, color) in zip(axes.flatten(), plot_configs):\n",
            "    ax.plot(global_ts.index, global_ts[col], color=color, linewidth=2.5)\n",
            "    ax.fill_between(global_ts.index, global_ts[col], alpha=0.15, color=color)\n",
            "    ax.set_title(label, fontweight='bold')\n",
            "    ax.set_xlabel('Year')\n",
            "    ax.grid(True, alpha=0.3)\n",
            "    # Mark COVID dip\n",
            "    if 2020 in global_ts.index:\n",
            "        ax.axvline(2020, color='gray', linestyle='--', alpha=0.7, linewidth=1)\n",
            "        ax.text(2020.2, ax.get_ylim()[0]*1.02, 'COVID', fontsize=8, color='gray')\n",
            "\n",
            "plt.suptitle('Global Time-Series Trends (1990–present)', fontsize=14, fontweight='bold')\n",
            "plt.tight_layout()\n",
            "plt.show()\n",
            "print('Note: COVID-19 caused a visible dip in CO₂ emissions in 2020, but emissions rebounded sharply in 2021.')"
        ]
    },
]

# ─── Cells to append to notebook 03 ────────────────────────────────────────
NEW_CELLS_03 = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Additional Models — Linear Regression & Gradient Boosting"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from sklearn.linear_model import LinearRegression\n",
            "from sklearn.ensemble import GradientBoostingRegressor\n",
            "\n",
            "def mape(y_true, y_pred):\n",
            "    mask = y_true != 0\n",
            "    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100\n",
            "\n",
            "# Linear Regression\n",
            "lr = LinearRegression()\n",
            "lr.fit(X_train, y_train)\n",
            "lr_preds = lr.predict(X_test)\n",
            "lr_rmse  = root_mean_squared_error(y_test, lr_preds)\n",
            "lr_mae   = mean_absolute_error(y_test, lr_preds)\n",
            "lr_mape  = mape(y_test.values, lr_preds)\n",
            "lr_r2    = r2_score(y_test, lr_preds)\n",
            "print(f'Linear Regression → RMSE: {lr_rmse:.4f} | MAE: {lr_mae:.4f} | MAPE: {lr_mape:.2f}% | R²: {lr_r2:.4f}')\n",
            "\n",
            "# Gradient Boosting\n",
            "gb = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=42)\n",
            "gb.fit(X_train, y_train)\n",
            "gb_preds = gb.predict(X_test)\n",
            "gb_rmse  = root_mean_squared_error(y_test, gb_preds)\n",
            "gb_mae   = mean_absolute_error(y_test, gb_preds)\n",
            "gb_mape  = mape(y_test.values, gb_preds)\n",
            "gb_r2    = r2_score(y_test, gb_preds)\n",
            "print(f'Gradient Boosting → RMSE: {gb_rmse:.4f} | MAE: {gb_mae:.4f} | MAPE: {gb_mape:.2f}% | R²: {gb_r2:.4f}')\n",
            "\n",
            "# Also re-compute MAPE for RF and XGBoost\n",
            "rf_mape  = mape(y_test.values, rf_preds)\n",
            "xgb_mape = mape(y_test.values, xgb_preds)\n",
            "\n",
            "# Extended comparison table\n",
            "all_metrics = pd.DataFrame({\n",
            "    'Model':    ['Linear Regression', 'Random Forest', 'XGBoost', 'Gradient Boosting'],\n",
            "    'RMSE':     [lr_rmse,   rf_rmse,   xgb_rmse,   gb_rmse],\n",
            "    'MAE':      [lr_mae,    rf_mae,    xgb_mae,    gb_mae],\n",
            "    'MAPE (%)': [lr_mape,   rf_mape,   xgb_mape,   gb_mape],\n",
            "    'R² Score': [lr_r2,     rf_r2,     xgb_r2,     gb_r2],\n",
            "})\n",
            "print('\\n--- Full Model Comparison ---')\n",
            "display(all_metrics.set_index('Model').round(4))\n",
            "best = all_metrics.loc[all_metrics['RMSE'].idxmin(), 'Model']\n",
            "print(f'\\n✅ Best Model: {best} (lowest RMSE)')\n",
            "\n",
            "# Model Comparison Visualizations\n",
            "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
            "colors = ['#e74c3c', '#2ecc71', '#3498db', '#f1c40f']\n",
            "axes[0].bar(all_metrics['Model'], all_metrics['R² Score'], color=colors)\n",
            "axes[0].set_title('Model R² Score Comparison (higher is better)', fontweight='bold')\n",
            "axes[0].set_ylim(0.7, 1.0)\n",
            "axes[0].set_ylabel('R² Score')\n",
            "for i, v in enumerate(all_metrics['R² Score']):\n",
            "    axes[0].text(i, v + 0.005, f\"{v:.3f}\", ha='center', fontweight='bold')\n",
            "\n",
            "axes[1].bar(all_metrics['Model'], all_metrics['RMSE'], color=colors)\n",
            "axes[1].set_title('Model RMSE Comparison (lower is better)', fontweight='bold')\n",
            "axes[1].set_ylabel('RMSE')\n",
            "for i, v in enumerate(all_metrics['RMSE']):\n",
            "    axes[1].text(i, v + 0.05, f\"{v:.3f}\", ha='center', fontweight='bold')\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Principal Component Analysis (PCA)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from sklearn.preprocessing import StandardScaler\n",
            "from sklearn.decomposition import PCA\n",
            "\n",
            "scaler = StandardScaler()\n",
            "X_scaled = scaler.fit_transform(df[features].dropna())\n",
            "\n",
            "pca = PCA(n_components=4)\n",
            "pca.fit(X_scaled)\n",
            "\n",
            "explained = pca.explained_variance_ratio_\n",
            "cumulative = np.cumsum(explained)\n",
            "\n",
            "fig, ax = plt.subplots(figsize=(8, 4))\n",
            "ax.bar(range(1, len(explained)+1), explained*100, color='#3498db', label='Individual')\n",
            "ax.plot(range(1, len(explained)+1), cumulative*100, 'o-', color='#e74c3c', label='Cumulative')\n",
            "ax.set_xlabel('Principal Component')\n",
            "ax.set_ylabel('Variance Explained (%)')\n",
            "ax.set_title('PCA — Explained Variance by Component', fontweight='bold')\n",
            "ax.legend()\n",
            "ax.grid(True, alpha=0.3)\n",
            "plt.tight_layout()\n",
            "plt.show()\n",
            "\n",
            "# PCA Biplot / Loadings plot\n",
            "fig, ax = plt.subplots(figsize=(8, 6))\n",
            "for i, feature in enumerate(features):\n",
            "    ax.arrow(0, 0, pca.components_[0, i], pca.components_[1, i], \n",
            "             head_width=0.03, head_length=0.03, color='#e74c3c', width=0.005)\n",
            "    ax.text(pca.components_[0, i]*1.15, pca.components_[1, i]*1.15, feature, \n",
            "            color='black', ha='center', va='center', fontweight='bold')\n",
            "ax.set_xlim(-1, 1)\n",
            "ax.set_ylim(-1, 1)\n",
            "ax.set_xlabel('PC1')\n",
            "ax.set_ylabel('PC2')\n",
            "ax.set_title('PCA Loadings Biplot (PC1 vs PC2)', fontweight='bold')\n",
            "ax.grid(True, alpha=0.3)\n",
            "plt.tight_layout()\n",
            "plt.show()\n",
            "\n",
            "print(f'PC1 explains {explained[0]*100:.1f}% of variance')\n",
            "print(f'PC1 + PC2 explain {cumulative[1]*100:.1f}% of variance')\n",
            "print(f'PC1 + PC2 + PC3 explain {cumulative[2]*100:.1f}% of variance')\n",
            "\n",
            "# Loadings\n",
            "loadings = pd.DataFrame(pca.components_.T, index=features,\n",
            "                         columns=[f'PC{i+1}' for i in range(4)])\n",
            "print('\\nPCA Loadings:')\n",
            "display(loadings.round(3))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 7. K-Means Cluster Analysis — Country Emission Profiles"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from sklearn.cluster import KMeans\n",
            "\n",
            "# Use latest year per country for clustering\n",
            "latest_year = df['year'].max()\n",
            "cluster_df  = df[df['year'] == latest_year][['iso_code'] + features + ['co2']].dropna().set_index('iso_code')\n",
            "\n",
            "scaler2  = StandardScaler()\n",
            "X_cl     = scaler2.fit_transform(cluster_df[features + ['co2']])\n",
            "\n",
            "# Elbow method\n",
            "inertias = []\n",
            "K_range  = range(2, 9)\n",
            "for k in K_range:\n",
            "    km = KMeans(n_clusters=k, random_state=42, n_init=10)\n",
            "    km.fit(X_cl)\n",
            "    inertias.append(km.inertia_)\n",
            "\n",
            "fig, ax = plt.subplots(figsize=(7, 4))\n",
            "ax.plot(list(K_range), inertias, 'o-', color='#2980b9', linewidth=2)\n",
            "ax.set_xlabel('Number of Clusters (K)')\n",
            "ax.set_ylabel('Inertia (within-cluster SSE)')\n",
            "ax.set_title('K-Means Elbow Method', fontweight='bold')\n",
            "ax.grid(True, alpha=0.3)\n",
            "plt.tight_layout()\n",
            "plt.show()\n",
            "\n",
            "# Fit with K=4\n",
            "km4 = KMeans(n_clusters=4, random_state=42, n_init=10)\n",
            "cluster_df['Cluster'] = km4.fit_predict(X_cl)\n",
            "\n",
            "print('\\nCluster Size:')\n",
            "print(cluster_df['Cluster'].value_counts())\n",
            "\n",
            "print('\\nCluster Centroids (mean CO₂ per cluster):')\n",
            "display(cluster_df.groupby('Cluster')['co2'].mean().sort_values(ascending=False).rename('Avg CO₂ (Mt)').round(1))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 8. OLS Regression — Causal Relationship Analysis"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import statsmodels.api as sm\n",
            "\n",
            "ols_df = df[features + ['co2']].dropna()\n",
            "X_ols  = sm.add_constant(ols_df[features])\n",
            "y_ols  = ols_df['co2']\n",
            "\n",
            "ols_model = sm.OLS(y_ols, X_ols).fit()\n",
            "print(ols_model.summary())\n",
            "print('\\n--- Interpretation ---')\n",
            "print('Coefficients with p < 0.05 are statistically significant drivers of CO₂ emissions.')"
        ]
    },
]

# ─── Cells to append to notebook 04 ────────────────────────────────────────
NEW_CELLS_04 = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Additional Forecasts — Population, Energy & Renewable Energy"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Population forecast\n",
            "print('Forecasting Population...')\n",
            "pop_forecast = generate_forecast(global_trend['population'], order=(1, 1, 0))\n",
            "\n",
            "# Energy consumption forecast\n",
            "print('Forecasting Primary Energy Consumption...')\n",
            "energy_forecast = generate_forecast(global_trend['primary_energy_consumption'], order=(1, 1, 1))\n",
            "\n",
            "# Population scenarios\n",
            "pop_optimistic  = pop_forecast * np.power(0.9995, np.arange(1, forecast_steps+1))  # slower growth\n",
            "pop_worst       = pop_forecast * np.power(1.005,  np.arange(1, forecast_steps+1))  # faster growth\n",
            "\n",
            "# Energy scenarios\n",
            "energy_optimistic = energy_forecast * np.power(0.98, np.arange(1, forecast_steps+1))  # efficiency gains\n",
            "energy_worst      = energy_forecast * np.power(1.03, np.arange(1, forecast_steps+1))  # high demand\n",
            "\n",
            "# ── Plot Population ──────────────────────────────────────────────────\n",
            "fig, axes = plt.subplots(1, 2, figsize=(16, 5))\n",
            "\n",
            "ax = axes[0]\n",
            "ax.plot(global_trend.index, global_trend['population']/1e9, color='black', linewidth=2, label='Historical')\n",
            "ax.plot(forecast_index, pop_worst/1e9,       color='red',    linestyle='--', label='Worst-Case')\n",
            "ax.plot(forecast_index, pop_forecast.values/1e9,  color='orange', linewidth=2, label='Realistic')\n",
            "ax.plot(forecast_index, pop_optimistic/1e9,  color='green',  linestyle='--', label='Optimistic')\n",
            "ax.axvline(global_trend.index.max(), color='gray', linestyle=':', alpha=0.7)\n",
            "ax.set_title('Global Population Forecast to 2050 (Billion)', fontweight='bold')\n",
            "ax.set_xlabel('Year'); ax.set_ylabel('Billion People')\n",
            "ax.legend(); ax.grid(True, alpha=0.3)\n",
            "\n",
            "# ── Plot Energy ───────────────────────────────────────────────────────\n",
            "ax2 = axes[1]\n",
            "ax2.plot(global_trend.index, global_trend['primary_energy_consumption'], color='black', linewidth=2, label='Historical')\n",
            "ax2.plot(forecast_index, energy_worst.values,       color='red',    linestyle='--', label='Worst-Case')\n",
            "ax2.plot(forecast_index, energy_forecast.values,    color='orange', linewidth=2, label='Realistic')\n",
            "ax2.plot(forecast_index, energy_optimistic.values,  color='green',  linestyle='--', label='Optimistic')\n",
            "ax2.axvline(global_trend.index.max(), color='gray', linestyle=':', alpha=0.7)\n",
            "ax2.set_title('Primary Energy Consumption Forecast to 2050 (TWh)', fontweight='bold')\n",
            "ax2.set_xlabel('Year'); ax2.set_ylabel('TWh')\n",
            "ax2.legend(); ax2.grid(True, alpha=0.3)\n",
            "\n",
            "plt.suptitle('Scenario Forecasts to 2050', fontsize=13, fontweight='bold')\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Renewable Energy Adoption & Temperature Anomaly Projections\n",
            "*Note: These are trend-based projections as our dataset does not include direct renewable share or temperature data.*"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Renewable Energy Adoption — proxy: modeled as CO₂ intensity declining\n",
            "# We proxy 'renewable share' as inverse of carbon intensity of energy\n",
            "df['carbon_intensity_energy'] = df['co2'] / df['primary_energy_consumption'].replace(0, np.nan)\n",
            "ci_trend = df.groupby('year')['carbon_intensity_energy'].mean()\n",
            "\n",
            "# Project declining carbon intensity (renewable growth scenario)\n",
            "ci_last = ci_trend.iloc[-1]\n",
            "renewable_years = np.arange(global_trend.index.max()+1, 2051)\n",
            "\n",
            "# Scenarios: compounding annual decline in carbon intensity of energy\n",
            "ci_optimistic = ci_last * np.power(0.96, np.arange(1, forecast_steps+1))  # 4% annual reduction\n",
            "ci_realistic  = ci_last * np.power(0.98, np.arange(1, forecast_steps+1))  # 2% annual reduction\n",
            "ci_worst      = ci_last * np.power(1.005,np.arange(1, forecast_steps+1))  # slight increase\n",
            "\n",
            "# Temperature anomaly — linear projection based on CO₂ forcing (simplified)\n",
            "# Using ECS (equilibrium climate sensitivity) proxy: ~3°C per CO₂ doubling\n",
            "co2_2020_baseline = global_trend.loc[global_trend.index.min(), 'co2']  # 1990 baseline\n",
            "temp_base_1990 = 0.5  # degrees C above pre-industrial (1990 approx)\n",
            "\n",
            "def temp_anomaly(co2_series, base_co2, base_temp, ecs=3.0):\n",
            "    return base_temp + ecs * np.log2(co2_series / base_co2)\n",
            "\n",
            "hist_temp = temp_anomaly(global_trend['co2'], co2_2020_baseline, temp_base_1990)\n",
            "opt_temp  = temp_anomaly(pd.Series(scenario_optimistic.values), co2_2020_baseline, temp_base_1990)\n",
            "real_temp = temp_anomaly(pd.Series(scenario_realistic.values),  co2_2020_baseline, temp_base_1990)\n",
            "worst_temp= temp_anomaly(pd.Series(scenario_worst.values),      co2_2020_baseline, temp_base_1990)\n",
            "\n",
            "# ── Plots ─────────────────────────────────────────────────────────────\n",
            "fig, axes = plt.subplots(1, 2, figsize=(16, 5))\n",
            "\n",
            "ax = axes[0]\n",
            "ax.plot(ci_trend.index, ci_trend.values, color='black', linewidth=2, label='Historical')\n",
            "ax.plot(renewable_years, ci_worst,     color='red',    linestyle='--', label='Worst-Case')\n",
            "ax.plot(renewable_years, ci_realistic, color='orange', linewidth=2,   label='Realistic')\n",
            "ax.plot(renewable_years, ci_optimistic,color='green',  linestyle='--', label='Optimistic')\n",
            "ax.axvline(global_trend.index.max(), color='gray', linestyle=':', alpha=0.7)\n",
            "ax.set_title('Carbon Intensity of Energy (CO₂/TWh) → Renewable Transition', fontweight='bold')\n",
            "ax.set_xlabel('Year'); ax.set_ylabel('CO₂ per TWh')\n",
            "ax.legend(); ax.grid(True, alpha=0.3)\n",
            "\n",
            "ax2 = axes[1]\n",
            "ax2.plot(global_trend.index, hist_temp.values, color='black', linewidth=2, label='Historical (proxy)')\n",
            "ax2.plot(forecast_index, worst_temp.values,  color='red',    linestyle='--', label='Worst-Case')\n",
            "ax2.plot(forecast_index, real_temp.values,   color='orange', linewidth=2,   label='Realistic')\n",
            "ax2.plot(forecast_index, opt_temp.values,    color='green',  linestyle='--', label='Optimistic')\n",
            "ax2.axvline(global_trend.index.max(), color='gray', linestyle=':', alpha=0.7)\n",
            "ax2.axhline(1.5, color='blue', linestyle=':', alpha=0.7, label='Paris 1.5°C target')\n",
            "ax2.axhline(2.0, color='purple', linestyle=':', alpha=0.7, label='Paris 2.0°C target')\n",
            "ax2.set_title('Global Temperature Anomaly Projection to 2050 (°C)', fontweight='bold')\n",
            "ax2.set_xlabel('Year'); ax2.set_ylabel('°C above pre-industrial')\n",
            "ax2.legend(loc='upper left', fontsize=8); ax2.grid(True, alpha=0.3)\n",
            "\n",
            "plt.suptitle('Renewable Adoption & Temperature Anomaly Scenarios to 2050', fontsize=13, fontweight='bold')\n",
            "plt.tight_layout()\n",
            "plt.show()\n",
            "print(f'\\n2050 Temperature Projections:')\n",
            "print(f'  Optimistic:  {opt_temp.values[-1]:.2f}°C')\n",
            "print(f'  Realistic:   {real_temp.values[-1]:.2f}°C')\n",
            "print(f'  Worst-Case:  {worst_temp.values[-1]:.2f}°C')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Summary Table — All 2050 Projections"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "summary_2050 = pd.DataFrame({\n",
            "    'Indicator':  ['CO₂ Emissions (Mt)', 'GDP (Trillion USD)', 'Population (Billion)', 'Energy (TWh)', 'Temp Anomaly (°C)'],\n",
            "    'Optimistic': [\n",
            "        f\"{scenario_optimistic.values[-1]:,.0f}\",\n",
            "        f\"${gdp_forecast.values[-1]/1e12:.1f}T\",\n",
            "        f\"{pop_optimistic[-1]/1e9:.2f}B\",\n",
            "        f\"{energy_optimistic.values[-1]:,.0f}\",\n",
            "        f\"{opt_temp.values[-1]:.2f}°C\",\n",
            "    ],\n",
            "    'Realistic':  [\n",
            "        f\"{scenario_realistic.values[-1]:,.0f}\",\n",
            "        f\"${gdp_forecast.values[-1]/1e12:.1f}T\",\n",
            "        f\"{pop_forecast.values[-1]/1e9:.2f}B\",\n",
            "        f\"{energy_forecast.values[-1]:,.0f}\",\n",
            "        f\"{real_temp.values[-1]:.2f}°C\",\n",
            "    ],\n",
            "    'Worst-Case': [\n",
            "        f\"{scenario_worst.values[-1]:,.0f}\",\n",
            "        f\"${gdp_forecast.values[-1]/1e12:.1f}T\",\n",
            "        f\"{pop_worst[-1]/1e9:.2f}B\",\n",
            "        f\"{energy_worst.values[-1]:,.0f}\",\n",
            "        f\"{worst_temp.values[-1]:.2f}°C\",\n",
            "    ],\n",
            "})\n",
            "print('2050 Scenario Summary:')\n",
            "display(summary_2050.set_index('Indicator'))"
        ]
    },
]


def patch_notebook(nb_path, new_cells):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    existing_sources = [' '.join(c.get('source', [])) for c in nb['cells']]
    for cell in new_cells:
        sig = ' '.join(cell.get('source', []))[:60]
        if any(sig in s for s in existing_sources):
            print(f'  Skipping (already exists): {sig[:40]}...')
            continue
        nb['cells'].append(cell)

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f'  Patched: {os.path.basename(nb_path)}')


if __name__ == '__main__':
    nb02 = os.path.join(PROJ, 'notebooks', '02_exploratory_data_analysis.ipynb')
    nb03 = os.path.join(PROJ, 'notebooks', '03_advanced_analytics_and_ml.ipynb')
    nb04 = os.path.join(PROJ, 'notebooks', '04_time_series_forecasting.ipynb')

    print('Patching notebooks...')
    patch_notebook(nb02, NEW_CELLS_02)
    patch_notebook(nb03, NEW_CELLS_03)
    patch_notebook(nb04, NEW_CELLS_04)
    print('Done.')
