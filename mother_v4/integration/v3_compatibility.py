"""
MOTHER V3 Compatibility Layer

Provides backward compatibility with V3 while gradually migrating to V4.

Strategy: Adapter Pattern (Gang of Four, 1994)
Purpose: Allow V3 and V4 to coexist during migration
"""

import sys
import logging
from pathlib import Path
from typing import Optional

# Add mother_v4 to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import MOTHER as MOTHER_V4

logger = logging.getLogger(__name__)


class MOTHER_V3_Adapter:
    """
    Adapter that makes MOTHER V4 compatible with V3 interface.
    
    This allows existing V3 code to work with V4 without changes.
    """
    
    def __init__(self):
        """Initialize V3 adapter"""
        self.v4 = MOTHER_V4(environment="production")
        self.v4_initialized = False
        logger.info("MOTHER V3 Compatibility Adapter created")
    
    def bootstrap(self) -> bool:
        """
        V3-style bootstrap function.
        
        Maps to V4's initialize() method.
        """
        try:
            if not self.v4_initialized:
                self.v4.initialize()
                self.v4_initialized = True
            return True
        except Exception as e:
            logger.error(f"Bootstrap failed: {e}")
            return False
    
    def load_principles(self) -> bool:
        """
        V3-style load_principles function.
        
        In V4, principles are loaded automatically during initialize().
        """
        if not self.v4_initialized:
            return self.bootstrap()
        
        # Principles already loaded in V4
        logger.debug("Principles already loaded in V4")
        return True
    
    def check_enforcement(self, principle: str) -> bool:
        """
        V3-style enforcement check.
        
        Args:
            principle: Principle name (e.g., "P1", "P2")
        
        Returns:
            True if enforcement is active
        """
        if not self.v4_initialized:
            self.bootstrap()
        
        # Check if strategy exists in V4
        for strategy in self.v4.enforcement.strategies:
            if principle in strategy.principle_name:
                return True
        
        return False
    
    def get_status(self) -> dict:
        """
        V3-style status function.
        
        Returns:
            Status dictionary compatible with V3
        """
        if not self.v4_initialized:
            return {
                "initialized": False,
                "version": "4.0 (V3 compatibility mode)",
                "error": "Not initialized"
            }
        
        return {
            "initialized": self.v4.initialized,
            "version": "4.0 (V3 compatibility mode)",
            "environment": self.v4.environment,
            "bootstrap": self.v4.bootstrap is not None,
            "enforcement": self.v4.enforcement is not None,
            "monitoring": self.v4.monitor is not None,
            "knowledge": self.v4.knowledge is not None and self.v4.knowledge.loaded
        }


def create_v3_compatible_bootstrap():
    """
    Create V3-compatible bootstrap script.
    
    This function can be called from V3's bootstrap.sh
    """
    adapter = MOTHER_V3_Adapter()
    success = adapter.bootstrap()
    
    if success:
        print("✓ MOTHER V4 (V3 compatibility mode) initialized successfully")
        status = adapter.get_status()
        for key, value in status.items():
            print(f"  {key}: {value}")
    else:
        print("✗ MOTHER V4 initialization failed")
        return 1
    
    return 0


if __name__ == "__main__":
    # Test compatibility layer
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("Testing MOTHER V3 Compatibility Layer")
    print("=" * 60)
    
    adapter = MOTHER_V3_Adapter()
    
    # Test bootstrap
    print("\n1. Testing bootstrap...")
    success = adapter.bootstrap()
    print(f"   Result: {'✓ Success' if success else '✗ Failed'}")
    
    # Test load_principles
    print("\n2. Testing load_principles...")
    success = adapter.load_principles()
    print(f"   Result: {'✓ Success' if success else '✗ Failed'}")
    
    # Test check_enforcement
    print("\n3. Testing check_enforcement...")
    for principle in ["P1", "P2", "P3", "P4", "P7"]:
        active = adapter.check_enforcement(principle)
        print(f"   {principle}: {'✓ Active' if active else '✗ Inactive'}")
    
    # Test get_status
    print("\n4. Testing get_status...")
    status = adapter.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 60)
    print("V3 Compatibility Layer Test Complete")
    print("=" * 60)
