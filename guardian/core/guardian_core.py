#!/usr/bin/env python3
"""
Guardian Core - Central Orchestrator for AI Reliability

Implements HRO Principles:
- Principle 3: Single Point of Responsibility
- Principle 5: Pre-Action Blocking
- Principle 10: Defined End-Point

This is the central orchestrator that manages the entire task lifecycle
and enforces reliability through mandatory checks.
"""

from typing import Tuple, Optional
from pathlib import Path

from state_tracker import StateTracker
from checklist_manager import ChecklistManager
from verification import VerificationEngine, IntegrationMonitor


class GuardianCore:
    """
    The central orchestrator for the Guardian System.
    
    Acts as the single point of responsibility for reliability enforcement.
    Manages the task lifecycle and enforces phase transitions.
    """
    
    def __init__(self):
        """Initialize the Guardian Core."""
        print("🛡️  Guardian Core initializing...")
        
        self.state_tracker = StateTracker()
        self.checklist_manager = ChecklistManager()
        self.verification_engine = VerificationEngine()
        self.integration_monitor = IntegrationMonitor()
        
        print("✅ Guardian Core initialized")
    
    def initialize_task(self, task_id: str, goal: str, checklist_name: str) -> None:
        """
        Initialize a new task.
        
        Args:
            task_id: Unique identifier for the task
            goal: The task goal
            checklist_name: Name of the checklist to use
        """
        print(f"\n🎯 Initializing task: {task_id}")
        print(f"   Goal: {goal}")
        
        # Initialize state
        self.state_tracker.initialize_task(task_id, goal, current_phase=1)
        
        # Load checklist
        self.checklist_manager.load_checklist(checklist_name)
        
        # Load checklist state from state tracker (if resuming)
        checklist_state = self.state_tracker.get('checklist_status', {})
        if checklist_state:
            self.checklist_manager.load_state(checklist_state)
        
        # Run initial health check
        print("\n🔍 Running initial health check...")
        all_healthy, report = self.integration_monitor.check_all()
        print(report)
        
        if not all_healthy:
            unhealthy = self.integration_monitor.get_unhealthy_systems()
            print(f"\n⚠️  Warning: Some systems are unhealthy: {unhealthy}")
            print("   Task can proceed, but these should be addressed.")
    
    def can_advance_phase(self, current_phase: int) -> Tuple[bool, str]:
        """
        Check if we can advance from the current phase.
        
        Implements Principle 5: Pre-Action Blocking
        
        Args:
            current_phase: The current phase number
            
        Returns:
            (can_advance, reason) tuple
        """
        print(f"\n🔒 Pre-Action Check: Can advance from Phase {current_phase}?")
        
        # Check 1: Are all critical checklist items complete?
        can_advance, checklist_reason = self.checklist_manager.can_advance_from_phase(current_phase)
        
        if not can_advance:
            print(f"✗ Checklist check FAILED")
            print(checklist_reason)
            return False, f"BLOCKED: Checklist incomplete\n\n{checklist_reason}"
        
        print(f"✓ Checklist check PASSED")
        
        # Check 2: Are all core systems still healthy?
        all_healthy, health_report = self.integration_monitor.check_all()
        
        if not all_healthy:
            print(f"✗ Health check FAILED")
            unhealthy = self.integration_monitor.get_unhealthy_systems()
            return False, f"BLOCKED: System health check failed\n\nUnhealthy systems: {unhealthy}\n\n{health_report}"
        
        print(f"✓ Health check PASSED")
        
        # All checks passed
        print(f"✅ All checks passed - advance approved")
        return True, "All checks passed"
    
    def advance_phase(self, from_phase: int, to_phase: int) -> Tuple[bool, str]:
        """
        Advance from one phase to another (with enforcement).
        
        Args:
            from_phase: Current phase
            to_phase: Target phase
            
        Returns:
            (success, message) tuple
        """
        # Enforce pre-action blocking
        can_advance, reason = self.can_advance_phase(from_phase)
        
        if not can_advance:
            return False, reason
        
        # Update state
        self.state_tracker.set('current_phase', to_phase)
        
        # Save checklist state
        self.state_tracker.set('checklist_status', self.checklist_manager.get_state())
        
        print(f"\n✅ Phase advanced: {from_phase} → {to_phase}")
        return True, f"Advanced to Phase {to_phase}"
    
    def mark_checklist_item_complete(self, item_id: str) -> None:
        """
        Mark a checklist item as complete.
        
        Args:
            item_id: The checklist item ID
        """
        self.checklist_manager.mark_complete(item_id)
        
        # Save to state
        self.state_tracker.set('checklist_status', self.checklist_manager.get_state())
    
    def get_checklist_report(self, phase: Optional[int] = None) -> str:
        """
        Get a checklist completion report.
        
        Args:
            phase: If specified, only report on that phase
            
        Returns:
            Formatted report string
        """
        return self.checklist_manager.get_completion_report(phase)
    
    def is_task_truly_done(self) -> Tuple[bool, str]:
        """
        Check if the task is truly complete (Defined End-Point).
        
        Implements Principle 10: Defined End-Point
        
        This is the ultimate check before allowing task completion.
        
        Returns:
            (is_done, reason) tuple
        """
        print("\n🔒 Final Check: Is task truly done?")
        
        # Check 1: Are ALL checklist items complete (not just critical)?
        is_complete, checklist_reason = self.checklist_manager.is_task_complete()
        
        if not is_complete:
            print(f"✗ Checklist check FAILED")
            print(checklist_reason)
            return False, f"BLOCKED: Task not complete\n\n{checklist_reason}"
        
        print(f"✓ Checklist check PASSED (all items complete)")
        
        # Check 2: Are all core systems still healthy?
        all_healthy, health_report = self.integration_monitor.check_all()
        
        if not all_healthy:
            print(f"✗ Health check FAILED")
            unhealthy = self.integration_monitor.get_unhealthy_systems()
            return False, f"BLOCKED: System health check failed\n\nUnhealthy systems: {unhealthy}\n\n{health_report}"
        
        print(f"✓ Health check PASSED")
        
        # All checks passed
        print(f"✅ All checks passed - task is truly done")
        return True, "Task complete - all checks passed"
    
    def get_current_phase(self) -> int:
        """
        Get the current phase number.
        
        Returns:
            Current phase number
        """
        return self.state_tracker.get('current_phase', 1)
    
    def get_task_summary(self) -> str:
        """
        Get a summary of the current task state.
        
        Returns:
            Formatted summary string
        """
        task_id = self.state_tracker.get('task_id', 'Unknown')
        goal = self.state_tracker.get('goal', 'Unknown')
        current_phase = self.get_current_phase()
        
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                    GUARDIAN TASK SUMMARY                     ║
╚══════════════════════════════════════════════════════════════╝

