"""
Main script to launch the Streamlit dashboard application.

This script provides a convenient way to start the Streamlit server
by running 'streamlit run dashboard/app.py' from the command line.
"""
import os
import sys
from pathlib import Path

def main():
    """
    Sets up the Python path and launches the Streamlit app.
    """
    # Add the project root to the Python path to ensure src modules can be found
    project_root = Path(__file__).parent.parent  # Go up one level from scripts/
    sys.path.insert(0, str(project_root))

    # The command to run the Streamlit app
    app_path = project_root / "dashboard" / "app.py"
    command = f"streamlit run {app_path}"

    print(f"Running command: {command}")
    os.system(command)

if __name__ == "__main__":
    main()