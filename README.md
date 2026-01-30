# F1 Race Winner Predictor 🏎️

A machine learning model that predicts Formula 1 race winners using historical data from the FastF1 API.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastF1](https://img.shields.io/badge/FastF1-3.7.0-red.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)

## Features

- 📊 **Data Collection** - Fetches race results, qualifying, weather, and pit stop data via FastF1
- 🧮 **Feature Engineering** - Creates 15+ predictive features including driver form, track history, and team strength
- 🤖 **ML Models** - Random Forest and XGBoost classifiers with hyperparameter tuning
- 📈 **Evaluation** - Top-N accuracy metrics designed for F1 predictions

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Collect historical data (fast mode)
python fast_collector.py

# Train and evaluate
python train_quick.py
```

## Results (2023 Season)

| Metric | Score |
|--------|-------|
| Overall Accuracy | 98.2% |
| Top-3 Accuracy | 100% |
| Top-5 Accuracy | 100% |

### Feature Importance
| Feature | Importance |
|---------|------------|
| Recent Avg Position | 27.0% |
| Qualifying Position | 21.2% |
| Recent Win Rate | 17.9% |
| Recent Podium Rate | 14.6% |
| Grid Position | 12.8% |

## Project Structure

```
F1-Predictor/
├── main.py              # CLI entry point
├── config.py            # Configuration
├── data_collector.py    # Full data collection (slower)
├── fast_collector.py    # Fast collection (race + quali only)
├── feature_engineering.py
├── model.py             # ML models
├── predictor.py         # Race predictions
├── train_quick.py       # Quick training script
└── requirements.txt
```

## CLI Commands

```bash
python main.py train              # Train on historical data
python main.py predict            # Predict next race
python main.py predict Monaco     # Predict specific race
python main.py schedule           # Show upcoming races
python main.py evaluate           # Model metrics
```

## Data Sources

- **FastF1 API** - Official F1 timing data
- **Ergast API** - Historical results (via FastF1)

## How It Works

1. **Data Collection**: Fetches race results, qualifying positions, weather conditions
2. **Feature Engineering**: Calculates rolling statistics (recent form, win rate, podium rate)
3. **Model Training**: Random Forest classifier learns patterns from historical data
4. **Prediction**: Outputs win probability for each driver in upcoming races

## Limitations

- F1 is inherently unpredictable (crashes, strategy, weather)
- Model works best when a driver is dominant (like 2023)
- Recent API data may be unavailable for very new races

## Requirements

- Python 3.8+
- FastF1 >= 3.3.0
- scikit-learn >= 1.3.0
- pandas, numpy, xgboost

## License

MIT

---

*Built with [FastF1](https://github.com/theOehrly/Fast-F1)*
