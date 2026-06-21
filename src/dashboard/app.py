import streamlit as st
import pandas as pd
import numpy as np
import os
import warnings
from pathlib import Path
warnings.filterwarnings('ignore')

from statsmodels.tsa.arima.model import ARIMA
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="🌍 Climate & Economics 2050",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    h1 { color: #2ecc71; }
    h2, h3 { color: #27ae60; }
    .stMetric label { font-size: 0.85rem; color: #888; }
    .stMetric .metric-container { background: #1e1e1e; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Data Loading
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), '../../data/processed/global_data.csv')
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

df = load_data()

if df is None:
    st.error("⚠️ Data not found. Please run `python src/data/ingestion.py` first.")
    st.stop()

# Pre-compute aggregates
global_trend = df.groupby('year')[['co2', 'gdp_constant_usd', 'population', 'primary_energy_consumption']].sum().reset_index()
global_trend.set_index('year', inplace=True)

latest_year = int(global_trend.index.max())
latest_data = global_trend.loc[latest_year]
latest_year_df = df[df['year'] == latest_year].copy()

# Country name mapping helper (iso_code → display name where possible)
FORECAST_STEPS = 2050 - latest_year
FORECAST_INDEX = np.arange(latest_year + 1, 2051)

# Mapping iso_code to full country name if available, or fallback
# Let's inspect columns of df to see if we have a country name. 
# We'll use the 'iso_code' since it is the unique identifier, but let's make the hover cards very detailed.
latest_year_df = df[df['year'] == latest_year].copy()
if 'country' in latest_year_df.columns:
    hover_col = 'country'
else:
    hover_col = 'iso_code'

# ─────────────────────────────────────────────
# ARIMA helper
# ─────────────────────────────────────────────
@st.cache_data
def run_arima(series_values, order=(1, 1, 1), steps=FORECAST_STEPS):
    model = ARIMA(series_values, order=order)
    fit = model.fit()
    pred = fit.get_forecast(steps=steps)
    # Return forecast values and confidence intervals
    return pred.predicted_mean, pred.conf_int(alpha=0.05)

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
_logo_path = Path(__file__).parent / "assets" / "logo.png"
if _logo_path.exists():
    st.sidebar.image(str(_logo_path), use_container_width=True)
st.sidebar.title("🌍 Global Futures 2050")
st.sidebar.markdown("---")
st.sidebar.markdown("Explore historical data across tabs, and adjust policies directly in the **🔮 Forecast** tab.")
st.sidebar.markdown("---")
st.sidebar.caption(f"Data covers 1990 – {latest_year} · {len(df):,} country-year records")

# ─────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌍 Overview",
    "🌐 Countries",
    "🌡️ Climate",
    "💰 Economics",
    "🔮 Forecast",
])

