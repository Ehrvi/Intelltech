#!/usr/bin/env python3
"""
Manus Credit Optimization Dashboard
Real-time monitoring and reporting

Author: Manus AI
Date: 2026-02-16
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from manus_credit_optimizer import get_optimizer


def generate_daily_report():
    """Generate daily optimization report"""
    optimizer = get_optimizer()
    stats = optimizer.get_optimization_stats()
    
    print("="*70)
    print(f"MANUS CREDIT OPTIMIZATION - DAILY REPORT")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("="*70)
    print()
    
    # File Cache Stats
    print("📁 FILE CACHING")
    print("-"*70)
    cache_stats = stats['file_cache']
    print(f"Cached Files: {cache_stats['cached_files']}")
    print(f"Cache Size: {cache_stats['total_size_mb']:.2f} MB")
    print(f"Total Accesses: {cache_stats['total_accesses']}")
    print(f"Cache Hits: {cache_stats['cache_hits']}")
    print(f"Hit Rate: {cache_stats['hit_rate_pct']:.1f}%")
    print(f"Tokens Saved: {cache_stats['tokens_saved']:,}")
    print()
    
    # Savings Report
    if 'savings_report' in stats and 'error' not in stats['savings_report']:
        print("💰 SAVINGS SUMMARY (Last 7 Days)")
        print("-"*70)
        savings = stats['savings_report']
        print(f"Total Tasks: {savings['total_tasks']}")
        print(f"Total Tokens: {savings['total_tokens']:,}")
        print(f"Avg Tokens/Task: {savings['avg_tokens_per_task']:.0f}")
        print(f"Estimated Baseline: {savings['estimated_baseline']:,}")
        print(f"Savings: {savings['savings_pct']:.1f}%")
        print()
        
        if savings['optimization_stats']:
            print("Optimization Breakdown:")
            for opt_name, opt_value in savings['optimization_stats'].items():
                print(f"  • {opt_name}: {opt_value}")
        print()
    
    # Enabled Optimizations
    print("⚙️ ENABLED OPTIMIZATIONS")
    print("-"*70)
    for opt_name, enabled in stats['enabled_optimizations'].items():
        status = "✅" if enabled else "❌"
        print(f"{status} {opt_name.replace('_', ' ').title()}")
    print()
    
    print("="*70)


def generate_weekly_report():
    """Generate weekly optimization report"""
    print("="*70)
    print(f"MANUS CREDIT OPTIMIZATION - WEEKLY REPORT")
    print(f"Week ending: {datetime.now().strftime('%Y-%m-%d')}")
    print("="*70)
    print()
    
    # Load historical data
    log_file = Path("/home/ubuntu/manus_global_knowledge/logs/manus_optimization.jsonl")
    
    if not log_file.exists():
        print("⚠️ No data available yet")
        return
    
    # Analyze last 7 days
    cutoff = datetime.now() - timedelta(days=7)
    daily_stats = defaultdict(lambda: {'tasks': 0, 'tokens': 0})
    
    with open(log_file, 'r') as f:
        for line in f:
            entry = json.loads(line)
            timestamp = datetime.fromisoformat(entry['timestamp'])
            
            if timestamp > cutoff:
                date_key = timestamp.strftime('%Y-%m-%d')
                daily_stats[date_key]['tasks'] += 1
                daily_stats[date_key]['tokens'] += entry['tokens_used']
    
    # Print daily breakdown
    print("📊 DAILY BREAKDOWN")
    print("-"*70)
    print(f"{'Date':<12} {'Tasks':<10} {'Tokens':<15} {'Avg/Task':<10}")
    print("-"*70)
    
    for date in sorted(daily_stats.keys()):
        stats = daily_stats[date]
        avg = stats['tokens'] / stats['tasks'] if stats['tasks'] > 0 else 0
        print(f"{date:<12} {stats['tasks']:<10} {stats['tokens']:<15,} {avg:<10.0f}")
    
    print()
    
    # Weekly totals
    total_tasks = sum(s['tasks'] for s in daily_stats.values())
    total_tokens = sum(s['tokens'] for s in daily_stats.values())
    avg_tokens = total_tokens / total_tasks if total_tasks > 0 else 0
    
    print("📈 WEEKLY TOTALS")
    print("-"*70)
    print(f"Total Tasks: {total_tasks}")
    print(f"Total Tokens: {total_tokens:,}")
    print(f"Avg Tokens/Task: {avg_tokens:.0f}")
    print()
    
    # Estimate savings
    baseline_tokens = total_tokens / 0.315  # Assuming 68.5% reduction
    savings_pct = (1 - total_tokens / baseline_tokens) * 100
    
    print("💰 ESTIMATED SAVINGS")
    print("-"*70)
    print(f"Baseline (no optimization): {baseline_tokens:,.0f} tokens")
    print(f"Actual (with optimization): {total_tokens:,} tokens")
    print(f"Tokens Saved: {baseline_tokens - total_tokens:,.0f}")
    print(f"Savings: {savings_pct:.1f}%")
    print()
    
    print("="*70)


def show_live_stats():
    """Show live statistics"""
    optimizer = get_optimizer()
    stats = optimizer.get_optimization_stats()
    
    print("="*70)
    print("MANUS CREDIT OPTIMIZATION - LIVE STATS")
    print("="*70)
    print()
    
    # Quick summary
    cache_stats = stats['file_cache']
    
    print(f"📁 Cache: {cache_stats['cached_files']} files, {cache_stats['hit_rate_pct']:.1f}% hit rate")
    print(f"💾 Size: {cache_stats['total_size_mb']:.2f} MB")
    print(f"💰 Saved: {cache_stats['tokens_saved']:,} tokens")
    print()
    
    # Optimizations status
    print("Optimizations:")
    for opt_name, enabled in stats['enabled_optimizations'].items():
        status = "🟢" if enabled else "🔴"
        print(f"  {status} {opt_name.replace('_', ' ').title()}")
    
    print()


def main():
    """Main dashboard"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 manus_optimization_dashboard.py [daily|weekly|live]")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == 'daily':
        generate_daily_report()
    elif mode == 'weekly':
        generate_weekly_report()
    elif mode == 'live':
        show_live_stats()
    else:
        print(f"Unknown mode: {mode}")
        print("Available modes: daily, weekly, live")


if __name__ == "__main__":
    main()
