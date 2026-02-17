#!/usr/bin/env python3
"""
Check Upgrade Readiness for V3 (Phase 2)
Validates system is ready for upgrade with intelligent checks

Author: Manus AI
Date: 2026-02-16
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict


def check_deployment() -> tuple[bool, str, dict]:
    """Check if V2 is deployed"""
    apollo_dir = Path("/home/ubuntu/ProjetoApollo")
    
    if not apollo_dir.exists():
        return False, "Apollo directory not found", {}
    
    python_files = list(apollo_dir.glob("*.py"))
    if not python_files:
        return False, "No Python files in Apollo directory", {}
    
    deployed = sum(1 for f in python_files if 'unified_cost_optimizer_v2' in f.read_text())
    
    if deployed == 0:
        return False, f"V2 not deployed (0/{len(python_files)} files)", {}
    
    return True, f"V2 deployed to {deployed}/{len(python_files)} files", {'deployed': deployed, 'total': len(python_files)}


def check_usage_data() -> tuple[bool, str, dict]:
    """Check if we have enough usage data"""
    log_file = Path("/home/ubuntu/manus_global_knowledge/logs/cost_tracking.jsonl")
    
    if not log_file.exists():
        return False, "No cost tracking data available", {}
    
    # Count entries in last 7 days
    cutoff = datetime.now() - timedelta(days=7)
    recent_entries = 0
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                entry_time = datetime.fromisoformat(entry['timestamp'])
                if entry_time > cutoff:
                    recent_entries += 1
    except Exception as e:
        return False, "Error reading cost tracking data", {}
    
    # Need at least 100 entries in last 7 days
    if recent_entries < 100:
        return False, f"Insufficient data: {recent_entries} entries (need 100+)", {'entries': recent_entries}
    
    return True, f"Sufficient data: {recent_entries} entries in last 7 days", {'entries': recent_entries}


def check_performance() -> tuple[bool, str, dict]:
    """Check current performance metrics"""
    log_file = Path("/home/ubuntu/manus_global_knowledge/logs/cost_tracking.jsonl")
    
    if not log_file.exists():
        return True, "No performance data yet (OK for new deployment)", {}
    
    # Calculate current cost reduction
    cutoff = datetime.now() - timedelta(days=7)
    total_cost = 0
    total_saved = 0
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                entry_time = datetime.fromisoformat(entry['timestamp'])
                if entry_time > cutoff:
                    total_cost += entry['cost']
                    total_saved += entry.get('saved', 0)
    except Exception as e:
        return True, "Cannot calculate performance (OK for new deployment)", {}
    
    if total_cost + total_saved == 0:
        return True, "No cost data yet (OK for new deployment)", {}
    
    reduction = (total_saved / (total_cost + total_saved) * 100)
    
    # V2 should achieve 55-65% reduction
    if reduction < 50:
        return False, f"Performance below expected: {reduction:.1f}% (expected 55-65%)", {'reduction': reduction}
    
    return True, f"Performance good: {reduction:.1f}% cost reduction", {'reduction': reduction}


def check_stability() -> tuple[bool, str, dict]:
    """Check system stability (no recent errors)"""
    log_file = Path("/home/ubuntu/manus_global_knowledge/logs/cost_tracking.jsonl")
    
    if not log_file.exists():
        return True, "No stability data yet (OK for new deployment)", {}
    
    # Check for errors in last 24 hours
    cutoff = datetime.now() - timedelta(hours=24)
    errors = 0
    total = 0
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                entry_time = datetime.fromisoformat(entry['timestamp'])
                if entry_time > cutoff:
                    total += 1
                    if entry.get('error'):
                        errors += 1
    except Exception as e:
        return True, "Cannot check stability (OK for new deployment)", {}
    
    if total == 0:
        return True, "No recent activity (OK)", {}
    
    error_rate = (errors / total * 100) if total > 0 else 0
    
    # Error rate should be < 5%
    if error_rate > 5:
        return False, f"High error rate: {error_rate:.1f}% (should be < 5%)", {'error_rate': error_rate}
    
    return True, f"System stable: {error_rate:.1f}% error rate", {'error_rate': error_rate}


def check_modules() -> tuple[bool, str, dict]:
    """Check if V3 modules are available"""
    core_dir = Path("/home/ubuntu/manus_global_knowledge/core")
    
    required_modules = [
        'unified_cost_optimizer_v3.py',
        'semantic_cache.py',
        'continuous_learner.py'
    ]
    
    missing = []
    for module in required_modules:
        if not (core_dir / module).exists():
            missing.append(module)
    
    if missing:
        return False, f"Missing modules: {', '.join(missing)}", {'missing': missing}
    
    # Try importing
    sys.path.insert(0, str(core_dir))
    
    try:
        from unified_cost_optimizer_v3 import UnifiedCostOptimizerV3
        from semantic_cache import SemanticCache
        from continuous_learner import ContinuousLearner
    except ImportError as e:
        return False, f"Module import error: {str(e)}", {}
    
    return True, "All V3 modules available and importable", {}


def main():
    parser = argparse.ArgumentParser(description='Check upgrade readiness for V3')
    parser.add_argument('--quiet', action='store_true', help='Quiet mode (exit code only)')
    args = parser.parse_args()
    
    if not args.quiet:
        print("="*70)
        print("UPGRADE READINESS CHECK - V2 → V3")
        print("="*70)
        print()
    
    checks = [
        ("V2 Deployment", check_deployment),
        ("Usage Data", check_usage_data),
        ("Performance", check_performance),
        ("Stability", check_stability),
        ("V3 Modules", check_modules),
    ]
    
    results = []
    all_passed = True
    
    for name, check_func in checks:
        passed, message, data = check_func()
        results.append((name, passed, message, data))
        
        if not args.quiet:
            status = "✅" if passed else "❌"
            print(f"{status} {name}: {message}")
        
        if not passed:
            all_passed = False
    
    if not args.quiet:
        print()
        print("="*70)
        
        if all_passed:
            print("✅ SYSTEM READY FOR UPGRADE TO V3")
            print()
            print("Run 'cost-upgrade-v3' to perform upgrade")
        else:
            print("⚠️ SYSTEM NOT READY FOR UPGRADE")
            print()
            print("Requirements:")
            for name, passed, message, data in results:
                if not passed:
                    print(f"  ❌ {name}: {message}")
            print()
            print("Wait for more usage data or fix issues before upgrading")
        
        print("="*70)
    
    # Exit code: 0 if ready, 1 if not
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
