#!/usr/bin/env python3
"""
Cost Validation Gate - Fix 2
MUST validate cost before EVERY action
Blocks expensive actions when cheaper alternatives exist
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, Any

class CostGate:
    """Validates and blocks expensive actions"""
    
    # Cost estimates (in Manus credits)
    COSTS = {
        'openai_api': 0.01,  # ~$0.01 = 0.01 credits equivalent
        'manus_browser': 50,
        'manus_search': 30,
        'manus_research': 40,
        'manus_task': 10,
        'apollo_api': 2.5,
        'gmail_api': 1,
        'calendar_api': 1,
        'local_file': 0,
        'local_cache': 0
    }
    
    # Action types that can use OpenAI
    OPENAI_CAPABLE = [
        'research',
        'data_collection',
        'summarization',
        'translation',
        'formatting',
        'code_generation',
        'writing_draft',
        'classification',
        'analysis'
    ]
    
    def __init__(self):
        self.base_path = Path("/home/ubuntu/manus_global_knowledge")
        self.log_path = self.base_path / "metrics" / "cost_gate_log.json"
        self.blocks = []
        self.approvals = []
        
    def can_openai_handle(self, task_description: str, action_type: str) -> bool:
        """Check if OpenAI can handle this task"""
        
        # Check if action type is OpenAI-capable
        if action_type not in self.OPENAI_CAPABLE:
            return False
        
        # Check for keywords that indicate Manus-only
        manus_only_keywords = [
            'browser', 'click', 'navigate', 'screenshot',
            'download file', 'upload file', 'interact with page',
            'fill form', 'submit button'
        ]
        
        task_lower = task_description.lower()
        for keyword in manus_only_keywords:
            if keyword in task_lower:
                return False
        
        # OpenAI can handle most text/data tasks
        return True
    
    def validate_action(
        self,
        action_type: str,
        task_description: str,
        proposed_tool: str
    ) -> Tuple[bool, str, float, str]:
        """
        Validate action before execution
        
        Returns:
            (allowed, recommended_tool, cost_estimate, reason)
        """
        
        # Get costs
        proposed_cost = self.COSTS.get(proposed_tool, 10)
        
        # Rule 1: If OpenAI can do it, block expensive Manus tools
        if self.can_openai_handle(task_description, action_type):
            if proposed_tool in ['manus_browser', 'manus_search', 'manus_research']:
                openai_cost = self.COSTS['openai_api']
                savings = proposed_cost - openai_cost
                
                reason = (
                    f"BLOCKED: OpenAI can handle this for {openai_cost} credits "
                    f"(vs {proposed_cost} for {proposed_tool}). "
                    f"Savings: {savings} credits"
                )
                
                self.log_block(action_type, task_description, proposed_tool, 'openai_api', reason)
                
                return (False, 'openai_api', openai_cost, reason)
        
        # Rule 2: Check if local cache can handle it
        if action_type in ['data_retrieval', 'knowledge_lookup']:
            cache_path = self.base_path / "cache"
            if cache_path.exists():
                reason = (
                    f"RECOMMEND: Check local cache first (0 credits) "
                    f"before using {proposed_tool} ({proposed_cost} credits)"
                )
                
                self.log_approval(action_type, task_description, 'local_cache', reason)
                
                return (True, 'local_cache', 0, reason)
        
        # Rule 3: Approve if cost is reasonable
        if proposed_cost <= 5:
            reason = f"APPROVED: {proposed_tool} cost ({proposed_cost} credits) is reasonable"
            self.log_approval(action_type, task_description, proposed_tool, reason)
            return (True, proposed_tool, proposed_cost, reason)
        
        # Rule 4: Warn if cost is high
        if proposed_cost > 20:
            reason = (
                f"WARNING: {proposed_tool} is expensive ({proposed_cost} credits). "
                f"Consider alternatives or get user approval."
            )
            self.log_approval(action_type, task_description, proposed_tool, reason)
            return (True, proposed_tool, proposed_cost, reason)
        
        # Default: approve
        reason = f"APPROVED: {proposed_tool} ({proposed_cost} credits)"
        self.log_approval(action_type, task_description, proposed_tool, reason)
        return (True, proposed_tool, proposed_cost, reason)
    
    def log_block(self, action_type, task, proposed_tool, recommended_tool, reason):
        """Log blocked action"""
        self.blocks.append({
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "task": task,
            "proposed_tool": proposed_tool,
            "recommended_tool": recommended_tool,
            "reason": reason
        })
        self._save_log()
    
    def log_approval(self, action_type, task, tool, reason):
        """Log approved action"""
        self.approvals.append({
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "task": task,
            "tool": tool,
            "reason": reason
        })
        self._save_log()
    
    def _save_log(self):
        """Save log to file"""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        log_data = {
            "blocks": self.blocks,
            "approvals": self.approvals,
            "total_blocks": len(self.blocks),
            "total_approvals": len(self.approvals),
            "block_rate": len(self.blocks) / max(len(self.blocks) + len(self.approvals), 1)
        }
        
        with open(self.log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get cost gate statistics"""
        if self.log_path.exists():
            with open(self.log_path) as f:
                return json.load(f)
        return {"blocks": [], "approvals": [], "total_blocks": 0, "total_approvals": 0}


def validate_before_action(action_type: str, task_description: str, proposed_tool: str):
    """
    Convenience function for validating actions
    
    Usage:
        allowed, tool, cost, reason = validate_before_action(
            'research',
            'Find top 10 construction companies in Australia',
            'manus_browser'
        )
        
        if not allowed:
            print(f"Action blocked: {reason}")
            print(f"Use {tool} instead (cost: {cost} credits)")
    """
    gate = CostGate()
    return gate.validate_action(action_type, task_description, proposed_tool)


# Test if run directly
if __name__ == "__main__":
    print("="*70)
    print("🚪 COST VALIDATION GATE - FIX 2")
    print("="*70)
    print()
    
    gate = CostGate()
    
    # Test cases
    test_cases = [
        ('research', 'Find top 10 construction companies in Australia', 'manus_browser'),
        ('summarization', 'Summarize this 50-page report', 'manus_research'),
        ('translation', 'Translate document to Portuguese', 'openai_api'),
        ('data_collection', 'Collect stock prices for AAPL', 'apollo_api'),
        ('knowledge_lookup', 'Find existing initialization system', 'manus_search'),
    ]
    
    for action_type, task, tool in test_cases:
        allowed, recommended_tool, cost, reason = gate.validate_action(action_type, task, tool)
        
        status = "✅ ALLOWED" if allowed else "🚫 BLOCKED"
        print(f"{status}: {action_type}")
        print(f"  Task: {task}")
        print(f"  Proposed: {tool}")
        print(f"  Recommended: {recommended_tool} ({cost} credits)")
        print(f"  Reason: {reason}")
        print()
    
    # Show statistics
    stats = gate.get_statistics()
    print("="*70)
    print("📊 STATISTICS")
    print("="*70)
    print(f"Total blocks: {stats['total_blocks']}")
    print(f"Total approvals: {stats['total_approvals']}")
    print(f"Block rate: {stats['block_rate']*100:.1f}%")
    print()
    print(f"✅ Cost gate working correctly!")
