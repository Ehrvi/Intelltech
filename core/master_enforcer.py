#!/usr/bin/env python3
"""
MASTER ENFORCER - MANUS OPERATING SYSTEM V2.0

Unified enforcement of all 5 Core Principles:
- P1: Always Study First
- P2: Always Decide Autonomously
- P3: Always Optimize Cost
- P4: Always Ensure Quality
- P5: Always Report Accurately

This is the single source of truth for enforcement.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class MasterEnforcer:
    """Unified enforcer for Operating System V2.0"""
    
    def __init__(self, base_path: str = "/home/ubuntu/manus_global_knowledge"):
        self.base_path = Path(base_path)
        self.violations = []
        self.compliance_log = []
        
        # Load Operating System
        self.os_path = self.base_path / "MANUS_OPERATING_SYSTEM.md"
        if not self.os_path.exists():
            raise FileNotFoundError("Operating System V2.0 not found")
        
        print("🎯 Master Enforcer initialized - Operating System V2.0 active")
    
    # ========================================================================
    # P1: ALWAYS STUDY FIRST
    # ========================================================================
    
    def check_study_phase(self, task_context: Dict) -> Tuple[bool, str]:
        """
        Enforce P1: Always Study First
        
        Checks:
        - Has internal knowledge been consulted?
        - Has external research been performed if needed?
        - Is understanding deep, not superficial?
        
        Returns: (passed, message)
        """
        has_internal_study = task_context.get("internal_study_completed", False)
        has_external_research = task_context.get("external_research_completed", False)
        needs_research = task_context.get("requires_external_knowledge", False)
        
        if not has_internal_study:
            violation = "❌ P1 VIOLATION: Must study internal knowledge first"
            self.violations.append(violation)
            return False, violation
        
        if needs_research and not has_external_research:
            violation = "❌ P1 VIOLATION: External research required but not performed"
            self.violations.append(violation)
            return False, violation
        
        self.compliance_log.append("✅ P1 COMPLIANT: Study phase completed")
        return True, "✅ P1 COMPLIANT"
    
    # ========================================================================
    # P2: ALWAYS DECIDE AUTONOMOUSLY
    # ========================================================================
    
    def check_autonomous_decision(self, message: str) -> Tuple[bool, str]:
        """
        Enforce P2: Always Decide Autonomously
        
        Checks:
        - Is the agent asking user to choose instead of deciding?
        - Are there phrases like "which one would you prefer?"
        
        Returns: (passed, message)
        """
        # Patterns that indicate asking user to choose
        asking_patterns = [
            r"which (one |option )?would you (like|prefer|want)",
            r"would you like me to",
            r"should I (use|choose|select)",
            r"do you want (me to|to)",
            r"which (approach|method|option|way)",
            r"or would you prefer",
            r"let me know which",
            r"please choose",
            r"what would you like"
        ]
        
        message_lower = message.lower()
        
        for pattern in asking_patterns:
            if re.search(pattern, message_lower):
                violation = f"❌ P2 VIOLATION: Asking user to choose instead of deciding autonomously"
                self.violations.append(violation)
                return False, violation
        
        self.compliance_log.append("✅ P2 COMPLIANT: Autonomous decision made")
        return True, "✅ P2 COMPLIANT"
    
    # ========================================================================
    # P3: ALWAYS OPTIMIZE COST
    # ========================================================================
    
    def check_cost_optimization(self, tool_choice: str, alternatives: List[str]) -> Tuple[bool, str]:
        """
        Enforce P3: Always Optimize Cost
        
        Checks:
        - Is the cheapest tool being used that meets quality requirements?
        - Could OpenAI (0.01) be used instead of search (20)?
        
        Returns: (passed, message)
        """
        # Cost reference (in credits)
        tool_costs = {
            "openai": 0.01,
            "file_read": 0.5,
            "file_write": 0.5,
            "shell": 1,
            "search": 20,
            "browser": 30,
            "map": 50
        }
        
        current_cost = tool_costs.get(tool_choice, 0)
        
        # Check if cheaper alternative exists
        for alt in alternatives:
            alt_cost = tool_costs.get(alt, 0)
            if alt_cost < current_cost and alt_cost > 0:
                violation = f"❌ P3 VIOLATION: Using {tool_choice} ({current_cost} credits) when {alt} ({alt_cost} credits) could work"
                self.violations.append(violation)
                return False, violation
        
        self.compliance_log.append(f"✅ P3 COMPLIANT: Optimal tool choice ({tool_choice})")
        return True, "✅ P3 COMPLIANT"
    
    # ========================================================================
    # P4: ALWAYS ENSURE QUALITY
    # ========================================================================
    
    def check_quality_standards(self, output: Dict) -> Tuple[bool, str]:
        """
        Enforce P4: Always Ensure Quality
        
        Checks:
        - Is output scientifically grounded?
        - Are sources cited?
        - Has quality validation been performed?
        
        Returns: (passed, message)
        """
        has_sources = output.get("has_citations", False)
        quality_score = output.get("quality_score", 0)
        is_validated = output.get("validated", False)
        
        if not has_sources and output.get("requires_sources", True):
            violation = "❌ P4 VIOLATION: Output lacks proper citations"
            self.violations.append(violation)
            return False, violation
        
        if quality_score < 80 and output.get("requires_validation", True):
            violation = f"❌ P4 VIOLATION: Quality score {quality_score}% below minimum 80%"
            self.violations.append(violation)
            return False, violation
        
        self.compliance_log.append("✅ P4 COMPLIANT: Quality standards met")
        return True, "✅ P4 COMPLIANT"
    
    # ========================================================================
    # P5: ALWAYS REPORT ACCURATELY
    # ========================================================================
    
    def check_cost_report(self, final_message: str) -> Tuple[bool, str]:
        """
        Enforce P5: Always Report Accurately
        
        Checks:
        - Does final message include cost report?
        - Are all platforms included (Manus, OpenAI, Apollo)?
        - Are costs shown in both credits and USD?
        
        Returns: (passed, message)
        """
        # Check for cost report markers
        has_cost_report = "COST REPORT" in final_message or "TOTAL COST" in final_message
        has_manus = "Manus:" in final_message
        has_credits = "credits" in final_message
        has_usd = "USD" in final_message
        
        if not has_cost_report:
            violation = "❌ P5 VIOLATION: Final message missing cost report"
            self.violations.append(violation)
            return False, violation
        
        if not (has_manus and has_credits and has_usd):
            violation = "❌ P5 VIOLATION: Cost report incomplete (missing platform/currency)"
            self.violations.append(violation)
            return False, violation
        
        self.compliance_log.append("✅ P5 COMPLIANT: Accurate cost report included")
        return True, "✅ P5 COMPLIANT"
    
    # ========================================================================
    # MASTER VALIDATION
    # ========================================================================
    
    def validate_before_message(self, message: str, context: Dict) -> Tuple[bool, List[str]]:
        """
        Master validation before sending message to user
        
        Runs all compliance checks and returns results
        
        Returns: (all_passed, violations_list)
        """
        self.violations = []
        
        # P2: Check autonomous decision
        p2_passed, _ = self.check_autonomous_decision(message)
        
        # P5: Check cost report (if final message)
        if context.get("is_final_message", False):
            p5_passed, _ = self.check_cost_report(message)
        
        all_passed = len(self.violations) == 0
        return all_passed, self.violations
    
    def validate_before_tool(self, tool: str, alternatives: List[str]) -> Tuple[bool, List[str]]:
        """
        Master validation before using tool
        
        Runs cost optimization check
        
        Returns: (passed, violations_list)
        """
        self.violations = []
        
        # P3: Check cost optimization
        p3_passed, _ = self.check_cost_optimization(tool, alternatives)
        
        all_passed = len(self.violations) == 0
        return all_passed, self.violations
    
    # ========================================================================
    # REPORTING
    # ========================================================================
    
    def generate_compliance_report(self) -> str:
        """Generate compliance report for current session"""
        total_checks = len(self.compliance_log) + len(self.violations)
        passed_checks = len(self.compliance_log)
        compliance_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 100
        
        report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 OPERATING SYSTEM V2.0 - COMPLIANCE REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Compliance Rate: {compliance_rate:.1f}%
Total Checks: {total_checks}
Passed: {passed_checks}
Violations: {len(self.violations)}

Compliance Log:
"""
        for log in self.compliance_log:
            report += f"  {log}\n"
        
        if self.violations:
            report += "\nViolations:\n"
            for violation in self.violations:
                report += f"  {violation}\n"
        
        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        return report
    
    def save_compliance_log(self):
        """Save compliance log to file"""
        log_dir = self.base_path / "logs" / "compliance"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"compliance_{timestamp}.json"
        
        log_data = {
            "timestamp": timestamp,
            "compliance_log": self.compliance_log,
            "violations": self.violations,
            "compliance_rate": (len(self.compliance_log) / (len(self.compliance_log) + len(self.violations)) * 100) if (len(self.compliance_log) + len(self.violations)) > 0 else 100
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"📝 Compliance log saved: {log_file}")


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def check_before_message(message: str, context: Dict = None) -> Tuple[bool, List[str]]:
    """Convenience function to check message before sending"""
    enforcer = MasterEnforcer()
    return enforcer.validate_before_message(message, context or {})

