"""
Simple Global Logging Library

A simple Python logging wrapper library that enables global logging configuration 
across your entire project with automatic file output and stdout capture capabilities.
"""

from simple_global_logging.core import (
    setup_logging,
    setup_logging_with_stdout_capture,
    get_logger,
    restore_stdout,
    get_current_log_file,
    get_current_timezone
)

__version__ = "0.1.0"

# Convenience exports
__all__ = [
    'setup_logging',
    'setup_logging_with_stdout_capture', 
    'get_logger',
    'restore_stdout',
    'get_current_log_file',
    'get_current_timezone',
    '__version__'
] 