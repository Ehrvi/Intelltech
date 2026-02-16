import logging
#!/usr/bin/env python3
"""
Validation Test for MANUS OPERATING SYSTEM V2.0

Tests:
1. Operating System file exists and is readable
2. All 5 Core Principles are present
3. Prime Directive is defined
4. Master Checklist is present
5. Enforcement system is referenced
6. Compliance metrics are defined
7. Integration points are clear
"""

import os
import sys
from pathlib import Path

def test_file_exists():
    """Test that the Operating System file exists"""
    os_path = Path("/home/ubuntu/manus_global_knowledge/MANUS_OPERATING_SYSTEM.md")
    assert os_path.exists(), "❌ MANUS_OPERATING_SYSTEM.md not found"
    print("✅ Operating System file exists")
    return os_path

def test_content_structure(os_path):
    """Test that all required sections are present"""
    content = os_path.read_text()
    
    # Test Prime Directive
    assert "PRIME DIRECTIVE" in content, "❌ Prime Directive missing"
    assert "maximum value" in content.lower(), "❌ Prime Directive incomplete"
    print("✅ Prime Directive present")
    
    # Test 5 Core Principles
    principles = [
        "P1: Always Study First",
        "P2: Always Decide Autonomously",
        "P3: Always Optimize Cost",
        "P4: Always Ensure Quality",
        "P5: Always Report Accurately"
    ]
    
    for principle in principles:
        assert principle in content, f"❌ {principle} missing"
    print("✅ All 5 Core Principles present")
    
    # Test Master Checklist
    assert "MASTER CHECKLIST" in content, "❌ Master Checklist missing"
    assert "Before Starting Any Task" in content, "❌ Checklist incomplete"
    print("✅ Master Checklist present")
    
    # Test Enforcement System
    assert "ENFORCEMENT SYSTEM" in content, "❌ Enforcement System missing"
    assert "master_enforcer.py" in content, "❌ Master Enforcer not referenced"
    print("✅ Enforcement System referenced")
    
    # Test Compliance Metrics
    assert "COMPLIANCE METRICS" in content, "❌ Compliance Metrics missing"
    assert "Target" in content and "Measurement" in content, "❌ Metrics incomplete"
    print("✅ Compliance Metrics defined")
    
    # Test Integration
    assert "AI UNIVERSITY" in content, "❌ AI University integration missing"
    assert "OPERATIONAL PROTOCOLS" in content, "❌ Protocol integration missing"
    print("✅ Integration points clear")
    
    return content

def test_consolidation(content):
    """Test that lessons are properly consolidated"""
    # Check that key lessons are referenced
    lesson_refs = ["LESSON_017", "LESSON_020", "LESSON_021", "LESSON_022"]
    
    for lesson in lesson_refs:
        assert lesson in content, f"❌ {lesson} not consolidated"
    
    print("✅ Lessons properly consolidated")

def test_hierarchy(content):
    """Test that hierarchy is clear"""
    hierarchy_elements = [
        "Prime Directive",
        "Core Principles",
        "Operational Protocols",
        "Master Checklist"
    ]
    
    for element in hierarchy_elements:
        assert element in content, f"❌ Hierarchy element '{element}' missing"
    
    print("✅ Clear hierarchy established")

def test_activation_status(content):
    """Test that system is marked as active"""
    assert "ACTIVE" in content, "❌ System not marked as ACTIVE"
    assert "Status: 🟢 ACTIVE" in content or "Status:** ACTIVE" in content, "❌ Activation status unclear"
    print("✅ System marked as ACTIVE")

def main():
    """Run all validation tests"""
    print("\n" + "="*60)
    print("MANUS OPERATING SYSTEM V2.0 - VALIDATION TEST")
    print("="*60 + "\n")
    
    try:
        # Test 1: File exists
        os_path = test_file_exists()
        
        # Test 2: Content structure
        content = test_content_structure(os_path)
        
        # Test 3: Consolidation
        test_consolidation(content)
        
        # Test 4: Hierarchy
        test_hierarchy(content)
        
        # Test 5: Activation
        test_activation_status(content)
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED - OPERATING SYSTEM V2.0 VALIDATED")
        print("="*60 + "\n")
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ VALIDATION FAILED: {e}\n")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
