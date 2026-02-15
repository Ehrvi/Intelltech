#!/usr/bin/env python3
"""
Monitoring and Auto-Improvement System

Real-time monitoring, dashboards, and continuous improvement.
Implements missing scientific method steps: 9 (Monitor) and 12 (Auto-improve)
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

class Monitor:
    """System monitoring and auto-improvement"""
    
    def __init__(self, base_path: Path = Path("/home/ubuntu/manus_global_knowledge")):
        self.base_path = base_path
        self.logs_dir = base_path / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        self.operations_log = self.logs_dir / "operations.jsonl"
        self.improvements_log = self.logs_dir / "improvements.jsonl"
        self.alerts_log = self.logs_dir / "alerts.jsonl"
    
    def check_health(self) -> Dict:
        """
        Check system health and generate alerts if needed
        
        Returns:
            Dict with health status and alerts
        """
        health = {
            'status': 'healthy',
            'alerts': [],
            'warnings': [],
            'metrics': {}
        }
        
        # Check 1: Are we actually saving money?
        stats = self._get_recent_stats(hours=24)
        
        if stats['total_operations'] > 0:
            savings_rate = stats['savings_percent']
            health['metrics']['savings_rate'] = savings_rate
            
            if savings_rate < 50:
                health['alerts'].append({
                    'severity': 'HIGH',
                    'message': f'Savings rate is only {savings_rate:.1f}% (target: 80%+)',
                    'action': 'Review tool selection decisions'
                })
                health['status'] = 'degraded'
            elif savings_rate < 80:
                health['warnings'].append({
                    'severity': 'MEDIUM',
                    'message': f'Savings rate is {savings_rate:.1f}% (target: 80%+)',
                    'action': 'Consider more aggressive cost optimization'
                })
        
        # Check 2: Quality levels
        if stats['avg_quality'] > 0:
            health['metrics']['avg_quality'] = stats['avg_quality']
            
            if stats['avg_quality'] < 70:
                health['alerts'].append({
                    'severity': 'HIGH',
                    'message': f"Quality is {stats['avg_quality']:.1f}/100 (target: 80+)",
                    'action': 'Enable Guardian validation on all outputs'
                })
                health['status'] = 'degraded'
            elif stats['avg_quality'] < 80:
                health['warnings'].append({
                    'severity': 'MEDIUM',
                    'message': f"Quality is {stats['avg_quality']:.1f}/100 (target: 80+)",
                    'action': 'Review quality validation process'
                })
        
        # Check 3: Cache hit rate
        cache_stats = self._get_cache_stats()
        if cache_stats['total_queries'] > 0:
            hit_rate = cache_stats['hit_rate']
            health['metrics']['cache_hit_rate'] = hit_rate
            
            if hit_rate < 20:
                health['warnings'].append({
                    'severity': 'LOW',
                    'message': f'Cache hit rate is {hit_rate:.1f}% (target: 30%+)',
                    'action': 'Ensure all research is being cached'
                })
        
        # Log alerts
        if health['alerts']:
            self._log_alerts(health['alerts'])
        
        return health
    
    def generate_dashboard(self) -> str:
        """Generate a text-based dashboard"""
        health = self.check_health()
        stats = self._get_recent_stats(hours=24)
        
        dashboard = []
        dashboard.append("=" * 80)
        dashboard.append("MANUS GLOBAL KNOWLEDGE SYSTEM - MONITORING DASHBOARD")
        dashboard.append("=" * 80)
        dashboard.append("")
        
        # Status indicator
        status_emoji = "✅" if health['status'] == 'healthy' else "⚠️"
        dashboard.append(f"System Status: {status_emoji} {health['status'].upper()}")
        dashboard.append("")
        
        # Key metrics
        dashboard.append("KEY METRICS (Last 24 hours)")
        dashboard.append("-" * 80)
        dashboard.append(f"  Operations: {stats['total_operations']}")
        dashboard.append(f"  Total Cost: {stats['total_cost']:.3f} credits")
        dashboard.append(f"  Total Savings: {stats['total_savings']:.3f} credits")
        dashboard.append(f"  Savings Rate: {stats['savings_percent']:.1f}% {'✅' if stats['savings_percent'] >= 80 else '⚠️'}")
        dashboard.append(f"  Avg Quality: {stats['avg_quality']:.1f}/100 {'✅' if stats['avg_quality'] >= 80 else '⚠️'}")
        dashboard.append(f"  Cache Hit Rate: {health['metrics'].get('cache_hit_rate', 0):.1f}%")
        dashboard.append("")
        
        # Tool usage
        if stats['tool_usage']:
            dashboard.append("TOOL USAGE")
            dashboard.append("-" * 80)
            for tool, data in sorted(stats['tool_usage'].items(), key=lambda x: x[1]['count'], reverse=True):
                dashboard.append(f"  {tool:20s} {data['count']:3d} ops  {data['cost']:8.3f} credits")
            dashboard.append("")
        
        # Alerts
        if health['alerts']:
            dashboard.append("🚨 ALERTS")
            dashboard.append("-" * 80)
            for alert in health['alerts']:
                dashboard.append(f"  [{alert['severity']}] {alert['message']}")
                dashboard.append(f"           Action: {alert['action']}")
            dashboard.append("")
        
        # Warnings
        if health['warnings']:
            dashboard.append("⚠️  WARNINGS")
            dashboard.append("-" * 80)
            for warning in health['warnings']:
                dashboard.append(f"  [{warning['severity']}] {warning['message']}")
                dashboard.append(f"           Action: {warning['action']}")
            dashboard.append("")
        
        # Recommendations
        recommendations = self.get_recommendations()
        if recommendations:
            dashboard.append("💡 RECOMMENDATIONS")
            dashboard.append("-" * 80)
            for i, rec in enumerate(recommendations, 1):
                dashboard.append(f"  {i}. {rec}")
            dashboard.append("")
        
        dashboard.append("=" * 80)
        dashboard.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        dashboard.append("=" * 80)
        
        return "\n".join(dashboard)
    
    def get_recommendations(self) -> List[str]:
        """Generate improvement recommendations based on data"""
        recommendations = []
        stats = self._get_recent_stats(hours=24)
        
        # Analyze tool usage patterns
        if stats['tool_usage']:
            # Check if search is being used when OpenAI could work
            if 'search' in stats['tool_usage']:
                search_count = stats['tool_usage']['search']['count']
                if search_count > 0:
                    recommendations.append(
                        f"You used 'search' {search_count} times. Consider using OpenAI API for research instead (20x cheaper)."
                    )
            
            # Check if map is being overused
            if 'map' in stats['tool_usage']:
                map_count = stats['tool_usage']['map']['count']
                if map_count > 5:
                    recommendations.append(
                        f"High map usage ({map_count} ops). Consider sequential processing with OpenAI for smaller batches."
                    )
        
        # Check savings rate
        if stats['savings_percent'] < 80:
            recommendations.append(
                "Savings rate below target. Review the cognitive enforcement protocol before each tool use."
            )
        
        # Check quality
        if 0 < stats['avg_quality'] < 80:
            recommendations.append(
                "Quality below target. Enable Guardian validation on all critical outputs."
            )
        
        return recommendations
    
    def auto_improve(self) -> Dict:
        """
        Automatically improve system based on collected data
        
        Returns:
            Dict with improvements made
        """
        improvements = {
            'timestamp': datetime.now().isoformat(),
            'changes': []
        }
        
        stats = self._get_recent_stats(hours=24)
        
        # Auto-improvement 1: Update cost estimates based on actual usage
        if stats['tool_usage']:
            for tool, data in stats['tool_usage'].items():
                avg_cost = data['cost'] / data['count'] if data['count'] > 0 else 0
                improvements['changes'].append({
                    'type': 'cost_estimate_update',
                    'tool': tool,
                    'new_avg_cost': avg_cost
                })
        
        # Auto-improvement 2: Identify frequently used queries for caching
        # (Would analyze query patterns here)
        
        # Log improvements
        with open(self.improvements_log, 'a') as f:
            f.write(json.dumps(improvements) + '\n')
        
        return improvements
    
    def _get_recent_stats(self, hours: int = 24) -> Dict:
        """Get statistics for recent operations"""
        if not self.operations_log.exists():
            return {
                'total_operations': 0,
                'total_cost': 0,
                'total_savings': 0,
                'savings_percent': 0,
                'avg_quality': 0,
                'tool_usage': {}
            }
        
        cutoff = datetime.now() - timedelta(hours=hours)
        
        entries = []
        with open(self.operations_log, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if datetime.fromisoformat(entry['timestamp']) > cutoff:
                        entries.append(entry)
                except:
                    continue
        
        if not entries:
            return {
                'total_operations': 0,
                'total_cost': 0,
                'total_savings': 0,
                'savings_percent': 0,
                'avg_quality': 0,
                'tool_usage': {}
            }
        
        total_cost = sum(e.get('cost', 0) for e in entries)
        total_savings = sum(e.get('savings', 0) for e in entries)
        quality_scores = [e['quality_score'] for e in entries if e.get('quality_score') is not None]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        tool_usage = defaultdict(lambda: {'count': 0, 'cost': 0})
        for entry in entries:
            tool = entry.get('tool_used', 'unknown')
            tool_usage[tool]['count'] += 1
            tool_usage[tool]['cost'] += entry.get('cost', 0)
        
        return {
            'total_operations': len(entries),
            'total_cost': total_cost,
            'total_savings': total_savings,
            'savings_percent': (total_savings / (total_cost + total_savings) * 100) if (total_cost + total_savings) > 0 else 0,
            'avg_quality': avg_quality,
            'tool_usage': dict(tool_usage)
        }
    
    def _get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        # Placeholder - would integrate with knowledge_cache.py
        return {
            'total_queries': 0,
            'cache_hits': 0,
            'hit_rate': 0
        }
    
    def _log_alerts(self, alerts: List[Dict]):
        """Log alerts to file"""
        for alert in alerts:
            entry = {
                'timestamp': datetime.now().isoformat(),
                **alert
            }
            with open(self.alerts_log, 'a') as f:
                f.write(json.dumps(entry) + '\n')


# Convenience functions
_monitor = None

def get_monitor() -> Monitor:
    """Get the global monitor instance"""
    global _monitor
    if _monitor is None:
        _monitor = Monitor()
    return _monitor


def check_health() -> Dict:
    """Quick health check"""
    return get_monitor().check_health()


def show_dashboard():
    """Quick dashboard display"""
    print(get_monitor().generate_dashboard())


if __name__ == '__main__':
    # Demo usage
    monitor = Monitor()
    
    # Show dashboard
    print(monitor.generate_dashboard())
