# utils/logger.py
import logging
import sys

def setup_logger():
    """
    Sets up a basic logger to print messages to the console.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(module)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )