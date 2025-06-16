"""Example demonstrating custom filename feature for logging."""

import logging
import simple_global_logging

def main():
    """Demonstrate append mode with custom filename."""
    print("=== Custom Filename Example ===\n")
    
    # Example 1: Using auto-generated filename (default behavior)
    print("1. Default behavior - auto-generated filename:")
    logger = simple_global_logging.setup_logging(verbose=True)
    logging.info("This creates a new timestamped log file")
    log_file = simple_global_logging.get_current_log_file()
    print(f"   Log file: {log_file}\n")
    
    # Reset for next example
    simple_global_logging.restore_stdout()
    logging.getLogger().handlers.clear()
    
    # Example 2: Using custom filename
    print("2. Custom filename - first run:")
    logger = simple_global_logging.setup_logging(
        verbose=True,
        filename="application.log"
    )
    logging.info("First run with custom filename")
    log_file = simple_global_logging.get_current_log_file()
    print(f"   Log file: {log_file}")
    
    # Reset and run again with same filename
    logging.getLogger().handlers.clear()
    
    print("\n3. Custom filename - second run (appends to same file):")
    logger = simple_global_logging.setup_logging(
        verbose=True,
        filename="application.log"
    )
    logging.info("Second run - this message is appended")
    print("   Check application.log to see both messages\n")
    
    # Example 3: Custom filename with stdout capture
    logging.getLogger().handlers.clear()
    
    print("4. Custom filename with stdout capture:")
    logger = simple_global_logging.setup_logging_with_stdout_capture(
        verbose=True,
        filename="app_with_stdout.log"
    )
    print("This print statement is captured to the log file")
    logging.info("This log message is also in the file")
    
    print("\nDone! Check the 'out' directory for the log files.")

if __name__ == "__main__":
    main()