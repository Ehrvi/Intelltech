#!/usr/bin/env python3
"""
MOTHER V5 - Compliance Engine
==============================

Central orchestrator for the MOTHER compliance system.

Responsibilities:
- Initialize and load all enforcers
- Execute pre-action checklists and block on failure
- Trigger post-action audits
- Coordinate with ViolationLogger, Dashboard, and Report

Author: MOTHER V5 Compliance System
Version: 1.0.0
Date: 2026-02-16
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add enforcers to path
sys.path.insert(0, str(Path(__file__).parent / "enforcers"))

from enforcers.base_enforcer import (
    BaseEnforcer,
    ComplianceResult,
    Severity,
    ENFORCER_REGISTRY
)


class ComplianceEngine:
    """
    Central orchestrator for MOTHER compliance system.
    
    Manages the entire compliance lifecycle:
    1. Bootstrap: Initialize all enforcers
    2. Pre-action: Execute checklists and block violations
    3. Post-action: Run audits
    4. End-of-task: Generate compliance report
    """
    
    def __init__(self):
        self.enforcers: Dict[str, BaseEnforcer] = {}
        self.violations: List[Dict[str, Any]] = []
        self.checks_performed: int = 0
        self.checks_passed: int = 0
        self.checks_failed: int = 0
        self.session_start = datetime.now()
        self.initialized = False
    
    def initialize(self) -> bool:
        """
        Initialize the compliance engine.
        
        Loads all enforcers from the registry.
        
        Returns:
            True if initialization successful, False otherwise.
        """
        try:
            # Import all enforcer modules to trigger registration
            from enforcers import p6_learn_improve_enforcer
            from enforcers import p7_truthful_enforcer
            
            # Load enforcers from registry
            self.enforcers = ENFORCER_REGISTRY.get_all()
            
            if not self.enforcers:
                print("⚠️  WARNING: No enforcers registered!")
                return False
            
            print(f"✅ ComplianceEngine initialized with {len(self.enforcers)} enforcers:")
            for principle_id, enforcer in self.enforcers.items():
                print(f"   - {principle_id}: {enforcer.principle_name}")
            
            self.initialized = True
            return True
            
        except Exception as e:
            print(f"❌ ERROR: Failed to initialize ComplianceEngine: {e}")
            return False
    
    def pre_action_check(
        self,
        action_type: str,
        context: Dict[str, Any]
    ) -> ComplianceResult:
        """
        Execute pre-action compliance checks.
        
        This is the BLOCKING gate that prevents actions from executing
        if compliance is not met.
        
        Args:
            action_type: Type of action (e.g., "send_message", "use_tool")
            context: Context for the check
        
        Returns:
            ComplianceResult indicating pass/fail
        """
        if not self.initialized:
            return ComplianceResult(
                passed=False,
                principle="SYSTEM",
                message="ComplianceEngine not initialized",
                severity=Severity.BLOCKING
            )
        
        context["phase"] = "pre_action"
        context["action_type"] = action_type
        
        # Run checks for all enforcers
        results = []
        for principle_id, enforcer in self.enforcers.items():
            result = enforcer.check(context)
            results.append(result)
            self.checks_performed += 1
            
            if result.passed:
                self.checks_passed += 1
            else:
                self.checks_failed += 1
                self._log_violation(result, action_type, context)
        
        # If any BLOCKING violation, return failure
        for result in results:
            if not result.passed and result.severity == Severity.BLOCKING:
                return result
        
        # All checks passed or only warnings
        return ComplianceResult(
            passed=True,
            principle="ALL",
            message=f"Pre-action checks passed ({len(results)} checks)",
            severity=Severity.INFO
        )
    
    def post_action_audit(
        self,
        action_type: str,
        context: Dict[str, Any]
    ) -> ComplianceResult:
        """
        Execute post-action compliance audit.
        
        This catches violations that occurred during action execution.
        
        Args:
            action_type: Type of action that was executed
            context: Context for the audit
        
        Returns:
            ComplianceResult indicating pass/fail
        """
        if not self.initialized:
            return ComplianceResult(
                passed=False,
                principle="SYSTEM",
                message="ComplianceEngine not initialized",
                severity=Severity.CRITICAL
            )
        
        context["phase"] = "post_action"
        context["action_type"] = action_type
        
        # Run audits for all enforcers
        results = []
        for principle_id, enforcer in self.enforcers.items():
            result = enforcer.check(context)
            results.append(result)
            self.checks_performed += 1
            
            if result.passed:
                self.checks_passed += 1
            else:
                self.checks_failed += 1
                self._log_violation(result, action_type, context)
        
        # Return first critical failure, or success
        for result in results:
            if not result.passed and result.severity == Severity.CRITICAL:
                return result
        
        return ComplianceResult(
            passed=True,
            principle="ALL",
            message=f"Post-action audit passed ({len(results)} checks)",
            severity=Severity.INFO
        )
    
    def end_of_task_check(
        self,
        context: Dict[str, Any]
    ) -> ComplianceResult:
        """
        Execute end-of-task compliance checks.
        
        This is the final validation before task completion.
        
        Args:
            context: Context for the check
        
        Returns:
            ComplianceResult indicating pass/fail
        """
        if not self.initialized:
            return ComplianceResult(
                passed=False,
                principle="SYSTEM",
                message="ComplianceEngine not initialized",
                severity=Severity.BLOCKING
            )
        
        context["phase"] = "end_of_task"
        
        # Run checks for all enforcers
        results = []
        for principle_id, enforcer in self.enforcers.items():
            result = enforcer.check(context)
            results.append(result)
            self.checks_performed += 1
            
            if result.passed:
                self.checks_passed += 1
            else:
                self.checks_failed += 1
                self._log_violation(result, "end_of_task", context)
        
        # If any BLOCKING or CRITICAL violation, return failure
        for result in results:
            if not result.passed and result.severity in [Severity.BLOCKING, Severity.CRITICAL]:
                return result
        
        # All checks passed or only warnings
        return ComplianceResult(
            passed=True,
            principle="ALL",
            message=f"End-of-task checks passed ({len(results)} checks)",
            severity=Severity.INFO
        )
    
    def _log_violation(
        self,
        result: ComplianceResult,
        action_type: str,
        context: Dict[str, Any]
    ):
        """Log a compliance violation."""
        violation = {
            "timestamp": datetime.now().isoformat(),
            "principle": result.principle,
            "severity": result.severity.value,
            "message": result.message,
            "action_type": action_type,
            "context": result.context
        }
        self.violations.append(violation)
    
    def get_compliance_percentage(self) -> float:
        """Calculate overall compliance percentage."""
        if self.checks_performed == 0:
            return 1.0  # No checks = 100% (nothing to violate)
        return self.checks_passed / self.checks_performed
    
    def get_violations_by_severity(self) -> Dict[str, int]:
        """Get count of violations by severity."""
        counts = {
            "BLOCKING": 0,
            "CRITICAL": 0,
            "WARNING": 0,
            "INFO": 0
        }
        for violation in self.violations:
            severity = violation["severity"]
            counts[severity] = counts.get(severity, 0) + 1
        return counts
    
    def get_violations_by_principle(self) -> Dict[str, int]:
        """Get count of violations by principle."""
        counts = {}
        for violation in self.violations:
            principle = violation["principle"]
            counts[principle] = counts.get(principle, 0) + 1
        return counts
    
    def generate_summary(self) -> str:
        """Generate a summary of compliance status."""
        compliance_pct = self.get_compliance_percentage() * 100
        violations_by_severity = self.get_violations_by_severity()
        violations_by_principle = self.get_violations_by_principle()
        
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║         MOTHER V5 COMPLIANCE ENGINE - SESSION SUMMARY        ║
╚══════════════════════════════════════════════════════════════╝

📊 Overall Compliance: {compliance_pct:.1f}%

📈 Checks Performed:
   • Total: {self.checks_performed}
   • Passed: {self.checks_passed}
   • Failed: {self.checks_failed}

⚠️  Violations by Severity:
   • BLOCKING: {violations_by_severity['BLOCKING']}
   • CRITICAL: {violations_by_severity['CRITICAL']}
   • WARNING: {violations_by_severity['WARNING']}
   • INFO: {violations_by_severity['INFO']}

📋 Violations by Principle:
"""
        for principle, count in sorted(violations_by_principle.items()):
            summary += f"   • {principle}: {count}\n"
        
        summary += f"\n⏱️  Session Duration: {datetime.now() - self.session_start}\n"
        
        return summary
    
    def __repr__(self):
        return (
            f"<ComplianceEngine "
            f"enforcers={len(self.enforcers)} "
            f"compliance={self.get_compliance_percentage()*100:.1f}% "
            f"violations={len(self.violations)}>"
        )


# Global compliance engine instance
COMPLIANCE_ENGINE = ComplianceEngine()
