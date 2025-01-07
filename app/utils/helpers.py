# utils/helpers.py
import os
import json
import logging

# Set up logging for helper functions
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Example 1: File operations
def read_file(file_path):
    """Reads the content of a file and returns it."""
    if not os.path.exists(file_path):
        logger.error(f"File {file_path} does not exist.")
        return None
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    """Writes content to a file."""
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        logger.info(f"Successfully wrote to {file_path}.")
    except Exception as e:
        logger.error(f"Failed to write to {file_path}: {e}")

# Example 2: JSON operations
def load_json(file_path):
    """Loads and returns JSON data from a file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        logger.error(f"Error reading JSON from {file_path}: {e}")
        return None

def save_json(file_path, data):
    """Saves Python dictionary data to a JSON file."""
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        logger.info(f"Successfully saved JSON to {file_path}.")
    except Exception as e:
        logger.error(f"Failed to save JSON to {file_path}: {e}")

# Example 3: String manipulations
def to_snake_case(text):
    """Converts a string to snake_case."""
    return text.strip().lower().replace(" ", "_")

def validate_email(email):
    """Validates an email address format."""
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))

# Example 4: Date & Time utilities
from datetime import datetime

def current_timestamp():
    """Returns the current timestamp in YYYY-MM-DD HH:MM:SS format."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def parse_date(date_string):
    """Parses a date string into a datetime object."""
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        logger.error(f"Invalid date format: {date_string}. Expected YYYY-MM-DD.")
        return None

# Example 5: Miscellaneous helper function
def debounce(func, wait):
    """Debounces a function call by the specified wait time (in seconds)."""
    from time import sleep
    def wrapper(*args, **kwargs):
        sleep(wait)
        return func(*args, **kwargs)
    return wrapper