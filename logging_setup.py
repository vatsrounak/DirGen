import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    """
    Sets up logging configuration with a rotating file handler.
    """

    # Create the root logger & set the base logging level
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set to DEBUG for detailed output
    
    # formatter for all log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    
    
    # Setup console handler to display INFO level and above messages    # Create a rotating file handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Setup a rotating file handler to log DEBUG level and above messages
    file_handler = RotatingFileHandler('app.log', maxBytes=10*1024*1024, backupCount=5)# this means the log file will be rotated when it reaches 10 MB, keeping 5 backups
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Log a startup message
    # add a message if you want.
    