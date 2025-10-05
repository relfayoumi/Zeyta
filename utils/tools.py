# utils/tools.py
# Placeholder for common helper functions that don't fit elsewhere.

import datetime

def get_current_time():
    """Returns the current time as a formatted string."""
    return datetime.datetime.now().strftime("%H:%M")

def get_current_date():
    """Returns the current date as a formatted string."""
    return datetime.datetime.now().strftime("%B %d, %Y")