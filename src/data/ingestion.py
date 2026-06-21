import pandas as pd
import wbgapi as wb
import os

def download_world_bank_data():
    print("Downloading World Bank Data...")
    # Indicators: Population, GDP (constant 2015 US$), Life Expectancy
    indicators = {
        'SP.POP.TOTL': 'population',
        'NY.GDP.MKTP.KD': 'gdp_constant_usd',
        'SP.DYN.LE00.IN': 'life_expectancy'
    }
    
    # Download data from 1990 to 2023
    wb_data = wb.data.DataFrame(list(indicators.keys()), time=range(1990, 2024), numericTimeKeys=True, labels=False)
    
    # wb_data is multi-indexed: (economy, series). Let's unstack and reset index.
    wb_data = wb_data.reset_index()
    # Melt years into a single 'year' column
    wb_melted = wb_data.melt(id_vars=['economy', 'series'], var_name='year', value_name='value')
    # Pivot series so each indicator is a column
    wb_pivoted = wb_melted.pivot_table(index=['economy', 'year'], columns='series', values='value').reset_index()
    
    # Rename columns based on our indicators mapping
    wb_pivoted.rename(columns=indicators, inplace=True)
    wb_pivoted.rename(columns={'economy': 'iso_code'}, inplace=True)
    
    return wb_pivoted

import requests
from io import StringIO
import time

def download_owid_data():
    print("Downloading OWID CO2 Data...")
    url = "https://nyc3.digitaloceanspaces.com/owid-public/data/co2/owid-co2-data.csv"
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            owid_data = pd.read_csv(StringIO(response.text))
            break
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(5)
            
    # Filter columns to what we need
    cols = ['iso_code', 'year', 'co2', 'co2_per_capita', 'energy_per_capita', 'primary_energy_consumption']
    # Many regions don't have iso_code in OWID (e.g. continents). We will drop those for the merge.
    owid_filtered = owid_data[cols].dropna(subset=['iso_code'])
    return owid_filtered

def merge_and_clean(wb_df, owid_df):
    print("Merging datasets...")
    # Merge on iso_code and year
    merged = pd.merge(wb_df, owid_df, on=['iso_code', 'year'], how='inner')
    
    print("Cleaning data...")
    # Sort values
    merged = merged.sort_values(['iso_code', 'year'])
    
    # Forward fill missing values within each country without dropping the grouping column
    filled = merged.groupby('iso_code').ffill()
    merged.update(filled)
    filled = merged.groupby('iso_code').bfill()
    merged.update(filled)
    
    # Drop any remaining NAs (e.g. countries with no data at all for a column)
    merged = merged.dropna()
    
    return merged

if __name__ == "__main__":
    # Resolve project root dir correctly relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '../../'))
    data_dir = os.path.join(project_root, 'data', 'processed')
    
    os.makedirs(data_dir, exist_ok=True)
    
    wb_df = download_world_bank_data()
    owid_df = download_owid_data()
    
    final_df = merge_and_clean(wb_df, owid_df)
    
    output_path = os.path.join(data_dir, 'global_data.csv')
    final_df.to_csv(output_path, index=False)
    print(f"Data ingestion complete. Final dataset shape: {final_df.shape}")
    print(f"Saved to {output_path}")
