import logging
import os

# Define the log directory and log file name
LOG_DIR = "logs"
LOG_FILE = "app.log"

# Ensure the log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Set up the logger
def setup_logger():
    """
    Set up and return the logger for the application.
    Logs are saved to a file (app.log) and also shown in the console.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Log all levels from DEBUG and above

    # Create file handler for logging to a file
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, LOG_FILE))
    file_handler.setLevel(logging.DEBUG)  # Log all levels from DEBUG and above
    
    # Create console handler for logging to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Log INFO level and above to console

    # Define log format for both handlers
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # Set the formatter for both handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Initialize the logger
logger = setup_logger()