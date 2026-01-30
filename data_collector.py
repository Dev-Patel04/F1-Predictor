"""
Data Collector Module
Fetches F1 race data using FastF1 API including results, qualifying, 
practice sessions, weather, and pit stop data.
"""
import fastf1
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any
from pathlib import Path
import warnings
import config

# Enable FastF1 cache
fastf1.Cache.enable_cache(str(config.FASTF1_CACHE))

# Suppress FastF1 warnings for cleaner output
warnings.filterwarnings('ignore', module='fastf1')


def get_season_schedule(year: int) -> pd.DataFrame:
    """Get the race schedule for a given season."""
    try:
        schedule = fastf1.get_event_schedule(year)
        # Filter to only include race events (not testing)
        schedule = schedule[schedule['EventFormat'] != 'testing']
        return schedule
    except Exception as e:
        print(f"Error fetching {year} schedule: {e}")
        return pd.DataFrame()


def get_session_data(year: int, event: str, session_type: str = 'R') -> Optional[fastf1.core.Session]:
    """
    Load session data for a specific event.
    
    Args:
        year: Season year
        event: Event name or round number
        session_type: 'R' for Race, 'Q' for Qualifying, 'FP1'/'FP2'/'FP3' for practice
    
    Returns:
        Session object or None if failed
    """
    try:
        session = fastf1.get_session(year, event, session_type)
        session.load(telemetry=False, weather=True, messages=False)
        return session
    except Exception as e:
        print(f"Error loading {session_type} for {event} {year}: {e}")
        return None


def extract_race_results(session: fastf1.core.Session) -> pd.DataFrame:
    """Extract race results from a session."""
    if session is None:
        return pd.DataFrame()
    
    results = session.results
    if results.empty:
        return pd.DataFrame()
    
    df = pd.DataFrame({
        'Driver': results['Abbreviation'],
        'DriverNumber': results['DriverNumber'],
        'Team': results['TeamName'],
        'GridPosition': results['GridPosition'],
        'Position': results['Position'],
        'Points': results['Points'],
        'Status': results['Status'],
        'Time': results['Time'],
        'Year': session.event['EventDate'].year,
        'EventName': session.event['EventName'],
        'Round': session.event['RoundNumber']
    })
    
    # Mark winner
    df['IsWinner'] = (df['Position'] == 1).astype(int)
    df['IsPodium'] = (df['Position'] <= 3).astype(int)
    
    return df


def extract_qualifying_results(session: fastf1.core.Session) -> pd.DataFrame:
    """Extract qualifying results from a session."""
    if session is None:
        return pd.DataFrame()
    
    results = session.results
    if results.empty:
        return pd.DataFrame()
    
    df = pd.DataFrame({
        'Driver': results['Abbreviation'],
        'Team': results['TeamName'],
        'QualifyingPosition': results['Position'],
        'Q1': results['Q1'],
        'Q2': results['Q2'],
        'Q3': results['Q3'],
    })
    
    # Convert times to seconds
    for col in ['Q1', 'Q2', 'Q3']:
        df[f'{col}_seconds'] = df[col].apply(
            lambda x: x.total_seconds() if pd.notna(x) else np.nan
        )
    
    return df


def extract_practice_results(session: fastf1.core.Session) -> pd.DataFrame:
    """Extract practice session results."""
    if session is None:
        return pd.DataFrame()
    
    try:
        laps = session.laps
        if laps.empty:
            return pd.DataFrame()
        
        # Get best lap per driver
        best_laps = laps.groupby('Driver').agg({
            'LapTime': 'min',
            'Sector1Time': 'min',
            'Sector2Time': 'min', 
            'Sector3Time': 'min',
            'Compound': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown'
        }).reset_index()
        
        # Convert times to seconds
        for col in ['LapTime', 'Sector1Time', 'Sector2Time', 'Sector3Time']:
            best_laps[f'{col}_seconds'] = best_laps[col].apply(
                lambda x: x.total_seconds() if pd.notna(x) else np.nan
            )
        
        return best_laps
    except Exception as e:
        print(f"Error extracting practice data: {e}")
        return pd.DataFrame()


def extract_weather_data(session: fastf1.core.Session) -> Dict[str, Any]:
    """Extract weather data from a session."""
    if session is None:
        return {}
    
    try:
        weather = session.weather_data
        if weather is None or weather.empty:
            return {}
        
        return {
            'AirTemp': weather['AirTemp'].mean(),
            'TrackTemp': weather['TrackTemp'].mean(),
            'Humidity': weather['Humidity'].mean(),
            'Pressure': weather['Pressure'].mean(),
            'WindSpeed': weather['WindSpeed'].mean(),
            'WindDirection': weather['WindDirection'].mean(),
            'Rainfall': weather['Rainfall'].any(),  # Boolean: was there rain?
        }
    except Exception as e:
        print(f"Error extracting weather: {e}")
        return {}


