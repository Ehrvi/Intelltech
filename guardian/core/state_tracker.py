#!/usr/bin/env python3
"""
State Tracker - External Memory for Guardian System

Implements HRO Principles:
- Principle 1: External Memory
- Principle 8: Error-Resilient Design

This module provides persistent state management across task sessions.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class StateTracker:
    """
    Manages persistent task state in an external JSON file.
    
    Provides external memory that survives context window limitations,
    interruptions, and session boundaries.
    """
    
    def __init__(self, state_file: str = "~/.guardian_state.json"):
        """
        Initialize the State Tracker.
        
        Args:
            state_file: Path to the state file (supports ~ expansion)
        """
        self.state_file = Path(state_file).expanduser()
        self.state: Dict[str, Any] = {}
        self.load_state()
    
    def load_state(self) -> Dict[str, Any]:
        """
        Load state from file.
        
        Returns:
            The loaded state dictionary
        """
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    self.state = json.load(f)
                print(f"✅ State loaded from {self.state_file}")
            except json.JSONDecodeError:
                print(f"⚠️  State file corrupted, starting fresh")
                self.state = {}
        else:
            print(f"ℹ️  No existing state file, starting fresh")
            self.state = {}
        
        return self.state
    
    def save_state(self) -> None:
        """
        Save current state to file.
        
        Updates the last_update timestamp automatically.
        """
        self.state['last_update'] = datetime.utcnow().isoformat() + 'Z'
        
        # Ensure parent directory exists
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write atomically (write to temp, then rename)
        temp_file = self.state_file.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(self.state, f, indent=2)
        temp_file.replace(self.state_file)
        
        print(f"💾 State saved to {self.state_file}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from state.
        
        Args:
            key: The key to retrieve
            default: Default value if key doesn't exist
            
        Returns:
            The value, or default if not found
        """
        return self.state.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a value in state and save immediately.
        
        Args:
            key: The key to set
            value: The value to store
        """
        self.state[key] = value
        self.save_state()
    
    def update(self, updates: Dict[str, Any]) -> None:
        """
        Update multiple values at once.
        
        Args:
            updates: Dictionary of key-value pairs to update
        """
        self.state.update(updates)
        self.save_state()
    
    def get_nested(self, *keys: str, default: Any = None) -> Any:
        """
        Get a nested value from state.
        
        Example:
            state.get_nested('checklist_status', 'phase_6_implementation_started')
        
        Args:
            *keys: Path to the nested value
            default: Default value if path doesn't exist
            
        Returns:
            The nested value, or default if not found
        """
        current = self.state
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    
    def set_nested(self, *keys, value: Any) -> None:
        """
        Set a nested value in state.
        
        Example:
            state.set_nested('checklist_status', 'phase_6_implementation_started', True)
        
        Args:
            *keys: Path to the nested value
            value: The value to store (keyword argument)
        """
        if len(keys) < 1:
            raise ValueError("Must provide at least one key")
        
        # Navigate to parent
        current = self.state
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set final key
        current[keys[-1]] = value
        self.save_state()
    
    def clear(self) -> None:
        """
        Clear all state (use with caution).
        """
        self.state = {}
        self.save_state()
        print("🗑️  State cleared")
    
    def get_full_state(self) -> Dict[str, Any]:
        """
        Get the entire state dictionary.
        
        Returns:
            The complete state
        """
        return self.state.copy()
    
    def initialize_task(self, task_id: str, goal: str, current_phase: int = 1) -> None:
        """
        Initialize state for a new task.
        
        Args:
            task_id: Unique identifier for the task
            goal: The task goal
            current_phase: Starting phase (default: 1)
        """
        self.update({
            'task_id': task_id,
            'goal': goal,
            'current_phase': current_phase,
            'checklist_status': {},
            'verification_results': {},
            'started_at': datetime.utcnow().isoformat() + 'Z'
        })
        print(f"🎯 Task initialized: {task_id}")


# Convenience function for quick access
def get_state_tracker() -> StateTracker:
    """
    Get the singleton StateTracker instance.
    
    Returns:
        The StateTracker instance
    """
    return StateTracker()


if __name__ == "__main__":
    # Test the StateTracker
    print("Testing StateTracker...")
    
    tracker = StateTracker("~/.guardian_state_test.json")
    
    # Initialize a task
    tracker.initialize_task(
        task_id="test_task_001",
        goal="Test the StateTracker functionality",
        current_phase=1
    )
    
    # Set some nested values
    tracker.set_nested('checklist_status', 'phase_1_research_complete', value=True)
    tracker.set_nested('checklist_status', 'phase_2_design_complete', value=False)
    
    # Get values
    print(f"Current phase: {tracker.get('current_phase')}")
    print(f"Research complete: {tracker.get_nested('checklist_status', 'phase_1_research_complete')}")
    
    # Update multiple values
    tracker.update({
        'current_phase': 2,
        'notes': 'Moving to design phase'
    })
    
    # Print full state
    print("\nFull state:")
    print(json.dumps(tracker.get_full_state(), indent=2))
    
    print("\n✅ StateTracker test complete!")
