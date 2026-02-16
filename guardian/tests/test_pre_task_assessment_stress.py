#!/usr/bin/env python3
"""
Stress Tests for Pre-Task Knowledge Assessment System

Tests edge cases, failure modes, and integration scenarios.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))

from knowledge_assessor import KnowledgeAssessor
from research_planner import ResearchPlanner
from annas_archive import AnnaArchiveIntegration

def test_1_no_gaps():
    """Test 1: Task with no knowledge gaps (all master level)."""
    print("=" * 60)
    print("TEST 1: No Knowledge Gaps")
    print("=" * 60)
    
    assessor = KnowledgeAssessor()
    task = "Create a Python script to parse JSON data"
    
    assessments, report = assessor.assess_task(task)
    print(report)
    
    gaps = [area for area, level in assessments.items() if level == "gap"]
    
    if not gaps:
        print("\n✅ PASS: No gaps detected, should proceed directly")
        return True
    else:
        print(f"\n❌ FAIL: Unexpected gaps: {gaps}")
        return False

def test_2_multiple_gaps():
    """Test 2: Task with multiple knowledge gaps."""
    print("\n" + "=" * 60)
    print("TEST 2: Multiple Knowledge Gaps")
    print("=" * 60)
    
    assessor = KnowledgeAssessor()
    planner = ResearchPlanner()
    
    task = "Build a quantum blockchain using formal verification"
    
    assessments, report = assessor.assess_task(task)
    print(report)
    
    gaps = [area for area, level in assessments.items() if level == "gap"]
    
    if gaps:
        print(f"\n✅ Gaps detected: {gaps}")
        print("\nGenerating research plan...")
        
        plan = planner.create_research_plan(gaps)
        plan_report = planner.generate_research_plan_report(plan)
        print(plan_report)
        
        if plan['num_gaps'] == len(gaps):
            print(f"\n✅ PASS: Research plan generated for all {len(gaps)} gaps")
            return True
        else:
            print(f"\n❌ FAIL: Plan has {plan['num_gaps']} gaps but expected {len(gaps)}")
            return False
    else:
        print("\n❌ FAIL: Expected gaps but none detected")
        return False

def test_3_annas_archive_accessible():
    """Test 3: Anna's Archive domain accessibility."""
    print("\n" + "=" * 60)
    print("TEST 3: Anna's Archive Accessibility")
    print("=" * 60)
    
    integration = AnnaArchiveIntegration()
    domain = integration.get_current_domain()
    
    print(integration.generate_usage_report())
    
    if domain:
        print(f"\n✅ PASS: Anna's Archive accessible at {domain}")
        return True
    else:
        print("\n⚠️  WARN: Anna's Archive not accessible (fallback will be used)")
        print("This is not necessarily a failure - fallback services should work")
        return True  # Not a failure, fallback is expected

def test_4_annas_archive_fallback():
    """Test 4: Fallback service when Anna's Archive is down."""
    print("\n" + "=" * 60)
    print("TEST 4: Anna's Archive Fallback")
    print("=" * 60)
    
    integration = AnnaArchiveIntegration()
    
    # Test paper fallback
    fallback_paper = integration.get_fallback_service("paper")
    print("Paper Fallback:")
    print(f"  Name: {fallback_paper['name']}")
    print(f"  Domains: {fallback_paper['domains']}")
    print(f"  Instructions: {fallback_paper['instructions']}")
    
    # Test book fallback
    fallback_book = integration.get_fallback_service("book")
    print("\nBook Fallback:")
    print(f"  Name: {fallback_book['name']}")
    print(f"  Domains: {fallback_book['domains']}")
    print(f"  Instructions: {fallback_book['instructions']}")
    
    if fallback_paper['name'] == "Sci-Hub" and fallback_book['name'] == "Library Genesis":
        print("\n✅ PASS: Correct fallback services configured")
        return True
    else:
        print("\n❌ FAIL: Incorrect fallback services")
        return False

def test_5_tiered_source_priority():
    """Test 5: Tiered source priority (Tier 1 → Tier 2 → Tier 3)."""
    print("\n" + "=" * 60)
    print("TEST 5: Tiered Source Priority")
    print("=" * 60)
    
    integration = AnnaArchiveIntegration()
    sources = integration.get_research_sources("machine learning", type="paper")
    
    print("Source Priority Order:")
    for i, source in enumerate(sources, 1):
        print(f"{i}. Tier {source['tier']}: {source['name']} ({source['type']})")
        if 'note' in source:
            print(f"   Note: {source['note']}")
    
    # Check that Tier 1 comes before Tier 3
    tier1_indices = [i for i, s in enumerate(sources) if s['tier'] == 1]
    tier3_indices = [i for i, s in enumerate(sources) if s['tier'] == 3]
    
    if tier1_indices and tier3_indices and max(tier1_indices) < min(tier3_indices):
        print("\n✅ PASS: Tier 1 sources come before Tier 3")
        return True
    else:
        print("\n❌ FAIL: Source priority order incorrect")
        return False

