#!/usr/bin/env python3
"""
Example demonstrating stdout capture functionality.

This shows how to capture print statements and other stdout output to log files.
"""

import simple_global_logging
import logging


def main():
    """Main function demonstrating stdout capture."""
    
    # Initialize logging with stdout capture
    print("Setting up logging with stdout capture...")
    logger = simple_global_logging.setup_logging_with_stdout_capture(verbose=True)
    
    # Regular logging
    logging.info("This is logged via logging module")
    
    # Print statements will also be captured to log file
    print("This print statement will be captured to log file")
    print("Multiple print statements are supported")
    
    # Mixed usage
    logging.warning("Warning message via logging")
    print("Another print statement")
    
    # Show current log file
    log_file = simple_global_logging.get_current_log_file()
    logging.info(f"All output is being saved to: {log_file}")
    
    # Demonstrate with some computation
    for i in range(3):
        print(f"Processing item {i+1}")
        logging.debug(f"Debug: Processing item {i+1}")
    
    print("All done! Check the log file to see captured output.")
    
    # Optionally restore stdout (useful for testing)
    # simple_global_logging.restore_stdout()


if __name__ == "__main__":
    main() 