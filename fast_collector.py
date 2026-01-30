"""
Fast Data Collector - Fetches only essential data (race results + qualifying)
Skips practice sessions for 4x faster collection.
"""
import fastf1
import pandas as pd
import numpy as np
from typing import List
import config

# Enable FastF1 cache
fastf1.Cache.enable_cache(str(config.FASTF1_CACHE))


def collect_fast(seasons: List[int] = None) -> pd.DataFrame:
    """
    Fast data collection - only race results and qualifying.
    ~4x faster than full collection.
    """
    if seasons is None:
        seasons = [2023]
    
    all_data = []
    
    for year in seasons:
        print(f"\n{'='*50}")
        print(f"Collecting {year} season (fast mode)...")
        print('='*50)
        
        try:
            schedule = fastf1.get_event_schedule(year)
            schedule = schedule[schedule['EventFormat'] != 'testing']
        except Exception as e:
            print(f"Error getting schedule: {e}")
            continue
        
        for _, event in schedule.iterrows():
            event_name = event['EventName']
            print(f"  {event_name}...", end=" ")
            
            try:
                # Get race session
                race = fastf1.get_session(year, event_name, 'R')
                race.load(telemetry=False, weather=True, messages=False)
                
                results = race.results
                if results.empty:
                    print("no data")
                    continue
                
                # Build DataFrame
                df = pd.DataFrame({
                    'Driver': results['Abbreviation'],
                    'Team': results['TeamName'],
                    'GridPosition': results['GridPosition'],
                    'Position': results['Position'],
                    'Points': results['Points'],
                    'Status': results['Status'],
                    'Year': year,
                    'EventName': event_name,
                    'Round': event['RoundNumber']
                })
                
                df['IsWinner'] = (df['Position'] == 1).astype(int)
                df['IsPodium'] = (df['Position'] <= 3).astype(int)
                
                # Get qualifying
                try:
                    quali = fastf1.get_session(year, event_name, 'Q')
                    quali.load(telemetry=False, weather=False, messages=False)
                    quali_results = quali.results
                    
                    if not quali_results.empty:
                        quali_df = pd.DataFrame({
                            'Driver': quali_results['Abbreviation'],
                            'QualifyingPosition': quali_results['Position'],
                        })
                        df = df.merge(quali_df, on='Driver', how='left')
                except:
                    pass
                
                # Get weather
                try:
                    weather = race.weather_data
                    if weather is not None and not weather.empty:
                        df['AirTemp'] = weather['AirTemp'].mean()
                        df['TrackTemp'] = weather['TrackTemp'].mean()
                        df['Rainfall'] = weather['Rainfall'].any()
                except:
                    pass
                
                all_data.append(df)
                print(f"✓ ({len(df)} drivers)")
                
            except Exception as e:
                print(f"error: {str(e)[:30]}")
                continue
    
    if not all_data:
        return pd.DataFrame()
    
    combined = pd.concat(all_data, ignore_index=True)
    
    # Save
    cache_path = config.DATA_DIR / "historical_data.csv"
    combined.to_csv(cache_path, index=False)
    print(f"\n✓ Saved {len(combined)} rows to {cache_path}")
    
    return combined


if __name__ == "__main__":
    data = collect_fast([2023])
    print(f"\nCollected {len(data)} race entries")
    print(f"Columns: {data.columns.tolist()}")
