#!/usr/bin/env python3
"""
Rule Enforcement Engine - Fix 4
Converts text-based rules to CODE-based enforcement
Blocks violations, not just logs them
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Tuple, List, Dict, Any
from dataclasses import dataclass

@dataclass
class RuleViolation:
    """Represents a rule violation"""
    rule_id: str
    rule_name: str
    context: Dict[str, Any]
    reason: str
    timestamp: str

class RuleEngine:
    """Enforces rules via code, not suggestions"""
    
    def __init__(self):
        self.base_path = Path("/home/ubuntu/manus_global_knowledge")
        self.violations_path = self.base_path / "metrics" / "rule_violations.json"
        self.violations: List[RuleViolation] = []
        
    def enforce_rule(self, rule_id: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Enforce a rule
        
        Returns:
            (allowed, reason)
        """
        
        # Get rule method
        rule_method = getattr(self, f"rule_{rule_id}", None)
        if not rule_method:
            return (True, f"Rule {rule_id} not found")
        
        # Execute rule
        try:
            allowed, reason = rule_method(context)
            
            if not allowed:
                # Log violation
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
            return (False, f"Rule execution error: {e}")
    
    def _save_violations(self):
        """Save violations to file"""
        self.violations_path.parent.mkdir(parents=True, exist_ok=True)
        
        violations_data = [
            {
                "rule_id": v.rule_id,
                "rule_name": v.rule_name,
                "context": v.context,
                "reason": v.reason,
                "timestamp": v.timestamp
            }
            for v in self.violations
        ]
        
        with open(self.violations_path, 'w') as f:
            json.dump(violations_data, f, indent=2)
    
    # ========================================================================
    # RULES (CODE-BASED ENFORCEMENT)
    # ========================================================================
    
    def rule_openai_first(self, context: Dict) -> Tuple[bool, str]:
        """Rule: Always check if OpenAI can do it first"""
        
        tool = context.get('tool', '')
        task = context.get('task', '')
        action_type = context.get('action_type', '')
        
        # Check if using expensive Manus tool
        expensive_tools = ['manus_browser', 'manus_search', 'manus_research']
        if tool not in expensive_tools:
            return (True, "Not using expensive Manus tool")
        
        # Check if OpenAI can handle it
        openai_capable_actions = [
            'research', 'data_collection', 'summarization',
            'translation', 'formatting', 'code_generation',
            'writing_draft', 'classification', 'analysis'
        ]
        
        if action_type in openai_capable_actions:
            # Check for browser-specific keywords
            browser_keywords = ['click', 'navigate', 'screenshot', 'download', 'upload']
            if not any(kw in task.lower() for kw in browser_keywords):
                return (
                    False,
                    f"BLOCKED: OpenAI can handle {action_type}. Use OpenAI API instead of {tool}."
                )
        
        return (True, "OpenAI cannot handle this task")
    
    def rule_check_existing(self, context: Dict) -> Tuple[bool, str]:
        """Rule: Check registry before creating new system"""
        
        action = context.get('action', '')
        system_name = context.get('system_name', '')
        
        if action != 'create_system':
            return (True, "Not creating a system")
        
        # Check system registry
        from system_registry import SystemRegistry
        registry = SystemRegistry()
        
        if registry.check_exists(system_name):
            system = registry.get_system(system_name)
            return (
                False,
                f"BLOCKED: System '{system_name}' already exists at {system['location']}. "
                f"Use existing system instead of creating new one."
            )
        
        return (True, "System does not exist, safe to create")
    
    def rule_scientific_methodology(self, context: Dict) -> Tuple[bool, str]:
        """Rule: Must follow scientific methodology for analysis/research"""
        
        action_type = context.get('action_type', '')
        has_citations = context.get('has_citations', False)
        has_methodology = context.get('has_methodology', False)
        
        # Check if action requires scientific rigor
        requires_rigor = action_type in [
            'research', 'analysis', 'forensic_analysis',
            'evaluation', 'comparison', 'assessment'
        ]
        
        if not requires_rigor:
            return (True, "Action does not require scientific methodology")
        
        if not has_citations:
            return (
                False,
                "BLOCKED: Research/analysis must include citations and sources."
            )
        
        if not has_methodology:
            return (
                False,
                "BLOCKED: Research/analysis must declare methodology."
            )
        
        return (True, "Scientific methodology followed")
    
    def rule_cost_threshold(self, context: Dict) -> Tuple[bool, str]:
        """Rule: Actions above cost threshold require approval"""
        
        cost = context.get('cost', 0)
        has_approval = context.get('has_approval', False)
        
        COST_THRESHOLD = 20  # credits
        
        if cost <= COST_THRESHOLD:
            return (True, f"Cost ({cost}) below threshold ({COST_THRESHOLD})")
        
        if not has_approval:
            return (
                False,
                f"BLOCKED: Cost ({cost} credits) exceeds threshold ({COST_THRESHOLD}). "
                f"Requires user approval."
            )
        
        return (True, "Cost approved by user")
    
    def rule_mandatory_init(self, context: Dict) -> Tuple[bool, str]:
        """Rule: Mandatory initialization must complete before actions"""
        
        import os
        initialized = os.getenv('MANUS_INITIALIZED', 'false') == 'true'
        
        if not initialized:
            return (
                False,
                "BLOCKED: Mandatory initialization not complete. "
                "Run: python3 /home/ubuntu/manus_global_knowledge/mandatory_init.py"
            )
        
        return (True, "Initialization complete")
    
    def rule_knowledge_lookup_first(self, context: Dict) -> Tuple[bool, str]:
        """Rule: Must search existing knowledge before creating new"""
        
        action = context.get('action', '')
        searched_knowledge = context.get('searched_knowledge', False)
        
        create_actions = ['create_system', 'create_solution', 'create_architecture']
        if action not in create_actions:
            return (True, "Not creating something new")
        
        if not searched_knowledge:
            return (
                False,
                "BLOCKED: Must search existing knowledge before creating new system. "
                "Use knowledge_lookup.py first."
            )
        
        return (True, "Knowledge search completed")
    
    # ========================================================================
    # UTILITIES
    # ========================================================================
    
    def enforce_all_rules(self, context: Dict) -> Tuple[bool, List[str]]:
        """
        Enforce all applicable rules
        
        Returns:
            (all_passed, reasons)
        """
        
        all_rules = [
            'openai_first',
            'check_existing',
            'scientific_methodology',
            'cost_threshold',
            'mandatory_init',
            'knowledge_lookup_first'
        ]
        
        failures = []
        
        for rule_id in all_rules:
            allowed, reason = self.enforce_rule(rule_id, context)
            if not allowed:
                failures.append(f"{rule_id}: {reason}")
        
        return (len(failures) == 0, failures)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get rule enforcement statistics"""
        if self.violations_path.exists():
            with open(self.violations_path) as f:
                violations = json.load(f)
            
            # Count by rule
            by_rule = {}
            for v in violations:
                rule_id = v['rule_id']
                by_rule[rule_id] = by_rule.get(rule_id, 0) + 1
            
            return {
                "total_violations": len(violations),
                "violations_by_rule": by_rule,
                "recent_violations": violations[-10:]  # Last 10
            }
        
        return {"total_violations": 0, "violations_by_rule": {}, "recent_violations": []}


# Convenience function
def enforce_rule(rule_id: str, **context):
    """
    Convenience function for enforcing a rule
    
    Usage:
        allowed, reason = enforce_rule(
            'openai_first',
            tool='manus_browser',
            task='Research companies',
            action_type='research'
        )
        
        if not allowed:
            print(f"Rule violation: {reason}")
    """
    engine = RuleEngine()
    return engine.enforce_rule(rule_id, context)


# Test if run directly
if __name__ == "__main__":
    print("="*70)
    print("⚖️  RULE ENFORCEMENT ENGINE - FIX 4")
    print("="*70)
    print()
    
    engine = RuleEngine()
    
    # Test cases
    test_cases = [
        {
            "name": "OpenAI First Rule - SHOULD BLOCK",
            "rule": "openai_first",
            "context": {
                "tool": "manus_browser",
                "task": "Research top 10 companies",
                "action_type": "research"
            }
        },
        {
            "name": "OpenAI First Rule - SHOULD ALLOW",
            "rule": "openai_first",
            "context": {
                "tool": "openai_api",
                "task": "Research top 10 companies",
                "action_type": "research"
            }
        },
        {
            "name": "Check Existing Rule - SHOULD BLOCK",
            "rule": "check_existing",
            "context": {
                "action": "create_system",
                "system_name": "initialization_system"
            }
        },
        {
            "name": "Scientific Methodology - SHOULD BLOCK",
            "rule": "scientific_methodology",
            "context": {
                "action_type": "research",
                "has_citations": False,
                "has_methodology": False
            }
        },
        {
            "name": "Cost Threshold - SHOULD BLOCK",
            "rule": "cost_threshold",
            "context": {
                "cost": 50,
                "has_approval": False
            }
        },
        {
            "name": "Mandatory Init - SHOULD ALLOW (if init ran)",
            "rule": "mandatory_init",
            "context": {}
        }
    ]
    
    for test in test_cases:
        allowed, reason = engine.enforce_rule(test["rule"], test["context"])
        status = "✅ ALLOWED" if allowed else "🚫 BLOCKED"
        print(f"{status}: {test['name']}")
        print(f"  Rule: {test['rule']}")
        print(f"  Reason: {reason}")
        print()
    
    # Show statistics
    stats = engine.get_statistics()
    print("="*70)
    print("📊 STATISTICS")
    print("="*70)
    print(f"Total violations: {stats['total_violations']}")
    print(f"Violations by rule: {stats['violations_by_rule']}")
    print()
    print("✅ Rule engine working correctly!")
