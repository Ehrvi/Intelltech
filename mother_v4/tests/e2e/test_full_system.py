"""
End-to-End Tests for MOTHER V4

Tests the complete system: Bootstrap → Enforcement → Monitoring → Knowledge
"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from main import MOTHER
from application.services.enforcement_engine import TaskContext, Severity


def test_full_system_lifecycle():
    """Test complete system lifecycle"""
    print("\n" + "=" * 70)
    print("END-TO-END TEST: Full System Lifecycle")
    print("=" * 70)
    
    # 1. Initialize
    print("\n[1/6] Initializing MOTHER V4...")
    mother = MOTHER(environment="test")
    success = mother.initialize()
    
    assert success, "Initialization failed"
    assert mother.initialized, "System not marked as initialized"
    print("✓ Initialization successful")
    
    # 2. Verify components
    print("\n[2/6] Verifying components...")
    assert mother.bootstrap is not None, "Bootstrap not initialized"
    assert mother.enforcement is not None, "Enforcement not initialized"
    assert mother.monitor is not None, "Monitor not initialized"
    assert mother.knowledge is not None, "Knowledge not initialized"
    print("✓ All components initialized")
    
    # 3. Test enforcement (P1 violation)
    print("\n[3/6] Testing enforcement (P1 violation)...")
    context_fail = TaskContext(
        task_type="research",
        task_description="Find papers without research",
        used_annas_archive=False,
        used_browser=False
    )
    results_fail = mother.enforce_task(context_fail)
    
    # Should have at least one failure (P1)
    p1_failed = any(not r.passed and "P1" in r.principle for r in results_fail)
    assert p1_failed, "P1 should have failed but didn't"
    print("✓ P1 violation detected correctly")
    
    # 4. Test enforcement (all pass)
    print("\n[4/6] Testing enforcement (all pass)...")
    context_pass = TaskContext(
        task_type="research",
        task_description="Find papers with research",
        used_annas_archive=True,
        cost_estimate=2.5,
        quality_score=0.9
    )
    results_pass = mother.enforce_task(context_pass)
    
    # All should pass
    all_passed = all(r.passed for r in results_pass)
    assert all_passed, f"Some enforcements failed: {[r.principle for r in results_pass if not r.passed]}"
    print("✓ All enforcements passed")
    
    # 5. Test knowledge search
    print("\n[5/6] Testing knowledge search...")
    results = mother.search_knowledge("P1")
    assert len(results) > 0, "No results found for 'P1'"
    print(f"✓ Found {len(results)} results for 'P1'")
    
    # 6. Test metrics
    print("\n[6/6] Testing metrics...")
    metrics = mother.get_metrics()
    # Metrics might be empty in test mode, just verify it doesn't crash
    print(f"✓ Metrics retrieved: {len(metrics)} entries")
    
    # Shutdown
    print("\n[Cleanup] Shutting down...")
    mother.shutdown()
    assert not mother.initialized, "System still marked as initialized after shutdown"
    print("✓ Shutdown successful")
    
    print("\n" + "=" * 70)
    print("✓ END-TO-END TEST PASSED")
    print("=" * 70)
    
    return True


def test_v3_compatibility():
    """Test V3 compatibility layer"""
    print("\n" + "=" * 70)
    print("END-TO-END TEST: V3 Compatibility")
    print("=" * 70)
    
    from integration.v3_compatibility import MOTHER_V3_Adapter
    
    # 1. Create adapter
    print("\n[1/4] Creating V3 adapter...")
    adapter = MOTHER_V3_Adapter()
    print("✓ Adapter created")
    
    # 2. Bootstrap
    print("\n[2/4] Testing V3-style bootstrap...")
    success = adapter.bootstrap()
    assert success, "V3 bootstrap failed"
    print("✓ V3 bootstrap successful")
    
    # 3. Check enforcements
    print("\n[3/4] Checking enforcements...")
    for principle in ["P1", "P2", "P3", "P4", "P7"]:
        active = adapter.check_enforcement(principle)
        assert active, f"{principle} not active"
        print(f"✓ {principle} active")
    
    # 4. Get status
    print("\n[4/4] Getting status...")
    status = adapter.get_status()
    assert status["initialized"], "Not initialized according to status"
    assert "4.0" in status["version"], "Wrong version"
    print("✓ Status correct")
    
    print("\n" + "=" * 70)
    print("✓ V3 COMPATIBILITY TEST PASSED")
    print("=" * 70)
    
    return True


def test_error_handling():
    """Test error handling and recovery"""
    print("\n" + "=" * 70)
    print("END-TO-END TEST: Error Handling")
    print("=" * 70)
    
    # 1. Test using system before initialization
    print("\n[1/3] Testing pre-initialization usage...")
    mother = MOTHER(environment="test")
    
    try:
        context = TaskContext(task_type="other", task_description="Test")
        mother.enforce_task(context)
        assert False, "Should have raised RuntimeError"
    except RuntimeError as e:
        assert "not initialized" in str(e).lower()
        print("✓ Correctly raised error for pre-initialization usage")
    
    # 2. Initialize and test normal operation
    print("\n[2/3] Initializing and testing normal operation...")
    mother.initialize()
    context = TaskContext(task_type="other", task_description="Test")
    results = mother.enforce_task(context)
    assert len(results) > 0, "No enforcement results"
    print("✓ Normal operation works after initialization")
    
    # 3. Test double initialization
    print("\n[3/3] Testing double initialization...")
    success = mother.initialize()
    assert success, "Double initialization should succeed gracefully"
    print("✓ Double initialization handled gracefully")
    
    mother.shutdown()
    
    print("\n" + "=" * 70)
    print("✓ ERROR HANDLING TEST PASSED")
    print("=" * 70)
    
    return True


def test_performance():
    """Test system performance"""
    print("\n" + "=" * 70)
    print("END-TO-END TEST: Performance")
    print("=" * 70)
    
    import time
    
    # 1. Initialization time
    print("\n[1/3] Measuring initialization time...")
    mother = MOTHER(environment="test")
    start = time.time()
    mother.initialize()
    init_time = time.time() - start
    print(f"✓ Initialization time: {init_time:.3f}s")
    assert init_time < 5.0, f"Initialization too slow: {init_time:.3f}s"
    
    # 2. Enforcement time
    print("\n[2/3] Measuring enforcement time...")
    context = TaskContext(
        task_type="research",
        task_description="Test",
        used_annas_archive=True,
        quality_score=0.9
    )
    
    start = time.time()
    for _ in range(100):
        mother.enforce_task(context)
    enforcement_time = (time.time() - start) / 100
    print(f"✓ Average enforcement time: {enforcement_time*1000:.2f}ms")
    assert enforcement_time < 0.1, f"Enforcement too slow: {enforcement_time*1000:.2f}ms"
    
    # 3. Search time
    print("\n[3/3] Measuring search time...")
    start = time.time()
    for _ in range(10):
        mother.search_knowledge("P1")
    search_time = (time.time() - start) / 10
    print(f"✓ Average search time: {search_time*1000:.2f}ms")
    assert search_time < 1.0, f"Search too slow: {search_time*1000:.2f}ms"
    
    mother.shutdown()
    
    print("\n" + "=" * 70)
    print("✓ PERFORMANCE TEST PASSED")
    print("=" * 70)
    
    return True


def run_all_e2e_tests():
    """Run all end-to-end tests"""
    logging.basicConfig(level=logging.WARNING)  # Reduce noise
    
    print("\n" + "=" * 70)
    print("RUNNING ALL END-TO-END TESTS")
    print("=" * 70)
    
    tests = [
        ("Full System Lifecycle", test_full_system_lifecycle),
        ("V3 Compatibility", test_v3_compatibility),
        ("Error Handling", test_error_handling),
        ("Performance", test_performance)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success, None))
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"\n✗ TEST FAILED: {name}")
            print(f"  Error: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for name, success, error in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {name}")
        if error:
            print(f"       Error: {error}")
    
    print("\n" + "=" * 70)
    print(f"RESULTS: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_e2e_tests()
    sys.exit(0 if success else 1)
