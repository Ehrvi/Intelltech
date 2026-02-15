"""
Automatic Cost Reporting Reminder System

This system creates visible reminders to generate cost reports.
Since we can't intercept Manus tools automatically, we use cognitive enforcement.
"""

import os
from pathlib import Path

def create_reminder_file():
    """Create a reminder file that forces cost reporting"""
    reminder_path = Path("/home/ubuntu/.cost_report_reminder")
    
    reminder_text = """
╔════════════════════════════════════════════════════════════════════╗
║                    ⚠️  COST REPORT REQUIRED  ⚠️                     ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  Before sending FINAL result to user, you MUST:                   ║
║                                                                    ║
║  1. Generate cost report manually                                 ║
║  2. Include report in final message                               ║
║  3. Format: Compact 10-line report                                ║
║                                                                    ║
║  Command:                                                          ║
║  $ python3 -c "from core.precise_cost_tracker import *; ..."      ║
║                                                                    ║
║  This is MANDATORY. No exceptions.                                ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
"""
    
    with open(reminder_path, 'w') as f:
        f.write(reminder_text)
    
    return reminder_path


def show_reminder():
    """Display the cost reporting reminder"""
    reminder_path = Path("/home/ubuntu/.cost_report_reminder")
    
    if reminder_path.exists():
        with open(reminder_path, 'r') as f:
            print(f.read())
    else:
        create_reminder_file()
        show_reminder()


def generate_simple_cost_report(operations_count: dict) -> str:
    """
    Generate a simple cost report from operation counts.
    
    Args:
        operations_count: Dict of {tool_name: count}
    
    Returns:
        Formatted cost report string
    """
    # Manus costs
    COSTS = {
        'shell': 1.0,
        'file_read': 0.5,
        'file_write': 0.5,
        'file_edit': 0.5,
        'search': 20.0,
        'browser': 30.0,
        'browser_action': 5.0,
        'openai': 0.01,
        'map': 10.0,
        'generate': 15.0,
        'mcp': 2.0,
    }
    
    total_cost = 0
    total_saved = 0
    lines = []
    
    # Calculate costs
    for tool, count in sorted(operations_count.items(), 
                             key=lambda x: -x[1] * COSTS.get(x[0], 0)):
        cost = COSTS.get(tool, 0)
        total = count * cost
        total_cost += total
        
        # Calculate savings for OpenAI
        if tool == 'openai':
            saved_per = 50.0 - 0.01  # vs search+browser
            saved = count * saved_per
            total_saved += saved
            lines.append(f"  {tool:12s} {count:3d}x  {total:7.2f} credits  (saved {saved:7.2f})")
        else:
            lines.append(f"  {tool:12s} {count:3d}x  {total:7.2f} credits")
    
    # Calculate savings rate
    if total_saved > 0:
        savings_rate = (total_saved / (total_cost + total_saved)) * 100
    else:
        savings_rate = 0
    
    # Format report
    report = "=" * 70 + "\n"
    report += "📊 COST REPORT\n"
    report += "=" * 70 + "\n"
    report += f"Total Cost: {total_cost:.2f} credits | "
    report += f"Savings: {total_saved:.2f} credits | "
    report += f"Savings Rate: {savings_rate:.1f}%\n\n"
    report += "Operations:\n"
    report += "\n".join(lines)
    report += "\n" + "=" * 70
    
    return report


if __name__ == "__main__":
    # Show reminder when this module is run
    show_reminder()
