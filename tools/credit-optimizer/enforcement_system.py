#!/usr/bin/env python3
"""
Enforcement Protocol Compliance System
Version: 3.0
Ensures all tool usage follows mandatory enforcement protocol
"""

import os
import json
from datetime import datetime
from typing import Dict, Tuple, Optional

class EnforcementSystem:
    """
    Enforces cost optimization and decision-making protocol
    """
    
    def __init__(self):
        self.log_file = "/home/ubuntu/manus_global_knowledge/logs/enforcement_decisions.jsonl"
        self.ensure_log_dir()
        
        # Cost estimates (in Manus credits)
        self.tool_costs = {
            'openai_api': 0.01,  # Extremely cheap
            'file_read': 1,
            'file_write': 1,
            'shell_simple': 2,
            'shell_complex': 5,
            'search': 20,
            'browser': 30,
            'generate': 40,
            'map': 100,  # Per item
        }
        
        # Decision tree thresholds
        self.cost_threshold_warning = 50
        self.cost_threshold_block = 100
        
    def ensure_log_dir(self):
        """Ensure log directory exists"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def pre_tool_check(self, tool_name: str, task_description: str, 
                      can_use_openai: bool = True) -> Tuple[bool, str, Dict]:
        """
        MANDATORY check before using any Manus tool
        
        Args:
            tool_name: Name of tool to use (search, browser, file, etc)
            task_description: What you're trying to accomplish
            can_use_openai: Whether OpenAI API can accomplish this task
            
        Returns:
            (allowed, reason, decision_log)
        """
        
        decision = {
            'timestamp': datetime.now().isoformat(),
            'tool': tool_name,
            'task': task_description,
            'can_use_openai': can_use_openai,
        }
        
        # Step 1: Can OpenAI API do this?
        if can_use_openai:
            decision['decision'] = 'BLOCKED'
            decision['reason'] = 'OpenAI API can do this task (1000x cheaper)'
            decision['alternative'] = 'Use OpenAI API'
            decision['estimated_cost'] = self.tool_costs['openai_api']
            decision['savings'] = self.tool_costs.get(tool_name, 20) - 0.01
            
            self._log_decision(decision)
            return False, decision['reason'], decision
        
        # Step 2: Is this a necessary Manus operation?
        necessary_tools = ['browser', 'mcp', 'file', 'shell']
        if any(t in tool_name.lower() for t in necessary_tools):
            estimated_cost = self.tool_costs.get(tool_name, 10)
            decision['estimated_cost'] = estimated_cost
            
            # Check cost threshold
            if estimated_cost > self.cost_threshold_block:
                decision['decision'] = 'BLOCKED'
                decision['reason'] = f'Cost too high ({estimated_cost} credits > {self.cost_threshold_block} threshold)'
                decision['alternative'] = 'Find cheaper alternative or ask user approval'
                
                self._log_decision(decision)
                return False, decision['reason'], decision
            
            elif estimated_cost > self.cost_threshold_warning:
                decision['decision'] = 'ALLOWED_WITH_WARNING'
                decision['reason'] = f'High cost ({estimated_cost} credits) but necessary'
                decision['justification'] = 'No cheaper alternative exists'
                
                self._log_decision(decision)
                return True, decision['reason'], decision
            
            else:
                decision['decision'] = 'ALLOWED'
                decision['reason'] = f'Necessary operation, reasonable cost ({estimated_cost} credits)'
                
                self._log_decision(decision)
                return True, decision['reason'], decision
        
        # Step 3: Check if it's an expensive search/generate operation
        estimated_cost = self.tool_costs.get(tool_name, 20)
        decision['estimated_cost'] = estimated_cost
        
        if estimated_cost > self.cost_threshold_warning:
            decision['decision'] = 'BLOCKED'
            decision['reason'] = f'Expensive operation ({estimated_cost} credits) with possible alternatives'
            decision['alternative'] = 'Use OpenAI API or break into smaller operations'
            
            self._log_decision(decision)
            return False, decision['reason'], decision
        
        # Default: Allow but log
        decision['decision'] = 'ALLOWED'
        decision['reason'] = f'Reasonable cost ({estimated_cost} credits)'
        
        self._log_decision(decision)
        return True, decision['reason'], decision
    
    def _log_decision(self, decision: Dict):
        """Log decision to file"""
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(decision) + '\n')
        except Exception as e:
            print(f"Warning: Failed to log decision: {e}")
    
    def get_statistics(self) -> Dict:
        """Get enforcement statistics"""
        if not os.path.exists(self.log_file):
            return {'total_decisions': 0}
        
        stats = {
            'total_decisions': 0,
            'allowed': 0,
            'blocked': 0,
            'warnings': 0,
            'total_estimated_cost': 0,
            'total_savings': 0,
        }
        
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    decision = json.loads(line.strip())
                    stats['total_decisions'] += 1
                    
                    if decision['decision'] == 'ALLOWED':
                        stats['allowed'] += 1
                    elif decision['decision'] == 'BLOCKED':
                        stats['blocked'] += 1
                        stats['total_savings'] += decision.get('savings', 0)
                    elif decision['decision'] == 'ALLOWED_WITH_WARNING':
                        stats['warnings'] += 1
                    
                    stats['total_estimated_cost'] += decision.get('estimated_cost', 0)
        
        except Exception as e:
            print(f"Warning: Failed to read statistics: {e}")
        
        return stats
    
    def print_statistics(self):
        """Print enforcement statistics"""
        stats = self.get_statistics()
        
        print("\n" + "="*70)
        print("ENFORCEMENT PROTOCOL STATISTICS")
        print("="*70)
        print(f"Total Decisions: {stats['total_decisions']}")
        print(f"Allowed: {stats['allowed']}")
        print(f"Blocked: {stats['blocked']}")
        print(f"Warnings: {stats['warnings']}")
        print(f"Estimated Cost: {stats['total_estimated_cost']:.2f} credits")
        print(f"Estimated Savings: {stats['total_savings']:.2f} credits")
        
        if stats['total_decisions'] > 0:
            block_rate = (stats['blocked'] / stats['total_decisions']) * 100
            print(f"Block Rate: {block_rate:.1f}%")
        
        print("="*70)


# Global enforcement instance
enforcement = EnforcementSystem()


def check_before_tool_use(tool_name: str, task: str, can_use_openai: bool = True) -> bool:
    """
    Convenience function to check before using any tool
    
    Usage:
        if check_before_tool_use('search', 'Find AI companies', can_use_openai=True):
            # Use tool
        else:
            # Use alternative (OpenAI API)
    """
    allowed, reason, decision = enforcement.pre_tool_check(tool_name, task, can_use_openai)
    
    if not allowed:
        print(f"⚠️ BLOCKED: {reason}")
        if 'alternative' in decision:
            print(f"💡 Alternative: {decision['alternative']}")
    
    return allowed


if __name__ == "__main__":
    # Test the enforcement system
    print("Testing Enforcement System\n")
    
    # Test 1: Should block (OpenAI can do it)
    print("Test 1: Research task")
    check_before_tool_use('search', 'Research top AI companies', can_use_openai=True)
    
    # Test 2: Should allow (browser necessary)
    print("\nTest 2: Web scraping")
    check_before_tool_use('browser', 'Scrape website data', can_use_openai=False)
    
    # Test 3: Should block (too expensive)
    print("\nTest 3: Expensive map operation")
    check_before_tool_use('map', 'Process 100 items in parallel', can_use_openai=False)
    
    # Print statistics
    enforcement.print_statistics()
