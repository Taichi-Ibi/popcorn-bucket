#!/usr/bin/env python3
"""Simple test script to verify CLI functionality."""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

try:
    from cli.main import create_parser
    print("✅ Import successful")
    
    parser = create_parser()
    print("✅ Parser created successfully")
    
    # Test help
    parser.parse_args(['--help'])
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
