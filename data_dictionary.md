# Data Dictionary

This document outlines the expected variables from the combined datasets (World Bank, UN, IEA, NASA, etc.) used in this analysis.

| Variable Name | Description | Source | Expected Unit |
|---|---|---|---|
| `country_code` | ISO 3-letter country code | UN/World Bank | String |
| `year` | Year of observation (2020-2050) | All | Integer |
| `population` | Total population | UN Population Div | Count |
| `population_growth_rate` | Annual population growth rate | UN Population Div | Percentage (%) |
| `gdp_usd` | Gross Domestic Product (current US$) | World Bank | USD |
| `gdp_per_capita` | GDP divided by midyear population | World Bank | USD |
| `energy_consumption_twh` | Total primary energy consumption | IEA/Our World in Data | Terawatt-hours (TWh) |
| `renewable_energy_share` | Share of energy from renewable sources | IEA | Percentage (%) |
| `co2_emissions_mt` | Total territorial CO2 emissions | Global Carbon Project | Million tonnes (Mt) |
| `co2_per_capita` | CO2 emissions per capita | Global Carbon Project | Tonnes per capita |
| `avg_temperature_anomaly` | Average temperature anomaly | NASA/NOAA | Degrees Celsius (°C) |
| `life_expectancy` | Life expectancy at birth | WHO/World Bank | Years |
| `urban_population_pct` | Percentage of population in urban areas | World Bank | Percentage (%) |
| `fdi_inflows_usd` | Foreign Direct Investment inflows | IMF | USD |
