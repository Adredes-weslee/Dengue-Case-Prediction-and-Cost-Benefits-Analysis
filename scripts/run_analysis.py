"""Executes the cost-benefit analysis pipeline.

This script uses the processed historical data to calculate the total number of
dengue cases in the analysis year (2020) and then runs the cost-benefit
analysis, saving the results to a JSON file.
"""
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import src.config as config
from src.cost_benefit_analysis import calculate_cost_benefit, save_analysis_results

def main():
    """Main function to run the cost-benefit analysis."""
    print("--- Starting Cost-Benefit Analysis Pipeline ---")

    # Load the processed data
    processed_data_path = config.PROCESSED_DATA_DIR / config.PROCESSED_DATA_FILE
    
    if not processed_data_path.exists():
        print(f"Error: Processed data file not found at {processed_data_path}")
        print("Please run 'python scripts/run_preprocessing.py' first.")
        return

    df = pd.read_csv(processed_data_path, parse_dates=[config.DATE_COLUMN])

    # Filter for 2020 data only
    df_2020 = df[(df[config.DATE_COLUMN].dt.year == 2020)].copy()
    
    if len(df_2020) == 0:
        print("Error: No 2020 data found in the dataset")
        print(f"Available years: {sorted(df[config.DATE_COLUMN].dt.year.unique())}")
        return

    # Calculate total cases in 2020
    total_cases_2020 = int(df_2020[config.TARGET_VARIABLE].sum())
    
    print(f"2020 data: {len(df_2020)} weeks")
    print(f"Average weekly cases in 2020: {df_2020[config.TARGET_VARIABLE].mean():.1f}")
    print(f"Total dengue cases in 2020 for analysis: {total_cases_2020}")

    # Get population for 2020 (use the population from 2020 data)
    population_2020 = int(df_2020['population'].iloc[0])  # Population should be consistent in 2020

    # Run the cost-benefit analysis using the correct parameter names
    results = calculate_cost_benefit(
        total_cases_2020=total_cases_2020,
        population=population_2020,
        wolbachia_cost_pp=config.WOLBACHIA_COST_PER_PERSON,
        dengvaxia_cost_pp=config.DENGVAXIA_COST_PER_PERSON,
        daly_per_case=config.DALY_PER_CASE,
        cases_averted_wolbachia_pct=config.WOLBACHIA_EFFICACY,  # Fixed parameter name
        cases_averted_dengvaxia_pct=config.DENGVAXIA_EFFICACY   # Fixed parameter name
    )

    # Save the results
    output_path = config.OUTPUT_DIR / config.COST_BENEFIT_FILE
    save_analysis_results(results, output_path)

    print("--- Cost-Benefit Analysis Pipeline Finished ---")

if __name__ == "__main__":
    main()