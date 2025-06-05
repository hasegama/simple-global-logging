#!/usr/bin/env python3
"""
Basic usage example for simple_global_logging library.

This example demonstrates how to initialize and use the global logging functionality.
"""

import simple_global_logging
import logging


def main():
    """Main function demonstrating basic usage."""
    
    # Initialize global logging - do this once in your main file
    print("Setting up global logging...")
    logger = simple_global_logging.setup_logging(verbose=True)
    
    # Now you can use standard logging anywhere in your codebase
    logging.info("Application started")
    logging.debug("This is a debug message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")
    print("Another print statement")
    
    # Demonstrate logging from different modules
    from examples.submodule import do_something
    do_something()
    
    # Show current log file
    log_file = simple_global_logging.get_current_log_file()
    logging.info(f"Log file: {log_file}")
    
    logging.info("Application finished")


if __name__ == "__main__":
    main() 