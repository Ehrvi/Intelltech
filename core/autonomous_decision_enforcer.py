import logging
"""
Autonomous Decision Enforcement System

This module enforces MANDATORY autonomous decision-making.
Blocks the agent from asking the user to choose when it should decide.

Version: 1.0
Date: 2026-02-16
Priority: CRITICAL
"""

import re
from typing import Tuple, List

class AutonomousDecisionEnforcer:
    """
    Enforces autonomous decision-making by detecting and blocking
    messages that ask the user to choose instead of deciding.
    """
    
    # Patterns that indicate asking user to choose (VIOLATIONS)
    VIOLATION_PATTERNS = [
        r"which\s+(do\s+you\s+)?(prefer|want|choose|like)",
        r"(option|choice)\s+[ABC].*or.*option\s+[ABC]",
        r"should\s+I\s+(use|implement|choose|do)",
        r"do\s+you\s+want\s+(me\s+to|to)",
        r"would\s+you\s+like\s+(me\s+to|to)",
        r"what\s+(would|should)\s+you\s+like",
        r"which\s+(option|approach|method|solution)",
        r"(pick|select|choose)\s+one",
        r"let\s+me\s+know\s+(which|what)\s+you",
        r"tell\s+me\s+(which|what)\s+you",
    ]
    
    # Exceptions (legitimate questions - 0.1% cases)
    EXCEPTION_PATTERNS = [
        r"(brand|color|style|aesthetic|personal\s+preference)",
        r"(strategic\s+direction|business\s+model|major\s+pivot)",
        r"(delete|remove|destroy).*important",
        r"spending.*\$\d{4,}",  # Large amounts ($1000+)
        r"(unclear|ambiguous|contradictory).*intent",
    ]
    
    def __init__(self):
        self.violation_count = 0
        self.decision_count = 0
    
    def check_message(self, message: str) -> Tuple[bool, str, List[str]]:
        """
        Check if message violates autonomous decision-making principle.
        
        Args:
            message: The message to check
            
        Returns:
            Tuple of (is_violation, reason, violations_found)
        """
        message_lower = message.lower()
        
        # Check for exceptions first
        for pattern in self.EXCEPTION_PATTERNS:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return (False, "Exception: Legitimate question", [])
        
        # Check for violations
        violations = []
        for pattern in self.VIOLATION_PATTERNS:
            matches = re.findall(pattern, message_lower, re.IGNORECASE)
            if matches:
                violations.append(f"Pattern: {pattern} | Match: {matches[0]}")
        
        if violations:
            self.violation_count += 1
            reason = f"VIOLATION: Asking user to choose instead of deciding autonomously"
            return (True, reason, violations)
        
        # No violation - good autonomous decision
        self.decision_count += 1
        return (False, "OK: Autonomous decision or legitimate question", [])
    
    def get_correction_message(self, violations: List[str]) -> str:
        """
        Generate correction message when violation is detected.
        
        Args:
            violations: List of violations found
            
        Returns:
            Correction message
        """
        msg = "\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += "🚫 AUTONOMOUS DECISION ENFORCEMENT - VIOLATION DETECTED\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "**CRITICAL FAILURE:** You are asking the user to choose instead of deciding autonomously.\n\n"
        msg += "**Violations Found:**\n"
        for v in violations:
            msg += f"  • {v}\n"
        msg += "\n"
        msg += "**MANDATORY ACTION:**\n"
        msg += "1. STOP asking user to choose\n"
        msg += "2. ANALYZE all options yourself\n"
        msg += "3. CHOOSE the best option\n"
        msg += "4. EXPLAIN your decision\n"
        msg += "5. PROCEED with implementation\n\n"
        msg += "**Remember:** \"Don't ask, decide. Then explain why.\"\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        return msg
    
    def get_stats(self) -> dict:
        """Get enforcement statistics"""
        total = self.violation_count + self.decision_count
        compliance_rate = (self.decision_count / total * 100) if total > 0 else 0
        
        return {
            'total_checks': total,
            'violations': self.violation_count,
            'autonomous_decisions': self.decision_count,
            'compliance_rate': compliance_rate,
            'target_rate': 99.9,
            'status': 'PASS' if compliance_rate >= 99.0 else 'FAIL'
        }


def check_before_sending(message: str) -> Tuple[bool, str]:
    """
    Convenience function to check message before sending to user.
    
    Args:
        message: The message to check
        
    Returns:
        Tuple of (is_ok_to_send, feedback_message)
    """
    enforcer = AutonomousDecisionEnforcer()
    is_violation, reason, violations = enforcer.check_message(message)
    
    if is_violation:
        correction = enforcer.get_correction_message(violations)
        return (False, correction)
    
    return (True, "✅ Message OK - Autonomous decision or legitimate question")


# Example usage
if __name__ == "__main__":
    enforcer = AutonomousDecisionEnforcer()
    
    # Test cases
    test_messages = [
        # VIOLATIONS
        "Which option do you prefer: A, B, or C?",
        "Should I use OpenAI or Manus search?",
        "Do you want me to implement this now?",
        "Let me know which approach you'd like.",
        
        # OK (Autonomous decisions)
        "I'm implementing Option A because it's the best choice.",
        "Using OpenAI for this task (99.9% cheaper than search).",
        "Starting implementation now based on analysis.",
        
        # OK (Legitimate questions - exceptions)
        "What color would you like for the brand logo?",
        "This will delete 10,000 important records. Confirm?",
        "Your requirements are contradictory. Please clarify.",
    ]
    
    print("Testing Autonomous Decision Enforcement:\n")
    for msg in test_messages:
        is_violation, reason, violations = enforcer.check_message(msg)
        status = "❌ VIOLATION" if is_violation else "✅ OK"
        print(f"{status}: {msg[:50]}...")
        if violations:
            print(f"  Reason: {reason}")
            for v in violations:
                print(f"    - {v}")
        print()
    
    # Show stats
    stats = enforcer.get_stats()
    print("\n" + "="*70)
    print("ENFORCEMENT STATISTICS")
    print("="*70)
    print(f"Total Checks: {stats['total_checks']}")
    print(f"Violations: {stats['violations']}")
    print(f"Autonomous Decisions: {stats['autonomous_decisions']}")
    print(f"Compliance Rate: {stats['compliance_rate']:.1f}%")
    print(f"Target Rate: {stats['target_rate']}%")
    print(f"Status: {stats['status']}")
    print("="*70)
