#!/usr/bin/env python3
"""
Cost Validation Gate - Refactored
Loads all rules from YAML configuration, removing hardcoded values.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, Any, Optional

class CostGate:
    """Validates actions based on dynamically loaded cost rules."""

    def __init__(self, rules: Dict[str, Any], base_path: Path):
        """Initialize the CostGate with configuration.

        Args:
            rules: A dictionary containing the cost rules configuration.
            base_path: The base path of the knowledge system for logging.
        """
        self.config = rules
        self.base_path = base_path
        self.log_path = self.base_path / "metrics" / "cost_gate_log.json"
        self.blocks = []
        self.approvals = []

    def can_openai_handle(self, action_type: str, task_description: str) -> bool:
        """Check if OpenAI can handle this task based on routing rules."""
        routing_rules = self.config.get("routing", {})
        
        # If the action is explicitly Manus-only, OpenAI cannot handle it.
        if action_type in routing_rules.get("manus_only", []):
            return False

        # If the action is a candidate for OpenAI, it can handle it.
        if action_type in routing_rules.get("openai_first", []):
            return True

        # Check for keywords that indicate Manus-only browser tasks
        manus_only_keywords = self.config.get("manus_only_keywords", [
            'browser', 'click', 'navigate', 'screenshot',
            'download file', 'upload file', 'interact with page',
            'fill form', 'submit button'
        ])
        
        task_lower = task_description.lower()
        if any(keyword in task_lower for keyword in manus_only_keywords):
            return False
        
        # Default to true if not explicitly defined, allows for flexibility
        return True

    def validate_action(
        self,
        action_type: str,
        task_description: str,
        proposed_tool: str,
        cost_estimate: float
    ) -> Tuple[bool, str, float, str]:
        """Validate action before execution based on loaded rules.

        Returns:
            (allowed, recommended_tool, final_cost, reason)
        """
        cost_multipliers = self.config.get("cost_multiplier", {})
        thresholds = self.config.get("thresholds", {})
        blocking_rules = self.config.get("blocking", {})

        proposed_cost = cost_estimate * cost_multipliers.get(proposed_tool, 1.0)

        # Rule 1: If OpenAI can do it, block expensive Manus tools
        if blocking_rules.get("block_if_cheaper_exists", True) and self.can_openai_handle(action_type, task_description):
            if proposed_tool in ["manus_browser", "manus_search", "manus_research"]:
                openai_cost = cost_multipliers.get("openai", 0.0001)
                if proposed_cost > openai_cost:
                    savings = proposed_cost - openai_cost
                    reason = f"BLOCKED: OpenAI can handle this for ~{openai_cost:.4f} credits (vs {proposed_cost} for {proposed_tool}). Savings: {savings:.2f} credits"
                    self.log_block(action_type, task_description, proposed_tool, "openai", reason)
                    return (False, "openai", openai_cost, reason)

        # Rule 2: Check for high-cost actions that require justification
        critical_threshold = thresholds.get("critical", 100)
        if blocking_rules.get("require_justification_above") and proposed_cost > critical_threshold:
            reason = f"BLOCKED: Action cost ({proposed_cost}) exceeds critical threshold ({critical_threshold}). Requires explicit user approval."
            self.log_block(action_type, task_description, proposed_tool, proposed_tool, reason)
            return (False, proposed_tool, proposed_cost, reason)

        # Default: Approve the action
        reason = f"APPROVED: {proposed_tool} cost ({proposed_cost:.4f} credits) is within acceptable limits."
        self.log_approval(action_type, task_description, proposed_tool, reason)
        return (True, proposed_tool, proposed_cost, reason)

    def log_block(self, action_type, task, proposed_tool, recommended_tool, reason):
        self._log_entry("blocks", {
            "action_type": action_type,
            "task": task,
            "proposed_tool": proposed_tool,
            "recommended_tool": recommended_tool,
            "reason": reason
        })

    def log_approval(self, action_type, task, tool, reason):
        self._log_entry("approvals", {
            "action_type": action_type,
            "task": task,
            "tool": tool,
            "reason": reason
        })

    def _log_entry(self, log_type: str, data: Dict[str, Any]):
        """Log an entry for a blocked or approved action."""
        entry = {"timestamp": datetime.now().isoformat(), **data}
        getattr(self, log_type).append(entry)
        self._save_log()

    def _save_log(self):
        """Save the current logs to a file."""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        log_data = {
            "blocks": self.blocks,
            "approvals": self.approvals,
            "total_blocks": len(self.blocks),
            "total_approvals": len(self.approvals),
            "block_rate": len(self.blocks) / max(len(self.blocks) + len(self.approvals), 1)
        }
        with self.log_path.open("w") as f:
            json.dump(log_data, f, indent=2)
