"""
Core logging functionality for simple_global_logging.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional

from simple_global_logging.utils import generate_log_filename
from simple_global_logging.capture import LogCapture

# Global variables to track state
_logging_initialized = False
_stdout_captured = False
_original_stdout = None
_original_stderr = None
_log_file_path = None
_current_timezone = None


def setup_logging(verbose: bool = False, base_dir: str = "out", tz: Optional[timezone] = None) -> logging.Logger:
    """Setup logging configuration for both console and file output.
    
    Args:
        verbose: Enable debug level logging if True
        base_dir: Base directory for log files (default: "out")
        tz: Timezone for timestamps (default: UTC)
        
    Returns:
        Root logger instance
    """
    global _logging_initialized, _log_file_path, _current_timezone
    
    # Default to UTC if no timezone specified
    if tz is None:
        tz = timezone.utc
    
    _current_timezone = tz
    
    # Generate log file path
    log_file = generate_log_filename(base_dir, tz)
    _log_file_path = log_file
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # Remove any existing handlers from root logger
    root_logger.handlers.clear()
    
    # Create formatters
    verbose_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Set the formatter to use specified timezone
    verbose_formatter.converter = lambda *args: datetime.now(tz).timetuple()
    
    simple_formatter = logging.Formatter('%(message)s')
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_formatter if verbose else simple_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(verbose_formatter)
    root_logger.addHandler(file_handler)

    # Ensure all child loggers propagate to root
    for name in logging.root.manager.loggerDict:
        logger = logging.getLogger(name)
        if name == "urllib3":
            logger.setLevel(logging.INFO)
            continue
        logger.propagate = True
        # Remove any existing handlers from child loggers
        logger.handlers.clear()

    root_logger.info(f"Logging started. Output file: {log_file}")
    if verbose:
        root_logger.debug("Verbose logging enabled")
    
    _logging_initialized = True
    return root_logger


def setup_logging_with_stdout_capture(verbose: bool = False, base_dir: str = "out", remove_ansi: bool = True, tz: Optional[timezone] = None) -> logging.Logger:
    """Setup logging with stdout/stderr capture enabled.
    
    Args:
        verbose: Enable debug level logging if True
        base_dir: Base directory for log files (default: "out")
        remove_ansi: Whether to remove ANSI escape sequences from log file (default: True)
        tz: Timezone for timestamps (default: UTC)
        
    Returns:
        Root logger instance
    """
    global _stdout_captured, _original_stdout, _original_stderr, _log_file_path
    
    # First setup regular logging
    logger = setup_logging(verbose=verbose, base_dir=base_dir, tz=tz)
    
    # Setup stdout/stderr capture if not already done
    if not _stdout_captured and _log_file_path:
        _original_stdout = sys.stdout
        _original_stderr = sys.stderr
        
        # Create capture objects with ANSI removal option and timezone
        stdout_capture = LogCapture(_original_stdout, _log_file_path, remove_ansi=remove_ansi, tz=_current_timezone)
        stderr_capture = LogCapture(_original_stderr, _log_file_path, remove_ansi=remove_ansi, tz=_current_timezone)
        
        # Replace sys.stdout and sys.stderr
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture
        
        _stdout_captured = True
        logger.info("Standard output capture enabled")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance. If logging is not initialized, will setup with defaults.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    
    # If root logger has no handlers, setup logging with defaults
    if not logging.root.handlers and not _logging_initialized:
        setup_logging()
    
    return logger


def restore_stdout():
    """Restore original stdout/stderr streams."""
    global _stdout_captured, _original_stdout, _original_stderr
    
    if _stdout_captured:
        sys.stdout = _original_stdout
        sys.stderr = _original_stderr
        _stdout_captured = False
        
        if _logging_initialized:
            logger = logging.getLogger()
            logger.info("Standard output capture disabled")


def get_current_log_file() -> Optional[Path]:
    """Get the current log file path.
    
    Returns:
        Path to current log file or None if logging not initialized
    """
    return _log_file_path


def get_current_timezone() -> Optional[timezone]:
    """Get the current timezone being used for logging.
    
    Returns:
        Current timezone or None if logging not initialized
    """
    return _current_timezone 