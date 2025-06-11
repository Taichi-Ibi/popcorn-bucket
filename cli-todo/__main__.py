#!/usr/bin/env python3
"""CLI TODO Manager entry point."""

import sys
from pathlib import Path

# Add the src directory to Python path for imports
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from cli.main import main

if __name__ == "__main__":
    main()
