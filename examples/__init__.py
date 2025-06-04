"""
Examples package for simple_global_logging.

This package contains example scripts demonstrating various features
of the simple_global_logging library.
"""

from examples.submodule import do_something

__all__ = [
    'do_something',
]

# Example usage documentation
__doc__ += """

Available examples:
- basic_usage.py: Basic logging setup and usage
- stdout_capture_example.py: Standard output capture demonstration
- submodule.py: Example of logging from different modules
- timezone_example.py: Timezone configuration examples with different timezones

Available functions:
- do_something(): Example function that demonstrates logging from submodules
""" 