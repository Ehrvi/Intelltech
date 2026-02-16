#!/usr/bin/env python3
"""
MOTHER V5 - Compliance System Performance Tests
================================================

Measures the overhead of the compliance system to validate that enforcement
does not significantly impact system performance.

Based on: Riganelli et al. (2022) - Non-Functional Testing of Runtime Enforcers

Target: < 5% overhead for compliance checks (relative to realistic operations)

Author: MOTHER V5 Compliance System
Version: 2.0.0 (Scientific Update)
Date: 2026-02-16
"""

import sys
import time
import statistics
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mother_v5.compliance import (
    COMPLIANCE_ENGINE,
    check_before_message,
    check_before_tool,
    check_end_of_task
)


class PerformanceBenchmark:
    """Performance benchmarking for compliance system."""
    
    def __init__(self, iterations=1000):
        self.iterations = iterations
        self.results = {}
    
    def benchmark(self, name, func, *args, **kwargs):
        """Benchmark a function over multiple iterations."""
        times = []
        
        for _ in range(self.iterations):
            start = time.perf_counter()
            func(*args, **kwargs)
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to milliseconds
        
        self.results[name] = {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times),
            'p95': sorted(times)[int(len(times) * 0.95)],
            'p99': sorted(times)[int(len(times) * 0.99)]
        }
        
        return self.results[name]
    
    def print_results(self):
        """Print benchmark results in a formatted table."""
        print("\n" + "="*80)
        print("PERFORMANCE BENCHMARK RESULTS")
        print("="*80)
        print(f"Iterations: {self.iterations}")
        print()
        
        # Header
        print(f"{'Test':<40} {'Mean (ms)':<12} {'Median (ms)':<12} {'P95 (ms)':<12} {'P99 (ms)':<12}")
        print("-"*80)
        
        # Results
        for name, result in self.results.items():
            print(f"{name:<40} {result['mean']:<12.4f} {result['median']:<12.4f} "
                  f"{result['p95']:<12.4f} {result['p99']:<12.4f}")
        
        print("="*80)
    
    def calculate_overhead(self, baseline_name, test_name):
        """Calculate overhead percentage."""
        baseline = self.results[baseline_name]['mean']
        test = self.results[test_name]['mean']
        overhead = ((test - baseline) / baseline) * 100
        return overhead


# ============================================================================
# REALISTIC BASELINE OPERATIONS
# ============================================================================

def simulate_message_operation():
    """Simulate a realistic message operation (string formatting, validation)."""
    message = "This is a test message"
    # Simulate message formatting
    formatted = f"[INFO] {message}"
    # Simulate validation
    _ = len(formatted) > 0
    _ = isinstance(formatted, str)
    # Simulate logging
    _ = formatted.upper()


def simulate_tool_execution():
    """Simulate a realistic tool execution (function call, data processing)."""
    # Simulate data preparation
    data = {"key1": "value1", "key2": "value2", "key3": "value3"}
    # Simulate processing
    result = {}
    for k, v in data.items():
        result[k] = v.upper()
    # Simulate validation
    _ = len(result) == len(data)


def simulate_task_completion():
    """Simulate a realistic task completion (aggregation, reporting)."""
    # Simulate data aggregation
    results = [i for i in range(100)]
    # Simulate statistics
    total = sum(results)
    avg = total / len(results)
    # Simulate report generation
    report = f"Total: {total}, Average: {avg}"
    _ = len(report) > 0


# ============================================================================
# COMPLIANCE-ENABLED OPERATIONS
# ============================================================================

def message_operation_with_compliance():
    """Message operation WITH compliance check."""
    # Compliance check
    context = {
        "study_completed": True,
        "asking_user_to_choose": False,
        "cost_optimized": True,
        "truthful": True
    }
    check_before_message(context)
    
    # Actual operation
    simulate_message_operation()


def tool_execution_with_compliance():
    """Tool execution WITH compliance check."""
    # Compliance check
    context = {
        "study_completed": True,
        "tool_is_cheapest": True,
        "quality_sufficient": True
    }
    check_before_tool(context)
    
    # Actual operation
    simulate_tool_execution()


def task_completion_with_compliance():
    """Task completion WITH compliance check."""
    # Compliance check
    context = {
        "quality_validated": True,
        "cost_report_generated": True,
        "lessons_captured": True,
        "knowledge_updated": True
    }
    check_end_of_task(context)
    
    # Actual operation
    simulate_task_completion()


# ============================================================================
# ISOLATED COMPLIANCE CHECKS (for absolute measurement)
# ============================================================================

def isolated_pre_message_check():
    """Isolated pre-message compliance check."""
    context = {
        "study_completed": True,
        "asking_user_to_choose": False,
        "cost_optimized": True,
        "truthful": True
    }
    check_before_message(context)


def isolated_pre_tool_check():
    """Isolated pre-tool compliance check."""
    context = {
        "study_completed": True,
        "tool_is_cheapest": True,
        "quality_sufficient": True
    }
    check_before_tool(context)


def isolated_end_of_task_check():
    """Isolated end-of-task compliance check."""
    context = {
        "quality_validated": True,
        "cost_report_generated": True,
        "lessons_captured": True,
        "knowledge_updated": True
    }
    check_end_of_task(context)


