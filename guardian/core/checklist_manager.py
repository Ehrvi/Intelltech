#!/usr/bin/env python3
"""
Checklist Manager - Mandatory Checklists for Guardian System

Implements HRO Principles:
- Principle 2: Mandatory Checklists
- Principle 7: Logical Organization
- Principle 11: Critical Items First

This module manages task-specific checklists that must be completed before
phase advancement or task completion.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class ChecklistItem:
    """Represents a single checklist item."""
    id: str
    text: str
    priority: str = "normal"  # "critical" or "normal"
    completed: bool = False


@dataclass
class ChecklistPhase:
    """Represents a phase in the checklist."""
    phase: int
    items: List[ChecklistItem]


class ChecklistManager:
    """
    Manages mandatory checklists for different task types.
    
    Loads checklist templates from YAML files and tracks completion status.
    """
    
    def __init__(self, checklist_dir: str = "~/manus_global_knowledge/guardian/checklists"):
        """
        Initialize the Checklist Manager.
        
        Args:
            checklist_dir: Directory containing checklist YAML files
        """
        self.checklist_dir = Path(checklist_dir).expanduser()
        self.current_checklist: Optional[Dict[str, Any]] = None
        self.phases: Dict[int, ChecklistPhase] = {}
        self.completion_status: Dict[str, bool] = {}
    
    def load_checklist(self, checklist_name: str) -> None:
        """
        Load a checklist from a YAML file.
        
        Args:
            checklist_name: Name of the checklist (without .yaml extension)
        """
        checklist_file = self.checklist_dir / f"{checklist_name}.yaml"
        
        if not checklist_file.exists():
            raise FileNotFoundError(f"Checklist not found: {checklist_file}")
        
        with open(checklist_file, 'r') as f:
            self.current_checklist = yaml.safe_load(f)
        
        # Parse phases
        self.phases = {}
        for phase_data in self.current_checklist.get('phases', []):
            phase_num = phase_data['phase']
            items = [
                ChecklistItem(
                    id=item['id'],
                    text=item['text'],
                    priority=item.get('priority', 'normal')
                )
                for item in phase_data.get('items', [])
            ]
            self.phases[phase_num] = ChecklistPhase(phase=phase_num, items=items)
        
        # Initialize completion status
        self.completion_status = {
            item.id: False
            for phase in self.phases.values()
            for item in phase.items
        }
        
        print(f"✅ Checklist loaded: {self.current_checklist['name']}")
        print(f"   Phases: {len(self.phases)}, Total items: {len(self.completion_status)}")
    
    def get_phase_items(self, phase: int) -> List[ChecklistItem]:
        """
        Get all checklist items for a specific phase.
        
        Args:
            phase: The phase number
            
        Returns:
            List of checklist items for that phase
        """
        if phase not in self.phases:
            return []
        return self.phases[phase].items
    
    def get_critical_items(self, phase: int) -> List[ChecklistItem]:
        """
        Get critical checklist items for a specific phase.
        
        Args:
            phase: The phase number
            
        Returns:
            List of critical checklist items
        """
        items = self.get_phase_items(phase)
        return [item for item in items if item.priority == "critical"]
    
    def mark_complete(self, item_id: str) -> None:
        """
        Mark a checklist item as complete.
        
        Args:
            item_id: The ID of the checklist item
        """
        if item_id not in self.completion_status:
            raise ValueError(f"Unknown checklist item: {item_id}")
        
        self.completion_status[item_id] = True
        print(f"✓ Checklist item completed: {item_id}")
    
    def mark_incomplete(self, item_id: str) -> None:
        """
        Mark a checklist item as incomplete.
        
        Args:
            item_id: The ID of the checklist item
        """
        if item_id not in self.completion_status:
            raise ValueError(f"Unknown checklist item: {item_id}")
        
        self.completion_status[item_id] = False
        print(f"✗ Checklist item marked incomplete: {item_id}")
    
    def is_complete(self, item_id: str) -> bool:
        """
        Check if a checklist item is complete.
        
        Args:
            item_id: The ID of the checklist item
            
        Returns:
            True if complete, False otherwise
        """
        return self.completion_status.get(item_id, False)
    
    def is_phase_complete(self, phase: int, critical_only: bool = False) -> bool:
        """
        Check if all items in a phase are complete.
        
        Args:
            phase: The phase number
            critical_only: If True, only check critical items
            
        Returns:
            True if all (critical) items are complete, False otherwise
        """
        if critical_only:
            items = self.get_critical_items(phase)
        else:
            items = self.get_phase_items(phase)
        
        if not items:
            return True  # No items means complete
        
        return all(self.is_complete(item.id) for item in items)
    
    def get_incomplete_items(self, phase: int, critical_only: bool = False) -> List[ChecklistItem]:
        """
        Get all incomplete items for a phase.
        
        Args:
            phase: The phase number
            critical_only: If True, only return critical items
            
        Returns:
            List of incomplete checklist items
        """
        if critical_only:
            items = self.get_critical_items(phase)
        else:
            items = self.get_phase_items(phase)
        
        return [item for item in items if not self.is_complete(item.id)]
    
    def get_completion_report(self, phase: Optional[int] = None) -> str:
        """
        Generate a human-readable completion report.
        
        Args:
            phase: If specified, only report on that phase. Otherwise, all phases.
            
        Returns:
            A formatted report string
        """
        if not self.current_checklist:
            return "No checklist loaded."
        
        report_lines = [f"Checklist: {self.current_checklist['name']}", ""]
        
        phases_to_report = [phase] if phase else sorted(self.phases.keys())
        
        for p in phases_to_report:
            if p not in self.phases:
                continue
            
            phase_obj = self.phases[p]
            report_lines.append(f"Phase {p}:")
            
            for item in phase_obj.items:
                status = "✓" if self.is_complete(item.id) else "✗"
                priority_mark = " [CRITICAL]" if item.priority == "critical" else ""
                report_lines.append(f"  {status} {item.text}{priority_mark}")
            
            # Summary
            total = len(phase_obj.items)
            completed = sum(1 for item in phase_obj.items if self.is_complete(item.id))
            critical_items = [item for item in phase_obj.items if item.priority == "critical"]
            critical_completed = sum(1 for item in critical_items if self.is_complete(item.id))
            
            report_lines.append(f"  Summary: {completed}/{total} complete")
            if critical_items:
                report_lines.append(f"  Critical: {critical_completed}/{len(critical_items)} complete")
            report_lines.append("")
        
        return "\n".join(report_lines)
    
    def can_advance_from_phase(self, phase: int) -> tuple[bool, str]:
        """
        Check if we can advance from a phase (all critical items complete).
        
        Args:
            phase: The phase number
            
        Returns:
            (can_advance, reason) tuple
        """
        if not self.is_phase_complete(phase, critical_only=True):
            incomplete = self.get_incomplete_items(phase, critical_only=True)
            reason = f"Cannot advance: {len(incomplete)} critical item(s) incomplete:\n"
            for item in incomplete:
                reason += f"  - {item.text}\n"
            return False, reason
        
        return True, "All critical items complete"
    
    def is_task_complete(self) -> tuple[bool, str]:
        """
        Check if the entire task is complete (all items in all phases).
        
        Returns:
            (is_complete, reason) tuple
        """
        incomplete_phases = []
        
        for phase_num in sorted(self.phases.keys()):
            if not self.is_phase_complete(phase_num, critical_only=False):
                incomplete = self.get_incomplete_items(phase_num, critical_only=False)
                incomplete_phases.append((phase_num, incomplete))
        
        if incomplete_phases:
            reason = f"Task incomplete: {len(incomplete_phases)} phase(s) have incomplete items:\n"
            for phase_num, items in incomplete_phases:
                reason += f"\nPhase {phase_num}:\n"
                for item in items:
                    priority_mark = " [CRITICAL]" if item.priority == "critical" else ""
                    reason += f"  - {item.text}{priority_mark}\n"
            return False, reason
        
        return True, "All checklist items complete"
    
    def load_state(self, state: Dict[str, bool]) -> None:
        """
        Load completion state from a dictionary (e.g., from StateTracker).
        
        Args:
            state: Dictionary mapping item IDs to completion status
        """
        for item_id, completed in state.items():
            if item_id in self.completion_status:
                self.completion_status[item_id] = completed
        print(f"✅ Checklist state loaded: {sum(state.values())}/{len(state)} items complete")
    
    def get_state(self) -> Dict[str, bool]:
        """
        Get the current completion state as a dictionary.
        
        Returns:
            Dictionary mapping item IDs to completion status
        """
        return self.completion_status.copy()


if __name__ == "__main__":
    # Test the ChecklistManager
    print("Testing ChecklistManager...")
    
    # First, create a test checklist
    test_checklist_dir = Path("~/guardian_test_checklists").expanduser()
    test_checklist_dir.mkdir(exist_ok=True)
    
    test_checklist = {
        'name': 'Test Software Development',
        'phases': [
            {
                'phase': 1,
                'items': [
                    {'id': 'research_complete', 'text': 'Research papers reviewed', 'priority': 'critical'},
                    {'id': 'design_doc', 'text': 'Design document created'}
                ]
            },
            {
                'phase': 2,
                'items': [
                    {'id': 'code_written', 'text': 'Code implemented'},
                    {'id': 'unit_tests', 'text': 'Unit tests passing', 'priority': 'critical'}
                ]
            },
            {
                'phase': 3,
                'items': [
                    {'id': 'integration', 'text': 'Integrated into main system', 'priority': 'critical'},
                    {'id': 'e2e_test', 'text': 'End-to-end test passing', 'priority': 'critical'}
                ]
            }
        ]
    }
    
    with open(test_checklist_dir / "test_software.yaml", 'w') as f:
        yaml.dump(test_checklist, f)
    
    # Test the manager
    manager = ChecklistManager(str(test_checklist_dir))
    manager.load_checklist("test_software")
    
    print("\n" + manager.get_completion_report())
    
    # Mark some items complete
    manager.mark_complete('research_complete')
    manager.mark_complete('design_doc')
    
    print("\n" + manager.get_completion_report(phase=1))
    
    # Check if we can advance
    can_advance, reason = manager.can_advance_from_phase(1)
    print(f"\nCan advance from Phase 1? {can_advance}")
    print(reason)
    
    # Try to advance from Phase 2 (should fail - critical item not done)
    can_advance, reason = manager.can_advance_from_phase(2)
    print(f"\nCan advance from Phase 2? {can_advance}")
    print(reason)
    
    # Complete Phase 2 critical item
    manager.mark_complete('unit_tests')
    can_advance, reason = manager.can_advance_from_phase(2)
    print(f"\nCan advance from Phase 2 now? {can_advance}")
    print(reason)
    
    print("\n✅ ChecklistManager test complete!")
