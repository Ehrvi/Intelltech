#!/usr/bin/env python3
"""
MOTHER V5 - Compliance Report
==============================

End-of-task compliance report generator.

Author: MOTHER V5 Compliance System
Version: 1.0.0
Date: 2026-02-16
"""

from typing import Dict, Any, List
from datetime import datetime
from .compliance_engine import COMPLIANCE_ENGINE
from .violation_logger import VIOLATION_LOGGER


class ComplianceReport:
    """
    Generates end-of-task compliance reports.
    
    Reports include:
    - Overall compliance percentage
    - Violations by principle
    - Violations by severity
    - Recommendations for improvement
    """
    
    def __init__(self):
        self.engine = COMPLIANCE_ENGINE
        self.logger = VIOLATION_LOGGER
    
    def generate(self, task_description: str = None) -> str:
        """
        Generate compliance report for current task.
        
        Args:
            task_description: Brief description of the task (optional)
        
        Returns:
            Formatted compliance report
        """
        # Get engine stats
        compliance_pct = self.engine.get_compliance_percentage() * 100
        checks_performed = self.engine.checks_performed
        checks_passed = self.engine.checks_passed
        checks_failed = self.engine.checks_failed
        
        violations_by_principle = self.engine.get_violations_by_principle()
        violations_by_severity = self.engine.get_violations_by_severity()
        
        # Determine status
        if compliance_pct >= 95:
            status = "🟢 COMPLIANT"
            status_desc = "Excellent compliance with MOTHER principles."
        elif compliance_pct >= 80:
            status = "🟡 MOSTLY COMPLIANT"
            status_desc = "Good compliance, but some violations detected."
        else:
            status = "🔴 NON-COMPLIANT"
            status_desc = "Significant violations detected. Immediate action required."
        
        # Build report
        report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 MOTHER V5 COMPLIANCE REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        if task_description:
            report += f"\n📋 Task: {task_description}\n"
        
        report += f"""
🎯 Overall Compliance: {compliance_pct:.1f}%
📊 Status: {status}
💬 {status_desc}

📈 Checks Summary:
   • Total Performed: {checks_performed}
   • Passed: {checks_passed}
   • Failed: {checks_failed}
"""
        
        # Violations by principle
        if violations_by_principle:
            report += "\n📋 Violations by Principle:\n"
            for principle, count in sorted(violations_by_principle.items()):
                report += f"   • {principle}: {count}\n"
        else:
            report += "\n✅ No principle violations detected.\n"
        
        # Violations by severity
        if violations_by_severity:
            report += "\n⚠️  Violations by Severity:\n"
            blocking = violations_by_severity.get("BLOCKING", 0)
            critical = violations_by_severity.get("CRITICAL", 0)
            warning = violations_by_severity.get("WARNING", 0)
            info = violations_by_severity.get("INFO", 0)
            
            if blocking > 0:
                report += f"   🛑 BLOCKING: {blocking}\n"
            if critical > 0:
                report += f"   ❌ CRITICAL: {critical}\n"
            if warning > 0:
                report += f"   ⚠️  WARNING: {warning}\n"
            if info > 0:
                report += f"   ℹ️  INFO: {info}\n"
        else:
            report += "\n✅ No severity violations detected.\n"
        
        # Recommendations
        recommendations = self._generate_recommendations(
            compliance_pct,
            violations_by_principle,
            violations_by_severity
        )
        
        if recommendations:
            report += "\n💡 Recommendations:\n"
            for i, rec in enumerate(recommendations, 1):
                report += f"   {i}. {rec}\n"
        
        report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        return report
    
    def generate_compact(self) -> str:
        """
        Generate compact compliance report for inline display.
        
        Returns:
            Compact formatted report
        """
        compliance_pct = self.engine.get_compliance_percentage() * 100
        violations = len(self.engine.violations)
        
        if compliance_pct >= 95:
            icon = "🟢"
        elif compliance_pct >= 80:
            icon = "🟡"
        else:
            icon = "🔴"
        
        return f"{icon} Compliance: {compliance_pct:.1f}% | Violations: {violations}"
    
    def _generate_recommendations(
        self,
        compliance_pct: float,
        violations_by_principle: Dict[str, int],
        violations_by_severity: Dict[str, int]
    ) -> List[str]:
        """Generate recommendations based on violations."""
        recommendations = []
        
        # Overall compliance
        if compliance_pct < 95:
            recommendations.append(
                "Review MOTHER principles and ensure all checklists are followed."
            )
        
        # Specific principles
        if violations_by_principle.get("P1", 0) > 0:
            recommendations.append(
                "P1 (Study First): Always research before implementing. Use Anna's Archive for papers."
            )
        
        if violations_by_principle.get("P2", 0) > 0:
            recommendations.append(
                "P2 (Decide Autonomously): Stop asking user to choose. Make decisions autonomously."
            )
        
        if violations_by_principle.get("P3", 0) > 0:
            recommendations.append(
                "P3 (Optimize Cost): Use OpenAI (0.01 credits) before expensive tools."
            )
        
        if violations_by_principle.get("P4", 0) > 0:
            recommendations.append(
                "P4 (Ensure Quality): Validate all outputs with scientific sources and citations."
            )
        
        if violations_by_principle.get("P5", 0) > 0:
            recommendations.append(
                "P5 (Report Accurately): Always include cost report at end of task."
            )
        
        if violations_by_principle.get("P6", 0) > 0:
            recommendations.append(
                "P6 (Learn and Improve): Capture lessons learned and update knowledge base."
            )
        
        if violations_by_principle.get("P7", 0) > 0:
            recommendations.append(
                "P7 (Be Truthful): Never claim completion without actual work. Admit violations."
            )
        
        # Severity-based
        if violations_by_severity.get("BLOCKING", 0) > 0:
            recommendations.append(
                "CRITICAL: BLOCKING violations detected. These must be resolved immediately."
            )
        
        return recommendations


# Global report generator instance
COMPLIANCE_REPORT = ComplianceReport()


def generate_report(task_description: str = None) -> str:
    """Generate compliance report."""
    return COMPLIANCE_REPORT.generate(task_description)


def generate_compact_report() -> str:
    """Generate compact compliance report."""
    return COMPLIANCE_REPORT.generate_compact()
