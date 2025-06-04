"""
Submodule example showing that logging works from any module.

No need to import simple_global_logging here - just use standard logging.
"""

import logging


def do_something():
    """Function that logs messages using standard logging."""
    logging.info("Function in submodule called")
    logging.debug("Processing some data...")
    
    try:
        # Simulate some work
        result = 10 / 2
        logging.info(f"Calculation result: {result}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    
    logging.info("Function in submodule finished") 