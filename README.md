# Simple Global Logging

A simple Python logging extension library that enhances the standard logging functionality with global configuration and stdout capture capabilities.

## Features

- **Global Logging Setup**: Initialize once, use everywhere with standard `import logging`
- **Automatic File Output**: Logs saved to timestamped files in `out/` directory
- **Standard Output Capture**: Capture console output to log files
- **pytest Integration**: Capture pytest output via conftest.py
- **Configurable Timezone**: All timestamps in specified timezone (default: UTC)

> [!IMPORTANT]
> This library clears all existing handlers from the root logger and its children during initialization.
> If your application uses other logging handlers, make sure to:
> - Initialize this library **before** setting up other handlers
> - Or manually re-add your handlers after initialization

## Installation

```bash
pip install simple-global-logging
```

## Quick Start

```python
import simple_global_logging
import logging

# Basic setup
simple_global_logging.setup_logging(verbose=True)
logging.info("This will be logged to file and console")

# With stdout capture
simple_global_logging.setup_logging_with_stdout_capture()
print("This will also be logged")
```

## API Reference

### Core Functions

```python
# Basic logging setup
setup_logging(
    verbose=False,  # Enable DEBUG level if True
    base_dir="out", # Log directory
    tz=None        # Timezone (default: UTC)
)

# With stdout capture
setup_logging_with_stdout_capture(
    verbose=False,
    base_dir="out",
    remove_ansi=True,  # Remove terminal color codes
    tz=None
)

# Utility functions
get_logger(name)           # Get logger instance
restore_stdout()           # Restore original stdout
get_current_log_file()     # Get current log file path
get_current_timezone()     # Get current timezone
```

### Log File Format

- Location: `out/` directory (customizable)
- Filename: `YYYYMMDD-0000001.log` (7-digit sequential number)
- Content: Timestamps in specified timezone

## Examples

The library includes example scripts in the `examples/` directory:

- `basic_usage.py`: Basic logging setup
- `stdout_capture_example.py`: Output capture
- `submodule.py`: Logging from different modules
- `timezone_example.py`: Timezone configuration

For pytest integration, see `conftest_template.py` in the `tests/` directory.

## Requirements

- Python 3.10 or higher

## Development

This library was developed using [Cursor](https://cursor.sh), a modern AI-powered IDE.

## License

Apache License 2.0 