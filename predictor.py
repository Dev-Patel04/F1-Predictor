"""
Predictor Module
User-facing prediction interface for upcoming F1 races.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import config
from data_collector import (
    get_season_schedule, get_session_data, 
    extract_qualifying_results, extract_practice_results,
    extract_weather_data
)
from feature_engineering import get_feature_columns
from model import F1Predictor


def get_upcoming_races(limit: int = 5) -> pd.DataFrame:
    """
    Get upcoming races from the current season schedule.
    
    Args:
        limit: Maximum number of upcoming races to return
    
    Returns:
        DataFrame with upcoming race information
    """
    current_year = datetime.now().year
    schedule = get_season_schedule(current_year)
    
    if schedule.empty:
        return pd.DataFrame()
    
    # Filter to future races
    today = datetime.now()
    schedule['EventDate'] = pd.to_datetime(schedule['EventDate'])
    upcoming = schedule[schedule['EventDate'] > today].head(limit)
    
    return upcoming[['RoundNumber', 'EventName', 'Country', 'EventDate']]


def get_current_standings() -> pd.DataFrame:
    """
    Get current driver standings for the season.
    
    Returns:
        DataFrame with driver standings
    """
    current_year = datetime.now().year
    
    # Get all completed races this season
    schedule = get_season_schedule(current_year)
    if schedule.empty:
        return pd.DataFrame()
    
    today = datetime.now()
    schedule['EventDate'] = pd.to_datetime(schedule['EventDate'])
    completed = schedule[schedule['EventDate'] < today]
    
    if completed.empty:
        return pd.DataFrame()
    
    # Get results from each race and calculate standings
    standings = {}
    
    for _, race in completed.iterrows():
        session = get_session_data(current_year, race['EventName'], 'R')
        if session is None:
            continue
        
        results = session.results
        for _, driver in results.iterrows():
            abbrev = driver['Abbreviation']
            points = driver['Points']
            
            if abbrev not in standings:
                standings[abbrev] = {'Driver': abbrev, 'Team': driver['TeamName'], 'Points': 0}
            standings[abbrev]['Points'] += points
    
    standings_df = pd.DataFrame(standings.values())
    standings_df = standings_df.sort_values('Points', ascending=False)
    standings_df['Position'] = range(1, len(standings_df) + 1)
    
    return standings_df


def prepare_race_prediction_data(year: int, event: str) -> pd.DataFrame:
    """
    Prepare data for predicting an upcoming race.
    
    Fetches qualifying results, practice data, and any available 
    pre-race information to create features for prediction.
    
    Args:
        year: Season year
        event: Event name
    
    Returns:
        DataFrame with one row per driver containing prediction features
    """
    print(f"Preparing prediction data for {event} {year}...")
    
    # Get qualifying results
    quali_session = get_session_data(year, event, 'Q')
    quali_results = extract_qualifying_results(quali_session)
    
    if quali_results.empty:
        print("Warning: No qualifying data available")
        return pd.DataFrame()
    
    # Get practice sessions
    practice_data = {}
    for fp in ['FP1', 'FP2', 'FP3']:
        fp_session = get_session_data(year, event, fp)
        fp_results = extract_practice_results(fp_session)
        if not fp_results.empty:
            practice_data[fp] = fp_results
    
    # Get weather forecast (from latest available session)
    weather = {}
    for session_type in ['FP3', 'Q', 'FP2', 'FP1']:
        session = get_session_data(year, event, session_type)
        weather = extract_weather_data(session)
        if weather:
            break
    
    # Merge all data
    prediction_data = quali_results.copy()
    
    for fp_name, fp_data in practice_data.items():
        fp_data = fp_data.add_prefix(f'{fp_name}_')
        fp_data = fp_data.rename(columns={f'{fp_name}_Driver': 'Driver'})
        prediction_data = prediction_data.merge(fp_data, on='Driver', how='left')
    
    # Add weather
    for key, value in weather.items():
        prediction_data[key] = value
    
    # Add grid position (same as qualifying for now, could be adjusted for penalties)
    prediction_data['GridPosition'] = prediction_data['QualifyingPosition']
    
    prediction_data['Year'] = year
    prediction_data['EventName'] = event
    
    return prediction_data


def add_historical_features(prediction_data: pd.DataFrame, 
                           historical_data: pd.DataFrame) -> pd.DataFrame:
    """
    Add historical performance features to prediction data.
    
    Handles new teams (like Cadillac) by:
    1. Using driver's personal history (even from other teams)
    2. Applying baseline defaults for new team metrics
    
    Args:
        prediction_data: Current race data
        historical_data: Historical race results
    
    Returns:
        Prediction data with historical features added
    """
    if historical_data.empty:
        return prediction_data
    
    event_name = prediction_data['EventName'].iloc[0] if 'EventName' in prediction_data.columns else None
    
    # Get new team defaults from config
    new_team_defaults = getattr(config, 'NEW_TEAM_DEFAULTS', {})
    
    for idx, row in prediction_data.iterrows():
        driver = row['Driver']
        team = row['Team']
        
        # Get driver history (regardless of team - captures moved drivers like Perez, Bottas)
        driver_history = historical_data[historical_data['Driver'] == driver]
        
        if not driver_history.empty:
            # Recent form (last 5 races) - uses driver's personal history
            recent = driver_history.tail(config.RECENT_RACES_WINDOW)
            prediction_data.loc[idx, 'RecentAvgPosition'] = recent['Position'].mean()
            prediction_data.loc[idx, 'RecentAvgPoints'] = recent['Points'].mean()
            prediction_data.loc[idx, 'RecentWinRate'] = recent['IsWinner'].mean()
            prediction_data.loc[idx, 'RecentPodiumRate'] = (recent['Position'] <= 3).mean()
            
            # Track-specific history (driver's personal track record)
            if event_name:
                track_history = driver_history[driver_history['EventName'] == event_name]
                if not track_history.empty:
                    prediction_data.loc[idx, 'TrackAvgPosition'] = track_history['Position'].mean()
                    prediction_data.loc[idx, 'TrackBestPosition'] = track_history['Position'].min()
                    prediction_data.loc[idx, 'TrackWinRate'] = track_history['IsWinner'].mean()
                    prediction_data.loc[idx, 'TrackRaceCount'] = len(track_history)
        
        # Team stats - handle new teams differently
        team_history = historical_data[historical_data['Team'] == team]
        
        if not team_history.empty:
            # Existing team - use their history
            recent_team = team_history.tail(config.RECENT_RACES_WINDOW * 2)  # 2 drivers
            prediction_data.loc[idx, 'TeamAvgPosition'] = recent_team['Position'].mean()
            prediction_data.loc[idx, 'TeamSeasonWins'] = recent_team['IsWinner'].sum()
        elif team in new_team_defaults:
            # New team (like Cadillac) - use configured defaults
            defaults = new_team_defaults[team]
            prediction_data.loc[idx, 'TeamAvgPosition'] = defaults.get('baseline_constructor_position', 10) * 2
            prediction_data.loc[idx, 'TeamSeasonWins'] = 0
            prediction_data.loc[idx, 'TeamReliabilityFactor'] = defaults.get('reliability_factor', 0.85)
        else:
            # Unknown new team - conservative defaults
            prediction_data.loc[idx, 'TeamAvgPosition'] = 15  # Mid-back of grid
            prediction_data.loc[idx, 'TeamSeasonWins'] = 0
    
    return prediction_data


def predict_race(event: str = None, year: int = None, 
                model_type: str = None) -> pd.DataFrame:
    """
    Predict race winner for an upcoming race.
    
    Args:
        event: Event name. If None, uses next upcoming race.
        year: Season year. If None, uses current year.
        model_type: Model to use. If None, uses config default.
    
    Returns:
        DataFrame with predicted win probabilities for each driver
    """
    if year is None:
        year = datetime.now().year
    
    # Get next race if not specified
    if event is None:
        upcoming = get_upcoming_races(1)
        if upcoming.empty:
            print("No upcoming races found")
            return pd.DataFrame()
        event = upcoming.iloc[0]['EventName']
        print(f"Predicting next race: {event}")
    
    # Load model
    predictor = F1Predictor(model_type)
    try:
        predictor.load()
    except FileNotFoundError:
        print("No trained model found. Please run 'python main.py train' first.")
        return pd.DataFrame()
    
    # Prepare prediction data
    prediction_data = prepare_race_prediction_data(year, event)
    
    if prediction_data.empty:
        print("Could not prepare prediction data")
        return pd.DataFrame()
    
    # Load historical data for additional features
    from data_collector import load_cached_data
    historical_data = load_cached_data()
    
    if historical_data is not None:
        prediction_data = add_historical_features(prediction_data, historical_data)
    
    # Make predictions
    feature_cols = get_feature_columns()
    results = predictor.predict_race(prediction_data, feature_cols)
    
    return results


def format_predictions(predictions: pd.DataFrame) -> str:
    """Format predictions for display."""
    if predictions.empty:
        return "No predictions available"
    
    output = []
    output.append("\n" + "="*60)
    output.append("F1 RACE WINNER PREDICTION")
    output.append("="*60)
    output.append("")
    output.append(f"{'Pos':<5}{'Driver':<10}{'Team':<25}{'Win Prob':<12}{'Grid':<5}")
    output.append("-"*60)
    
    for _, row in predictions.iterrows():
        grid = int(row['GridPosition']) if pd.notna(row['GridPosition']) else '-'
        output.append(
            f"{int(row['PredictedPosition']):<5}"
            f"{row['Driver']:<10}"
            f"{row['Team'][:24]:<25}"
            f"{row['WinProbability']:>8.1%}    "
            f"{grid:<5}"
        )
    
    output.append("="*60)
    
    return "\n".join(output)


if __name__ == "__main__":
    # Test predictions
    predictions = predict_race()
    print(format_predictions(predictions))
