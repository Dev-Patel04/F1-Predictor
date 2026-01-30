"""
ML Model Module
Trains and evaluates machine learning models for F1 race winner prediction.
Supports Random Forest and XGBoost classifiers.
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)
import xgboost as xgb
import joblib
from pathlib import Path
from typing import Tuple, Dict, Any, Optional
import config


class F1Predictor:
    """F1 race winner prediction model."""
    
    def __init__(self, model_type: str = None):
        """
        Initialize the predictor.
        
        Args:
            model_type: 'random_forest' or 'xgboost'. Defaults to config setting.
        """
        self.model_type = model_type or config.MODEL_TYPE
        self.model = None
        self.feature_names = None
        self.is_trained = False
        
    def _create_model(self):
        """Create the ML model based on model_type."""
        if self.model_type == "random_forest":
            return RandomForestClassifier(**config.RF_PARAMS)
        elif self.model_type == "xgboost":
            return xgb.XGBClassifier(**config.XGB_PARAMS)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def train(self, X: pd.DataFrame, y: pd.Series, 
              test_size: float = 0.2) -> Dict[str, float]:
        """
        Train the model.
        
        Args:
            X: Feature matrix
            y: Target vector
            test_size: Fraction of data for testing
        
        Returns:
            Dictionary with evaluation metrics
        """
        print(f"\nTraining {self.model_type} model...")
        print(f"Data shape: {X.shape}")
        
        # Store feature names
        self.feature_names = X.columns.tolist()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=config.RANDOM_STATE, stratify=y
        )
        
        print(f"Training set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")
        print(f"Class balance - Train: {y_train.mean():.2%}, Test: {y_test.mean():.2%}")
        
        # Create and train model
        self.model = self._create_model()
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test)[:, 1]
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
        }
        
        # Calculate top-N accuracy (important for F1 prediction)
        # Sort by probability and check if winner is in top N
        test_df = pd.DataFrame({
            'y_true': y_test.values,
            'y_prob': y_prob
        })
        
        # Calculate per-race top-N accuracy if we have race groupings
        metrics['top3_accuracy'] = self._calculate_top_n_accuracy(X_test, y_test, y_prob, n=3)
        metrics['top5_accuracy'] = self._calculate_top_n_accuracy(X_test, y_test, y_prob, n=5)
        
        print("\n" + "="*50)
        print("Model Evaluation Results")
        print("="*50)
        print(f"Accuracy: {metrics['accuracy']:.2%}")
        print(f"Precision: {metrics['precision']:.2%}")
        print(f"Recall: {metrics['recall']:.2%}")
        print(f"F1 Score: {metrics['f1']:.2%}")
        print(f"Top-3 Accuracy: {metrics['top3_accuracy']:.2%}")
        print(f"Top-5 Accuracy: {metrics['top5_accuracy']:.2%}")
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Not Winner', 'Winner']))
        
        return metrics
    
    def _calculate_top_n_accuracy(self, X: pd.DataFrame, y: pd.Series, 
                                   probs: np.ndarray, n: int = 3) -> float:
        """Calculate if actual winner is in top-N predictions."""
        # Simple approximation: check if any of the top-N probabilities were winners
        sorted_indices = np.argsort(probs)[::-1][:n]
        return y.iloc[sorted_indices].max()
    
    def cross_validate(self, X: pd.DataFrame, y: pd.Series, cv: int = 5) -> Dict[str, float]:
        """
        Perform cross-validation.
        
        Args:
            X: Feature matrix
            y: Target vector
            cv: Number of folds
        
        Returns:
            Dictionary with CV scores
        """
        print(f"\nPerforming {cv}-fold cross-validation...")
        
        model = self._create_model()
        
        scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
        
        print(f"CV Accuracy: {scores.mean():.2%} (+/- {scores.std() * 2:.2%})")
        
        return {
            'cv_mean': scores.mean(),
            'cv_std': scores.std(),
            'cv_scores': scores.tolist()
        }
    
    def get_feature_importance(self) -> pd.DataFrame:
        """Get feature importance from the trained model."""
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        if self.model_type == "random_forest":
            importances = self.model.feature_importances_
        elif self.model_type == "xgboost":
            importances = self.model.feature_importances_
        else:
            return pd.DataFrame()
        
        importance_df = pd.DataFrame({
            'Feature': self.feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=False)
        
        return importance_df
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict race winner (binary)."""
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        return self.model.predict(X)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Predict win probability for each driver."""
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        return self.model.predict_proba(X)[:, 1]
    
    def predict_race(self, race_data: pd.DataFrame, feature_cols: list) -> pd.DataFrame:
        """
        Predict race outcome with win probabilities for each driver.
        
        Args:
            race_data: DataFrame with driver data for upcoming race
            feature_cols: List of feature columns to use
        
        Returns:
            DataFrame with drivers ranked by win probability
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        # Prepare features
        available_features = [col for col in feature_cols if col in race_data.columns]
        X = race_data[available_features].fillna(race_data[available_features].median())
        
        # Predict probabilities
        probabilities = self.predict_proba(X)
        
        # Create results DataFrame
        results = pd.DataFrame({
            'Driver': race_data['Driver'].values,
            'Team': race_data['Team'].values,
            'WinProbability': probabilities,
            'GridPosition': race_data.get('GridPosition', pd.Series([np.nan] * len(race_data))).values
        })
        
        # Rank by probability
        results = results.sort_values('WinProbability', ascending=False)
        results['PredictedPosition'] = range(1, len(results) + 1)
        
        return results
    
    def save(self, path: Path = None):
        """Save the trained model to disk."""
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        if path is None:
            path = config.MODEL_DIR / f"f1_predictor_{self.model_type}.joblib"
        
        model_data = {
            'model': self.model,
            'model_type': self.model_type,
            'feature_names': self.feature_names
        }
        
        joblib.dump(model_data, path)
        print(f"Model saved to {path}")
    
    def load(self, path: Path = None):
        """Load a trained model from disk."""
        if path is None:
            path = config.MODEL_DIR / f"f1_predictor_{self.model_type}.joblib"
        
        if not path.exists():
            raise FileNotFoundError(f"No model found at {path}")
        
        model_data = joblib.load(path)
        
        self.model = model_data['model']
        self.model_type = model_data['model_type']
        self.feature_names = model_data['feature_names']
        self.is_trained = True
        
        print(f"Model loaded from {path}")


