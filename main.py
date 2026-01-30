"""
F1 Race Winner Prediction System
================================
Main entry point for training models and making predictions.

Usage:
    python main.py train              # Train model on historical data
    python main.py predict            # Predict next race winner
    python main.py predict Monaco     # Predict specific race
    python main.py evaluate           # Show model performance
    python main.py schedule           # Show upcoming races
    python main.py collect            # Collect/update historical data
"""
import sys
import argparse
from datetime import datetime
import config


def cmd_train(args):
    """Train the prediction model on historical data."""
    from data_collector import collect_historical_data, load_cached_data
    from feature_engineering import create_features, prepare_training_data
    from model import train_model
    
    print("\n" + "="*60)
    print("F1 RACE WINNER PREDICTION MODEL TRAINING")
    print("="*60)
    
    # Check for cached data or collect new
    data = load_cached_data()
    
    if data is None or args.refresh:
        print("\nCollecting historical data...")
        seasons = args.seasons if args.seasons else config.SEASONS
        data = collect_historical_data(seasons)
    else:
        print(f"\nUsing cached data with {len(data)} rows")
    
    if data is None or data.empty:
        print("Error: No data available for training")
        return
    
    # Feature engineering
    print("\nEngineering features...")
    featured_data = create_features(data)
    
    # Prepare training data
    X, y, features = prepare_training_data(featured_data)
    
    if len(X) == 0:
        print("Error: No valid training samples")
        return
    
    # Train model
    model_type = args.model if args.model else config.MODEL_TYPE
    predictor, metrics = train_model(X, y, model_type)
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE")
    print("="*60)
    print(f"Model saved to: {config.MODEL_DIR}")


def cmd_predict(args):
    """Predict race winner."""
    from predictor import predict_race, format_predictions
    
    event = args.event if args.event else None
    year = args.year if args.year else datetime.now().year
    model_type = args.model if args.model else None
    
    predictions = predict_race(event, year, model_type)
    print(format_predictions(predictions))


def cmd_evaluate(args):
    """Show model evaluation metrics."""
    from data_collector import load_cached_data
    from feature_engineering import create_features, prepare_training_data
    from model import F1Predictor
    
    print("\n" + "="*60)
    print("MODEL EVALUATION")
    print("="*60)
    
    model_type = args.model if args.model else config.MODEL_TYPE
    predictor = F1Predictor(model_type)
    
    try:
        predictor.load()
    except FileNotFoundError:
        print("No trained model found. Run 'python main.py train' first.")
        return
    
    # Show feature importance
    print("\nFeature Importance:")
    print("-"*40)
    importance = predictor.get_feature_importance()
    print(importance.to_string(index=False))
    
    # Cross-validation on available data
    data = load_cached_data()
    if data is not None:
        featured = create_features(data)
        X, y, _ = prepare_training_data(featured)
        
        if len(X) > 0:
            print("\nCross-Validation Results:")
            print("-"*40)
            cv_results = predictor.cross_validate(X, y)


def cmd_schedule(args):
    """Show upcoming races."""
    from predictor import get_upcoming_races
    
    print("\n" + "="*60)
    print("UPCOMING F1 RACES")
    print("="*60)
    
    upcoming = get_upcoming_races(args.limit if args.limit else 10)
    
    if upcoming.empty:
        print("No upcoming races found")
        return
    
    print(f"\n{'Round':<8}{'Race':<30}{'Country':<20}{'Date':<15}")
    print("-"*75)
    
    for _, race in upcoming.iterrows():
        date_str = race['EventDate'].strftime('%Y-%m-%d')
        print(f"{race['RoundNumber']:<8}{race['EventName'][:29]:<30}{race['Country'][:19]:<20}{date_str:<15}")


def cmd_collect(args):
    """Collect/update historical data."""
    from data_collector import collect_historical_data
    
    print("\n" + "="*60)
    print("COLLECTING HISTORICAL DATA")
    print("="*60)
    
    seasons = args.seasons if args.seasons else config.SEASONS
    data = collect_historical_data(seasons)
    
    print(f"\nCollected {len(data)} race entries")


def main():
    parser = argparse.ArgumentParser(
        description="F1 Race Winner Prediction System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Train command
    train_parser = subparsers.add_parser('train', help='Train prediction model')
    train_parser.add_argument('--seasons', type=int, nargs='+', 
                             help='Seasons to use for training')
    train_parser.add_argument('--model', choices=['random_forest', 'xgboost'],
                             help='Model type to train')
    train_parser.add_argument('--refresh', action='store_true',
                             help='Refresh data even if cached')
    
    # Predict command
    predict_parser = subparsers.add_parser('predict', help='Predict race winner')
    predict_parser.add_argument('event', nargs='?', help='Event name (e.g., Monaco)')
    predict_parser.add_argument('--year', type=int, help='Season year')
    predict_parser.add_argument('--model', choices=['random_forest', 'xgboost'],
                               help='Model to use for prediction')
    
    # Evaluate command
    eval_parser = subparsers.add_parser('evaluate', help='Evaluate model performance')
    eval_parser.add_argument('--model', choices=['random_forest', 'xgboost'],
                            help='Model to evaluate')
    
    # Schedule command
    schedule_parser = subparsers.add_parser('schedule', help='Show upcoming races')
    schedule_parser.add_argument('--limit', type=int, default=10,
                                help='Number of races to show')
    
    # Collect command
    collect_parser = subparsers.add_parser('collect', help='Collect historical data')
    collect_parser.add_argument('--seasons', type=int, nargs='+',
                               help='Seasons to collect')
    
    args = parser.parse_args()
    
    if args.command == 'train':
        cmd_train(args)
    elif args.command == 'predict':
        cmd_predict(args)
    elif args.command == 'evaluate':
        cmd_evaluate(args)
    elif args.command == 'schedule':
        cmd_schedule(args)
    elif args.command == 'collect':
        cmd_collect(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
