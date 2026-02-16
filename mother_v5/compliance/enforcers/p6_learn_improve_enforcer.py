#!/usr/bin/env python3
"""
MOTHER V5 - P6 Enforcer: Always Learn and Improve
==================================================

Enforces P6: Continuously learn from every task and systematically
improve processes, knowledge, and performance.

Author: MOTHER V5 Compliance System
Version: 1.0.0
Date: 2026-02-16
"""

from typing import Dict, Any
from .base_enforcer import BaseEnforcer, ComplianceResult, Severity


class P6LearnImproveEnforcer(BaseEnforcer):
    """
    Enforcer for P6: Always Learn and Improve.
    
    Ensures that:
    - Lessons are captured from every task
    - Knowledge base is updated automatically
    - Patterns in successes/failures are identified
    - Improvements are implemented immediately
    - Improvement is measured over time
    """
    
    def get_principle_id(self) -> str:
        return "P6"
    
    def get_principle_name(self) -> str:
        return "Always Learn and Improve"
    
    def get_target_compliance(self) -> float:
        return 1.0  # 100% compliance
    
    def get_severity(self) -> Severity:
        return Severity.CRITICAL
    
    def check(self, context: Dict[str, Any]) -> ComplianceResult:
        """
        Check P6 compliance.
        
        Expected context:
        {
            "phase": "pre_action" | "post_action" | "end_of_task",
            "task_description": str,
            "lessons_captured": bool,  # For end_of_task
            "knowledge_updated": bool,  # For end_of_task
            "patterns_identified": bool,  # For end_of_task
            "improvements_implemented": bool,  # For end_of_task
        }
        """
        phase = context.get("phase", "unknown")
        
        if phase == "end_of_task":
            return self._check_end_of_task(context)
        elif phase == "pre_action":
            # P6 is primarily checked at end of task
            return self._pass("P6 check deferred to end of task")
        elif phase == "post_action":
            # P6 is primarily checked at end of task
            return self._pass("P6 check deferred to end of task")
        else:
            return self._fail(f"Unknown phase: {phase}")
    
    def _check_end_of_task(self, context: Dict[str, Any]) -> ComplianceResult:
        """Check P6 compliance at end of task."""
        
        # Check 1: Were lessons captured?
        lessons_captured = context.get("lessons_captured", False)
        if not lessons_captured:
            return self._fail(
                "P6 VIOLATION: No lessons captured from this task. "
                "Every task must contribute to learning.",
                context={"missing": "lessons_captured"}
            )
        
        # Check 2: Was knowledge base updated?
        knowledge_updated = context.get("knowledge_updated", False)
        if not knowledge_updated:
            return self._fail(
                "P6 VIOLATION: Knowledge base not updated. "
                "Lessons must be integrated into the knowledge system.",
                context={"missing": "knowledge_updated"}
            )
        
        # Check 3: Were patterns identified?
        patterns_identified = context.get("patterns_identified", False)
        if not patterns_identified:
            return self._fail(
                "P6 VIOLATION: No patterns identified. "
                "Must analyze successes and failures to identify patterns.",
                context={"missing": "patterns_identified"}
            )
        
        # Check 4: Were improvements implemented?
        improvements_implemented = context.get("improvements_implemented", False)
        if not improvements_implemented:
            return self._fail(
                "P6 VIOLATION: No improvements implemented. "
                "Identified patterns must lead to concrete improvements.",
                context={"missing": "improvements_implemented"}
            )
        
        # All checks passed
        return self._pass(
            "P6 COMPLIANT: Task contributed to learning and improvement.",
            context={
                "lessons_captured": True,
                "knowledge_updated": True,
                "patterns_identified": True,
                "improvements_implemented": True
            }
        )


# Register the enforcer
from .base_enforcer import ENFORCER_REGISTRY
ENFORCER_REGISTRY.register(P6LearnImproveEnforcer())
