"""
Model Training and Prediction Pipeline Module

This module contains functions for training the Prophet time-series model,
making future predictions, and evaluating the model's performance using MAPE.
"""
import pandas as pd
import numpy as np
from prophet import Prophet
import pickle
from pathlib import Path
from typing import Tuple

def calculate_mape(y_true: pd.Series, y_pred: pd.Series) -> float:
    """
    Calculate Mean Absolute Percentage Error (MAPE).
    
    Args:
        y_true (pd.Series): Actual values
        y_pred (pd.Series): Predicted values
    
    Returns:
        float: MAPE as a percentage
    """
    # Avoid division by zero
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

def train_prophet_model(df: pd.DataFrame, target_col: str, date_col: str) -> Tuple[Prophet, dict]:
    """
    Trains a Prophet forecasting model with optimized hyperparameters from the notebook.

    Args:
        df (pd.DataFrame): The training data.
        target_col (str): The name of the target variable column.
        date_col (str): The name of the date column.

    Returns:
        Tuple[Prophet, dict]: The trained Prophet model and evaluation metrics.
    """
    # Prophet requires columns to be named 'ds' (datestamp) and 'y' (target)
    model_df = df.rename(columns={date_col: 'ds', target_col: 'y'}).copy()
    
    print("Training Prophet model with optimized hyperparameters...")
    
    # Use hyperparameters from the original notebook
    model = Prophet(
        growth='linear',
        changepoint_range=0.40,
        changepoint_prior_scale=0.10,
        seasonality_mode='multiplicative',  # Better for dengue seasonality
        seasonality_prior_scale=10.0,
        yearly_seasonality=True,
        weekly_seasonality=False,  # Data is weekly, so this would be redundant
        daily_seasonality=False,
        interval_width=0.95
    )
    
    # Fit the model
    model.fit(model_df)
    
    print("Model training complete. Evaluating performance...")
    
    # Generate in-sample predictions for evaluation
    in_sample_forecast = model.predict(model_df)
    
    # Calculate MAPE
    mape = calculate_mape(model_df['y'], in_sample_forecast['yhat'])
    
    # Calculate other metrics
    mae = np.mean(np.abs(model_df['y'] - in_sample_forecast['yhat']))
    rmse = np.sqrt(np.mean((model_df['y'] - in_sample_forecast['yhat']) ** 2))
    
    evaluation_metrics = {
        'mape': mape,
        'mae': mae,
        'rmse': rmse,
        'training_samples': len(model_df)
    }
    
    print(f"Model Performance Metrics:")
    print(f"  MAPE: {mape:.2f}%")
    print(f"  MAE: {mae:.2f}")
    print(f"  RMSE: {rmse:.2f}")
    
    return model, evaluation_metrics

def make_predictions(model: Prophet, future_periods: int) -> pd.DataFrame:
    """
    Uses a trained Prophet model to make future predictions.

    Args:
        model (Prophet): The trained Prophet model.
        future_periods (int): The number of periods (weeks) to forecast.

    Returns:
        pd.DataFrame: A DataFrame containing the forecast results.
    """
    print(f"Making predictions for the next {future_periods} weeks...")
    
    # Create future dataframe
    future_df = model.make_future_dataframe(periods=future_periods, freq='W')
    
    # Generate predictions
    forecast_df = model.predict(future_df)
    
    # Ensure non-negative predictions (dengue cases can't be negative)
    forecast_df['yhat'] = np.maximum(forecast_df['yhat'], 0)
    forecast_df['yhat_lower'] = np.maximum(forecast_df['yhat_lower'], 0)
    forecast_df['yhat_upper'] = np.maximum(forecast_df['yhat_upper'], 0)
    
    print("Prediction complete.")
    return forecast_df

def evaluate_model_on_holdout(df: pd.DataFrame, target_col: str, date_col: str, 
                             holdout_weeks: int = 16) -> dict:
    """
    Evaluate model performance on a holdout set (last N weeks).
    
    Args:
        df (pd.DataFrame): The full dataset
        target_col (str): Target column name
        date_col (str): Date column name
        holdout_weeks (int): Number of weeks to hold out for testing
    
    Returns:
        dict: Evaluation metrics on holdout set
    """
    print(f"Evaluating model on {holdout_weeks}-week holdout set...")
    
    # Split data
    train_df = df.iloc[:-holdout_weeks].copy()
    test_df = df.iloc[-holdout_weeks:].copy()
    
    # Train model on training set
    model, _ = train_prophet_model(train_df, target_col, date_col)
    
    # Make predictions for test period
    future_df = model.make_future_dataframe(periods=holdout_weeks, freq='W')
    forecast = model.predict(future_df)
    
    # Get predictions for test period
    test_predictions = forecast.iloc[-holdout_weeks:]
    
    # Calculate metrics
    actual = test_df[target_col].values
    predicted = test_predictions['yhat'].values
    
    mape = calculate_mape(pd.Series(actual), pd.Series(predicted))
    mae = np.mean(np.abs(actual - predicted))
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))
    
    holdout_metrics = {
        'holdout_mape': mape,
        'holdout_mae': mae,
        'holdout_rmse': rmse,
        'holdout_weeks': holdout_weeks
    }
    
    print(f"Holdout Performance Metrics:")
    print(f"  MAPE: {mape:.2f}%")
    print(f"  MAE: {mae:.2f}")
    print(f"  RMSE: {rmse:.2f}")
    
    return holdout_metrics

def save_model(model: Prophet, filepath: Path, metrics: dict = None):
    """Saves the trained model and metrics to files."""
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {filepath}")
    
    # Save metrics if provided
    if metrics:
        metrics_path = filepath.parent / f"{filepath.stem}_metrics.json"
        import json
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=4)
        print(f"Metrics saved to {metrics_path}")

def load_model(filepath: Path) -> Prophet:
    """Loads a trained model from a file."""
    with open(filepath, 'rb') as f:
        model = pickle.load(f)
    print(f"Model loaded from {filepath}")
    return model