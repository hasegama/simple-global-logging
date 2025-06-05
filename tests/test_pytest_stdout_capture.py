"""Test file to verify pytest stdout capture functionality."""

import pytest
import logging


def test_print_statements():
    """Test function with print statements."""
    print("This is a print statement from test_print_statements")
    logging.info("This is a logging info message from test_print_statements")
    assert True


def test_with_assertions():
    """Test function with assertions and output."""
    print("Testing assertions...")
    value = 42
    print(f"Value is: {value}")
    logging.debug(f"Debug: checking value {value}")
    assert value == 42
    print("Assertion passed!")


def test_multiple_outputs():
    """Test function with multiple types of output."""
    print("=== Multiple outputs test ===")
    
    for i in range(3):
        print(f"Loop iteration {i+1}")
        logging.warning(f"Warning from iteration {i+1}")
    
    print("=== Test completed ===")
    assert True


@pytest.mark.parametrize("input_val,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_parametrized(input_val, expected):
    """Parametrized test with output."""
    print(f"Testing input: {input_val}, expected: {expected}")
    result = input_val * 2
    logging.info(f"Result calculation: {input_val} * 2 = {result}")
    print(f"Calculated result: {result}")
    assert result == expected 