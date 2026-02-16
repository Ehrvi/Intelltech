#!/usr/bin/env python3
"""
MOTHER V5 - Compliance Dashboard
=================================

Real-time compliance status visualization.

Author: MOTHER V5 Compliance System
Version: 1.0.0
Date: 2026-02-16
"""

from typing import Dict, Any
from datetime import datetime, timedelta
from .violation_logger import VIOLATION_LOGGER
from .compliance_engine import COMPLIANCE_ENGINE


class ComplianceDashboard:
    """
    Real-time compliance dashboard.
    
    Provides a text-based interface showing:
    - Overall compliance percentage
    - Violations by principle
    - Violations by severity
    - Recent violations
    - Trends over time
    """
    
    def __init__(self):
        self.logger = VIOLATION_LOGGER
        self.engine = COMPLIANCE_ENGINE
    
    def get_status(self, days: int = 7) -> str:
        """
        Get current compliance status.
        
        Args:
            days: Number of days to include in analysis
        
        Returns:
            Formatted status string
        """
        # Get engine stats
        if self.engine.initialized:
            engine_compliance = self.engine.get_compliance_percentage() * 100
            engine_checks = self.engine.checks_performed
            engine_violations = len(self.engine.violations)
        else:
            engine_compliance = 0.0
            engine_checks = 0
            engine_violations = 0
        
        # Get historical violations
        since = datetime.now() - timedelta(days=days)
        violations = self.logger.get_violations(since=since)
        by_principle = self.logger.get_violations_by_principle()
        by_severity = self.logger.get_violations_by_severity()
        
        # Calculate trend
        trend = self._calculate_trend(days)
        
        # Build dashboard
        dashboard = f"""
╔══════════════════════════════════════════════════════════════╗
║              MOTHER V5 COMPLIANCE DASHBOARD                  ║
╚══════════════════════════════════════════════════════════════╝

🎯 CURRENT SESSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Overall Compliance: {engine_compliance:.1f}%
  Checks Performed:   {engine_checks}
  Violations:         {engine_violations}
  Status:             {"🟢 COMPLIANT" if engine_compliance >= 95 else "🔴 NON-COMPLIANT"}

📊 HISTORICAL (Last {days} days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Violations:   {len(violations)}
  Trend:              {trend}

📋 VIOLATIONS BY PRINCIPLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # Sort by count descending
        for principle, count in sorted(by_principle.items(), key=lambda x: x[1], reverse=True):
            bar = self._create_bar(count, max(by_principle.values()) if by_principle else 1)
            dashboard += f"  {principle:4s} │ {bar} {count}\n"
        
        dashboard += f"""
⚠️  VIOLATIONS BY SEVERITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for severity in ["BLOCKING", "CRITICAL", "WARNING", "INFO"]:
            count = by_severity.get(severity, 0)
            bar = self._create_bar(count, max(by_severity.values()) if by_severity else 1)
            icon = self._get_severity_icon(severity)
            dashboard += f"  {icon} {severity:8s} │ {bar} {count}\n"
        
        dashboard += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        return dashboard
    
    def get_recent_violations(self, limit: int = 10) -> str:
        """
        Get recent violations.
        
        Args:
            limit: Maximum number of violations to show
        
        Returns:
            Formatted violations list
        """
        violations = self.logger.get_violations(limit=limit)
        
        if not violations:
            return "No recent violations."
        
        output = f"""
╔══════════════════════════════════════════════════════════════╗
║                    RECENT VIOLATIONS                         ║
╚══════════════════════════════════════════════════════════════╝

"""
        
        for i, violation in enumerate(reversed(violations), 1):
            timestamp = violation.get("timestamp", "unknown")
            principle = violation.get("principle", "UNKNOWN")
            severity = violation.get("severity", "UNKNOWN")
            message = violation.get("message", "No message")
            
            icon = self._get_severity_icon(severity)
            
            output += f"{i}. [{timestamp}] {icon} {principle} - {severity}\n"
            output += f"   {message}\n\n"
        
        return output
    
    def _calculate_trend(self, days: int) -> str:
        """Calculate trend in violations."""
        # Get violations for current period
        since = datetime.now() - timedelta(days=days)
        current = self.logger.get_violations(since=since)
        
        # Get violations for previous period
        prev_since = since - timedelta(days=days)
        previous = self.logger.get_violations(since=prev_since)
        previous = [v for v in previous if datetime.fromisoformat(v["timestamp"]) < since]
        
        current_count = len(current)
        previous_count = len(previous)
        
        if previous_count == 0:
            if current_count == 0:
                return "📊 Stable (no violations)"
            else:
                return f"📈 Increasing (+{current_count} violations)"
        
        change = ((current_count - previous_count) / previous_count) * 100
        
        if change > 10:
            return f"📈 Increasing (+{change:.1f}%)"
        elif change < -10:
            return f"📉 Decreasing ({change:.1f}%)"
        else:
            return "📊 Stable"
    
    def _create_bar(self, value: int, max_value: int, width: int = 20) -> str:
        """Create a text-based bar chart."""
        if max_value == 0:
            return "░" * width
        
        filled = int((value / max_value) * width)
        return "█" * filled + "░" * (width - filled)
    
    def _get_severity_icon(self, severity: str) -> str:
        """Get icon for severity level."""
        icons = {
            "BLOCKING": "🛑",
            "CRITICAL": "❌",
            "WARNING": "⚠️",
            "INFO": "ℹ️"
        }
        return icons.get(severity, "❓")


# Global dashboard instance
COMPLIANCE_DASHBOARD = ComplianceDashboard()


def show_status(days: int = 7):
    """Show compliance status."""
    print(COMPLIANCE_DASHBOARD.get_status(days))


def show_recent_violations(limit: int = 10):
    """Show recent violations."""
    print(COMPLIANCE_DASHBOARD.get_recent_violations(limit))


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "violations":
        show_recent_violations()
    else:
        show_status()
