"""
Generate dengue case predictions using the trained Prophet model.

This module loads the trained Prophet model and generates forecasts
for the specified horizon, saving results to predictions.csv.
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import warnings
warnings.filterwarnings('ignore')

# Add project root to path for imports  
PROJECT_ROOT = Path(__file__).parent.parent  # Go up from scripts/ to project root
sys.path.insert(0, str(PROJECT_ROOT))

# Import project modules
import src.config as config
from src.model_pipeline import load_model, make_predictions

def generate_predictions():
    """
    Generate and save dengue case predictions.
    
    Returns:
        pd.DataFrame: The forecast dataframe with predictions
    """
    print("--- Starting Forecasting Pipeline ---")
    
    # Check if model exists
    model_path = config.OUTPUT_DIR / config.MODEL_FILE
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    print(f"Loading model from: {model_path}")
    
    # Load the trained model
    try:
        model = load_model(model_path)
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        raise
    
    # Generate predictions
    print(f"Generating {config.FORECAST_HORIZON} weeks of predictions...")
    try:
        forecast = make_predictions(model, config.FORECAST_HORIZON)
        print(f"✅ Generated forecast with {len(forecast)} data points")
    except Exception as e:
        print(f"❌ Error generating predictions: {e}")
        raise
    
    # Save predictions
    predictions_path = config.OUTPUT_DIR / config.PREDICTIONS_FILE
    try:
        forecast.to_csv(predictions_path, index=False)
        print(f"✅ Predictions saved to: {predictions_path}")
    except Exception as e:
        print(f"❌ Error saving predictions: {e}")
        raise
    
    # Display summary
    print("\n📊 Forecast Summary:")
    print(f"Forecast period: {forecast['ds'].min()} to {forecast['ds'].max()}")
    print(f"Average predicted cases: {forecast['yhat'].mean():.1f}")
    print(f"Max predicted cases: {forecast['yhat'].max():.1f}")
    print(f"Min predicted cases: {forecast['yhat'].min():.1f}")
    
    print("--- Forecasting Pipeline Complete ---")
    return forecast

def main():
    """Main entry point for forecasting script."""
    try:
        forecast = generate_predictions()
        return forecast
    except Exception as e:
        print(f"❌ Forecasting pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()