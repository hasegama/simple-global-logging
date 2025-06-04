"""Tests for simple_global_logging library."""

import pytest
import logging
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta
import re
import glob

import simple_global_logging
from simple_global_logging import core


class TestSimpleGlobalLogging:
    """Test suite for simple_global_logging library."""
    
    def setup_method(self):
        """Setup test environment."""
        # Create temporary directory for test logs
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Reset logging state
        logging.getLogger().handlers.clear()
        core._logging_initialized = False
        core._stdout_captured = False
        core._log_file_path = None
        
        # Restore stdout if captured
        if hasattr(core, '_original_stdout') and core._original_stdout:
            sys.stdout = core._original_stdout
            sys.stderr = core._original_stderr
    
    def teardown_method(self):
        """Cleanup test environment."""
        # Restore stdout
        simple_global_logging.restore_stdout()
        
        # Clear logging handlers
        logging.getLogger().handlers.clear()
        
        # Remove temporary directory
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_setup_logging_basic(self):
        """Test basic logging setup."""
        logger = simple_global_logging.setup_logging(base_dir=str(self.temp_dir))
        
        assert isinstance(logger, logging.Logger)
        assert logger == logging.getLogger()
        assert len(logger.handlers) == 2  # Console + File handler
        
        # Check log file was created
        log_files = list(self.temp_dir.glob("*.log"))
        assert len(log_files) == 1
        
        # Check filename format
        log_file = log_files[0]
        utc = timezone.utc
        today = datetime.now(utc).strftime("%Y%m%d")
        assert re.match(rf"{today}-\d{{7}}\.log", log_file.name)
    
    def test_logging_output(self):
        """Test that logging output works correctly."""
        logger = simple_global_logging.setup_logging(base_dir=str(self.temp_dir))
        
        # Log some messages
        logging.info("Test info message")
        logging.warning("Test warning message")
        logging.error("Test error message")
        
        # Check log file content
        log_files = list(self.temp_dir.glob("*.log"))
        assert len(log_files) == 1
        
        with open(log_files[0], 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "Test info message" in content
        assert "Test warning message" in content
        assert "Test error message" in content
        assert "Logging started" in content
    
    def test_verbose_logging(self):
        """Test verbose logging mode."""
        logger = simple_global_logging.setup_logging(verbose=True, base_dir=str(self.temp_dir))
        
        # Debug messages should be logged in verbose mode
        logging.debug("Debug message")
        logging.info("Info message")
        
        log_files = list(self.temp_dir.glob("*.log"))
        with open(log_files[0], 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "Debug message" in content
        assert "Info message" in content
        assert "Verbose logging enabled" in content
    
    def test_non_verbose_logging(self):
        """Test non-verbose logging mode."""
        logger = simple_global_logging.setup_logging(verbose=False, base_dir=str(self.temp_dir))
        
        # Debug messages should not be logged in non-verbose mode
        logging.debug("Debug message")
        logging.info("Info message")
        
        log_files = list(self.temp_dir.glob("*.log"))
        with open(log_files[0], 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "Debug message" not in content
        assert "Info message" in content
    
    def test_get_logger(self):
        """Test get_logger function."""
        # Should auto-initialize if not setup
        logger = simple_global_logging.get_logger("test.module")
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test.module"
        
        # Root logger should now have handlers
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) >= 1
    
    def test_stdout_capture(self):
        """Test stdout capture functionality."""
        original_stdout = sys.stdout
        
        logger = simple_global_logging.setup_logging_with_stdout_capture(base_dir=str(self.temp_dir))
        
        # stdout should be captured now
        assert sys.stdout != original_stdout
        
        # Print something
        print("Test stdout capture")
        
        # Check that it appears in log file
        log_files = list(self.temp_dir.glob("*.log"))
        assert len(log_files) == 1
        
        with open(log_files[0], 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "STDOUT: Test stdout capture" in content
        
        # Restore stdout
        simple_global_logging.restore_stdout()
        assert sys.stdout == original_stdout
    
    def test_log_file_naming_sequence(self):
        """Test that log files are numbered sequentially."""
        # Create first log file
        logger1 = simple_global_logging.setup_logging(base_dir=str(self.temp_dir))
        log_file1 = simple_global_logging.get_current_log_file()
        
        # Reset and create second log file
        core._logging_initialized = False
        core._log_file_path = None
        logging.getLogger().handlers.clear()
        
        logger2 = simple_global_logging.setup_logging(base_dir=str(self.temp_dir))
        log_file2 = simple_global_logging.get_current_log_file()
        
        assert log_file1 != log_file2
        
        # Check numbering
        utc = timezone.utc
        today = datetime.now(utc).strftime("%Y%m%d")
        
        assert log_file1.name == f"{today}-0000001.log"
        assert log_file2.name == f"{today}-0000002.log"
    
    def test_get_current_log_file(self):
        """Test get_current_log_file function."""
        # Should return None if not initialized
        assert simple_global_logging.get_current_log_file() is None
        
        # Should return log file path after initialization
        logger = simple_global_logging.setup_logging(base_dir=str(self.temp_dir))
        log_file = simple_global_logging.get_current_log_file()
        
        assert log_file is not None
        assert isinstance(log_file, Path)
        assert log_file.exists()
    
    def test_child_logger_propagation(self):
        """Test that child loggers properly propagate to root."""
        simple_global_logging.setup_logging(base_dir=str(self.temp_dir))
        
        # Create child logger
        child_logger = logging.getLogger("test.child")
        child_logger.info("Child logger message")
        
        # Check that message appears in log file
        log_files = list(self.temp_dir.glob("*.log"))
        with open(log_files[0], 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "Child logger message" in content 