def extract_pit_stop_data(session: fastf1.core.Session) -> pd.DataFrame:
    """Extract pit stop data from a race session."""
    if session is None:
        return pd.DataFrame()
    
    try:
        laps = session.laps
        if laps.empty:
            return pd.DataFrame()
        
        # Count pit stops and get pit stop times
        pit_data = laps.groupby('Driver').agg({
            'PitInTime': lambda x: x.notna().sum(),  # Count of pit stops
            'PitOutTime': 'count'
        }).reset_index()
        
        pit_data.columns = ['Driver', 'PitStopCount', 'TotalLaps']
        
        # Calculate average pit stop frequency
        pit_data['PitStopFrequency'] = pit_data['PitStopCount'] / pit_data['TotalLaps']
        
        return pit_data
    except Exception as e:
        print(f"Error extracting pit stop data: {e}")
        return pd.DataFrame()


def collect_race_data(year: int, event: str) -> pd.DataFrame:
    """
    Collect all relevant data for a single race event.
    
    Returns a DataFrame with one row per driver containing:
    - Race results
    - Qualifying results
    - Practice pace
    - Weather conditions
    - Pit stop data
    """
    print(f"Collecting data for {event} {year}...")
    
    # Get race results
    race_session = get_session_data(year, event, 'R')
    race_results = extract_race_results(race_session)
    
    if race_results.empty:
        print(f"No race results for {event} {year}")
        return pd.DataFrame()
    
    # Get qualifying results
    quali_session = get_session_data(year, event, 'Q')
    quali_results = extract_qualifying_results(quali_session)
    
    # Get practice sessions (FP1, FP2, FP3)
    fp_results = []
    for fp in ['FP1', 'FP2', 'FP3']:
        fp_session = get_session_data(year, event, fp)
        fp_data = extract_practice_results(fp_session)
        if not fp_data.empty:
            fp_data = fp_data.add_prefix(f'{fp}_')
            fp_data = fp_data.rename(columns={f'{fp}_Driver': 'Driver'})
            fp_results.append(fp_data)
    
    # Get weather from race
    weather = extract_weather_data(race_session)
    
    # Get pit stop data
    pit_data = extract_pit_stop_data(race_session)
    
    # Merge all data
    merged = race_results.copy()
    
    if not quali_results.empty:
        merged = merged.merge(quali_results, on='Driver', how='left', suffixes=('', '_quali'))
    
    for fp_data in fp_results:
        merged = merged.merge(fp_data, on='Driver', how='left')
    
    if not pit_data.empty:
        merged = merged.merge(pit_data, on='Driver', how='left')
    
    # Add weather data as columns
    for key, value in weather.items():
        merged[key] = value
    
    return merged


def collect_season_data(year: int) -> pd.DataFrame:
    """Collect data for all races in a season."""
    schedule = get_season_schedule(year)
    
    if schedule.empty:
        return pd.DataFrame()
    
    all_races = []
    
    for _, event in schedule.iterrows():
        event_name = event['EventName']
        
        # Skip future races (no data yet)
        if pd.isna(event.get('EventDate')):
            continue
            
        race_data = collect_race_data(year, event_name)
        if not race_data.empty:
            all_races.append(race_data)
    
    if not all_races:
        return pd.DataFrame()
    
    return pd.concat(all_races, ignore_index=True)


def collect_historical_data(seasons: List[int] = None) -> pd.DataFrame:
    """
    Collect historical data for multiple seasons.
    
    Args:
        seasons: List of years to collect. Defaults to config.SEASONS
    
    Returns:
        Combined DataFrame with all historical race data
    """
    if seasons is None:
        seasons = config.SEASONS
    
    all_data = []
    
    for year in seasons:
        print(f"\n{'='*50}")
        print(f"Collecting {year} season data...")
        print('='*50)
        
        season_data = collect_season_data(year)
        if not season_data.empty:
            all_data.append(season_data)
    
    if not all_data:
        return pd.DataFrame()
    
    combined = pd.concat(all_data, ignore_index=True)
    
    # Save to cache
    cache_path = config.DATA_DIR / "historical_data.csv"
    combined.to_csv(cache_path, index=False)
    print(f"\nSaved {len(combined)} rows to {cache_path}")
    
    return combined


def load_cached_data() -> Optional[pd.DataFrame]:
    """Load previously cached historical data."""
    cache_path = config.DATA_DIR / "historical_data.csv"
    
    if cache_path.exists():
        return pd.read_csv(cache_path)
    
    return None


if __name__ == "__main__":
    # Test data collection with a single race
    test_data = collect_race_data(2024, 'Monaco')
    print("\nSample data columns:")
    print(test_data.columns.tolist())
    print(f"\nShape: {test_data.shape}")
    print("\nFirst few rows:")
    print(test_data.head())
