#!/usr/bin/env python3
"""
Rule Enforcement Engine - Refactored
Loads rules from YAML configuration for centralized management.
"""

import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Tuple, List, Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class RuleViolation:
    """Represents a rule violation"""
    rule_id: str
    rule_name: str
    context: Dict[str, Any]
    reason: str
    timestamp: str

class RuleEngine:
    """Enforces rules based on dynamically loaded configuration."""
    
    def __init__(self, rules_config: Dict[str, Any], base_path: Path):
        """Initializes the RuleEngine with configuration."""
        self.config = rules_config
        self.base_path = base_path
        self.violations_path = self.base_path / "metrics" / "rule_violations.json"
        self.violations: List[RuleViolation] = []
        
    def enforce_rule(self, rule_id: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        """Enforces a single rule by its ID."""
        rule_method = getattr(self, f"rule_{rule_id}", None)
        if not rule_method:
            return (True, f"Rule {rule_id} not implemented.")
        
        try:
            allowed, reason = rule_method(context)
            if not allowed:
                violation = RuleViolation(
                    rule_id=rule_id,
                    rule_name=rule_method.__doc__ or rule_id,
                    context=context,
                    reason=reason,
                    timestamp=datetime.now().isoformat()
                )
                self.violations.append(violation)
                self._save_violations()
            return (allowed, reason)
        except Exception as e:
            return (False, f"Rule {rule_id} execution failed: {e}")

    def _save_violations(self):
        """Saves the list of violations to a JSON file."""
        self.violations_path.parent.mkdir(parents=True, exist_ok=True)
        with self.violations_path.open("w") as f:
            json.dump([asdict(v) for v in self.violations], f, indent=2)

    # --- Rule Implementations ---

    def rule_openai_first(self, context: Dict) -> Tuple[bool, str]:
        """Rule: Always check if OpenAI can do it first."""
        tool = context.get("tool", "")
        task = context.get("task", "")
        action_type = context.get("action_type", "")
        
        routing_rules = self.config.get("routing", {})
        expensive_tools = ["manus_browser", "manus_search", "manus_research"]

        if tool not in expensive_tools:
            return (True, "Not using an expensive Manus tool.")

        if action_type in routing_rules.get("openai_first", []):
            manus_only_keywords = self.config.get("manus_only_keywords", [])
            if not any(kw in task.lower() for kw in manus_only_keywords):
                return (False, f"BLOCKED: OpenAI can handle '{action_type}'. Use OpenAI API instead of {tool}.")
        
        return (True, "Task requires a specific Manus tool.")

    def rule_cost_threshold(self, context: Dict) -> Tuple[bool, str]:
        """Rule: Actions above cost threshold require approval."""
        cost = context.get("cost", 0)
        has_approval = context.get("has_approval", False)
        
        thresholds = self.config.get("thresholds", {})
        critical_threshold = thresholds.get("critical", 100)
        
        if cost <= critical_threshold:
            return (True, f"Cost ({cost}) is within the critical threshold ({critical_threshold}).")
        
        if not has_approval:
            return (False, f"BLOCKED: Cost ({cost}) exceeds critical threshold ({critical_threshold}). Requires user approval.")
        
        return (True, "High cost was approved by the user.")

    def rule_mandatory_init(self, context: Dict) -> Tuple[bool, str]:
        """Rule: Mandatory initialization must complete before actions."""
        initialized = (self.base_path / "state" / "initialized.flag").exists()
        if not initialized:
            return (False, "BLOCKED: System not initialized. The bootstrap process must complete first.")
        return (True, "System is initialized.")

    def enforce_all_rules(self, context: Dict) -> Tuple[bool, List[str]]:
        """Enforces all defined rules."""
        all_rules = self.config.get("active_rules", [
            "openai_first",
            "cost_threshold",
            "mandatory_init"
        ])
        
        failures = []
        for rule_id in all_rules:
            allowed, reason = self.enforce_rule(rule_id, context)
            if not allowed:
                failures.append(f"{rule_id}: {reason}")
        
        return (len(failures) == 0, failures)

if __name__ == "__main__":
    print("="*70)
    print("⚖️  RULE ENFORCEMENT ENGINE - REFACTORED")
    print("="*70)
    
    base_path = Path(__file__).parent.parent
    rules_path = base_path / "rules" / "cost_rules.yaml"
    with rules_path.open("r") as f:
        config = yaml.safe_load(f)

    engine = RuleEngine(config, base_path)
    
    # Test Cases
    test_cases = [
        {
            "name": "OpenAI First - SHOULD BLOCK",
            "rule": "openai_first",
            "context": {"tool": "manus_browser", "task": "Research top 10 companies", "action_type": "research"}
        },
        {
            "name": "OpenAI First - SHOULD ALLOW (Browser Keyword)",
            "rule": "openai_first",
            "context": {"tool": "manus_browser", "task": "Click the login button", "action_type": "research"}
        },
        {
            "name": "Cost Threshold - SHOULD BLOCK",
            "rule": "cost_threshold",
            "context": {"cost": 150, "has_approval": False}
        },
        {
            "name": "Cost Threshold - SHOULD ALLOW",
            "rule": "cost_threshold",
            "context": {"cost": 150, "has_approval": True}
        },
    ]

    for test in test_cases:
        allowed, reason = engine.enforce_rule(test["rule"], test["context"])
        status = "✅ ALLOWED" if allowed else "🚫 BLOCKED"
        print(f"\n{status}: {test['name']}")
        print(f"  Reason: {reason}")

    print("\n✅ Rule engine refactoring test complete!")
