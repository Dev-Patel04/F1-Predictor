"""
Alternative data collection script that uses round numbers directly
instead of relying on the schedule API which is currently failing.
"""
import fastf1
import pandas as pd
import numpy as np
from pathlib import Path
import config

# Enable cache
fastf1.Cache.enable_cache(str(config.FASTF1_CACHE))

# Known F1 calendar - number of races per season
RACES_PER_SEASON = {
    2022: 22,
    2023: 23,
    2024: 24,
    2025: 10,  # Races completed so far in 2025 (update as season progresses)
}

def collect_race_by_round(year: int, round_num: int) -> pd.DataFrame:
    """Collect race data for a specific round."""
    try:
        # Load race session
        session = fastf1.get_session(year, round_num, 'R')
        session.load(telemetry=False, weather=True, messages=False)
        
        results = session.results
        if results.empty:
            return pd.DataFrame()
        
        event_name = session.event['EventName']
        print(f"  Collected: {event_name}")
        
        df = pd.DataFrame({
            'Driver': results['Abbreviation'],
            'DriverNumber': results['DriverNumber'],
            'Team': results['TeamName'],
            'GridPosition': results['GridPosition'],
            'Position': results['Position'],
            'Points': results['Points'],
            'Status': results['Status'],
            'Year': year,
            'EventName': event_name,
            'Round': round_num
        })
        
        df['IsWinner'] = (df['Position'] == 1).astype(int)
        df['IsPodium'] = (df['Position'] <= 3).astype(int)
        
        # Try to add qualifying data
        try:
            quali = fastf1.get_session(year, round_num, 'Q')
            quali.load(telemetry=False, weather=False, messages=False)
            quali_df = pd.DataFrame({
                'Driver': quali.results['Abbreviation'],
                'QualifyingPosition': quali.results['Position'],
            })
            df = df.merge(quali_df, on='Driver', how='left')
        except:
            pass
        
        # Try to add weather
        try:
            weather = session.weather_data
            if weather is not None and not weather.empty:
                df['AirTemp'] = weather['AirTemp'].mean()
                df['TrackTemp'] = weather['TrackTemp'].mean()
                df['Humidity'] = weather['Humidity'].mean()
                df['WindSpeed'] = weather['WindSpeed'].mean()
                df['Rainfall'] = weather['Rainfall'].any()
        except:
            pass
        
        return df
        
    except Exception as e:
        print(f"  Round {round_num}: No data ({e})")
        return pd.DataFrame()


def collect_all_data():
    """Collect all historical data using round numbers."""
    all_data = []
    
    for year, num_races in RACES_PER_SEASON.items():
        print(f"\n{'='*50}")
        print(f"Collecting {year} season ({num_races} races)...")
        print('='*50)
        
        for round_num in range(1, num_races + 1):
            race_data = collect_race_by_round(year, round_num)
            if not race_data.empty:
                all_data.append(race_data)
    
    if not all_data:
        print("No data collected!")
        return
    
    combined = pd.concat(all_data, ignore_index=True)
    
    # Save to CSV
    output_path = config.DATA_DIR / "historical_data.csv"
    combined.to_csv(output_path, index=False)
    
    print(f"\n{'='*50}")
    print(f"COLLECTION COMPLETE")
    print(f"{'='*50}")
    print(f"Total rows: {len(combined)}")
    print(f"Seasons: {sorted(combined['Year'].unique())}")
    print(f"Events: {combined['EventName'].nunique()}")
    print(f"Saved to: {output_path}")
    
    # Show 2025 Canadian GP result to verify accuracy
    canada_2025 = combined[(combined['Year'] >= 2024) & (combined['EventName'].str.contains('Canada', na=False))]
    if not canada_2025.empty:
        print(f"\nCanadian GP results (recent):")
        print(canada_2025[['Year', 'Driver', 'Position', 'Team']].sort_values(['Year', 'Position']).head(6))


if __name__ == "__main__":
    collect_all_data()
