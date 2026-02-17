#!/usr/bin/env python3
"""
Manus Credit Optimization - Auto-Initialization
Automatically initializes optimizer at conversation start

This script is called by bootstrap to ensure optimizer is ready
"""

import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent / "core"))

try:
    from manus_credit_optimizer import get_optimizer
    
    # Initialize optimizer
    optimizer = get_optimizer()
    
    # Silent success (don't clutter output)
    # Optimizer is now ready for use
    
except Exception as e:
    # Silent failure (don't break bootstrap)
    pass
