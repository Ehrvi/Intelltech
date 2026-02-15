#!/usr/bin/env python3
"""
Metrics collection system for Phase 1 credit optimization
Tracks: cache hits/misses, Google Drive calls, credit consumption
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

METRICS_DIR = Path(__file__).parent
METRICS_FILE = METRICS_DIR / "optimization_metrics.json"
SYNC_LOG = METRICS_DIR / "sync_log.csv"

def init_metrics():
    """Initialize metrics file if not exists"""
    if not METRICS_FILE.exists():
        metrics = {
            "phase1_start_date": datetime.now().isoformat(),
            "total_conversations": 0,
            "google_drive_calls": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "estimated_credits_saved": 0.0,
            "daily_stats": []
        }
        save_metrics(metrics)
    return load_metrics()

def load_metrics():
    """Load metrics from file"""
    if METRICS_FILE.exists():
        with open(METRICS_FILE, 'r') as f:
            return json.load(f)
    return init_metrics()

def save_metrics(metrics):
    """Save metrics to file"""
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    with open(METRICS_FILE, 'w') as f:
        json.dump(metrics, f, indent=2)

def log_conversation_start():
    """Log start of new conversation"""
    metrics = load_metrics()
    metrics["total_conversations"] += 1
    
    # Add daily stat if new day
    today = datetime.now().date().isoformat()
    if not metrics["daily_stats"] or metrics["daily_stats"][-1]["date"] != today:
        metrics["daily_stats"].append({
            "date": today,
            "conversations": 0,
            "drive_calls": 0,
            "cache_hits": 0,
            "cache_misses": 0
        })
    
    metrics["daily_stats"][-1]["conversations"] += 1
    save_metrics(metrics)

def log_cache_hit():
    """Log cache hit (Google Drive call avoided)"""
    metrics = load_metrics()
    metrics["cache_hits"] += 1
    metrics["estimated_credits_saved"] += 5.0  # Estimate: 5 credits per avoided sync
    
    if metrics["daily_stats"]:
        metrics["daily_stats"][-1]["cache_hits"] += 1
    
    save_metrics(metrics)

def log_cache_miss():
    """Log cache miss (Google Drive call made)"""
    metrics = load_metrics()
    metrics["cache_misses"] += 1
    metrics["google_drive_calls"] += 1
    
    if metrics["daily_stats"]:
        metrics["daily_stats"][-1]["cache_misses"] += 1
        metrics["daily_stats"][-1]["drive_calls"] += 1
    
    save_metrics(metrics)

def log_drive_call(operation="unknown"):
    """Log Google Drive API call"""
    metrics = load_metrics()
    metrics["google_drive_calls"] += 1
    
    if metrics["daily_stats"]:
        metrics["daily_stats"][-1]["drive_calls"] += 1
    
    save_metrics(metrics)

def calculate_savings_percentage():
    """Calculate credit savings percentage"""
    metrics = load_metrics()
    total_ops = metrics["cache_hits"] + metrics["cache_misses"]
    
    if total_ops == 0:
        return 0.0
    
    # Without cache: every conversation would sync (1 call)
    # With cache: only cache misses sync
    baseline_calls = total_ops
    actual_calls = metrics["cache_misses"]
    
    if baseline_calls == 0:
        return 0.0
    
    savings = ((baseline_calls - actual_calls) / baseline_calls) * 100
    return round(savings, 2)

def get_cache_hit_rate():
    """Calculate cache hit rate"""
    metrics = load_metrics()
    total = metrics["cache_hits"] + metrics["cache_misses"]
    
    if total == 0:
        return 0.0
    
    return round((metrics["cache_hits"] / total) * 100, 2)

def days_since_start():
    """Calculate days since Phase 1 start"""
    metrics = load_metrics()
    start_date = datetime.fromisoformat(metrics["phase1_start_date"])
    return (datetime.now() - start_date).days

def generate_summary():
    """Generate metrics summary"""
    metrics = load_metrics()
    days = days_since_start()
    savings_pct = calculate_savings_percentage()
    hit_rate = get_cache_hit_rate()
    
    summary = f"""
📊 Phase 1 Optimization Metrics Summary

⏱️  Days since implementation: {days}
💬 Total conversations: {metrics["total_conversations"]}
📞 Google Drive calls: {metrics["google_drive_calls"]}
✅ Cache hits: {metrics["cache_hits"]}
❌ Cache misses: {metrics["cache_misses"]}

📈 Performance:
   Cache hit rate: {hit_rate}%
   Credit savings: {savings_pct}%
   Estimated credits saved: {metrics["estimated_credits_saved"]:.0f}

🎯 Target: 80% savings
   Status: {"✅ ACHIEVED" if savings_pct >= 80 else "🟡 IN PROGRESS" if savings_pct >= 60 else "🔴 BELOW TARGET"}
"""
    
    return summary

def should_generate_weekly_report():
    """Check if weekly report should be generated"""
    return days_since_start() >= 7

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: collect_metrics.py {conversation_start|cache_hit|cache_miss|drive_call|summary}")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "conversation_start":
        log_conversation_start()
        print("✅ Logged conversation start")
    elif command == "cache_hit":
        log_cache_hit()
        print("✅ Logged cache hit")
    elif command == "cache_miss":
        log_cache_miss()
        print("✅ Logged cache miss")
    elif command == "drive_call":
        log_drive_call()
        print("✅ Logged Google Drive call")
    elif command == "summary":
        print(generate_summary())
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
