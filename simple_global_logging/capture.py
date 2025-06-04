"""
Standard output capture functionality for simple_global_logging.
"""

from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import TextIO, Optional
import threading
import re


class LogCapture:
    """Captures stdout/stderr and redirects to both original stream and log file."""
    
    def __init__(self, original_stream: TextIO, log_file_path: Path, remove_ansi: bool = True, tz: Optional[timezone] = None):
        """Initialize LogCapture.
        
        Args:
            original_stream: Original stdout/stderr stream
            log_file_path: Path to log file for writing captured output
            remove_ansi: Whether to remove ANSI escape sequences from log file (default: True)
            tz: Timezone for timestamps (default: UTC)
        """
        self.original_stream = original_stream
        self.log_file_path = log_file_path
        self.remove_ansi = remove_ansi
        self.lock = threading.Lock()
        
        # Default to UTC if no timezone specified
        if tz is None:
            tz = timezone.utc
        self.timezone = tz
        
        # Regex pattern to remove ANSI escape sequences (color codes)
        if self.remove_ansi:
            self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    
    def _remove_ansi_codes(self, text: str) -> str:
        """Remove ANSI escape sequences from text.
        
        Args:
            text: Text that may contain ANSI escape sequences
            
        Returns:
            Text with ANSI escape sequences removed
        """
        if self.remove_ansi and hasattr(self, 'ansi_escape'):
            return self.ansi_escape.sub('', text)
        return text
    
    def write(self, text: str) -> int:
        """Write text to both original stream and log file.
        
        Args:
            text: Text to write
            
        Returns:
            Number of characters written to original stream
        """
        # Write to original stream (with color codes)
        result = self.original_stream.write(text)
        self.original_stream.flush()
        
        # Write to log file if text is not just whitespace
        if text.strip():
            # Remove ANSI escape sequences for log file if enabled
            clean_text = self._remove_ansi_codes(text)
            
            with self.lock:
                try:
                    with open(self.log_file_path, 'a', encoding='utf-8') as f:
                        # Add timestamp for stdout/stderr captures using specified timezone
                        timestamp = datetime.now(self.timezone).strftime("%Y-%m-%d %H:%M:%S")
                        f.write(f"[{timestamp}] STDOUT: {clean_text}")
                        if not clean_text.endswith('\n'):
                            f.write('\n')
                except Exception:
                    # If we can't write to log file, don't crash the application
                    pass
        
        return result
    
    def flush(self):
        """Flush the original stream."""
        self.original_stream.flush()
    
    def fileno(self):
        """Get file descriptor of original stream."""
        return self.original_stream.fileno()
    
    def isatty(self) -> bool:
        """Check if the original stream is a TTY."""
        try:
            return self.original_stream.isatty()
        except AttributeError:
            return False
    
    def readable(self) -> bool:
        """Check if the original stream is readable."""
        try:
            return self.original_stream.readable()
        except AttributeError:
            return False
    
    def writable(self) -> bool:
        """Check if the original stream is writable."""
        try:
            return self.original_stream.writable()
        except AttributeError:
            return True
    
    def seekable(self) -> bool:
        """Check if the original stream is seekable."""
        try:
            return self.original_stream.seekable()
        except AttributeError:
            return False
    
    def close(self):
        """Close the original stream."""
        if hasattr(self.original_stream, 'close'):
            self.original_stream.close()
    
    @property
    def closed(self) -> bool:
        """Check if the original stream is closed."""
        try:
            return self.original_stream.closed
        except AttributeError:
            return False
    
    def __getattr__(self, name):
        """Delegate any other attribute access to the original stream."""
        return getattr(self.original_stream, name) 