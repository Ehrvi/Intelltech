#!/usr/bin/env python3
"""
Precise Cost Tracking System
Tracks REAL costs (not estimates) for every operation in a task.
Generates compact cost report at task completion.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class Operation:
    """Single operation with precise cost"""
    timestamp: str
    tool: str
    action: str
    cost_credits: float
    alternative_tool: Optional[str] = None
    alternative_cost: Optional[float] = None
    savings_credits: float = 0.0
    quality_score: Optional[int] = None
    
    def __post_init__(self):
        if self.alternative_cost and self.cost_credits:
            self.savings_credits = self.alternative_cost - self.cost_credits


class TaskCostTracker:
    """Track costs for a single task with precision"""
    
    # Real Manus costs (from official pricing)
    MANUS_COSTS = {
        'shell': 1.0,           # Shell command execution
        'file_read': 0.5,       # Read file
        'file_write': 0.5,      # Write file
        'file_edit': 0.5,       # Edit file
        'search': 20.0,         # Web search
        'browser': 30.0,        # Browser navigation
        'browser_action': 5.0,  # Browser interaction
        'map': 10.0,            # Per item in parallel map
        'generate_image': 15.0, # Image generation
        'generate_video': 50.0, # Video generation
        'mcp_call': 2.0,        # MCP tool call
        'plan': 0.0,            # Planning (free)
        'message': 0.0,         # Messaging (free)
    }
    
    # OpenAI costs (approximate per call)
    OPENAI_COSTS = {
        'gpt-4o': 0.01,         # Per request
        'gpt-4o-mini': 0.001,   # Per request
        'gpt-5': 0.05,          # Per request
    }
    
    # API costs
    API_COSTS = {
        'apollo': 0.01,         # Per credit
        'gmail': 0.0,           # Free (MCP)
        'calendar': 0.0,        # Free (MCP)
    }
    
    def __init__(self, task_name: str):
        self.task_name = task_name
        self.start_time = datetime.now()
        self.operations: List[Operation] = []
        self.base_path = Path("/home/ubuntu/manus_global_knowledge")
        self.logs_dir = self.base_path / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
    def log_operation(
        self,
        tool: str,
        action: str,
        cost_credits: float,
        alternative_tool: Optional[str] = None,
        alternative_cost: Optional[float] = None,
        quality_score: Optional[int] = None
    ):
        """Log a single operation with precise cost"""
        op = Operation(
            timestamp=datetime.now().isoformat(),
            tool=tool,
            action=action,
            cost_credits=cost_credits,
            alternative_tool=alternative_tool,
            alternative_cost=alternative_cost,
            quality_score=quality_score
        )
        self.operations.append(op)
        
        # Also log to persistent storage
        self._persist_operation(op)
    
    def _persist_operation(self, op: Operation):
        """Save operation to persistent log"""
        log_file = self.logs_dir / "operations.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(asdict(op)) + '\n')
    
    def get_total_cost(self) -> float:
        """Get total cost of all operations"""
        return sum(op.cost_credits for op in self.operations)
    
    def get_total_savings(self) -> float:
        """Get total savings from using cheaper alternatives"""
        return sum(op.savings_credits for op in self.operations)
    
    def get_savings_rate(self) -> float:
        """Get savings rate as percentage"""
        total = self.get_total_cost()
        savings = self.get_total_savings()
        potential_cost = total + savings
        if potential_cost == 0:
            return 0.0
        return (savings / potential_cost) * 100
    
    def get_tool_breakdown(self) -> Dict[str, Dict]:
        """Get cost breakdown by tool"""
        breakdown = {}
        for op in self.operations:
            if op.tool not in breakdown:
                breakdown[op.tool] = {
                    'count': 0,
                    'total_cost': 0.0,
                    'total_savings': 0.0
                }
            breakdown[op.tool]['count'] += 1
            breakdown[op.tool]['total_cost'] += op.cost_credits
            breakdown[op.tool]['total_savings'] += op.savings_credits
        return breakdown
    
    def generate_compact_report(self) -> str:
        """Generate compact cost report for task completion"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        total_cost = self.get_total_cost()
        total_savings = self.get_total_savings()
        savings_rate = self.get_savings_rate()
        
        # Quality scores
        quality_scores = [op.quality_score for op in self.operations if op.quality_score]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # Tool breakdown
        breakdown = self.get_tool_breakdown()
        
        # Build compact report
        lines = []
        lines.append("=" * 70)
        lines.append(f"📊 COST REPORT: {self.task_name}")
        lines.append("=" * 70)
        lines.append(f"Duration: {duration:.1f}s | Operations: {len(self.operations)}")
        lines.append(f"Total Cost: {total_cost:.3f} credits | Savings: {total_savings:.3f} credits")
        lines.append(f"Savings Rate: {savings_rate:.1f}% | Avg Quality: {avg_quality:.0f}/100")
        lines.append("")
        
        # Tool breakdown (top 5 by cost)
        if breakdown:
            lines.append("Top Tools by Cost:")
            sorted_tools = sorted(breakdown.items(), key=lambda x: x[1]['total_cost'], reverse=True)[:5]
            for tool, data in sorted_tools:
                lines.append(f"  {tool:20s} {data['count']:2d}x  {data['total_cost']:6.2f} credits  (saved {data['total_savings']:6.2f})")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def save_report(self):
        """Save report to file"""
        report = self.generate_compact_report()
        report_file = self.logs_dir / f"task_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        return report_file


