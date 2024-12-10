from urllib.parse import urlparse
import re

def validate_url(url: str) -> tuple[bool, str]:
    """
    Validates if the input is a valid URL.
    Returns (is_valid, error_message)
    """
    try:
        # Basic string checks
        if not url.strip():
            return False, "URL cannot be empty"
        
        if len(url) > 2048:
            return False, "URL is too long (max 2048 characters)"

        # Parse the URL
        parsed = urlparse(url)
        
        # Check scheme
        if parsed.scheme not in ['http', 'https']:
            return False, "URL must start with http:// or https://"
        
        # Check if has domain
        if not parsed.netloc:
            return False, "URL must contain a valid domain"
        
        # Check domain format
        domain_pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        if not re.match(domain_pattern, parsed.netloc):
            return False, "Invalid domain format"
        
        # Check for common invalid characters
        invalid_chars = '<>"{}|\\^`'
        if any(char in url for char in invalid_chars):
            return False, f"URL contains invalid characters: {invalid_chars}"
        
        # Check for at least one dot in domain
        if '.' not in parsed.netloc:
            return False, "Domain must contain at least one dot"
        
        return True, "URL is valid"
        
    except Exception as e:
        return False, f"Invalid URL format: {str(e)}"