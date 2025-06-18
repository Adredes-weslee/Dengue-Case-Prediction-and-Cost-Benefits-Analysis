"""
Centralized Configuration for the Dengue Project

This module contains all the configuration variables, such as file paths,
model parameters, and constants used throughout the project.
This approach makes it easy to manage and update project settings from one place.
"""
from pathlib import Path

# --- Project Root ---
# Defines the base directory of the project.
PROJECT_ROOT = Path(__file__).parent.parent

# --- Data Paths ---
# Defines paths for raw, processed, and output data.
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "output"

# Ensure directories exist
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Filenames ---
# Defines the names of key data and model files.
RAW_FILES = {
    "cases": "WeeklyInfectiousDiseaseBulletinCases.csv",
    "weather": "Singapore_weather.csv",
    "google": "google_dengue_fever.csv",
    "population": "M810001.csv",
}
PROCESSED_DATA_FILE = "dengue_master_timeseries.csv"
MODEL_FILE = "forecasting_model.pkl"
PREDICTIONS_FILE = "predictions.csv"
COST_BENEFIT_FILE = "cost_benefit_analysis.json"

# --- Modeling Parameters ---
# Parameters for the time-series forecasting model (Prophet).
FORECAST_HORIZON = 16  # Weeks to forecast into the future
TARGET_VARIABLE = 'dengue_cases'
DATE_COLUMN = 'ds'

# --- Cost-Benefit Analysis Parameters ---
# All costs are in 2020 USD.
# These values are derived from the research notebook (Section 2.12) and its sources.

# Population for 2020 analysis (outbreak year with 35,068 cases)
POPULATION_2020 = 5_686_000  # Singapore population in 2020 (used for cost-benefit baseline)

# Intervention costs per person (2020 USD)
# Wolbachia: $27M annual program cost / 5.686M people = $4.75 per person
WOLBACHIA_COST_PER_PERSON = 4.75
# Dengvaxia: 3-dose regimen at Raffles Medical (from notebook Section 2.12)
DENGVAXIA_COST_PER_PERSON = 391.00

# DALY (Disability-Adjusted Life Years) per dengue case
# Based on empirically derived disability weights from notebook research
DALY_PER_CASE = 0.045  # Realistic value based on WHO estimates

# Intervention efficacy rates (from notebook research)
WOLBACHIA_EFFICACY = 0.77  # 77% reduction in cases (Singapore pilot results)
DENGVAXIA_EFFICACY = 0.819  # 81.9% efficacy after 3 doses (clinical trials)

# Legacy names for backward compatibility
CASES_AVERTED_WOLBACHIA_PERCENT = WOLBACHIA_EFFICACY
CASES_AVERTED_DENGVAXIA_PERCENT = DENGVAXIA_EFFICACY