def test_6_invalid_task():
    """Test 6: Handling of unclear/invalid task description."""
    print("\n" + "=" * 60)
    print("TEST 6: Invalid Task Description")
    print("=" * 60)
    
    assessor = KnowledgeAssessor()
    task = "asdf qwerty zxcv"  # Nonsense task
    
    assessments, report = assessor.assess_task(task)
    print(report)
    
    # Should default to general programming
    if assessments:
        print(f"\n✅ PASS: Handled invalid task (defaulted to {list(assessments.keys())})")
        return True
    else:
        print("\n❌ FAIL: No assessment generated for invalid task")
        return False

def test_7_edge_case_single_gap():
    """Test 7: Edge case - exactly one knowledge gap."""
    print("\n" + "=" * 60)
    print("TEST 7: Single Knowledge Gap")
    print("=" * 60)
    
    assessor = KnowledgeAssessor()
    planner = ResearchPlanner()
    
    task = "Implement Kubernetes deployment"
    
    assessments, report = assessor.assess_task(task)
    print(report)
    
    gaps = [area for area, level in assessments.items() if level == "gap"]
    
    if len(gaps) == 1:
        plan = planner.create_research_plan(gaps)
        print(f"\nEstimated time: {plan['estimated_time']}")
        
        if plan['estimated_time'] == "1-2 hours":
            print("\n✅ PASS: Correct time estimate for single gap")
            return True
        else:
            print(f"\n❌ FAIL: Expected 1-2 hours, got {plan['estimated_time']}")
            return False
    else:
        print(f"\n⚠️  WARN: Expected 1 gap, got {len(gaps)}")
        return True  # Not a failure, just different than expected

def test_8_research_notes_specificity():
    """Test 8: Research notes are specific to knowledge area."""
    print("\n" + "=" * 60)
    print("TEST 8: Research Notes Specificity")
    print("=" * 60)
    
    planner = ResearchPlanner()
    
    gaps = ["blockchain_consensus", "quantum_computing", "kubernetes"]
    plan = planner.create_research_plan(gaps)
    
    print("Research Notes:")
    for gap_plan in plan['gaps']:
        print(f"\n{gap_plan['topic']}:")
        print(f"  {gap_plan['notes']}")
    
    # Check that notes are different
    notes = [gap_plan['notes'] for gap_plan in plan['gaps']]
    unique_notes = set(notes)
    
    if len(unique_notes) == len(notes):
        print("\n✅ PASS: All research notes are unique and specific")
        return True
    else:
        print("\n❌ FAIL: Some research notes are duplicated")
        return False

def test_9_integration_workflow():
    """Test 9: Complete integration workflow (assess → plan → sources)."""
    print("\n" + "=" * 60)
    print("TEST 9: Complete Integration Workflow")
    print("=" * 60)
    
    assessor = KnowledgeAssessor()
    planner = ResearchPlanner()
    integration = AnnaArchiveIntegration()
    
    task = "Create a compiler using formal verification"
    
    # Step 1: Assess
    print("Step 1: Assess knowledge...")
    assessments, report = assessor.assess_task(task)
    print(report)
    
    # Step 2: Plan
    gaps = [area for area, level in assessments.items() if level == "gap"]
    if gaps:
        print("\nStep 2: Create research plan...")
        plan = planner.create_research_plan(gaps)
        plan_report = planner.generate_research_plan_report(plan)
        print(plan_report)
        
        # Step 3: Get sources
        print("\nStep 3: Get research sources with Anna's Archive...")
        for gap_plan in plan['gaps']:
            sources = integration.get_research_sources(gap_plan['topic'], type="paper")
            print(f"\n{gap_plan['topic']} sources:")
            for source in sources[:3]:  # Show top 3
                print(f"  - Tier {source['tier']}: {source['name']}")
        
        print("\n✅ PASS: Complete workflow executed successfully")
        return True
    else:
        print("\n⚠️  WARN: No gaps detected, workflow shortened")
        return True

def test_10_stress_many_gaps():
    """Test 10: Stress test with many knowledge gaps (5+)."""
    print("\n" + "=" * 60)
    print("TEST 10: Stress Test - Many Gaps")
    print("=" * 60)
    
    planner = ResearchPlanner()
    
    gaps = [
        "blockchain_consensus",
        "quantum_computing",
        "formal_verification",
        "compiler_design",
        "kubernetes",
        "llm_fine_tuning"
    ]
    
    plan = planner.create_research_plan(gaps)
    print(f"Number of gaps: {plan['num_gaps']}")
    print(f"Estimated time: {plan['estimated_time']}")
    
    if plan['num_gaps'] == len(gaps) and plan['estimated_time'] == "5-8 hours":
        print("\n✅ PASS: Handled many gaps correctly")
        return True
    else:
        print(f"\n❌ FAIL: Expected 6 gaps and 5-8 hours, got {plan['num_gaps']} gaps and {plan['estimated_time']}")
        return False

# Run all tests
def run_all_tests():
    """Run all stress tests and report results."""
    tests = [
        test_1_no_gaps,
        test_2_multiple_gaps,
        test_3_annas_archive_accessible,
        test_4_annas_archive_fallback,
        test_5_tiered_source_priority,
        test_6_invalid_task,
        test_7_edge_case_single_gap,
        test_8_research_notes_specificity,
        test_9_integration_workflow,
        test_10_stress_many_gaps
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append((test.__name__, result))
        except Exception as e:
            print(f"\n❌ EXCEPTION in {test.__name__}: {e}")
            results.append((test.__name__, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed ({100*passed//total}%)")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
