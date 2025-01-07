### Program imports
import datetime as dt
from datetime import date, datetime, timedelta
import os
import sys

### Program configuration

## Working directory configuration
"""
This section configures the working directory
    to ensure the script runs in the current file location.
"""
# Get the current working directory (where the script is located)
current_directory = os.path.dirname(os.path.abspath(__file__))
# Change the current working directory
os.chdir(current_directory)
# Now you can perform operations in the current directory
print(f"Current working directory is: {os.getcwd()}")

## Backend import to frontend
"""
This section enables us to import main.py into the main_window.py 
    even though it is not in the same folder
"""

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(
            __file__), '..'
            )
        )
    )

## A Music file configuration


## Google Sheets database configuration