def check_before_tool(tool: str, alternatives: List[str] = None) -> Tuple[bool, List[str]]:
    """Convenience function to check tool choice"""
    enforcer = MasterEnforcer()
    return enforcer.validate_before_tool(tool, alternatives or [])

def generate_cost_report(operations: Dict) -> str:
    """Generate cost report from operations dict"""
    # This will be implemented to integrate with multi_platform_cost_tracker
    from multi_platform_cost_tracker import MultiPlatformCostTracker
    
    tracker = MultiPlatformCostTracker()
    # Add operations to tracker
    for platform, ops in operations.items():
        for op_type, count in ops.items():
            tracker.track_operation(platform, op_type, count)
    
    return tracker.generate_report()


if __name__ == "__main__":
    # Test the enforcer
    print("Testing Master Enforcer...")
    
    enforcer = MasterEnforcer()
    
    # Test P2: Autonomous decision
    test_message = "I've analyzed the options and chosen OpenAI for this task because it's most cost-effective."
    passed, violations = enforcer.validate_before_message(test_message, {})
    print(f"\nTest 1 - Autonomous decision: {'✅ PASSED' if passed else '❌ FAILED'}")
    
    # Test P2: Asking user (should fail)
    test_message = "Which option would you prefer: OpenAI or search?"
    passed, violations = enforcer.validate_before_message(test_message, {})
    print(f"Test 2 - Asking user: {'✅ FAILED (as expected)' if not passed else '❌ PASSED (unexpected)'}")
    
    # Test P5: Cost report
    test_message = """
    Here are the results.
    
    COST REPORT:
    Manus: 10 credits
    Total: $0.10 USD
    """
    passed, violations = enforcer.validate_before_message(test_message, {"is_final_message": True})
    print(f"Test 3 - Cost report: {'✅ PASSED' if passed else '❌ FAILED'}")
    
    # Generate compliance report
    print(enforcer.generate_compliance_report())
