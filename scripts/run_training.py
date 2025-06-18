"""Executes the model training pipeline.

This script loads the processed data, trains the Prophet time-series model,
evaluates its performance, and saves the trained model object to the output 
directory for later use in analysis and the dashboard application.
"""
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import src.config as config
from src.model_pipeline import train_prophet_model, save_model, evaluate_model_on_holdout

def main():
    """Main function to run the model training with evaluation."""
    print("--- Starting Model Training Pipeline ---")

    # Load the processed data
    processed_data_path = config.PROCESSED_DATA_DIR / config.PROCESSED_DATA_FILE
    
    if not processed_data_path.exists():
        print(f"Error: Processed data file not found at {processed_data_path}")
        print("Please run 'python scripts/run_preprocessing.py' first.")
        return
    
    df = pd.read_csv(processed_data_path, parse_dates=[config.DATE_COLUMN])
    print(f"Loaded {len(df)} records from {df[config.DATE_COLUMN].min()} to {df[config.DATE_COLUMN].max()}")

    # Train the Prophet model with evaluation
    model, training_metrics = train_prophet_model(df, config.TARGET_VARIABLE, config.DATE_COLUMN)

    # Evaluate on holdout set
    holdout_metrics = evaluate_model_on_holdout(df, config.TARGET_VARIABLE, config.DATE_COLUMN)
    
    # Combine all metrics
    all_metrics = {**training_metrics, **holdout_metrics}

    # Save the trained model with metrics
    model_path = config.OUTPUT_DIR / config.MODEL_FILE
    save_model(model, model_path, all_metrics)

    print("--- Model Training Pipeline Finished ---")

if __name__ == "__main__":
    main()