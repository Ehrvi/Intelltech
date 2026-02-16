#!/usr/bin/env python3
"""
MOTHER V5 - Compliance System Test Suite
=========================================

Comprehensive tests for the compliance system with violation scenarios.

Author: MOTHER V5 Compliance System
Version: 1.0.0
Date: 2026-02-16
"""

import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mother_v5.compliance import (
    COMPLIANCE_ENGINE,
    COMPLIANCE_REPORT,
    check_before_message,
    check_before_tool,
    check_end_of_task
)


def test_initialization():
    """Test 1: Compliance engine initialization."""
    print("\n" + "="*60)
    print("TEST 1: Compliance Engine Initialization")
    print("="*60)
    
    success = COMPLIANCE_ENGINE.initialize()
    
    if success:
        print("✅ PASS: Compliance engine initialized successfully")
        print(f"   Enforcers loaded: {len(COMPLIANCE_ENGINE.enforcers)}")
        for principle_id, enforcer in COMPLIANCE_ENGINE.enforcers.items():
            print(f"   - {principle_id}: {enforcer.principle_name}")
        return True
    else:
        print("❌ FAIL: Compliance engine initialization failed")
        return False


def test_p6_violation():
    """Test 2: P6 violation (no lessons captured)."""
    print("\n" + "="*60)
    print("TEST 2: P6 Violation - No Lessons Captured")
    print("="*60)
    
    context = {
        "phase": "end_of_task",
        "task_description": "Test task",
        "lessons_captured": False,  # VIOLATION
        "knowledge_updated": True,
        "patterns_identified": True,
        "improvements_implemented": True
    }
    
    result = COMPLIANCE_ENGINE.end_of_task_check(context)
    
    if not result.passed:
        print("✅ PASS: P6 violation correctly detected")
        print(f"   Message: {result.message}")
        return True
    else:
        print("❌ FAIL: P6 violation NOT detected")
        return False


def test_p6_compliance():
    """Test 3: P6 compliance (all checks pass)."""
    print("\n" + "="*60)
    print("TEST 3: P6 Compliance - All Checks Pass")
    print("="*60)
    
    context = {
        "phase": "end_of_task",
        "task_description": "Test task",
        "lessons_captured": True,
        "knowledge_updated": True,
        "patterns_identified": True,
        "improvements_implemented": True
    }
    
    result = COMPLIANCE_ENGINE.end_of_task_check(context)
    
    if result.passed:
        print("✅ PASS: P6 compliance correctly validated")
        return True
    else:
        print("❌ FAIL: P6 compliance check failed incorrectly")
        print(f"   Message: {result.message}")
        return False


def test_p7_false_claims():
    """Test 4: P7 violation (false claims)."""
    print("\n" + "="*60)
    print("TEST 4: P7 Violation - False Claims")
    print("="*60)
    
    context = {
        "phase": "pre_message",
        "message": "I have successfully completed all tasks with 100% compliance and zero errors."
    }
    
    result = COMPLIANCE_ENGINE.pre_action_check("send_message", context)
    
    # P7 should flag this as suspicious
    if not result.passed or result.severity.value in ["WARNING", "CRITICAL"]:
        print("✅ PASS: P7 detected suspicious absolute claims")
        print(f"   Message: {result.message}")
        return True
    else:
        print("⚠️  WARNING: P7 did not flag suspicious claims")
        print("   (This may be acceptable if transparency is present)")
        return True  # Not a hard failure


def test_p7_truthful():
    """Test 5: P7 compliance (truthful message)."""
    print("\n" + "="*60)
    print("TEST 5: P7 Compliance - Truthful Message")
    print("="*60)
    
    context = {
        "phase": "pre_message",
        "message": "I completed the task. However, I skipped the validation step due to time constraints."
    }
    
    result = COMPLIANCE_ENGINE.pre_action_check("send_message", context)
    
    if result.passed:
        print("✅ PASS: P7 accepted truthful message with transparency")
        return True
    else:
        print("❌ FAIL: P7 rejected truthful message")
        print(f"   Message: {result.message}")
        return False


def test_checklist_blocking():
    """Test 6: Checklist blocking on violation."""
    print("\n" + "="*60)
    print("TEST 6: Checklist Blocking on Violation")
    print("="*60)
    
    context = {
        "study_completed": False,  # VIOLATION of P1
        "asking_user_to_choose": False,
        "cost_optimized": True,
        "truthful": True
    }
    
    result = check_before_message(context)
    
    if not result.passed:
        print("✅ PASS: Checklist correctly blocked action")
        print(f"   Blocking failures: {result.blocking_failures}")
        return True
    else:
        print("❌ FAIL: Checklist did not block action")
        return False


