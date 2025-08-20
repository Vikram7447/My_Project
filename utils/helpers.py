from datetime import datetime
import html

def get_current_timestamp(fmt="%Y-%m-%d %H:%M:%S"):
    """
    Returns the current timestamp as a formatted string.
    Default format: YYYY-MM-DD HH:MM:SS
    """
    return datetime.now().strftime(fmt)

def sanitize_input(user_input: str) -> str:
    """
    Basic input sanitizer.
    - Strips leading/trailing whitespace
    - Escapes HTML to prevent XSS attacks
    """
    if not isinstance(user_input, str):
        return ""
    return html.escape(user_input.strip())
