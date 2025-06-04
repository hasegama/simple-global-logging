"""
Utility functions for simple_global_logging.
"""

from pathlib import Path
from datetime import datetime, timezone, timedelta
import glob
import re
from typing import Optional


def generate_log_filename(base_dir: str, tz: Optional[timezone] = None) -> Path:
    """Generate log filename in format {yyyymmdd-7digit-serial-001}.log
    
    Args:
        base_dir: Base directory for log files
        tz: Timezone for timestamp (default: UTC)
        
    Returns:
        Path object for the log file
    """
    # Default to UTC if no timezone specified
    if tz is None:
        tz = timezone.utc
    
    today = datetime.now(tz).strftime("%Y%m%d")
    
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find existing files for today
    pattern = f"{today}-*.log"
    existing_files = glob.glob(str(output_dir / pattern))
    
    # Extract serial numbers from existing files
    serial_numbers = []
    for file_path in existing_files:
        filename = Path(file_path).name
        match = re.search(rf"{today}-(\d{{7}})\.log", filename)
        if match:
            serial_numbers.append(int(match.group(1)))
    
    # Determine next serial number
    if serial_numbers:
        next_serial = max(serial_numbers) + 1
    else:
        next_serial = 1
    
    # Format as 7-digit number
    serial_str = f"{next_serial:07d}"
    filename = f"{today}-{serial_str}.log"
    
    return output_dir / filename 