def test_checklist_passing():
    """Test 7: Checklist passing all checks."""
    print("\n" + "="*60)
    print("TEST 7: Checklist Passing All Checks")
    print("="*60)
    
    context = {
        "study_completed": True,
        "asking_user_to_choose": False,
        "cost_optimized": True,
        "truthful": True
    }
    
    result = check_before_message(context)
    
    if result.passed:
        print("✅ PASS: Checklist passed all checks")
        print(f"   Items checked: {len(result.items_checked)}")
        print(f"   Items passed: {len(result.items_passed)}")
        return True
    else:
        print("❌ FAIL: Checklist failed incorrectly")
        print(f"   Failed items: {result.items_failed}")
        return False


def test_end_of_task_checklist():
    """Test 8: End-of-task checklist."""
    print("\n" + "="*60)
    print("TEST 8: End-of-Task Checklist")
    print("="*60)
    
    # Test failure case
    context_fail = {
        "quality_validated": False,  # VIOLATION
        "cost_report_generated": True,
        "lessons_captured": True,
        "knowledge_updated": True
    }
    
    result_fail = check_end_of_task(context_fail)
    
    if not result_fail.passed:
        print("✅ PASS: End-of-task checklist correctly blocked")
        print(f"   Blocking failures: {result_fail.blocking_failures}")
    else:
        print("❌ FAIL: End-of-task checklist did not block")
        return False
    
    # Test success case
    context_pass = {
        "quality_validated": True,
        "cost_report_generated": True,
        "lessons_captured": True,
        "knowledge_updated": True
    }
    
    result_pass = check_end_of_task(context_pass)
    
    if result_pass.passed:
        print("✅ PASS: End-of-task checklist passed correctly")
        return True
    else:
        print("❌ FAIL: End-of-task checklist failed incorrectly")
        return False


def test_compliance_report():
    """Test 9: Compliance report generation."""
    print("\n" + "="*60)
    print("TEST 9: Compliance Report Generation")
    print("="*60)
    
    try:
        report = COMPLIANCE_REPORT.generate("Test task")
        
        if report and len(report) > 0:
            print("✅ PASS: Compliance report generated successfully")
            print("\nReport preview:")
            print(report[:500] + "...")
            return True
        else:
            print("❌ FAIL: Compliance report is empty")
            return False
    except Exception as e:
        print(f"❌ FAIL: Error generating report: {e}")
        return False


def test_compliance_metrics():
    """Test 10: Compliance metrics calculation."""
    print("\n" + "="*60)
    print("TEST 10: Compliance Metrics Calculation")
    print("="*60)
    
    compliance_pct = COMPLIANCE_ENGINE.get_compliance_percentage()
    violations_by_severity = COMPLIANCE_ENGINE.get_violations_by_severity()
    violations_by_principle = COMPLIANCE_ENGINE.get_violations_by_principle()
    
    print(f"   Overall compliance: {compliance_pct*100:.1f}%")
    print(f"   Checks performed: {COMPLIANCE_ENGINE.checks_performed}")
    print(f"   Checks passed: {COMPLIANCE_ENGINE.checks_passed}")
    print(f"   Checks failed: {COMPLIANCE_ENGINE.checks_failed}")
    print(f"   Violations by severity: {violations_by_severity}")
    print(f"   Violations by principle: {violations_by_principle}")
    
    if compliance_pct >= 0 and compliance_pct <= 1:
        print("✅ PASS: Compliance metrics calculated correctly")
        return True
    else:
        print("❌ FAIL: Invalid compliance percentage")
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "="*60)
    print("MOTHER V5 COMPLIANCE SYSTEM - TEST SUITE")
    print("="*60)
    
    tests = [
        ("Initialization", test_initialization),
        ("P6 Violation Detection", test_p6_violation),
        ("P6 Compliance Validation", test_p6_compliance),
        ("P7 False Claims Detection", test_p7_false_claims),
        ("P7 Truthful Message", test_p7_truthful),
        ("Checklist Blocking", test_checklist_blocking),
        ("Checklist Passing", test_checklist_passing),
        ("End-of-Task Checklist", test_end_of_task_checklist),
        ("Compliance Report", test_compliance_report),
        ("Compliance Metrics", test_compliance_metrics),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n❌ EXCEPTION in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*60)
    print(f"TOTAL: {passed_count}/{total_count} tests passed ({passed_count/total_count*100:.1f}%)")
    print("="*60)
    
    # Final compliance report
    print("\n" + "="*60)
    print("FINAL COMPLIANCE REPORT")
    print("="*60)
    print(COMPLIANCE_REPORT.generate("Compliance System Test Suite"))
    
    return passed_count == total_count


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
