"""
pytest configuration file to enable global stdout capture with simple_global_logging.
"""

import pytest
import sys
import simple_global_logging


def pytest_configure(config):
    """Called after command line options have been parsed."""
    print("pytest_configure called - setting up global stdout capture with simple_global_logging")
    
    # Initialize logging with stdout capture for pytest
    simple_global_logging.setup_logging_with_stdout_capture(
        verbose=True, 
        base_dir="out"
    )
    
    print("Global stdout capture has been configured with simple_global_logging")


def pytest_sessionstart(session):
    """Called after the Session object has been created."""
    print("pytest_sessionstart called")


def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished."""
    print(f"pytest_sessionfinish called with exit status: {exitstatus}")
    
    # Optionally restore stdout after tests (can be commented out)
    # simple_global_logging.restore_stdout()
    