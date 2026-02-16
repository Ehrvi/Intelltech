#!/usr/bin/env python3
"""
MOTHER V5 - Mandatory Checklist System
=======================================

Programmatic gate that blocks actions until all compliance checks pass.

Author: MOTHER V5 Compliance System
Version: 1.0.0
Date: 2026-02-16
"""

from typing import Dict, Any, List, Callable
from dataclasses import dataclass
from enum import Enum


class ChecklistPhase(Enum):
    """Phases where checklists are executed."""
    PRE_TASK = "pre_task"
    PRE_MESSAGE = "pre_message"
    PRE_TOOL = "pre_tool"
    POST_ACTION = "post_action"
    END_OF_TASK = "end_of_task"


@dataclass
class ChecklistItem:
    """A single item in a checklist."""
    id: str
    description: str
    check_function: Callable[[Dict[str, Any]], bool]
    blocking: bool = True
    principle: str = "GENERAL"


class ChecklistResult:
    """Result of a checklist execution."""
    
    def __init__(self, phase: ChecklistPhase):
        self.phase = phase
        self.items_checked: List[str] = []
        self.items_passed: List[str] = []
        self.items_failed: List[str] = []
        self.blocking_failures: List[str] = []
        self.passed = True
    
    def add_pass(self, item_id: str):
        """Record a passing check."""
        self.items_checked.append(item_id)
        self.items_passed.append(item_id)
    
    def add_fail(self, item_id: str, blocking: bool):
        """Record a failing check."""
        self.items_checked.append(item_id)
        self.items_failed.append(item_id)
        if blocking:
            self.blocking_failures.append(item_id)
            self.passed = False
    
    def __bool__(self):
        """Allow boolean evaluation."""
        return self.passed
    
    def __repr__(self):
        status = "✅ PASS" if self.passed else "❌ BLOCKED"
        return (
            f"<ChecklistResult {status} "
            f"phase={self.phase.value} "
            f"checked={len(self.items_checked)} "
            f"failed={len(self.items_failed)} "
            f"blocking={len(self.blocking_failures)}>"
        )


class Checklist:
    """
    Mandatory checklist system.
    
    Executes a series of checks and blocks execution if any
    blocking check fails.
    """
    
    def __init__(self, phase: ChecklistPhase):
        self.phase = phase
        self.items: List[ChecklistItem] = []
    
    def add_item(
        self,
        item_id: str,
        description: str,
        check_function: Callable[[Dict[str, Any]], bool],
        blocking: bool = True,
        principle: str = "GENERAL"
    ):
        """Add an item to the checklist."""
        item = ChecklistItem(
            id=item_id,
            description=description,
            check_function=check_function,
            blocking=blocking,
            principle=principle
        )
        self.items.append(item)
    
    def execute(self, context: Dict[str, Any]) -> ChecklistResult:
        """
        Execute the checklist.
        
        Args:
            context: Context for the checks
        
        Returns:
            ChecklistResult with pass/fail status
        """
        result = ChecklistResult(self.phase)
        
        for item in self.items:
            try:
                passed = item.check_function(context)
                if passed:
                    result.add_pass(item.id)
                else:
                    result.add_fail(item.id, item.blocking)
                    if item.blocking:
                        print(f"❌ BLOCKED: {item.description}")
                        print(f"   Principle: {item.principle}")
            except Exception as e:
                print(f"⚠️  ERROR in checklist item {item.id}: {e}")
                result.add_fail(item.id, item.blocking)
        
        return result
    
    def __len__(self):
        return len(self.items)
    
    def __repr__(self):
        return f"<Checklist phase={self.phase.value} items={len(self.items)}>"


class ChecklistFactory:
    """Factory for creating standard checklists."""
    
    @staticmethod
    def create_pre_message_checklist() -> Checklist:
        """Create checklist for before sending a message."""
        checklist = Checklist(ChecklistPhase.PRE_MESSAGE)
        
        # P1: Study First
        checklist.add_item(
            "p1_study_complete",
            "Have I studied internal knowledge?",
            lambda ctx: ctx.get("study_completed", False),
            blocking=True,
            principle="P1"
        )
        
        # P2: Decide Autonomously
        checklist.add_item(
            "p2_no_asking",
            "Am I about to ask user to choose? (Should decide first!)",
            lambda ctx: not ctx.get("asking_user_to_choose", False),
            blocking=True,
            principle="P2"
        )
        
        # P3: Cost Optimized
        checklist.add_item(
            "p3_cost_optimized",
            "Have I used the cheapest tool that meets quality?",
            lambda ctx: ctx.get("cost_optimized", True),
            blocking=False,
            principle="P3"
        )
        
        # P7: Truthful
        checklist.add_item(
            "p7_truthful",
            "Is my message truthful and accurate?",
            lambda ctx: ctx.get("truthful", True),
            blocking=True,
            principle="P7"
        )
        
        return checklist
    
    @staticmethod
    def create_pre_tool_checklist() -> Checklist:
        """Create checklist for before using a tool."""
        checklist = Checklist(ChecklistPhase.PRE_TOOL)
        
        # P3: Cost Optimization
        checklist.add_item(
            "p3_cheapest_tool",
            "Is this the cheapest tool that meets quality requirements?",
            lambda ctx: ctx.get("is_cheapest_tool", True),
            blocking=False,
            principle="P3"
        )
        
        # P3: OpenAI First
        checklist.add_item(
            "p3_openai_first",
            "Could I use OpenAI (0.01 credits) instead?",
            lambda ctx: ctx.get("openai_considered", True),
            blocking=False,
            principle="P3"
        )
        
        return checklist
    
    @staticmethod
    def create_end_of_task_checklist() -> Checklist:
        """Create checklist for end of task."""
        checklist = Checklist(ChecklistPhase.END_OF_TASK)
        
        # P4: Quality Ensured
        checklist.add_item(
            "p4_quality_validated",
            "Have I validated quality?",
            lambda ctx: ctx.get("quality_validated", False),
            blocking=True,
            principle="P4"
        )
        
        # P5: Cost Report
        checklist.add_item(
            "p5_cost_report",
            "Have I generated the cost report?",
            lambda ctx: ctx.get("cost_report_generated", False),
            blocking=True,
            principle="P5"
        )
        
        # P6: Lessons Captured
        checklist.add_item(
            "p6_lessons_captured",
            "Have I captured lessons learned?",
            lambda ctx: ctx.get("lessons_captured", False),
            blocking=True,
            principle="P6"
        )
        
        # P6: Knowledge Updated
        checklist.add_item(
            "p6_knowledge_updated",
            "Have I updated the knowledge base?",
            lambda ctx: ctx.get("knowledge_updated", False),
            blocking=True,
            principle="P6"
        )
        
        return checklist


# Convenience function for quick checks
def check_before_message(context: Dict[str, Any]) -> ChecklistResult:
    """Quick check before sending a message."""
    checklist = ChecklistFactory.create_pre_message_checklist()
    return checklist.execute(context)


def check_before_tool(context: Dict[str, Any]) -> ChecklistResult:
    """Quick check before using a tool."""
    checklist = ChecklistFactory.create_pre_tool_checklist()
    return checklist.execute(context)


def check_end_of_task(context: Dict[str, Any]) -> ChecklistResult:
    """Quick check at end of task."""
    checklist = ChecklistFactory.create_end_of_task_checklist()
    return checklist.execute(context)
