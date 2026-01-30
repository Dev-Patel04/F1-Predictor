"""
Feature Engineering Module
Creates predictive features from raw F1 data including driver form,
historical performance, team strength, and session-specific metrics.
"""
import pandas as pd
import numpy as np
from typing import Optional, Dict, List
import config


def calculate_driver_recent_form(df: pd.DataFrame, window: int = None) -> pd.DataFrame:
    """
    Calculate driver's recent form based on last N races.
    
    Features created:
    - RecentAvgPosition: Average finishing position in recent races
    - RecentAvgPoints: Average points scored in recent races
    - RecentWinRate: Win rate in recent races
    - RecentPodiumRate: Podium rate in recent races
    """
    if window is None:
        window = config.RECENT_RACES_WINDOW
    
    df = df.sort_values(['Year', 'Round'])
    
    form_features = []
    
    for driver in df['Driver'].unique():
        driver_data = df[df['Driver'] == driver].copy()
        
        # Rolling calculations
        driver_data['RecentAvgPosition'] = driver_data['Position'].rolling(
            window=window, min_periods=1
        ).mean().shift(1)  # Shift to avoid data leakage
        
        driver_data['RecentAvgPoints'] = driver_data['Points'].rolling(
            window=window, min_periods=1
        ).mean().shift(1)
        
        driver_data['RecentWinRate'] = driver_data['IsWinner'].rolling(
            window=window, min_periods=1
        ).mean().shift(1)
        
        driver_data['RecentPodiumRate'] = driver_data['IsPodium'].rolling(
            window=window, min_periods=1
        ).mean().shift(1)
        
        form_features.append(driver_data)
    
    return pd.concat(form_features, ignore_index=True)


def calculate_historical_track_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate driver's historical performance at each track.
    
    Features created:
    - TrackAvgPosition: Historical average position at this track
    - TrackBestPosition: Best ever position at this track
    - TrackWinRate: Win rate at this track
    - TrackRaceCount: Number of races at this track
    """
    df = df.sort_values(['Year', 'Round'])
    
    track_features = []
    
    for (driver, track) in df.groupby(['Driver', 'EventName']).groups.keys():
        driver_track_data = df[(df['Driver'] == driver) & (df['EventName'] == track)].copy()
        
        # Calculate cumulative historical stats (excluding current race to avoid leakage)
        driver_track_data['TrackAvgPosition'] = driver_track_data['Position'].expanding().mean().shift(1)
        driver_track_data['TrackBestPosition'] = driver_track_data['Position'].expanding().min().shift(1)
        driver_track_data['TrackWinRate'] = driver_track_data['IsWinner'].expanding().mean().shift(1)
        driver_track_data['TrackRaceCount'] = range(len(driver_track_data))
        
        track_features.append(driver_track_data)
    
    return pd.concat(track_features, ignore_index=True)


def calculate_team_strength(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate team strength metrics.
    
    Features created:
    - TeamSeasonPoints: Team's total points so far this season
    - TeamSeasonWins: Team's wins so far this season
    - TeamAvgPosition: Team's average position this season
    """
    df = df.sort_values(['Year', 'Round'])
    
    team_features = []
    
    for (team, year) in df.groupby(['Team', 'Year']).groups.keys():
        team_year_data = df[(df['Team'] == team) & (df['Year'] == year)].copy()
        
        # Cumulative team stats within season
        team_year_data['TeamSeasonPoints'] = team_year_data.groupby('Round')['Points'].transform('sum').cumsum().shift(1)
        team_year_data['TeamSeasonWins'] = team_year_data['IsWinner'].cumsum().shift(1)
        team_year_data['TeamAvgPosition'] = team_year_data['Position'].expanding().mean().shift(1)
        
        team_features.append(team_year_data)
    
    return pd.concat(team_features, ignore_index=True)


def calculate_qualifying_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create features from qualifying performance.
    
    Features created:
    - QualifyingGap: Gap to pole position (seconds)
    - QualifyingPercentile: Qualifying position percentile
    - GridVsQualifying: Difference between grid and qualifying position
    """
    df = df.copy()
    
    # Get best Q3 time in each race for gap calculation
    if 'Q3_seconds' in df.columns:
        df['QualifyingBestTime'] = df.groupby(['Year', 'Round'])['Q3_seconds'].transform('min')
        df['QualifyingGap'] = df['Q3_seconds'] - df['QualifyingBestTime']
    
    # Qualifying percentile (1 = pole, 0 = last)
    if 'QualifyingPosition' in df.columns:
        df['QualifyingPercentile'] = 1 - (df['QualifyingPosition'] - 1) / df.groupby(['Year', 'Round'])['QualifyingPosition'].transform('max')
    
    # Grid adjustments (penalties, etc.)
    if 'GridPosition' in df.columns and 'QualifyingPosition' in df.columns:
        df['GridVsQualifying'] = df['GridPosition'] - df['QualifyingPosition']
    
    return df


def calculate_practice_pace(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create features from practice session performance.
    
    Features created:
    - BestPracticePace: Best practice lap time percentile
    - PracticeConsistency: Consistency across practice sessions
    """
    df = df.copy()
    
    practice_cols = [col for col in df.columns if 'FP' in col and 'LapTime_seconds' in col]
    
    if practice_cols:
        # Get best practice time
        df['BestPracticeTime'] = df[practice_cols].min(axis=1)
        
        # Calculate percentile within each race
        df['BestPracticePace'] = 1 - df.groupby(['Year', 'Round'])['BestPracticeTime'].rank(pct=True)
        
        # Consistency across practice sessions (lower std = more consistent)
        df['PracticeConsistency'] = df[practice_cols].std(axis=1)
    
    return df


