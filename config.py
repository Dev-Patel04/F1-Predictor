"""
F1 Predictor Configuration
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
CACHE_DIR = PROJECT_ROOT / "cache"
MODEL_DIR = PROJECT_ROOT / "models"
DATA_DIR = PROJECT_ROOT / "data"

# Create directories if they don't exist
CACHE_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Data collection settings
SEASONS = [2022, 2023, 2024, 2025]  # Seasons to use for training (post-2022 regulations)
MIN_SEASON = 2022  # Don't go before regulation changes

# FastF1 cache
FASTF1_CACHE = CACHE_DIR / "fastf1"
FASTF1_CACHE.mkdir(exist_ok=True)

# Model settings
MODEL_TYPE = "random_forest"  # Options: "random_forest", "xgboost"
RANDOM_STATE = 42

# Random Forest hyperparameters
RF_PARAMS = {
    "n_estimators": 200,
    "max_depth": 15,
    "min_samples_split": 5,
    "min_samples_leaf": 2,
    "random_state": RANDOM_STATE,
    "n_jobs": -1
}

# XGBoost hyperparameters
XGB_PARAMS = {
    "n_estimators": 200,
    "max_depth": 8,
    "learning_rate": 0.1,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": RANDOM_STATE,
    "n_jobs": -1
}

# Feature engineering settings
RECENT_RACES_WINDOW = 5  # Number of recent races to consider for form
HISTORICAL_WEIGHT_DECAY = 0.9  # Decay factor for older race results

# 2025 F1 Teams and Drivers
TEAMS_2025 = {
    "Red Bull Racing": ["Max Verstappen", "Liam Lawson"],
    "Ferrari": ["Charles Leclerc", "Lewis Hamilton"],
    "McLaren": ["Lando Norris", "Oscar Piastri"],
    "Mercedes": ["George Russell", "Andrea Kimi Antonelli"],
    "Aston Martin": ["Fernando Alonso", "Lance Stroll"],
    "Alpine": ["Pierre Gasly", "Jack Doohan"],
    "Williams": ["Alex Albon", "Carlos Sainz"],
    "RB": ["Yuki Tsunoda", "Isack Hadjar"],
    "Kick Sauber": ["Nico Hulkenberg", "Gabriel Bortoleto"],
    "Haas F1 Team": ["Esteban Ocon", "Oliver Bearman"],
    "Cadillac": ["Sergio Perez", "Valtteri Bottas"],  # New 2025 team
}

# Driver to team mapping for quick lookup
DRIVER_TEAM_MAP_2025 = {
    driver: team 
    for team, drivers in TEAMS_2025.items() 
    for driver in drivers
}

# New team baseline settings (for teams without historical data)
NEW_TEAM_DEFAULTS = {
    "Cadillac": {
        "baseline_constructor_position": 10,  # Conservative estimate for new team
        "reliability_factor": 0.85,  # Slightly lower reliability expected
        "development_rate": 1.0,  # Neutral development assumption
    }
}
