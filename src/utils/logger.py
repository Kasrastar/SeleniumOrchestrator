# utils/logger.py

import logging
import re

class SensitiveDataFilter(logging.Filter):
    """
    Custom filter to exclude log messages containing sensitive information.
    """
    def __init__(self, keywords=None):
        super().__init__()
        self.keywords = keywords or []

    def filter(self, record):
        # Check if any of the keywords appear in the log message
        if any(keyword.lower() in record.getMessage().lower() for keyword in self.keywords):
            return False  # Exclude the record
        return True

class MaskingFilter(logging.Filter):
    """
    Custom filter to mask sensitive data in log messages.
    """
    def __init__(self, patterns=None):
        super().__init__()
        self.patterns = patterns or []

    def filter(self, record):
        # Mask sensitive data based on provided patterns
        message = record.getMessage()
        for pattern, replacement in self.patterns:
            message = re.sub(pattern, replacement, message)
        record.msg = message
        return True

def setup_logger(name: str, log_file: str = "selenium_orchestrator.log", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    try:
        # Create file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Set formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add filters
        sensitive_filter = SensitiveDataFilter(keywords=["password", "token", "credentials"])
        masking_filter = MaskingFilter(patterns=[
            (r"(password=)(\w+)", r"\1***"),  # Mask passwords
            (r"(token=)(\w+)", r"\1***"),  # Mask tokens
        ])
        file_handler.addFilter(sensitive_filter)
        console_handler.addFilter(masking_filter)

        # Add handlers if not already added
        if not logger.hasHandlers():
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

    except Exception as e:
        raise RuntimeError(f"Failed to set up logging: {e}")

    return logger

# Initialize the logger
logger = setup_logger("SeleniumOrchestrator")

# Example log messages
# logger.info("This is a safe message.")
# logger.info("User logged in with token=abcdef12345.")
# logger.info("Attempting with password=secret123.")
