"""
MOTHER V5 - Compliance System
==============================

Unified compliance system for all MOTHER principles.

Components:
- ComplianceEngine: Central orchestrator
- Enforcers: P1-P7 principle enforcers
- Checklist: Mandatory pre-action gates
- ViolationLogger: Immutable violation logging
- ComplianceDashboard: Real-time status
- ComplianceReport: End-of-task reports

Usage:
    from mother_v5.compliance import COMPLIANCE_ENGINE
    
    # Initialize
    COMPLIANCE_ENGINE.initialize()
    
    # Pre-action check
    result = COMPLIANCE_ENGINE.pre_action_check("send_message", context)
    if not result.passed:
        print("BLOCKED:", result.message)
        return
    
    # End of task
    result = COMPLIANCE_ENGINE.end_of_task_check(context)
    print(COMPLIANCE_REPORT.generate())
"""

from .compliance_engine import ComplianceEngine, COMPLIANCE_ENGINE
from .checklist import (
    Checklist,
    ChecklistFactory,
    ChecklistPhase,
    ChecklistResult,
    check_before_message,
    check_before_tool,
    check_end_of_task
)
from .violation_logger import ViolationLogger, VIOLATION_LOGGER
from .compliance_dashboard import ComplianceDashboard, COMPLIANCE_DASHBOARD
from .compliance_report import ComplianceReport, COMPLIANCE_REPORT

__all__ = [
    # Engine
    "ComplianceEngine",
    "COMPLIANCE_ENGINE",
    
    # Checklist
    "Checklist",
    "ChecklistFactory",
    "ChecklistPhase",
    "ChecklistResult",
    "check_before_message",
    "check_before_tool",
    "check_end_of_task",
    
    # Logging
    "ViolationLogger",
    "VIOLATION_LOGGER",
    
    # Dashboard
    "ComplianceDashboard",
    "COMPLIANCE_DASHBOARD",
    
    # Report
    "ComplianceReport",
    "COMPLIANCE_REPORT",
]
