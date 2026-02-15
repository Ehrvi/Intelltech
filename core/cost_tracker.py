#!/usr/bin/env python3
"""
Cost Tracking and Logging System

Tracks every operation, costs, savings, and provides analytics.
Fixes BUG-004: No Cost Tracking
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List

class CostTracker:
    """Track costs and savings for all operations"""
    
    def __init__(self, base_path: Path = Path("/home/ubuntu/manus_global_knowledge")):
        self.base_path = base_path
        self.logs_dir = base_path / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        self.operations_log = self.logs_dir / "operations.jsonl"
        self.daily_summary = self.logs_dir / "daily_summary.jsonl"
        
        # Cost reference (in credits)
        self.COST_TABLE = {
            'openai': 0.001,  # Extremely cheap
            'file_read': 1,
            'file_write': 2,
            'shell': 3,
            'search': 20,
            'browser': 40,
            'map_per_item': 10,
            'generate': 15,
        }
    
    def log_operation(
        self,
        operation: str,
        tool_used: str,
        cost: float,
        alternative_tool: Optional[str] = None,
        alternative_cost: Optional[float] = None,
        reason: str = "",
        quality_score: Optional[int] = None
    ) -> Dict:
        """
        Log a single operation with all details
        
        Args:
            operation: Description of what was done
            tool_used: Which tool was actually used
            cost: Actual cost in credits
            alternative_tool: What other tool could have been used
            alternative_cost: Cost of the alternative
            reason: Why this tool was chosen
            quality_score: Quality rating 0-100
        
        Returns:
            Dict with log entry
        """
        savings = 0
        if alternative_cost is not None:
            savings = alternative_cost - cost
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'tool_used': tool_used,
            'cost': cost,
            'alternative_tool': alternative_tool,
            'alternative_cost': alternative_cost,
            'savings': savings,
            'savings_percent': (savings / alternative_cost * 100) if alternative_cost and alternative_cost > 0 else 0,
            'reason': reason,
            'quality_score': quality_score
        }
        
        # Append to log file
        with open(self.operations_log, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        return entry
    
    def get_stats(self, days: int = 1) -> Dict:
        """
        Get statistics for the last N days
        
        Args:
            days: Number of days to analyze
        
        Returns:
            Dict with statistics
        """
        if not self.operations_log.exists():
            return {
                'total_operations': 0,
                'total_cost': 0,
                'total_savings': 0,
                'avg_quality': 0
            }
        
        # Read all entries
        entries = []
        with open(self.operations_log, 'r') as f:
            for line in f:
                entries.append(json.loads(line))
        
        # Filter by date
        cutoff = datetime.now().timestamp() - (days * 86400)
        recent_entries = [
            e for e in entries
            if datetime.fromisoformat(e['timestamp']).timestamp() > cutoff
        ]
        
        if not recent_entries:
            return {
                'total_operations': 0,
                'total_cost': 0,
                'total_savings': 0,
                'avg_quality': 0
            }
        
        # Calculate stats
        total_cost = sum(e['cost'] for e in recent_entries)
        total_savings = sum(e['savings'] for e in recent_entries)
        quality_scores = [e['quality_score'] for e in recent_entries if e['quality_score'] is not None]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # Tool usage breakdown
        tool_usage = {}
        for entry in recent_entries:
            tool = entry['tool_used']
            if tool not in tool_usage:
                tool_usage[tool] = {'count': 0, 'cost': 0}
            tool_usage[tool]['count'] += 1
            tool_usage[tool]['cost'] += entry['cost']
        
        return {
            'total_operations': len(recent_entries),
            'total_cost': total_cost,
            'total_savings': total_savings,
            'savings_percent': (total_savings / (total_cost + total_savings) * 100) if (total_cost + total_savings) > 0 else 0,
            'avg_quality': avg_quality,
            'tool_usage': tool_usage,
            'cost_per_operation': total_cost / len(recent_entries) if recent_entries else 0
        }
    
    def generate_daily_summary(self) -> Dict:
        """Generate and save daily summary"""
        stats = self.get_stats(days=1)
        
        summary = {
            'date': datetime.now().date().isoformat(),
            'timestamp': datetime.now().isoformat(),
            **stats
        }
        
        # Save to daily summary log
        with open(self.daily_summary, 'a') as f:
            f.write(json.dumps(summary) + '\n')
        
        return summary
    
    def print_report(self, days: int = 1):
        """Print a formatted report"""
        stats = self.get_stats(days)
        
        print("=" * 70)
        print(f"COST TRACKING REPORT - Last {days} day(s)")
        print("=" * 70)
        print()
        print(f"Total Operations: {stats['total_operations']}")
        print(f"Total Cost: {stats['total_cost']:.3f} credits")
        print(f"Total Savings: {stats['total_savings']:.3f} credits")
        print(f"Savings Rate: {stats['savings_percent']:.1f}%")
        print(f"Average Quality: {stats['avg_quality']:.1f}/100")
        print(f"Cost per Operation: {stats['cost_per_operation']:.3f} credits")
        print()
        
        if stats['tool_usage']:
            print("Tool Usage Breakdown:")
            print("-" * 70)
            for tool, data in sorted(stats['tool_usage'].items(), key=lambda x: x[1]['cost'], reverse=True):
                print(f"  {tool:20s} {data['count']:3d} ops  {data['cost']:8.3f} credits")
        
        print()
        print("=" * 70)


# Convenience functions for easy use
_tracker = None

def get_tracker() -> CostTracker:
    """Get the global cost tracker instance"""
    global _tracker
    if _tracker is None:
        _tracker = CostTracker()
    return _tracker


def log_cost(operation: str, tool: str, cost: float, **kwargs):
    """Quick logging function"""
    return get_tracker().log_operation(operation, tool, cost, **kwargs)


def get_stats(days: int = 1) -> Dict:
    """Quick stats function"""
    return get_tracker().get_stats(days)


def print_report(days: int = 1):
    """Quick report function"""
    get_tracker().print_report(days)


if __name__ == '__main__':
    # Demo usage
    tracker = CostTracker()
    
    # Log some example operations
    tracker.log_operation(
        operation="Research AI companies",
        tool_used="openai",
        cost=0.001,
        alternative_tool="search",
        alternative_cost=20,
        reason="OpenAI has this knowledge",
        quality_score=95
    )
    
    tracker.log_operation(
        operation="Scrape website",
        tool_used="browser",
        cost=40,
        alternative_tool=None,
        alternative_cost=None,
        reason="No alternative exists",
        quality_score=88
    )
    
    tracker.log_operation(
        operation="Generate code",
        tool_used="openai",
        cost=0.001,
        alternative_tool="generate",
        alternative_cost=15,
        reason="OpenAI is faster and cheaper",
        quality_score=92
    )
    
    # Print report
    tracker.print_report()
