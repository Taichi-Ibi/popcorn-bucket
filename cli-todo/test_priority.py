#!/usr/bin/env python3
"""Test priority validation behavior."""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from validators.task_validator import validate_priority_value

def test_priority_cases():
    test_cases = ["high", "HIGH", "medium", "MEDIUM", "low", "LOW", "invalid"]
    
    for priority in test_cases:
        result, error = validate_priority_value(priority)
        print(f"Priority '{priority}': valid={result}, error={error}")

if __name__ == "__main__":
    test_priority_cases()
