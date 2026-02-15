#!/usr/bin/env python3
"""
Automatic Cost Reporter
Generates cost reports automatically at conversation end
Integrates with Manus Global Knowledge System
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class AutoCostReporter:
    """Automatic cost reporting system"""
    
    # Manus operation costs (credits)
    MANUS_COSTS = {
        'shell': 1.0,
        'file_read': 0.5,
        'file_write': 0.5,
        'file_edit': 0.5,
        'search': 20.0,
        'browser': 30.0,
        'browser_action': 5.0,
        'map': 10.0,
        'generate_image': 15.0,
        'generate_video': 50.0,
        'mcp_call': 2.0,
        'plan': 0.0,
        'message': 0.0,
    }
    
    def __init__(self):
        self.base_path = Path("/home/ubuntu/manus_global_knowledge")
        self.reports_dir = self.base_path / "metrics" / "cost_reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Track operations in this session
        self.operations = {}
        self.openai_usage = {
            'calls': 0,
            'total_tokens': 0,
            'total_cost_usd': 0.0
        }
        
    def log_operation(self, tool: str, count: int = 1):
        """Log an operation"""
        if tool not in self.operations:
            self.operations[tool] = 0
        self.operations[tool] += count
        
    def log_openai(self, tokens: int, cost_usd: float):
        """Log OpenAI usage"""
        self.openai_usage['calls'] += 1
        self.openai_usage['total_tokens'] += tokens
        self.openai_usage['total_cost_usd'] += cost_usd
        
    def calculate_costs(self) -> Dict:
        """Calculate total costs"""
        manus_total = 0
        breakdown = {}
        
        for op, count in self.operations.items():
            cost = self.MANUS_COSTS.get(op, 0)
            total = count * cost
            manus_total += total
            if total > 0:
                breakdown[op] = {'count': count, 'cost': total}
        
        manus_usd = manus_total * 0.01  # 1 credit ≈ $0.01
        total_usd = manus_usd + self.openai_usage['total_cost_usd']
        
        return {
            'manus_credits': manus_total,
            'manus_usd': manus_usd,
            'openai_usd': self.openai_usage['total_cost_usd'],
            'openai_tokens': self.openai_usage['total_tokens'],
            'openai_calls': self.openai_usage['calls'],
            'total_usd': total_usd,
            'breakdown': breakdown
        }
    
    def calculate_savings(self) -> Dict:
        """Calculate cost savings from optimization"""
        # Estimate savings from using OpenAI instead of search+browser
        openai_calls = self.openai_usage['calls']
        if openai_calls > 0:
            alternative_cost = openai_calls * (self.MANUS_COSTS['search'] + self.MANUS_COSTS['browser'])
            actual_cost = openai_calls * 0.01  # Minimal Manus overhead
            savings = alternative_cost - actual_cost
            rate = (savings / alternative_cost * 100) if alternative_cost > 0 else 0
        else:
            alternative_cost = 0
            savings = 0
            rate = 0
            
        return {
            'alternative_cost': alternative_cost,
            'savings': savings,
            'rate': rate
        }
    
    def generate_compact_report(self) -> str:
        """Generate compact ASCII art cost report"""
        costs = self.calculate_costs()
        savings = self.calculate_savings()
        
        report = []
        report.append("╔" + "═" * 78 + "╗")
        report.append("║" + " " * 20 + "💰 CONVERSATION COST REPORT" + " " * 31 + "║")
        report.append("╠" + "═" * 78 + "╣")
        report.append("║" + " " * 78 + "║")
        
        # Summary
        report.append("║  📊 SUMMARY" + " " * 65 + "║")
        report.append("║" + " " * 78 + "║")
        report.append(f"║    Total Cost:        ${costs['total_usd']:.4f} USD" + " " * 44 + "║")
        report.append(f"║      ├─ Manus:        ${costs['manus_usd']:.4f} USD ({costs['manus_credits']:.1f} credits)" + " " * 27 + "║")
        
        if costs['openai_calls'] > 0:
            report.append(f"║      └─ OpenAI:       ${costs['openai_usd']:.4f} USD ({costs['openai_tokens']} tokens)" + " " * 24 + "║")
        
        report.append("║" + " " * 78 + "║")
        
        if savings['savings'] > 0:
            report.append(f"║    💎 Savings:        {savings['savings']:.1f} credits ({savings['rate']:.1f}% saved)" + " " * 29 + "║")
            report.append("║       vs using search+browser for research" + " " * 35 + "║")
            report.append("║" + " " * 78 + "║")
        
        # Breakdown (top 5)
        if costs['breakdown']:
            report.append("║  🔧 TOP OPERATIONS" + " " * 59 + "║")
            report.append("║" + " " * 78 + "║")
            
            sorted_ops = sorted(costs['breakdown'].items(), key=lambda x: x[1]['cost'], reverse=True)[:5]
            for op, data in sorted_ops:
                op_name = op.replace('_', ' ').title()
                line = f"║    {op_name:20s} {data['count']:3d}x  →  {data['cost']:6.1f} credits"
                padding = 78 - len(line) + 1
                report.append(line + " " * padding + "║")
            
            report.append("║" + " " * 78 + "║")
        
        # Footer
        report.append("╠" + "═" * 78 + "╣")
        report.append(f"║  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + " " * 46 + "║")
        report.append("║  Principle P3: Always Optimize Cost ✅" + " " * 38 + "║")
        report.append("╚" + "═" * 78 + "╝")
        
        return "\n".join(report)
    
    def save_report(self, report: str) -> Path:
        """Save report to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.reports_dir / f"cost_report_{timestamp}.txt"
        
        with open(report_file, 'w') as f:
            f.write(report)
            
        # Also save JSON for analysis
        costs = self.calculate_costs()
        savings = self.calculate_savings()
        
        json_file = self.reports_dir / f"cost_report_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'costs': costs,
                'savings': savings,
                'operations': self.operations,
                'openai_usage': self.openai_usage
            }, f, indent=2)
        
        return report_file
    
    def create_reminder(self):
        """Create reminder file for agent"""
        reminder_path = Path("/home/ubuntu/.cost_report_reminder")
        
        reminder = """
╔════════════════════════════════════════════════════════════════════╗
║                    ⚠️  COST REPORT REQUIRED  ⚠️                     ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  Before sending FINAL result to user, you MUST:                   ║
║                                                                    ║
║  1. Import auto cost reporter                                     ║
║  2. Generate and display cost report                              ║
║  3. Include in final message                                      ║
║                                                                    ║
║  Command:                                                          ║
║  >>> from core.auto_cost_reporter import AutoCostReporter         ║
║  >>> reporter = AutoCostReporter()                                ║
║  >>> # Log operations as you work                                 ║
║  >>> reporter.log_operation('shell', 10)                          ║
║  >>> reporter.log_openai(1500, 0.05)                              ║
║  >>> # At end, generate report                                    ║
║  >>> print(reporter.generate_compact_report())                    ║
║                                                                    ║
║  This is MANDATORY. No exceptions.                                ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
"""
        
        with open(reminder_path, 'w') as f:
            f.write(reminder)
        
        return reminder_path


