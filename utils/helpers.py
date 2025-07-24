# utils/helpers.py

from datetime import datetime

def get_current_timestamp():
    """Returns current timestamp as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def sanitize_input(user_input):
    """Basic input sanitizer – removes leading/trailing spaces."""
    return user_input.strip()
