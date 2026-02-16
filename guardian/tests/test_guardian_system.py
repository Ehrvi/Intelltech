#!/usr/bin/env python3
"""
Comprehensive test suite for Guardian System.

Tests all components and their integration.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))

from state_tracker import StateTracker
from checklist_manager import ChecklistManager
from verification import VerificationEngine, IntegrationMonitor
from guardian_core import GuardianCore


def test_state_tracker():
    """Test StateTracker functionality."""
    print("\n=== Testing StateTracker ===")
    
    tracker = StateTracker("~/.guardian_test_state.json")
    tracker.initialize_task("test_001", "Test task", 1)
    
    # Test nested values
    tracker.set_nested('checklist', 'item_1', value=True)
    assert tracker.get_nested('checklist', 'item_1') == True
    
    # Test update
    tracker.update({'phase': 2, 'status': 'in_progress'})
    assert tracker.get('phase') == 2
    
    print("✅ StateTracker tests passed")
    return True


def test_checklist_manager():
    """Test ChecklistManager functionality."""
    print("\n=== Testing ChecklistManager ===")
    
    manager = ChecklistManager()
    manager.load_checklist("software_development")
    
    # Test phase items
    phase_1_items = manager.get_phase_items(1)
    assert len(phase_1_items) > 0
    
    # Test marking complete
    manager.mark_complete('research_complete')
    assert manager.is_complete('research_complete')
    
    # Test can advance (should fail - not all critical items done)
    can_advance, _ = manager.can_advance_from_phase(1)
    assert not can_advance  # Should be blocked
    
    # Complete all critical items in phase 1
    for item in manager.get_critical_items(1):
        manager.mark_complete(item.id)
    
    can_advance, _ = manager.can_advance_from_phase(1)
    assert can_advance  # Should now be allowed
    
    print("✅ ChecklistManager tests passed")
    return True


def test_verification_engine():
    """Test VerificationEngine functionality."""
    print("\n=== Testing VerificationEngine ===")
    
    engine = VerificationEngine()
    
    # Test file verification
    result = engine.verify_file_exists("/home/ubuntu/manus_global_knowledge/bootstrap.sh")
    assert result.passed
    
    # Test command verification
    result = engine.verify_command_succeeds("echo test", "Echo test")
    assert result.passed
    
    # Test environment variable
    os.environ['TEST_VAR'] = 'value'
    result = engine.verify_env_var_set('TEST_VAR')
    assert result.passed
    
    print("✅ VerificationEngine tests passed")
    return True


def test_integration_monitor():
    """Test IntegrationMonitor functionality."""
    print("\n=== Testing IntegrationMonitor ===")
    
    monitor = IntegrationMonitor()
    
    # Test individual checks
    is_active, msg = monitor.check_api_keys()
    print(f"  API Keys: {msg}")
    
    # Test overall health
    all_healthy, report = monitor.check_all()
    print(f"  Overall health: {'✓' if all_healthy else '✗'}")
    
    print("✅ IntegrationMonitor tests passed")
    return True


def test_guardian_core():
    """Test GuardianCore orchestration."""
    print("\n=== Testing GuardianCore ===")
    
    guardian = GuardianCore()
    guardian.initialize_task("test_002", "Test Guardian Core", "software_development")
    
    # Test blocking without checklist
    success, _ = guardian.advance_phase(1, 2)
    assert not success  # Should be blocked
    
    # Complete critical items
    for item in guardian.checklist_manager.get_critical_items(1):
        guardian.mark_checklist_item_complete(item.id)
    
    # Should now advance
    success, _ = guardian.advance_phase(1, 2)
    assert success
    
    # Test task completion check (should fail - not all phases done)
    is_done, _ = guardian.is_task_truly_done()
    assert not is_done
    
    print("✅ GuardianCore tests passed")
    return True


def run_all_tests():
    """Run all tests."""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║            GUARDIAN SYSTEM - COMPREHENSIVE TESTS             ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    
    tests = [
        ("StateTracker", test_state_tracker),
        ("ChecklistManager", test_checklist_manager),
        ("VerificationEngine", test_verification_engine),
        ("IntegrationMonitor", test_integration_monitor),
        ("GuardianCore", test_guardian_core)
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ {name} test FAILED: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed}/{len(tests)} tests passed")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED!")
        return True
    else:
        print(f"⚠️  {failed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
