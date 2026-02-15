#!/usr/bin/env python3
"""
Weekly monitoring script for Phase 1 optimization
Analyzes metrics and generates recommendations for Phase 2 if needed
Semi-automatic: runs weekly, notifies user with analysis
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Import metrics functions
sys.path.insert(0, str(Path(__file__).parent / "metrics"))
from collect_metrics import (
    load_metrics,
    calculate_savings_percentage,
    get_cache_hit_rate,
    days_since_start,
    should_generate_weekly_report
)

def analyze_bottlenecks(metrics):
    """Identify optimization bottlenecks"""
    bottlenecks = []
    
    # Check cache miss rate
    total_ops = metrics["cache_hits"] + metrics["cache_misses"]
    if total_ops > 0:
        miss_rate = (metrics["cache_misses"] / total_ops) * 100
        if miss_rate > 20:
            bottlenecks.append(f"High cache miss rate ({miss_rate:.1f}%) - Consider longer TTL or predictive prefetching")
    
    # Check Google Drive call frequency
    if metrics["total_conversations"] > 0:
        calls_per_conversation = metrics["google_drive_calls"] / metrics["total_conversations"]
        if calls_per_conversation > 0.5:
            bottlenecks.append(f"Multiple Drive calls per conversation ({calls_per_conversation:.2f}) - Consider batch operations")
    
    # Check daily variance
    if len(metrics["daily_stats"]) > 3:
        recent_days = metrics["daily_stats"][-3:]
        drive_calls = [day["drive_calls"] for day in recent_days]
        if max(drive_calls) > 0 and min(drive_calls) == 0:
            bottlenecks.append("Inconsistent sync patterns - Cache may not be persisting correctly")
    
    return bottlenecks

def estimate_phase2_savings(current_savings):
    """Estimate additional savings from Phase 2"""
    if current_savings >= 90:
        return 2  # Minimal additional savings
    elif current_savings >= 80:
        return 5  # Small additional savings
    elif current_savings >= 70:
        return 10  # Moderate additional savings
    else:
        return 15  # Significant additional savings possible

def generate_weekly_report():
    """Generate comprehensive weekly report"""
    metrics = load_metrics()
    days = days_since_start()
    savings_pct = calculate_savings_percentage()
    hit_rate = get_cache_hit_rate()
    
    # Calculate averages
    avg_conversations_per_day = metrics["total_conversations"] / max(days, 1)
    avg_drive_calls_per_day = metrics["google_drive_calls"] / max(days, 1)
    
    report = f"""
╔══════════════════════════════════════════════════════════════╗
║         PHASE 1 OPTIMIZATION - WEEKLY REPORT                 ║
║         Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}                       ║
╚══════════════════════════════════════════════════════════════╝

📊 METRICS SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏱️  Implementation duration: {days} days
💬 Total conversations: {metrics["total_conversations"]}
📞 Google Drive calls: {metrics["google_drive_calls"]}
✅ Cache hits: {metrics["cache_hits"]}
❌ Cache misses: {metrics["cache_misses"]}

📈 PERFORMANCE METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Cache hit rate: {hit_rate}%
Credit savings: {savings_pct}%
Estimated credits saved: {metrics["estimated_credits_saved"]:.0f}

Daily averages:
  - Conversations: {avg_conversations_per_day:.1f}
  - Google Drive calls: {avg_drive_calls_per_day:.1f}

🎯 GOAL ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Target: 80% credit savings
Current: {savings_pct}%
Status: {"✅ GOAL ACHIEVED" if savings_pct >= 80 else "🟡 APPROACHING GOAL" if savings_pct >= 70 else "🔴 BELOW TARGET"}
"""
    
    # Add bottleneck analysis
    bottlenecks = analyze_bottlenecks(metrics)
    if bottlenecks:
        report += f"""
🔍 BOTTLENECK ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, bottleneck in enumerate(bottlenecks, 1):
            report += f"{i}. {bottleneck}\n"
    
    # Add recommendations
    if savings_pct < 80:
        phase2_additional = estimate_phase2_savings(savings_pct)
        report += f"""
💡 RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current savings ({savings_pct}%) are below the 80% target.

RECOMMENDED ACTION: Implement Phase 2 optimizations

Phase 2 includes:
  1. Compression & deduplication (reduce transfer size)
  2. Delta sync with rdiff (transfer only changes)
  3. Adaptive TTL (critical data = shorter TTL)

Estimated additional savings: +{phase2_additional}%
Projected total savings: {savings_pct + phase2_additional}%

Implementation time: 4-6 hours
Complexity: Medium

DECISION REQUIRED: Should we proceed with Phase 2?
  - YES: Implement Phase 2 for additional optimization
  - NO: Accept current savings level and monitor
  - ADJUST: Tune Phase 1 parameters (TTL, cache strategy)
"""
    else:
        report += f"""
✅ SUCCESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1 optimization has achieved the 80% savings target!

Current savings: {savings_pct}%
Status: Goal exceeded by {savings_pct - 80:.1f}%

RECOMMENDATION: Continue monitoring, Phase 2 not necessary.

Optional enhancements (if desired):
  - Implement Phase 2 for 85-95% savings (marginal benefit)
  - Focus on other optimization areas
  - Document learnings and best practices
"""
    
    report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 NEXT STEPS

1. Review this report
2. Make decision on Phase 2 (if recommended)
3. Continue monitoring for 1 more week
4. Update optimization strategy as needed

Report saved to: /home/ubuntu/manus_global_knowledge/weekly_report.txt
"""
    
    return report

def save_report(report):
    """Save report to file"""
    report_path = Path(__file__).parent / "weekly_report.txt"
    with open(report_path, 'w') as f:
        f.write(report)
    return report_path

def main():
    """Main execution"""
    if not should_generate_weekly_report():
        days = days_since_start()
        print(f"⏱️  Only {days} days since Phase 1 start. Weekly report will be generated after 7 days.")
        return
    
    print("📊 Generating weekly optimization report...")
    report = generate_weekly_report()
    report_path = save_report(report)
    
    print(report)
    print(f"\n✅ Report saved to: {report_path}")
    print("\n🔔 NOTIFICATION: Please review the report and make a decision on Phase 2.")

if __name__ == "__main__":
    main()
