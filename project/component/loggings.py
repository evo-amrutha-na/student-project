import logging

# Logging Levels
# https://docs.python.org/3/library/logging.html#logging-levels
# CRITICAL	50
# ERROR	40
# WARNING	30
# INFO	20
# DEBUG	10
# NOTSET	0


def set_up_logging():
    try:
        # Use the root logger instead of __name__ for better Lambda compatibility
        logger = logging.getLogger()
        # Clear any existing handlers to avoid duplicate logs
        if logger.handlers:
            for handler in logger.handlers:
                logger.removeHandler(handler)
                
        format = '[%(asctime)s] [%(levelname)s] [%(message)s] [--> %(pathname)s [%(process)d]:]'
        # Set level to DEBUG to see all logs
        logging.basicConfig(format=format, level=logging.DEBUG)
        
        # Explicitly set the level on the logger as well
        logger.setLevel(logging.DEBUG)

        return logger
    except Exception as e:
        print(f"Error setting up logging: {str(e)}")
        return logging.getLogger()

