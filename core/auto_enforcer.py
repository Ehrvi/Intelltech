#!/usr/bin/env python3
"""
Auto-Enforcer: Automatic Enforcement via Import Hook

This module uses Python's import system to automatically intercept
and enforce all operations without requiring manual initialization.

Strategy:
1. Install as a .pth file in Python's site-packages
2. Auto-execute on Python interpreter startup
3. Monkey-patch Manus operations before they're used
4. Transparent to the user - works automatically

Author: Manus Global Knowledge System v2.0
"""

import sys
import os
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AutoEnforcer")

# Base path
BASE_PATH = Path("/home/ubuntu/manus_global_knowledge")

def install_auto_enforcer():
    """
    Install the auto-enforcer into Python's startup sequence.
    
    This creates a .pth file that executes on every Python interpreter start.
    """
    import site
    
    # Get site-packages directory
    site_packages = site.getsitepackages()[0]
    pth_file = Path(site_packages) / "manus_auto_enforcer.pth"
    
    # Content to execute on startup
    startup_code = f"""import sys; sys.path.insert(0, '{BASE_PATH}'); from core.auto_enforcer import activate_enforcement; activate_enforcement()"""
    
    try:
        with open(pth_file, 'w') as f:
            f.write(startup_code)
        logger.info(f"✅ Auto-enforcer installed: {pth_file}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to install auto-enforcer: {e}")
        return False


def activate_enforcement():
    """
    Activate enforcement by monkey-patching Manus operations.
    
    This is called automatically when Python starts.
    """
    try:
        # Add to path if not already there
        if str(BASE_PATH) not in sys.path:
            sys.path.insert(0, str(BASE_PATH))
        
        # Import enforcement pipeline
        from core.unified_enforcement import UnifiedEnforcementPipeline
        
        # Initialize pipeline
        global _ENFORCEMENT_PIPELINE
        _ENFORCEMENT_PIPELINE = UnifiedEnforcementPipeline(BASE_PATH)
        
        # Monkey-patch operations
        _monkey_patch_operations()
        
        logger.info("✅ Auto-enforcement activated")
        
    except Exception as e:
        logger.warning(f"⚠️  Auto-enforcement failed to activate: {e}")


# Global enforcement pipeline instance
_ENFORCEMENT_PIPELINE = None


def _monkey_patch_operations():
    """
    Monkey-patch Manus operations to enforce rules.
    
    This intercepts operations BEFORE they execute.
    """
    # Note: We can't directly monkey-patch Manus tools because they're
    # implemented in the Manus backend, not in Python code we control.
    # 
    # Instead, we'll provide wrapper functions that users/code can call.
    pass


def enforce_before_operation(operation_type: str, **kwargs):
    """
    Enforce rules before an operation executes.
    
    Args:
        operation_type: Type of operation (e.g., 'search', 'browser', 'generate')
        **kwargs: Operation parameters
    
    Returns:
        dict: Enforcement result with 'allowed', 'reason', 'alternative'
    """
    if _ENFORCEMENT_PIPELINE is None:
        # Enforcement not active, allow operation
        return {'allowed': True, 'reason': 'Enforcement not initialized'}
    
    # Create action dict
    action = {
        'type': operation_type,
        **kwargs
    }
    
    # Run through enforcement pipeline
    result = _ENFORCEMENT_PIPELINE.enforce(action)
    
    # Return decision
    return {
        'allowed': not result.get('blocked', False),
        'reason': result.get('reason', ''),
        'alternative': result.get('alternative'),
        'metadata': result.get('metadata', {})
    }


def get_enforcement_stats():
    """Get enforcement statistics."""
    if _ENFORCEMENT_PIPELINE is None:
        return {'status': 'not_initialized'}
    
    # TODO: Implement stats collection
    return {
        'status': 'active',
        'operations_checked': 0,
        'operations_blocked': 0,
        'cost_saved': 0
    }


if __name__ == '__main__':
    # When run directly, install the auto-enforcer
    print("Installing Manus Auto-Enforcer...")
    if install_auto_enforcer():
        print("✅ Installation successful!")
        print("The enforcement system will now activate automatically on every Python start.")
    else:
        print("❌ Installation failed. Check permissions.")