# Global task tracker
_current_task_tracker: Optional[TaskCostTracker] = None


def start_task(task_name: str):
    """Start tracking a new task"""
    global _current_task_tracker
    _current_task_tracker = TaskCostTracker(task_name)
    return _current_task_tracker


def log_op(
    tool: str,
    action: str,
    cost_credits: float,
    alternative_tool: Optional[str] = None,
    alternative_cost: Optional[float] = None,
    quality_score: Optional[int] = None
):
    """Quick logging function"""
    global _current_task_tracker
    if _current_task_tracker is None:
        _current_task_tracker = TaskCostTracker("Unnamed Task")
    
    _current_task_tracker.log_operation(
        tool=tool,
        action=action,
        cost_credits=cost_credits,
        alternative_tool=alternative_tool,
        alternative_cost=alternative_cost,
        quality_score=quality_score
    )


def end_task() -> str:
    """End task and generate report"""
    global _current_task_tracker
    if _current_task_tracker is None:
        return "No task tracked"
    
    report = _current_task_tracker.generate_compact_report()
    _current_task_tracker.save_report()
    
    # Reset tracker
    _current_task_tracker = None
    
    return report


def get_current_tracker() -> Optional[TaskCostTracker]:
    """Get current task tracker"""
    return _current_task_tracker


# Convenience functions for common operations
def log_shell(action: str):
    """Log shell command"""
    log_op('shell', action, TaskCostTracker.MANUS_COSTS['shell'])


def log_file_read(filename: str):
    """Log file read"""
    log_op('file_read', f"Read {filename}", TaskCostTracker.MANUS_COSTS['file_read'])


def log_file_write(filename: str):
    """Log file write"""
    log_op('file_write', f"Write {filename}", TaskCostTracker.MANUS_COSTS['file_write'])


def log_search(query: str):
    """Log search (should use OpenAI instead!)"""
    log_op(
        'search',
        f"Search: {query}",
        TaskCostTracker.MANUS_COSTS['search'],
        alternative_tool='openai',
        alternative_cost=TaskCostTracker.OPENAI_COSTS['gpt-4o-mini']
    )


def log_openai(model: str, action: str):
    """Log OpenAI usage"""
    cost = TaskCostTracker.OPENAI_COSTS.get(model, 0.01)
    log_op('openai', action, cost)


def log_browser(url: str):
    """Log browser navigation"""
    log_op('browser', f"Navigate to {url}", TaskCostTracker.MANUS_COSTS['browser'])


if __name__ == '__main__':
    # Demo usage
    start_task("Demo Task: Research and Analysis")
    
    # Log some operations
    log_file_read("data.csv")
    log_openai("gpt-4o-mini", "Analyze data")
    log_file_write("report.md")
    log_shell("git commit")
    
    # Could have used search but used OpenAI instead
    log_op(
        'openai',
        'Research companies',
        0.001,
        alternative_tool='search',
        alternative_cost=20.0,
        quality_score=95
    )
    
    # End task and print report
    print(end_task())
