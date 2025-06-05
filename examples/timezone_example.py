#!/usr/bin/env python3
"""
Timezone Configuration Example for simple_global_logging

This example demonstrates how to configure different timezones
for logging timestamps.
"""

import simple_global_logging
import logging
from datetime import timezone, timedelta


def main():
    print("=== Timezone Configuration Examples ===\n")
    
    # Example 1: Default JST timezone
    print("1. Default JST (UTC+9) timezone:")
    simple_global_logging.setup_logging(verbose=True)
    logging.info("This log uses JST timezone (default)")
    current_tz = simple_global_logging.get_current_timezone()
    print(f"Current timezone: {current_tz}")
    print()
    
    # Example 2: UTC timezone
    print("2. UTC timezone:")
    utc_tz = timezone.utc
    simple_global_logging.setup_logging(verbose=True, base_dir="out_utc", tz=utc_tz)
    logging.info("This log uses UTC timezone")
    current_tz = simple_global_logging.get_current_timezone()
    print(f"Current timezone: {current_tz}")
    print()
    
    # Example 3: US Eastern Time (EST/EDT)
    print("3. US Eastern Time (EST: UTC-5):")
    est_tz = timezone(timedelta(hours=-5))
    simple_global_logging.setup_logging(verbose=True, base_dir="out_est", tz=est_tz)
    logging.info("This log uses US Eastern Time")
    current_tz = simple_global_logging.get_current_timezone()
    print(f"Current timezone: {current_tz}")
    print()
    
    # Example 4: Europe/London (GMT: UTC+0)
    print("4. Europe/London (GMT: UTC+0):")
    gmt_tz = timezone(timedelta(hours=0))
    simple_global_logging.setup_logging(verbose=True, base_dir="out_gmt", tz=gmt_tz)
    logging.info("This log uses GMT timezone")
    current_tz = simple_global_logging.get_current_timezone()
    print(f"Current timezone: {current_tz}")
    print()
    
    # Example 5: Custom timezone (UTC+5:30 - India Standard Time)
    print("5. India Standard Time (IST: UTC+5:30):")
    ist_tz = timezone(timedelta(hours=5, minutes=30))
    simple_global_logging.setup_logging(verbose=True, base_dir="out_ist", tz=ist_tz)
    logging.info("This log uses India Standard Time")
    current_tz = simple_global_logging.get_current_timezone()
    print(f"Current timezone: {current_tz}")
    print()
    
    # Example 6: With stdout capture and custom timezone
    print("6. Stdout capture with Pacific Time (PST: UTC-8):")
    pst_tz = timezone(timedelta(hours=-8))
    simple_global_logging.setup_logging_with_stdout_capture(
        verbose=True, 
        base_dir="out_pst", 
        tz=pst_tz
    )
    logging.info("This log uses Pacific Standard Time with stdout capture")
    print("This print statement will also be captured with PST timestamp")
    current_tz = simple_global_logging.get_current_timezone()
    print(f"Current timezone: {current_tz}")
    print()
    
    print("=== Check the log files in different directories ===")
    print("Each directory (out_utc, out_est, out_gmt, etc.) contains logs")
    print("with timestamps in the respective timezone.")
    

if __name__ == "__main__":
    main() 