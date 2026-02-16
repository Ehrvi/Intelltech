#!/usr/bin/env python3
"""
MOTHER V5 - Violation Logger
=============================

Immutable logging system for all compliance violations.

Author: MOTHER V5 Compliance System
Version: 1.0.0
Date: 2026-02-16
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional


class ViolationLogger:
    """
    Logger for compliance violations.
    
    Creates an immutable, append-only log of all violations
    in JSONL format for easy analysis.
    """
    
    def __init__(self, log_file: str = None):
        if log_file is None:
            log_file = "/home/ubuntu/manus_global_knowledge/mother_v5/compliance/violations.jsonl"
        
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create file if it doesn't exist
        if not self.log_file.exists():
            self.log_file.touch()
    
    def log(
        self,
        principle: str,
        severity: str,
        message: str,
        context: Dict[str, Any] = None,
        action_type: str = None
    ):
        """
        Log a compliance violation.
        
        Args:
            principle: Principle ID (e.g., "P1", "P2")
            severity: Severity level (BLOCKING, CRITICAL, WARNING, INFO)
            message: Human-readable description of the violation
            context: Additional context (optional)
            action_type: Type of action that triggered the violation (optional)
        """
        violation = {
            "timestamp": datetime.now().isoformat(),
            "principle": principle,
            "severity": severity,
            "message": message,
            "action_type": action_type,
            "context": context or {}
        }
        
        # Append to log file (JSONL format)
        with open(self.log_file, "a") as f:
            f.write(json.dumps(violation) + "\n")
    
    def get_violations(
        self,
        principle: str = None,
        severity: str = None,
        since: datetime = None,
        limit: int = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve violations from the log.
        
        Args:
            principle: Filter by principle (optional)
            severity: Filter by severity (optional)
            since: Filter by timestamp (optional)
            limit: Maximum number of violations to return (optional)
        
        Returns:
            List of violation dictionaries
        """
        violations = []
        
        if not self.log_file.exists():
            return violations
        
        with open(self.log_file, "r") as f:
            for line in f:
                try:
                    violation = json.loads(line.strip())
                    
                    # Apply filters
                    if principle and violation.get("principle") != principle:
                        continue
                    if severity and violation.get("severity") != severity:
                        continue
                    if since:
                        violation_time = datetime.fromisoformat(violation["timestamp"])
                        if violation_time < since:
                            continue
                    
                    violations.append(violation)
                    
                    # Check limit
                    if limit and len(violations) >= limit:
                        break
                        
                except json.JSONDecodeError:
                    continue
        
        return violations
    
    def get_violation_count(
        self,
        principle: str = None,
        severity: str = None,
        since: datetime = None
    ) -> int:
        """Get count of violations matching filters."""
        return len(self.get_violations(principle, severity, since))
    
    def get_violations_by_principle(self) -> Dict[str, int]:
        """Get count of violations grouped by principle."""
        violations = self.get_violations()
        counts = {}
        for violation in violations:
            principle = violation.get("principle", "UNKNOWN")
            counts[principle] = counts.get(principle, 0) + 1
        return counts
    
    def get_violations_by_severity(self) -> Dict[str, int]:
        """Get count of violations grouped by severity."""
        violations = self.get_violations()
        counts = {}
        for violation in violations:
            severity = violation.get("severity", "UNKNOWN")
            counts[severity] = counts.get(severity, 0) + 1
        return counts
    
    def clear_old_violations(self, days: int = 30):
        """
        Archive violations older than specified days.
        
        Args:
            days: Number of days to keep (default: 30)
        """
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        if not self.log_file.exists():
            return
        
        # Read all violations
        violations = []
        with open(self.log_file, "r") as f:
            for line in f:
                try:
                    violation = json.loads(line.strip())
                    violation_time = datetime.fromisoformat(violation["timestamp"])
                    if violation_time.timestamp() >= cutoff:
                        violations.append(violation)
                except (json.JSONDecodeError, ValueError):
                    continue
        
        # Write back only recent violations
        with open(self.log_file, "w") as f:
            for violation in violations:
                f.write(json.dumps(violation) + "\n")
    
    def generate_summary(self, days: int = 7) -> str:
        """
        Generate a summary of recent violations.
        
        Args:
            days: Number of days to include in summary
        
        Returns:
            Formatted summary string
        """
        since = datetime.now().timestamp() - (days * 24 * 60 * 60)
        since_dt = datetime.fromtimestamp(since)
        
        violations = self.get_violations(since=since_dt)
        by_principle = {}
        by_severity = {}
        
        for violation in violations:
            principle = violation.get("principle", "UNKNOWN")
            severity = violation.get("severity", "UNKNOWN")
            by_principle[principle] = by_principle.get(principle, 0) + 1
            by_severity[severity] = by_severity.get(severity, 0) + 1
        
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║           VIOLATION LOG SUMMARY (Last {days} days)                ║
╚══════════════════════════════════════════════════════════════╝

📊 Total Violations: {len(violations)}

📋 By Principle:
"""
        for principle, count in sorted(by_principle.items()):
            summary += f"   • {principle}: {count}\n"
        
        summary += "\n⚠️  By Severity:\n"
        for severity, count in sorted(by_severity.items()):
            summary += f"   • {severity}: {count}\n"
        
        return summary
    
    def __repr__(self):
        total = self.get_violation_count()
        return f"<ViolationLogger file={self.log_file} total_violations={total}>"


# Global logger instance
VIOLATION_LOGGER = ViolationLogger()
