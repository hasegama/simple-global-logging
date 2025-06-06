"""
conftest.py Template for simple_global_logging

Copy this file to your project root as 'conftest.py' to enable
automatic logging setup for pytest runs.

This template provides various configuration options for different use cases.
"""

import pytest
import simple_global_logging


# ==============================================================================
# Basic Configuration (Recommended)
# ==============================================================================

def pytest_configure(config):
    """Called after command line options have been parsed.
    
    This is the main setup function that initializes logging for pytest.
    """
    print("pytest_configure called - setting up global stdout capture with simple_global_logging")
    
    # Basic setup with stdout capture
    simple_global_logging.setup_logging_with_stdout_capture(
        verbose=True,           # Enable debug level logging
        base_dir="out",         # Directory for log files
        remove_ansi=True        # Remove color codes from log files (recommended)
    )
    
    print("Global stdout capture has been configured with simple_global_logging")


def pytest_sessionstart(session):
    """Called after the Session object has been created.
    
    This is called once per pytest session.
    """
    print("pytest_sessionstart called")


def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished.
    
    Args:
        session: pytest session object
        exitstatus: Exit status code (0 = success, non-zero = failure)
    """
    print(f"pytest_sessionfinish called with exit status: {exitstatus}")
    
    # Optional: Restore stdout after tests complete
    # Uncomment the line below if you want to restore stdout after pytest
    # simple_global_logging.restore_stdout()


# ==============================================================================
# Alternative Configurations
# ==============================================================================

# OPTION 1: Minimal setup (just basic logging, no stdout capture)
"""
def pytest_configure(config):
    simple_global_logging.setup_logging(verbose=True, base_dir="test_logs")
"""

# OPTION 2: Custom log directory with date-based subdirectories
"""
from datetime import datetime

def pytest_configure(config):
    # Create subdirectory based on current date
    today = datetime.now().strftime("%Y%m%d")
    log_dir = f"test_logs/{today}"
    
    simple_global_logging.setup_logging_with_stdout_capture(
        verbose=True,
        base_dir=log_dir,
        remove_ansi=True
    )
"""

# OPTION 3: Conditional setup based on pytest command line options
"""
def pytest_configure(config):
    # Check if --verbose flag was passed to pytest
    verbose_mode = config.getoption("verbose") > 0
    
    # Only setup stdout capture if running in verbose mode
    if verbose_mode:
        simple_global_logging.setup_logging_with_stdout_capture(
            verbose=True,
            base_dir="verbose_logs"
        )
    else:
        simple_global_logging.setup_logging(
            verbose=False,
            base_dir="quiet_logs"
        )
"""

# OPTION 4: Environment-based configuration
"""
import os

def pytest_configure(config):
    # Use environment variables for configuration
    log_level = os.getenv("TEST_LOG_LEVEL", "INFO").upper()
    log_dir = os.getenv("TEST_LOG_DIR", "out")
    capture_stdout = os.getenv("TEST_CAPTURE_STDOUT", "true").lower() == "true"
    
    verbose = log_level == "DEBUG"
    
    if capture_stdout:
        simple_global_logging.setup_logging_with_stdout_capture(
            verbose=verbose,
            base_dir=log_dir
        )
    else:
        simple_global_logging.setup_logging(
            verbose=verbose,
            base_dir=log_dir
        )
"""

# OPTION 5: Custom log file naming with test session info
"""
def pytest_configure(config):
    # Get information about the test session
    test_file_count = len(config.getoption("file_or_dir") or [])
    
    simple_global_logging.setup_logging_with_stdout_capture(
        verbose=True,
        base_dir=f"test_logs/session_{test_file_count}_files"
    )
"""


# ==============================================================================
# Advanced Hooks (Optional)
# ==============================================================================

def pytest_runtest_setup(item):
    """Called before each test function is executed.
    
    You can use this to log test-specific information.
    """
    import logging
    logging.info(f"Starting test: {item.name}")


def pytest_runtest_teardown(item, nextitem):
    """Called after each test function is executed.
    
    You can use this to log test completion or cleanup information.
    """
    import logging
    logging.info(f"Completed test: {item.name}")


def pytest_runtest_logreport(report):
    """Called after each test phase (setup, call, teardown).
    
    This can be used to log detailed test results.
    """
    import logging
    
    if report.when == "call":  # Only log the actual test execution
        if report.passed:
            logging.info(f"✅ PASSED: {report.nodeid}")
        elif report.failed:
            logging.error(f"❌ FAILED: {report.nodeid}")
            if hasattr(report, 'longrepr') and report.longrepr:
                # Log the failure details
                logging.error(f"Failure details: {report.longrepr}")
        elif report.skipped:
            logging.warning(f"⏭️ SKIPPED: {report.nodeid}")


# ==============================================================================
# Usage Instructions
# ==============================================================================

"""
To use this template:

1. Copy this file to your project root as 'conftest.py'
2. Choose one of the configuration options above
3. Uncomment the desired configuration
4. Comment out or remove the basic configuration
5. Customize as needed for your project

Environment Variables (for OPTION 4):
- TEST_LOG_LEVEL: DEBUG, INFO, WARNING, ERROR (default: INFO)
- TEST_LOG_DIR: Directory for log files (default: out)
- TEST_CAPTURE_STDOUT: true/false for stdout capture (default: true)

Example usage:
```bash
# Run tests with debug logging
TEST_LOG_LEVEL=DEBUG pytest tests/

# Run tests without stdout capture
TEST_CAPTURE_STDOUT=false pytest tests/

# Run tests with custom log directory
TEST_LOG_DIR=my_test_logs pytest tests/
```
""" 