def calculate_weather_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create features from weather data.
    
    Features created:
    - IsWetRace: Boolean for rain during race
    - TempCategory: Categorized temperature (cold/mild/hot)
    - HighWinds: Boolean for high wind speeds
    """
    df = df.copy()
    
    if 'Rainfall' in df.columns:
        df['IsWetRace'] = df['Rainfall'].astype(int)
    
    if 'TrackTemp' in df.columns:
        df['TempCategory'] = pd.cut(
            df['TrackTemp'],
            bins=[0, 25, 40, 100],
            labels=['cold', 'mild', 'hot']
        )
        # One-hot encode
        df = pd.get_dummies(df, columns=['TempCategory'], prefix='Temp')
    
    if 'WindSpeed' in df.columns:
        df['HighWinds'] = (df['WindSpeed'] > 5).astype(int)  # Threshold: 5 m/s
    
    return df


def calculate_pit_stop_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create features from pit stop data.
    
    Features created:
    - PitStopStrategy: Categorized pit stop count
    - AvgPitStopRate: Average pit stops per race historically
    """
    df = df.copy()
    
    if 'PitStopCount' in df.columns:
        # Categorize pit stop strategies
        df['PitStopStrategy'] = pd.cut(
            df['PitStopCount'].fillna(2),
            bins=[0, 1, 2, 3, 10],
            labels=['one_stop', 'two_stop', 'three_stop', 'multi_stop']
        )
    
    return df


def calculate_championship_position(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate current championship standings.
    
    Features created:
    - ChampionshipPosition: Current standing in championship
    - ChampionshipPoints: Total points so far
    - PointsToLeader: Gap to championship leader
    """
    df = df.sort_values(['Year', 'Round'])
    
    champ_features = []
    
    for year in df['Year'].unique():
        year_data = df[df['Year'] == year].copy()
        
        # Calculate cumulative points
        year_data['ChampionshipPoints'] = year_data.groupby('Driver')['Points'].cumsum().shift(1)
        
        # Calculate position based on cumulative points
        year_data['ChampionshipPosition'] = year_data.groupby('Round')['ChampionshipPoints'].rank(
            ascending=False, method='min'
        )
        
        # Gap to leader
        year_data['LeaderPoints'] = year_data.groupby('Round')['ChampionshipPoints'].transform('max')
        year_data['PointsToLeader'] = year_data['LeaderPoints'] - year_data['ChampionshipPoints']
        
        champ_features.append(year_data)
    
    return pd.concat(champ_features, ignore_index=True)


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all feature engineering to the dataset.
    
    Args:
        df: Raw race data from data_collector
    
    Returns:
        DataFrame with all engineered features
    """
    if df.empty:
        return df
    
    print("Calculating driver recent form...")
    df = calculate_driver_recent_form(df)
    
    print("Calculating historical track performance...")
    df = calculate_historical_track_performance(df)
    
    print("Calculating team strength...")
    df = calculate_team_strength(df)
    
    print("Calculating qualifying features...")
    df = calculate_qualifying_features(df)
    
    print("Calculating practice pace...")
    df = calculate_practice_pace(df)
    
    print("Calculating weather features...")
    df = calculate_weather_features(df)
    
    print("Calculating pit stop features...")
    df = calculate_pit_stop_features(df)
    
    print("Calculating championship position...")
    df = calculate_championship_position(df)
    
    return df


def get_feature_columns() -> List[str]:
    """Get list of feature columns to use for modeling."""
    return [
        # Recent form
        'RecentAvgPosition', 'RecentAvgPoints', 'RecentWinRate', 'RecentPodiumRate',
        # Historical track performance
        'TrackAvgPosition', 'TrackBestPosition', 'TrackWinRate', 'TrackRaceCount',
        # Team strength
        'TeamSeasonPoints', 'TeamSeasonWins', 'TeamAvgPosition',
        # Qualifying
        'QualifyingPosition', 'QualifyingGap', 'QualifyingPercentile', 'GridPosition',
        # Practice
        'BestPracticePace', 'PracticeConsistency',
        # Weather
        'AirTemp', 'TrackTemp', 'Humidity', 'WindSpeed', 'IsWetRace', 'HighWinds',
        # Pit stops
        'PitStopCount', 'PitStopFrequency',
        # Championship
        'ChampionshipPosition', 'ChampionshipPoints', 'PointsToLeader',
    ]


def prepare_training_data(df: pd.DataFrame) -> tuple:
    """
    Prepare data for model training.
    
    Returns:
        X: Feature matrix
        y: Target vector (IsWinner)
        feature_names: List of feature column names
    """
    feature_cols = get_feature_columns()
    
    # Filter to columns that exist
    available_features = [col for col in feature_cols if col in df.columns]
    
    # Remove rows with too many missing values
    df_clean = df.dropna(subset=['IsWinner'])
    
    X = df_clean[available_features].copy()
    y = df_clean['IsWinner'].copy()
    
    # Fill remaining NaN values
    X = X.fillna(X.median())
    
    print(f"Training data shape: {X.shape}")
    print(f"Features used: {available_features}")
    print(f"Winner rate: {y.mean():.2%}")
    
    return X, y, available_features


if __name__ == "__main__":
    # Test feature engineering
    from data_collector import load_cached_data
    
    data = load_cached_data()
    if data is not None:
        featured = create_features(data)
        X, y, features = prepare_training_data(featured)
        print(f"\nFeature matrix shape: {X.shape}")
        print(f"Target shape: {y.shape}")