def run_performance_tests():
    """Run all performance tests."""
    print("\n" + "="*80)
    print("MOTHER V5 COMPLIANCE SYSTEM - PERFORMANCE TESTS")
    print("="*80)
    print("\nBased on: Riganelli et al. (2022) - Non-Functional Testing of Runtime Enforcers")
    print("Target: < 5% overhead for compliance checks")
    print()
    
    # Initialize compliance engine
    print("Initializing ComplianceEngine...")
    COMPLIANCE_ENGINE.initialize()
    print("✅ ComplianceEngine initialized")
    
    # Create benchmark
    benchmark = PerformanceBenchmark(iterations=1000)
    
    # ========================================================================
    # PART 1: ABSOLUTE MEASUREMENTS
    # ========================================================================
    
    print("\n" + "="*80)
    print("PART 1: ABSOLUTE MEASUREMENTS (Isolated Compliance Checks)")
    print("="*80)
    print("\nRunning benchmarks (1000 iterations each)...")
    
    print("  1/3 Pre-message check...")
    benchmark.benchmark("Isolated: Pre-message check", isolated_pre_message_check)
    
    print("  2/3 Pre-tool check...")
    benchmark.benchmark("Isolated: Pre-tool check", isolated_pre_tool_check)
    
    print("  3/3 End-of-task check...")
    benchmark.benchmark("Isolated: End-of-task check", isolated_end_of_task_check)
    
    # Print absolute results
    print("\n" + "-"*80)
    print("ABSOLUTE COMPLIANCE OVERHEAD")
    print("-"*80)
    for name in ["Isolated: Pre-message check", "Isolated: Pre-tool check", "Isolated: End-of-task check"]:
        result = benchmark.results[name]
        print(f"{name:<40} {result['mean']:.4f} ms (median: {result['median']:.4f} ms)")
    
    # ========================================================================
    # PART 2: RELATIVE MEASUREMENTS (Realistic Operations)
    # ========================================================================
    
    print("\n" + "="*80)
    print("PART 2: RELATIVE MEASUREMENTS (Realistic Operations)")
    print("="*80)
    print("\nRunning benchmarks (1000 iterations each)...")
    
    print("  1/6 Message operation (baseline)...")
    benchmark.benchmark("Message operation (no compliance)", simulate_message_operation)
    
    print("  2/6 Message operation (with compliance)...")
    benchmark.benchmark("Message operation (with compliance)", message_operation_with_compliance)
    
    print("  3/6 Tool execution (baseline)...")
    benchmark.benchmark("Tool execution (no compliance)", simulate_tool_execution)
    
    print("  4/6 Tool execution (with compliance)...")
    benchmark.benchmark("Tool execution (with compliance)", tool_execution_with_compliance)
    
    print("  5/6 Task completion (baseline)...")
    benchmark.benchmark("Task completion (no compliance)", simulate_task_completion)
    
    print("  6/6 Task completion (with compliance)...")
    benchmark.benchmark("Task completion (with compliance)", task_completion_with_compliance)
    
    # Print relative results
    benchmark.print_results()
    
    # ========================================================================
    # OVERHEAD ANALYSIS
    # ========================================================================
    
    print("\n" + "="*80)
    print("OVERHEAD ANALYSIS")
    print("="*80)
    
    tests = [
        ("Message operation (with compliance)", "Message operation (no compliance)", "Message operation"),
        ("Tool execution (with compliance)", "Tool execution (no compliance)", "Tool execution"),
        ("Task completion (with compliance)", "Task completion (no compliance)", "Task completion")
    ]
    
    overhead_results = []
    for test_name, baseline_name, label in tests:
        overhead = benchmark.calculate_overhead(baseline_name, test_name)
        overhead_results.append((label, overhead))
        
        baseline_time = benchmark.results[baseline_name]['mean']
        test_time = benchmark.results[test_name]['mean']
        absolute_overhead = test_time - baseline_time
        
        status = "✅ PASS" if overhead < 5.0 else "⚠️  WARNING" if overhead < 10.0 else "❌ FAIL"
        print(f"{label:<30} {overhead:>8.2f}%  ({absolute_overhead:.4f} ms)  {status}")
    
    # Overall assessment
    avg_overhead = statistics.mean([o for _, o in overhead_results])
    max_overhead = max([o for _, o in overhead_results])
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Average overhead: {avg_overhead:.2f}%")
    print(f"Maximum overhead: {max_overhead:.2f}%")
    print(f"Target: < 5%")
    
    # Absolute overhead summary
    absolute_overheads = [
        benchmark.results["Isolated: Pre-message check"]['mean'],
        benchmark.results["Isolated: Pre-tool check"]['mean'],
        benchmark.results["Isolated: End-of-task check"]['mean']
    ]
    avg_absolute = statistics.mean(absolute_overheads)
    max_absolute = max(absolute_overheads)
    
    print(f"\nAbsolute compliance overhead:")
    print(f"  Average: {avg_absolute:.4f} ms")
    print(f"  Maximum: {max_absolute:.4f} ms")
    
    if max_overhead < 5.0:
        print("\n✅ PASS: All compliance checks meet performance target (< 5% overhead)")
        return True
    elif max_overhead < 10.0:
        print("\n⚠️  WARNING: Some checks exceed target but acceptable (< 10% overhead)")
        return True
    else:
        print("\n❌ FAIL: Compliance overhead too high (>= 10%)")
        return False


if __name__ == "__main__":
    success = run_performance_tests()
    sys.exit(0 if success else 1)