def train_model(X: pd.DataFrame, y: pd.Series, 
                model_type: str = None) -> Tuple[F1Predictor, Dict[str, float]]:
    """
    Train a new F1 predictor model.
    
    Args:
        X: Feature matrix
        y: Target vector
        model_type: 'random_forest' or 'xgboost'
    
    Returns:
        Trained predictor and metrics dictionary
    """
    predictor = F1Predictor(model_type)
    metrics = predictor.train(X, y)
    
    # Print feature importance
    print("\nTop 10 Most Important Features:")
    importance = predictor.get_feature_importance()
    print(importance.head(10).to_string(index=False))
    
    # Save model
    predictor.save()
    
    return predictor, metrics


if __name__ == "__main__":
    # Test model training
    from data_collector import load_cached_data
    from feature_engineering import create_features, prepare_training_data
    
    data = load_cached_data()
    if data is not None:
        featured = create_features(data)
        X, y, features = prepare_training_data(featured)
        
        # Train Random Forest
        print("\n" + "="*60)
        print("Training Random Forest Model")
        print("="*60)
        rf_model, rf_metrics = train_model(X, y, "random_forest")
        
        # Train XGBoost
        print("\n" + "="*60)
        print("Training XGBoost Model")
        print("="*60)
        xgb_model, xgb_metrics = train_model(X, y, "xgboost")