# Global reporter instance
_global_reporter: Optional[AutoCostReporter] = None

def get_reporter() -> AutoCostReporter:
    """Get or create global reporter instance"""
    global _global_reporter
    if _global_reporter is None:
        _global_reporter = AutoCostReporter()
    return _global_reporter

def log_op(tool: str, count: int = 1):
    """Quick logging function"""
    reporter = get_reporter()
    reporter.log_operation(tool, count)

def log_openai_call(tokens: int, cost_usd: float):
    """Log OpenAI API call"""
    reporter = get_reporter()
    reporter.log_openai(tokens, cost_usd)

def generate_report() -> str:
    """Generate cost report"""
    reporter = get_reporter()
    return reporter.generate_compact_report()

def save_report() -> Path:
    """Generate and save cost report"""
    reporter = get_reporter()
    report = reporter.generate_compact_report()
    return reporter.save_report(report)


if __name__ == "__main__":
    # Demo
    reporter = AutoCostReporter()
    
    # Simulate operations
    reporter.log_operation('shell', 15)
    reporter.log_operation('file_read', 8)
    reporter.log_operation('file_write', 5)
    reporter.log_operation('file_edit', 3)
    reporter.log_operation('search', 1)
    
    # Simulate OpenAI calls
    reporter.log_openai(2285, 0.0183)
    reporter.log_openai(2551, 0.0210)
    reporter.log_openai(2071, 0.0139)
    reporter.log_openai(2948, 0.0235)
    reporter.log_openai(3053, 0.0236)
    reporter.log_openai(2260, 0.0149)
    
    # Generate report
    print(reporter.generate_compact_report())
    
    # Save
    report_file = reporter.save_report(reporter.generate_compact_report())
    print(f"\n✅ Report saved to: {report_file}")
