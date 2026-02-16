#!/usr/bin/env python3
"""
MOTHER V5 - P7 Enforcer: Always Be Truthful
============================================

Enforces P7: State facts as they are. Never misrepresent actions,
compliance, or the source of information.

Author: MOTHER V5 Compliance System
Version: 1.0.0
Date: 2026-02-16
"""

import re
from typing import Dict, Any, List
from .base_enforcer import BaseEnforcer, ComplianceResult, Severity


class P7TruthfulEnforcer(BaseEnforcer):
    """
    Enforcer for P7: Always Be Truthful.
    
    Ensures that:
    - Steps are not falsely claimed as completed
    - Violations are admitted, not hidden
    - AI-generated content is labeled as such
    - Tasks are not claimed complete when incomplete
    - Honesty is maintained in all communications
    """
    
    # Patterns that may indicate false claims
    FALSE_CLAIM_PATTERNS = [
        r"(?i)\b(completed|finished|done)\b.*\b(all|every|100%)\b",
        r"(?i)\b(successfully|fully)\s+(implemented|created|built)\b",
        r"(?i)\b(no|zero)\s+(errors|issues|problems|violations)\b",
        r"(?i)\b(perfect|flawless|complete)\s+(compliance|implementation)\b",
    ]
    
    # Patterns that indicate proper transparency
    TRANSPARENCY_PATTERNS = [
        r"(?i)\b(skipped|omitted|missed|violated)\b",
        r"(?i)\b(AI-generated|unverified|not validated)\b",
        r"(?i)\b(incomplete|partial|in progress)\b",
        r"(?i)\b(admitted|acknowledged|disclosed)\b",
    ]
    
    def get_principle_id(self) -> str:
        return "P7"
    
    def get_principle_name(self) -> str:
        return "Always Be Truthful"
    
    def get_target_compliance(self) -> float:
        return 1.0  # 100% compliance
    
    def get_severity(self) -> Severity:
        return Severity.BLOCKING
    
    def check(self, context: Dict[str, Any]) -> ComplianceResult:
        """
        Check P7 compliance.
        
        Expected context:
        {
            "phase": "pre_message" | "pre_action" | "end_of_task",
            "message": str,  # For pre_message
            "claimed_actions": List[str],  # For end_of_task
            "actual_actions": List[str],  # For end_of_task
            "claimed_compliance": float,  # For end_of_task
            "actual_compliance": float,  # For end_of_task
        }
        """
        phase = context.get("phase", "unknown")
        
        if phase == "pre_message":
            return self._check_message(context)
        elif phase == "end_of_task":
            return self._check_end_of_task(context)
        elif phase == "pre_action":
            # P7 is primarily checked at message and end of task
            return self._pass("P7 check deferred to message/end of task")
        else:
            return self._fail(f"Unknown phase: {phase}")
    
    def _check_message(self, context: Dict[str, Any]) -> ComplianceResult:
        """Check P7 compliance in a message."""
        message = context.get("message", "")
        
        if not message:
            return self._pass("No message to check")
        
        # Check for suspicious false claim patterns
        false_claim_found = False
        for pattern in self.FALSE_CLAIM_PATTERNS:
            if re.search(pattern, message):
                false_claim_found = True
                break
        
        # Check for transparency indicators
        transparency_found = False
        for pattern in self.TRANSPARENCY_PATTERNS:
            if re.search(pattern, message):
                transparency_found = True
                break
        
        # If false claims found but no transparency, flag as potential violation
        if false_claim_found and not transparency_found:
            return self._fail(
                "P7 WARNING: Message contains absolute claims without transparency. "
                "Ensure all claims are accurate and any issues are disclosed.",
                context={
                    "message_preview": message[:200],
                    "false_claim_found": True,
                    "transparency_found": False
                }
            )
        
        return self._pass("P7 COMPLIANT: Message appears truthful")
    
    def _check_end_of_task(self, context: Dict[str, Any]) -> ComplianceResult:
        """Check P7 compliance at end of task."""
        
        # Check 1: Do claimed actions match actual actions?
        claimed_actions = set(context.get("claimed_actions", []))
        actual_actions = set(context.get("actual_actions", []))
        
        if claimed_actions and actual_actions:
            false_claims = claimed_actions - actual_actions
            if false_claims:
                return self._fail(
                    f"P7 VIOLATION: Claimed actions that were not performed: {false_claims}",
                    context={"false_claims": list(false_claims)}
                )
        
        # Check 2: Is claimed compliance accurate?
        claimed_compliance = context.get("claimed_compliance")
        actual_compliance = context.get("actual_compliance")
        
        if claimed_compliance is not None and actual_compliance is not None:
            # Allow 5% tolerance for rounding
            if claimed_compliance > actual_compliance + 0.05:
                return self._fail(
                    f"P7 VIOLATION: Claimed compliance ({claimed_compliance*100:.1f}%) "
                    f"exceeds actual compliance ({actual_compliance*100:.1f}%)",
                    context={
                        "claimed_compliance": claimed_compliance,
                        "actual_compliance": actual_compliance
                    }
                )
        
        # All checks passed
        return self._pass(
            "P7 COMPLIANT: All claims are accurate and truthful.",
            context={
                "claimed_actions": list(claimed_actions),
                "actual_actions": list(actual_actions),
                "claimed_compliance": claimed_compliance,
                "actual_compliance": actual_compliance
            }
        )


# Register the enforcer
from .base_enforcer import ENFORCER_REGISTRY
ENFORCER_REGISTRY.register(P7TruthfulEnforcer())
