#!/usr/bin/env python3
"""
MOTHER V3.2 - Critical Enforcement Checker
==========================================

PURPOSE: Verify 100% MOTHER enforcement compliance at bootstrap.
If compliance is not 100%, STOP all task execution immediately.

This is a CRITICAL safety mechanism to ensure MOTHER principles
are always active before any work begins.

Author: MOTHER V3.2
Version: 1.0.1
"""

import sys
import os
from pathlib import Path

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
RESET = '\033[0m'

def check_file_exists(path: str, description: str) -> bool:
    """Check if a file exists."""
    exists = Path(path).exists()
    if exists:
        print(f"   ✅ {description}")
    else:
        print(f"   ❌ {description} - MISSING: {path}")
    return exists

def critical_enforcement_check() -> bool:
    """
    Perform critical enforcement check.
    Returns True if 100% compliant, False otherwise.
    """
    print(f"\n{BOLD}🔒 CRITICAL ENFORCEMENT CHECK{RESET}")
    print("=" * 60)
    
    base_path = Path("/home/ubuntu/manus_global_knowledge")
    all_checks_passed = True
    
    # Check 1: Core Operating System
    print(f"\n{BOLD}1. Core Operating System (P1-P5){RESET}")
    if not check_file_exists(
        str(base_path / "MANUS_OPERATING_SYSTEM.md"),
        "MANUS_OPERATING_SYSTEM.md"
    ):
        all_checks_passed = False
    
    # Check 2: P3 Cost Optimization Enforcement
    print(f"\n{BOLD}2. P3 Cost Optimization Enforcement{RESET}")
    if not check_file_exists(
        str(base_path / "core" / "P3_COST_OPTIMIZATION_ENFORCED.md"),
        "P3_COST_OPTIMIZATION_ENFORCED.md"
    ):
        all_checks_passed = False
    
    # Check 3: Scientific Method Enforcement
    print(f"\n{BOLD}3. Scientific Method Enforcement{RESET}")
    if not check_file_exists(
        str(base_path / "core" / "SCIENTIFIC_METHODOLOGY_REQUIREMENTS.md"),
        "SCIENTIFIC_METHODOLOGY_REQUIREMENTS.md"
    ):
        all_checks_passed = False
    
    # Check 4: Bibliographic References
    print(f"\n{BOLD}4. Bibliographic References System{RESET}")
    if not check_file_exists(
        str(base_path / "core" / "BIBLIOGRAPHIC_REFERENCES.md"),
        "BIBLIOGRAPHIC_REFERENCES.md"
    ):
        all_checks_passed = False
    
    # Check 5: Anna's Archive Integration
    print(f"\n{BOLD}5. Anna's Archive Integration (P1){RESET}")
    if not check_file_exists(
        str(base_path / "core" / "annas_archive_workflow.py"),
        "annas_archive_workflow.py"
    ):
        all_checks_passed = False
    
    # Check 6: Cost Reporting System
    print(f"\n{BOLD}6. Cost Reporting System{RESET}")
    if not check_file_exists(
        str(base_path / "core" / "cost_reporting_reminder.py"),
        "cost_reporting_reminder.py"
    ):
        all_checks_passed = False
    
    # Check 7: Visual Identity
    print(f"\n{BOLD}7. Visual Identity System{RESET}")
    if not check_file_exists(
        str(base_path / "core" / "visual_identity_detector.py"),
        "visual_identity_detector.py"
    ):
        all_checks_passed = False
    
    # Check 8: Guardian Validation
    print(f"\n{BOLD}8. Guardian Quality Validation{RESET}")
    guardian_found = False
    if check_file_exists(
        str(base_path / "core" / "guardian.py"),
        "guardian.py"
    ):
        guardian_found = True
    if check_file_exists(
        str(base_path / "core" / "guardian_validator.py"),
        "guardian_validator.py"
    ):
        guardian_found = True
    
    if not guardian_found:
        print(f"   ❌ No Guardian validator found")
        all_checks_passed = False
    
    # Final verdict
    print("\n" + "=" * 60)
    if all_checks_passed:
        print(f"{GREEN}{BOLD}✅ ENFORCEMENT CHECK PASSED: 100% COMPLIANCE{RESET}")
        print(f"{GREEN}All MOTHER systems are active and operational.{RESET}")
        print(f"{GREEN}Task execution is AUTHORIZED.{RESET}\n")
        return True
    else:
        print(f"{RED}{BOLD}❌ ENFORCEMENT CHECK FAILED: < 100% COMPLIANCE{RESET}")
        print(f"{RED}MOTHER systems are NOT fully operational.{RESET}")
        print(f"{RED}{BOLD}TASK EXECUTION IS BLOCKED.{RESET}")
        print(f"\n{YELLOW}ACTION REQUIRED:{RESET}")
        print(f"  1. Fix missing enforcement files")
        print(f"  2. Re-run bootstrap.sh")
        print(f"  3. Verify 100% compliance before proceeding\n")
        return False

if __name__ == "__main__":
    # Run critical check
    passed = critical_enforcement_check()
    
    # Exit with appropriate code
    if passed:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure - blocks execution
