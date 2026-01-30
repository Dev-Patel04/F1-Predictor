"""
Quick Model Training and Evaluation
Uses the simplified data from fast_collector.py
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import config


def load_data():
    """Load collected data."""
    path = config.DATA_DIR / "historical_data.csv"
    return pd.read_csv(path)


def add_features(df):
    """Add simple features for prediction."""
    df = df.sort_values(['Year', 'Round'])
    
    # Calculate rolling stats per driver
    features = []
    
    for driver in df['Driver'].unique():
        driver_data = df[df['Driver'] == driver].copy()
        
        # Recent form (rolling average position)
        driver_data['RecentAvgPosition'] = driver_data['Position'].rolling(5, min_periods=1).mean().shift(1)
        driver_data['RecentWinRate'] = driver_data['IsWinner'].rolling(5, min_periods=1).mean().shift(1)
        driver_data['RecentPodiumRate'] = driver_data['IsPodium'].rolling(5, min_periods=1).mean().shift(1)
        
        features.append(driver_data)
    
    return pd.concat(features, ignore_index=True)


def train_and_evaluate():
    """Train model and show results."""
    print("="*60)
    print("F1 RACE WINNER PREDICTION - MODEL TRAINING")
    print("="*60)
    
    # Load and prepare data
    print("\nLoading data...")
    df = load_data()
    print(f"Loaded {len(df)} race entries from {df['EventName'].nunique()} races")
    
    # Add features
    print("Engineering features...")
    df = add_features(df)
    
    # Prepare training data
    feature_cols = ['GridPosition', 'QualifyingPosition', 'RecentAvgPosition', 
                    'RecentWinRate', 'RecentPodiumRate', 'AirTemp', 'TrackTemp']
    
    # Filter available columns
    available = [c for c in feature_cols if c in df.columns]
    print(f"Using features: {available}")
    
    # Remove rows with missing target
    df_clean = df.dropna(subset=['IsWinner'])
    
    X = df_clean[available].fillna(df_clean[available].median())
    y = df_clean['IsWinner']
    
    print(f"\nTraining data: {len(X)} samples")
    print(f"Winner rate: {y.mean():.1%} (baseline)")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    # Train model
    print("\nTraining Random Forest...")
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.1%}")
    
    # Top-N accuracy per race
    test_df = df_clean.iloc[X_test.index].copy()
    test_df['Probability'] = y_prob
    
    correct_in_top3 = 0
    correct_in_top5 = 0
    total_races = 0
    
    for (year, round_num), race in test_df.groupby(['Year', 'Round']):
        race_sorted = race.sort_values('Probability', ascending=False)
        actual_winner = race[race['IsWinner'] == 1]
        
        if len(actual_winner) == 0:
            continue
            
        total_races += 1
        winner_driver = actual_winner['Driver'].iloc[0]
        
        top3 = race_sorted.head(3)['Driver'].tolist()
        top5 = race_sorted.head(5)['Driver'].tolist()
        
        if winner_driver in top3:
            correct_in_top3 += 1
        if winner_driver in top5:
            correct_in_top5 += 1
    
    print(f"Top-3 Accuracy: {correct_in_top3}/{total_races} = {correct_in_top3/total_races:.1%}")
    print(f"Top-5 Accuracy: {correct_in_top5}/{total_races} = {correct_in_top5/total_races:.1%}")
    
    # Feature importance
    print("\n" + "-"*40)
    print("Feature Importance:")
    print("-"*40)
    importance = pd.DataFrame({
        'Feature': available,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    for _, row in importance.iterrows():
        bar = '█' * int(row['Importance'] * 50)
        print(f"{row['Feature']:25} {row['Importance']:.3f} {bar}")
    
    # Cross-validation
    print("\n" + "-"*40)
    print("5-Fold Cross-Validation:")
    print("-"*40)
    cv_scores = cross_val_score(model, X, y, cv=5)
    print(f"CV Accuracy: {cv_scores.mean():.1%} (+/- {cv_scores.std()*2:.1%})")
    
    # Show sample predictions
    print("\n" + "="*60)
    print("SAMPLE PREDICTION - Last Race in Test Set")
    print("="*60)
    
    last_race = test_df.groupby(['Year', 'Round']).last().reset_index()
    last_year = last_race['Year'].iloc[-1]
    last_round = last_race['Round'].iloc[-1]
    
    sample_race = test_df[(test_df['Year'] == last_year) & (test_df['Round'] == last_round)]
    sample_race = sample_race.sort_values('Probability', ascending=False)
    
    print(f"\nRace: {sample_race['EventName'].iloc[0]} {last_year}")
    print(f"\n{'Pred':<5}{'Driver':<8}{'Team':<22}{'Win Prob':<10}{'Actual':<8}")
    print("-"*55)
    
    for i, (_, row) in enumerate(sample_race.head(10).iterrows(), 1):
        actual = '★ WINNER' if row['IsWinner'] else f"P{int(row['Position'])}"
        print(f"{i:<5}{row['Driver']:<8}{row['Team'][:21]:<22}{row['Probability']:>7.1%}   {actual}")
    
    return model


if __name__ == "__main__":
    model = train_and_evaluate()