Task ID: {task_id}
Goal: {goal}
Current Phase: {current_phase}

{self.get_checklist_report(current_phase)}

Last Update: {self.state_tracker.get('last_update', 'Unknown')}
"""
        return summary


def create_guardian() -> GuardianCore:
    """
    Factory function to create a Guardian Core instance.
    
    Returns:
        GuardianCore instance
    """
    return GuardianCore()


if __name__ == "__main__":
    print("Testing GuardianCore...")
    
    # Create test checklist first
    test_checklist_dir = Path("~/guardian_test_checklists").expanduser()
    test_checklist_dir.mkdir(exist_ok=True)
    
    import yaml
    test_checklist = {
        'name': 'Test Task',
        'phases': [
            {
                'phase': 1,
                'items': [
                    {'id': 'item_1', 'text': 'First item', 'priority': 'critical'},
                    {'id': 'item_2', 'text': 'Second item'}
                ]
            },
            {
                'phase': 2,
                'items': [
                    {'id': 'item_3', 'text': 'Third item', 'priority': 'critical'}
                ]
            }
        ]
    }
    
    with open(test_checklist_dir / "test_task.yaml", 'w') as f:
        yaml.dump(test_checklist, f)
    
    # Test Guardian Core
    guardian = GuardianCore()
    guardian.checklist_manager.checklist_dir = test_checklist_dir
    guardian.initialize_task(
        task_id="test_001",
        goal="Test the Guardian Core",
        checklist_name="test_task"
    )
    
    print("\n" + guardian.get_task_summary())
    
    # Try to advance without completing checklist (should fail)
    print("\n--- Test 1: Try to advance without completing checklist ---")
    success, message = guardian.advance_phase(1, 2)
    if not success:
        print(f"✓ Correctly blocked advancement:\n{message}")
    
    # Complete critical item and try again
    print("\n--- Test 2: Complete critical item and try again ---")
    guardian.mark_checklist_item_complete('item_1')
    success, message = guardian.advance_phase(1, 2)
    if success:
        print(f"✓ Correctly allowed advancement:\n{message}")
    
    # Try to declare done without completing all items (should fail)
    print("\n--- Test 3: Try to declare done prematurely ---")
    is_done, reason = guardian.is_task_truly_done()
    if not is_done:
        print(f"✓ Correctly blocked task completion:\n{reason}")
    
    # Complete all items
    print("\n--- Test 4: Complete all items and check again ---")
    guardian.mark_checklist_item_complete('item_2')
    guardian.mark_checklist_item_complete('item_3')
    is_done, reason = guardian.is_task_truly_done()
    if is_done:
        print(f"✓ Correctly allowed task completion:\n{reason}")
    
    print("\n✅ GuardianCore test complete!")
