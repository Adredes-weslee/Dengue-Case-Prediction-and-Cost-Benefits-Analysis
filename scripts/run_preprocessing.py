"""Executes the data preprocessing pipeline.

This script runs the functions from the data_processing module to load all raw
data sources, process them, and save the final master time-series DataFrame
to the 'processed' data directory.
"""
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import src.config as config
from src.data_processing import create_master_dataframe

def main():
    """Main function to run the preprocessing."""
    print("--- Starting Data Preprocessing Pipeline ---")

    # Create the master dataframe from raw files
    master_df = create_master_dataframe(config.RAW_DATA_DIR, config.RAW_FILES)

    # Save the processed dataframe
    output_path = config.PROCESSED_DATA_DIR / config.PROCESSED_DATA_FILE
    master_df.to_csv(output_path, index=False)

    print(f"Processed data saved to: {output_path}")
    print("--- Data Preprocessing Pipeline Finished ---")

if __name__ == "__main__":
    main()