# ══════════════════════════════════════════════
# TAB 1 — Executive Dashboard
# ══════════════════════════════════════════════
with tab1:
    st.title("🌍 Global Climate & Economics — Executive Dashboard")
    st.markdown(f"*Data as of {latest_year} · World Bank + Our World in Data*")

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌏 World Population",   f"{latest_data['population']/1e9:.2f} Bn")
    c2.metric("💵 Global GDP",         f"${latest_data['gdp_constant_usd']/1e12:.1f} Tn")
    c3.metric("💨 Global CO₂",         f"{latest_data['co2']:,.0f} Mt")
    c4.metric("⚡ Primary Energy",      f"{latest_data['primary_energy_consumption']:,.0f} TWh")

    st.markdown("---")

    # ── Improved Choropleth Map ──────────────────
    st.subheader(f"🗺️ CO₂ Emissions by Country ({latest_year})")

    fig_map = px.choropleth(
        latest_year_df,
        locations="iso_code",
        color="co2",
        hover_name=hover_col,
        hover_data={"co2": ":.1f", "co2_per_capita": ":.2f", "gdp_constant_usd": ":,.0f", "iso_code": False},
        color_continuous_scale=[
            [0.00, "#0d2137"],
            [0.10, "#0a4f6c"],
            [0.25, "#0e7c4e"],
            [0.50, "#f5c518"],
            [0.75, "#e8621a"],
            [1.00, "#cc1212"],
        ],
        labels={"co2": "CO₂ (Mt)", "co2_per_capita": "CO₂/capita (t)", "gdp_constant_usd": "GDP (USD)"},
        title=f"Total CO₂ Emissions — {latest_year}",
    )
    fig_map.update_geos(
        showframe=False,
        showcoastlines=True, coastlinecolor="rgba(255,255,255,0.15)",
        showland=True,       landcolor="#111827",
        showocean=True,      oceancolor="#0a1628",
        showlakes=True,      lakecolor="#0a1628",
        showcountries=True,  countrycolor="rgba(255,255,255,0.12)",
        projection_type="natural earth",
    )
    fig_map.update_layout(
        height=520,
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(color="white"),
        coloraxis_colorbar=dict(
            title=dict(text="CO₂ (Mt)", font=dict(color="white")),
            tickfont=dict(color="white"),
            bgcolor="rgba(0,0,0,0)",
            outlinewidth=0,
            len=0.75,
        ),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # ── Top 10 Emitters ─────────────────────────
    st.subheader(f"🏭 Top 10 CO₂ Emitters ({latest_year})")
    top10 = latest_year_df.nlargest(10, 'co2').sort_values('co2')
    fig_bar = go.Figure(go.Bar(
        x=top10['co2'],
        y=top10['iso_code'],
        orientation='h',
        marker=dict(
            color=top10['co2'],
            colorscale='Reds',
            showscale=False,
        ),
        text=top10['co2'].apply(lambda x: f"{x:,.0f} Mt"),
        textposition='outside',
    ))
    fig_bar.update_layout(
        height=380,
        xaxis_title="CO₂ Emissions (Mt)",
        yaxis_title="Country",
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(color="white"),
        margin=dict(l=60, r=80, t=20, b=40),
    )
    st.plotly_chart(fig_bar, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 2 — Country Comparison Dashboard
# ══════════════════════════════════════════════
with tab2:
    st.title("🌐 Country Comparison Dashboard")

    all_countries = sorted(df['iso_code'].unique())
    default_picks = [c for c in ["USA", "CHN", "IND", "DEU", "GBR"] if c in all_countries]
    selected = st.multiselect("Select countries to compare:", all_countries, default=default_picks)

    if not selected:
        st.info("Please select at least one country.")
    else:
        cdf = df[df['iso_code'].isin(selected)]

        metric_options = {
            "CO₂ Emissions (Mt)":            "co2",
            "CO₂ per Capita (t)":            "co2_per_capita",
            "GDP (constant USD)":            "gdp_constant_usd",
            "Population":                    "population",
            "Primary Energy Consumption":    "primary_energy_consumption",
            "Energy per Capita (kWh)":       "energy_per_capita",
        }
        chosen_label = st.selectbox("Metric:", list(metric_options.keys()))
        chosen_col   = metric_options[chosen_label]

        fig_cmp = px.line(
            cdf,
            x="year",
            y=chosen_col,
            color="iso_code",
            title=f"{chosen_label} — Country Comparison (1990–{latest_year})",
            labels={"iso_code": "Country", "year": "Year", chosen_col: chosen_label},
            markers=False,
        )
        fig_cmp.update_layout(
            height=480,
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            font=dict(color="white"),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        )
        st.plotly_chart(fig_cmp, use_container_width=True)

        # Summary table
        st.subheader(f"Summary Table — {latest_year}")
        summary = (
            df[df['iso_code'].isin(selected) & (df['year'] == latest_year)]
            [['iso_code', 'co2', 'co2_per_capita', 'gdp_constant_usd', 'population', 'primary_energy_consumption']]
            .rename(columns={
                'iso_code':                   'Country',
                'co2':                        'CO₂ (Mt)',
                'co2_per_capita':             'CO₂/capita (t)',
                'gdp_constant_usd':           'GDP (USD)',
                'population':                 'Population',
                'primary_energy_consumption': 'Energy (TWh)',
            })
            .set_index('Country')
        )
        st.dataframe(summary.style.format({
            'CO₂ (Mt)': '{:,.1f}',
            'CO₂/capita (t)': '{:.2f}',
            'GDP (USD)': '${:,.0f}',
            'Population': '{:,.0f}',
            'Energy (TWh)': '{:,.1f}',
        }), use_container_width=True)


# ══════════════════════════════════════════════
# TAB 3 — Climate Dashboard
# ══════════════════════════════════════════════
with tab3:
    st.title("🌡️ Climate Dashboard")

    # Global CO₂ historical trend
    st.subheader("📈 Global CO₂ Emissions Trend (1990–" + str(latest_year) + ")")
    fig_co2 = go.Figure()
    fig_co2.add_trace(go.Scatter(
        x=global_trend.index,
        y=global_trend['co2'],
        mode='lines',
        fill='tozeroy',
        fillcolor='rgba(231,76,60,0.18)',
        line=dict(color='#e74c3c', width=2.5),
        name='Global CO₂ (Mt)',
    ))
    fig_co2.update_layout(
        height=360, paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font=dict(color="white"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", title="CO₂ (Mt)"),
        margin=dict(l=50, r=20, t=20, b=40),
    )
    st.plotly_chart(fig_co2, use_container_width=True)

    st.markdown("---")

    # CO₂ per capita map
    st.subheader(f"🌍 CO₂ per Capita ({latest_year})")
    fig_pc = px.choropleth(
        latest_year_df,
        locations="iso_code",
        color="co2_per_capita",
        color_continuous_scale=[
            [0.0, "#0d2137"], [0.15, "#0a4f6c"],
            [0.4, "#0e7c4e"], [0.65, "#f5c518"],
            [0.85, "#e8621a"], [1.0, "#cc1212"],
        ],
        labels={"co2_per_capita": "CO₂/capita (t)"},
        title=f"CO₂ per Capita — {latest_year}",
    )
    fig_pc.update_geos(
        showframe=False, showcoastlines=True, coastlinecolor="rgba(255,255,255,0.15)",
        showland=True, landcolor="#111827", showocean=True, oceancolor="#0a1628",
        showcountries=True, countrycolor="rgba(255,255,255,0.12)",
        projection_type="natural earth",
    )
    fig_pc.update_layout(
        height=460, margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font=dict(color="white"),
        coloraxis_colorbar=dict(title=dict(text="t CO₂/person", font=dict(color="white")),
                                tickfont=dict(color="white"), bgcolor="rgba(0,0,0,0)", outlinewidth=0),
    )
    st.plotly_chart(fig_pc, use_container_width=True)

    st.markdown("---")

    # Energy vs CO₂ scatter
    st.subheader(f"⚡ Energy Consumption vs CO₂ Emissions ({latest_year})")
    scatter_df = latest_year_df.dropna(subset=['primary_energy_consumption', 'co2', 'population'])
    fig_sc = px.scatter(
        scatter_df,
        x="primary_energy_consumption",
        y="co2",
        size="population",
        color="co2_per_capita",
        hover_name="iso_code",
        color_continuous_scale="RdYlGn_r",
        labels={
            "primary_energy_consumption": "Primary Energy (TWh)",
            "co2": "CO₂ Emissions (Mt)",
            "co2_per_capita": "CO₂/capita (t)",
        },
        title="Energy Consumption vs CO₂ (bubble size = population)",
        log_x=True,
        log_y=True,
    )
    fig_sc.update_layout(
        height=440, paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font=dict(color="white"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
    )
    st.plotly_chart(fig_sc, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 4 — Economic Dashboard
# ══════════════════════════════════════════════
with tab4:
    st.title("💰 Economic Dashboard")

    # Global GDP trend
    st.subheader("📈 Global GDP Trend (constant USD)")
    fig_gdp = go.Figure()
    fig_gdp.add_trace(go.Scatter(
        x=global_trend.index,
        y=global_trend['gdp_constant_usd'] / 1e12,
        mode='lines',
        fill='tozeroy',
        fillcolor='rgba(39,174,96,0.18)',
        line=dict(color='#2ecc71', width=2.5),
        name='Global GDP (Trillion USD)',
    ))
    fig_gdp.update_layout(
        height=360, paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font=dict(color="white"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", title="GDP (Trillion USD)"),
        margin=dict(l=60, r=20, t=20, b=40),
    )
    st.plotly_chart(fig_gdp, use_container_width=True)

    st.markdown("---")

    # Carbon Intensity of GDP (decoupling)
    st.subheader("🔗 Carbon Intensity of GDP — Decoupling Analysis")
    st.markdown("*Lower is better: measures how many tonnes of CO₂ are emitted per million USD of GDP.*")

    carbon_intensity = (global_trend['co2'] / (global_trend['gdp_constant_usd'] / 1e6)).reset_index()
    carbon_intensity.columns = ['year', 'carbon_intensity']

    # Compute decoupling rates (last year vs 1990)
    base_ci = carbon_intensity.iloc[0]['carbon_intensity']
    current_ci = carbon_intensity.iloc[-1]['carbon_intensity']
    decoupling_pct = ((base_ci - current_ci) / base_ci) * 100

    col_ci1, col_ci2 = st.columns(2)
    col_ci1.metric("📉 Carbon Intensity Reduction (since 1990)", f"{decoupling_pct:.1f}%", help="Total reduction in emissions per unit of economic output.")
    col_ci2.metric("🔄 Decoupling State", "Relative Decoupling", help="Economic growth has outpaced emissions growth, but absolute emissions are not yet declining to zero.")

    fig_ci = go.Figure()
    fig_ci.add_trace(go.Scatter(
        x=carbon_intensity['year'],
        y=carbon_intensity['carbon_intensity'],
        mode='lines+markers',
        line=dict(color='#f39c12', width=2.5),
        marker=dict(size=5),
        name='CO₂ / Million USD GDP',
    ))
    fig_ci.update_layout(
        height=340, paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font=dict(color="white"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", title="CO₂ (t) per $M GDP"),
        margin=dict(l=60, r=20, t=20, b=40),
    )
    st.plotly_chart(fig_ci, use_container_width=True)

    st.markdown("---")

    # GDP per capita map
    st.subheader(f"🌍 GDP per Capita ({latest_year})")
    gdp_pc_df = latest_year_df.copy()
    gdp_pc_df['gdp_per_capita'] = gdp_pc_df['gdp_constant_usd'] / gdp_pc_df['population']

    fig_gdpmap = px.choropleth(
        gdp_pc_df.dropna(subset=['gdp_per_capita']),
        locations="iso_code",
        color="gdp_per_capita",
        color_continuous_scale="Viridis",
        hover_name=hover_col,
        hover_data={"gdp_per_capita": ":,.0f", "population": ":,.0f", "iso_code": False},
        labels={"gdp_per_capita": "GDP/capita (USD)", "population": "Population"},
        title=f"GDP per Capita — {latest_year}",
    )
    fig_gdpmap.update_geos(
        showframe=False, showcoastlines=True, coastlinecolor="rgba(255,255,255,0.15)",
        showland=True, landcolor="#111827", showocean=True, oceancolor="#0a1628",
        showcountries=True, countrycolor="rgba(255,255,255,0.12)",
        projection_type="natural earth",
    )
    fig_gdpmap.update_layout(
        height=460, margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font=dict(color="white"),
        coloraxis_colorbar=dict(title=dict(text="USD/person", font=dict(color="white")),
                                tickfont=dict(color="white"), bgcolor="rgba(0,0,0,0)", outlinewidth=0),
    )
    st.plotly_chart(fig_gdpmap, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 5 — Forecast Dashboard
# ══════════════════════════════════════════════
with tab5:
    st.title("🔮 Forecast Dashboard — 2050 Projections")
    st.markdown("*ARIMA-based forecasts under three scenarios. Adjust policy parameters below to see the modeled impact on CO₂.*")

    # Policy controls organized inside the Forecast Tab
    st.markdown("### 🛠️ Policy Control Center")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        carbon_tax = st.slider("🏭 Carbon Tax ($/ton CO₂)", 0, 200, 50, help="Direct tax on carbon emissions to incentivize reduction.")
        renewable_inv = st.slider("☀️ Renewable Investment Boost (%)", 0, 100, 20, help="Percentage increase in government & private investments in solar, wind, and storage.")
    with col_p2:
        energy_eff = st.slider("⚡ Energy Efficiency Boost (%)", 0, 50, 10, help="Efficiency improvements in building codes, industrial machinery, and appliances.")
        reforest = st.slider("🌳 Reforestation & Carbon Sequestration (Mt CO₂/yr)", 0, 1000, 200, help="Global carbon removal capacity from planting trees and carbon capture technologies.")
    with col_p3:
        ev_rate = st.slider("🚗 EV Transition Rate (% Fleet by 2050)", 0, 100, 30, help="Percentage of global automotive fleet transitioning to zero-emission electric vehicles.")

    # Build modifiers from the expanded policy levers
    tax_effect = (carbon_tax / 200.0) * -0.02
    inv_effect = (renewable_inv / 100.0) * -0.02
    eff_effect = (energy_eff / 50.0) * -0.015
    ev_effect = (ev_rate / 100.0) * -0.01
    
    combined_rate = 1.0 + tax_effect + inv_effect + eff_effect + ev_effect
    
    # Apply modifier curve compounding year-over-year
    modifier_curve = np.power(combined_rate, np.arange(1, FORECAST_STEPS + 1))

    with st.spinner("Computing ARIMA forecasts…"):
        co2_base, co2_ci = run_arima(global_trend['co2'].values,               order=(1, 1, 1))
        gdp_base, gdp_ci = run_arima(global_trend['gdp_constant_usd'].values,  order=(2, 2, 1))
        pop_base, _      = run_arima(global_trend['population'].values,        order=(1, 1, 0))
        energy_base, _   = run_arima(global_trend['primary_energy_consumption'].values, order=(1, 1, 1))

    # Scenario modifiers
    optimistic_co2   = co2_base    * np.power(0.97, np.arange(1, FORECAST_STEPS + 1))
    worstcase_co2    = co2_base    * np.power(1.02, np.arange(1, FORECAST_STEPS + 1))
    
    # Apply global sequestration subtraction directly
    policy_co2       = (co2_base * modifier_curve) - reforest

    # Energy modifiers (Energy efficiency directly dampens primary energy consumption)
    optimistic_energy = energy_base * np.power(0.98, np.arange(1, FORECAST_STEPS + 1))
    worstcase_energy  = energy_base * np.power(1.03, np.arange(1, FORECAST_STEPS + 1))
    # Policy-adjusted energy uses energy efficiency boost to drop consumption trend
    policy_energy = energy_base * np.power(1.0 - (energy_eff/100.0 * 0.4), np.arange(1, FORECAST_STEPS + 1))

    # GDP modifiers (Carbon tax might slightly lower short term growth (-0.2% max), but renewable investment & efficiency boost economic growth (+0.5% max))
    optimistic_gdp = gdp_base * np.power(1.02, np.arange(1, FORECAST_STEPS + 1))
    worstcase_gdp  = gdp_base * np.power(0.98, np.arange(1, FORECAST_STEPS + 1))
    
    gdp_policy_rate = 1.0 - (carbon_tax/200.0 * 0.002) + (renewable_inv/100.0 * 0.005) + (energy_eff/50.0 * 0.003)
    policy_gdp = gdp_base * np.power(gdp_policy_rate, np.arange(1, FORECAST_STEPS + 1))

    # Population modifiers
    optimistic_pop = pop_base * np.power(0.9995, np.arange(1, FORECAST_STEPS + 1))
    worstcase_pop  = pop_base * np.power(1.005,  np.arange(1, FORECAST_STEPS + 1))
    # Policy controls do not directly impact population in our simplified model
    policy_pop = pop_base

    # ── CO₂ Forecast ──────────────────────────
    st.subheader("💨 Global CO₂ Emissions Forecast to 2050")
    fig_f1 = go.Figure()
    
    # 95% Confidence Interval for Baseline
    co2_lower = co2_ci[:, 0]
    co2_upper = co2_ci[:, 1]
    fig_f1.add_trace(go.Scatter(
        x=list(FORECAST_INDEX) + list(FORECAST_INDEX)[::-1],
        y=list(co2_upper) + list(co2_lower)[::-1],
        fill='toself',
        fillcolor='rgba(243,156,18,0.12)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=True,
        name='95% Confidence Interval'
    ))

    # Historical
    fig_f1.add_trace(go.Scatter(x=list(global_trend.index), y=list(global_trend['co2']),
        mode='lines', name='Historical', line=dict(color='white', width=2)))
    fig_f1.add_vrect(x0=latest_year, x1=latest_year, line_width=1, line_dash="dash", line_color="gray")
    # Scenarios
    fig_f1.add_trace(go.Scatter(x=list(FORECAST_INDEX), y=list(worstcase_co2),
        mode='lines', name='Worst-Case', line=dict(color='#e74c3c', dash='dot')))
    fig_f1.add_trace(go.Scatter(x=list(FORECAST_INDEX), y=list(co2_base),
        mode='lines', name='Realistic (Baseline)', line=dict(color='#f39c12', width=2)))
    fig_f1.add_trace(go.Scatter(x=list(FORECAST_INDEX), y=list(optimistic_co2),
        mode='lines', name='Optimistic', line=dict(color='#2ecc71', dash='dot')))
    fig_f1.add_trace(go.Scatter(x=list(FORECAST_INDEX), y=list(policy_co2),
        mode='lines', name=f'Policy-Adjusted Scenario',
        line=dict(color='#3498db', width=2.5)))
    fig_f1.update_layout(
        height=400, paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font=dict(color="white"),
        legend=dict(bgcolor="rgba(0,0,0,0.4)", x=0.01, y=0.99),
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", title="CO₂ (Mt)"),
        margin=dict(l=60, r=20, t=20, b=40),
    )
    st.plotly_chart(fig_f1, use_container_width=True)

    # ── GDP Forecast ───────────────────────────
    st.subheader("💵 Global GDP Forecast to 2050")
    fig_f2 = go.Figure()
    
    # 95% Confidence Interval for GDP
    gdp_lower = gdp_ci[:, 0] / 1e12
    gdp_upper = gdp_ci[:, 1] / 1e12
    fig_f2.add_trace(go.Scatter(
        x=list(FORECAST_INDEX) + list(FORECAST_INDEX)[::-1],
        y=list(gdp_upper) + list(gdp_lower)[::-1],
        fill='toself',
        fillcolor='rgba(243,156,18,0.12)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=True,
        name='95% Confidence Interval'
    ))

    fig_f2.add_trace(go.Scatter(x=list(global_trend.index), y=list(global_trend['gdp_constant_usd']/1e12),
        mode='lines', name='Historical', line=dict(color='white', width=2)))
    fig_f2.add_trace(go.Scatter(x=list(FORECAST_INDEX), y=list(worstcase_gdp/1e12),
        mode='lines', name='Worst-Case', line=dict(color='#e74c3c', dash='dot')))
    fig_f2.add_trace(go.Scatter(x=list(FORECAST_INDEX), y=list(gdp_base/1e12),
        mode='lines', name='Realistic', line=dict(color='#f39c12', width=2)))
    fig_f2.add_trace(go.Scatter(x=list(FORECAST_INDEX), y=list(optimistic_gdp/1e12),
        mode='lines', name='Optimistic', line=dict(color='#2ecc71', dash='dot')))
    fig_f2.add_trace(go.Scatter(x=list(FORECAST_INDEX), y=list(policy_gdp/1e12),
        mode='lines', name='Policy-Adjusted Scenario', line=dict(color='#3498db', width=2.5)))
    fig_f2.update_layout(
        height=380, paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font=dict(color="white"),
        legend=dict(bgcolor="rgba(0,0,0,0.4)", x=0.01, y=0.99),
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", title="GDP (Trillion USD)"),
        margin=dict(l=60, r=20, t=20, b=40),
    )
    st.plotly_chart(fig_f2, use_container_width=True)

    col_a, col_b = st.columns(2)

    # ── Population Forecast ───────────────────
    with col_a:
        st.subheader("👥 Global Population Forecast")
        fig_f3 = go.Figure()
        fig_f3.add_trace(go.Scatter(x=list(global_trend.index), y=list(global_trend['population']/1e9),
            mode='lines', name='Historical', line=dict(color='white', width=2)))
        fig_f3.add_trace(go.Scatter(x=list(FORECAST_INDEX), y=list(worstcase_pop/1e9),
            mode='lines', name='Worst-Case', line=dict(color='#e74c3c', dash='dot')))
        fig_f3.add_trace(go.Scatter(x=list(FORECAST_INDEX), y=list(pop_base/1e9),
            mode='lines', name='Realistic', line=dict(color='#f39c12', width=2)))
        fig_f3.add_trace(go.Scatter(x=list(FORECAST_INDEX), y=list(optimistic_pop/1e9),
            mode='lines', name='Optimistic', line=dict(color='#2ecc71', dash='dot')))
        # Policy adjusted population is identical to pop_base in this model
        fig_f3.update_layout(
            height=340, paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font=dict(color="white"),
            showlegend=False,
            xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.08)", title="Billion people"),
            margin=dict(l=50, r=20, t=20, b=40),
        )
        st.plotly_chart(fig_f3, use_container_width=True)

    # ── Energy Forecast ───────────────────────
    with col_b:
        st.subheader("⚡ Primary Energy Consumption Forecast")
        fig_f4 = go.Figure()
        fig_f4.add_trace(go.Scatter(x=list(global_trend.index), y=list(global_trend['primary_energy_consumption']),
            mode='lines', name='Historical', line=dict(color='white', width=2)))
        fig_f4.add_trace(go.Scatter(x=list(FORECAST_INDEX), y=list(worstcase_energy),
            mode='lines', name='Worst-Case', line=dict(color='#e74c3c', dash='dot')))
        fig_f4.add_trace(go.Scatter(x=list(FORECAST_INDEX), y=list(energy_base),
            mode='lines', name='Realistic', line=dict(color='#f39c12', width=2)))
        fig_f4.add_trace(go.Scatter(x=list(FORECAST_INDEX), y=list(optimistic_energy),
            mode='lines', name='Optimistic', line=dict(color='#2ecc71', dash='dot')))
        fig_f4.add_trace(go.Scatter(x=list(FORECAST_INDEX), y=list(policy_energy),
            mode='lines', name='Policy-Adjusted Scenario', line=dict(color='#3498db', width=2.5)))
        fig_f4.update_layout(
            height=340, paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font=dict(color="white"),
            showlegend=False,
            xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.08)", title="TWh"),
            margin=dict(l=60, r=20, t=20, b=40),
        )
        st.plotly_chart(fig_f4, use_container_width=True)

    # ── 2050 Summary Table ─────────────────────
    st.markdown("---")
    st.subheader("📊 2050 Projected Values — Scenario Summary")

    summary_data = {
        "Indicator":   ["CO₂ Emissions (Mt)", "GDP (Trillion USD)", "Population (Billion)", "Energy (TWh)"],
        "Optimistic":  [
            f"{float(optimistic_co2[-1]):,.0f}",
            f"${float(optimistic_gdp[-1])/1e12:.1f}T",
            f"{float(optimistic_pop[-1])/1e9:.2f}B",
            f"{float(optimistic_energy[-1]):,.0f}",
        ],
        "Realistic":   [
            f"{float(co2_base[-1]):,.0f}",
            f"${float(gdp_base[-1])/1e12:.1f}T",
            f"{float(pop_base[-1])/1e9:.2f}B",
            f"{float(energy_base[-1]):,.0f}",
        ],
        "Worst-Case":  [
            f"{float(worstcase_co2[-1]):,.0f}",
            f"${float(worstcase_gdp[-1])/1e12:.1f}T",
            f"{float(worstcase_pop[-1])/1e9:.2f}B",
            f"{float(worstcase_energy[-1]):,.0f}",
        ],
        "Policy-Adjusted": [
            f"{float(policy_co2[-1]):,.0f}",
            f"${float(policy_gdp[-1])/1e12:.1f}T",
            f"{float(policy_pop[-1])/1e9:.2f}B",
            f"{float(policy_energy[-1]):,.0f}",
        ]
    }
    st.dataframe(pd.DataFrame(summary_data).set_index("Indicator"), use_container_width=True)

    st.caption("*ARIMA forecasts are statistical extrapolations of historical trends and should be interpreted as indicative scenario ranges, not precise predictions.*")
