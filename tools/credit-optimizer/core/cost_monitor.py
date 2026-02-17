#!/usr/bin/env python3
"""
Cost Monitoring Dashboard and Alerts
Real-time monitoring and alerting for cost control

Features:
- Real-time cost tracking
- Budget alerts
- Anomaly notifications
- Performance dashboards
- Daily/weekly reports

Author: Manus AI
Date: 2026-02-16
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict


class CostMonitor:
    """
    Monitors costs and generates alerts
    """
    
    def __init__(self, base_path: str = "/home/ubuntu/manus_global_knowledge"):
        """
        Initialize cost monitor
        
        Args:
            base_path: Base path for logs and data
        """
        self.base_path = Path(base_path)
        self.logs_dir = self.base_path / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        self.cost_log = self.logs_dir / "cost_tracking.jsonl"
        self.alerts_log = self.logs_dir / "alerts.jsonl"
        
        # Budget configuration
        self.budgets = {
            'daily': 5.00,    # $5 per day
            'weekly': 30.00,  # $30 per week
            'monthly': 120.00  # $120 per month
        }
        
        # Alert thresholds (percentage of budget)
        self.alert_thresholds = {
            'warning': 0.75,   # 75% of budget
            'critical': 0.90,  # 90% of budget
            'exceeded': 1.00   # 100% of budget
        }
        
        # Alert state (to avoid duplicate alerts)
        self.alert_state = {
            'daily': {'warning': False, 'critical': False, 'exceeded': False},
            'weekly': {'warning': False, 'critical': False, 'exceeded': False},
            'monthly': {'warning': False, 'critical': False, 'exceeded': False}
        }
    
    def _load_costs(self, hours: int = None, days: int = None) -> List[Dict]:
        """
        Load costs from log
        
        Args:
            hours: Number of hours to look back
            days: Number of days to look back
            
        Returns:
            List of cost entries
        """
        if not self.cost_log.exists():
            return []
        
        if hours:
            cutoff = datetime.now() - timedelta(hours=hours)
        elif days:
            cutoff = datetime.now() - timedelta(days=days)
        else:
            cutoff = datetime.min
        
        entries = []
        
        try:
            with open(self.cost_log, 'r') as f:
                for line in f:
                    entry = json.loads(line)
                    entry_time = datetime.fromisoformat(entry['timestamp'])
                    
                    if entry_time > cutoff:
                        entries.append(entry)
        except Exception as e:
            print(f"⚠️ Warning: Failed to load cost log: {e}")
        
        return entries
    
    def get_current_spending(self) -> Dict:
        """
        Get current spending across different time periods
        
        Returns:
            Dict with spending by period
        """
        now = datetime.now()
        
        # Get costs for different periods
        daily_costs = self._load_costs(hours=24)
        weekly_costs = self._load_costs(days=7)
        monthly_costs = self._load_costs(days=30)
        
        spending = {
            'daily': {
                'spent': sum(e['cost'] for e in daily_costs),
                'saved': sum(e.get('saved', 0) for e in daily_costs),
                'budget': self.budgets['daily'],
                'operations': len(daily_costs)
            },
            'weekly': {
                'spent': sum(e['cost'] for e in weekly_costs),
                'saved': sum(e.get('saved', 0) for e in weekly_costs),
                'budget': self.budgets['weekly'],
                'operations': len(weekly_costs)
            },
            'monthly': {
                'spent': sum(e['cost'] for e in monthly_costs),
                'saved': sum(e.get('saved', 0) for e in monthly_costs),
                'budget': self.budgets['monthly'],
                'operations': len(monthly_costs)
            }
        }
        
        # Calculate percentages
        for period in spending:
            spent = spending[period]['spent']
            budget = spending[period]['budget']
            spending[period]['percentage'] = (spent / budget * 100) if budget > 0 else 0
            spending[period]['remaining'] = max(0, budget - spent)
        
        return spending
    
    def check_budgets(self) -> List[Dict]:
        """
        Check if budgets are exceeded and generate alerts
        
        Returns:
            List of alerts
        """
        spending = self.get_current_spending()
        alerts = []
        
        for period, data in spending.items():
            percentage = data['percentage'] / 100
            
            # Check each threshold
            for level, threshold in self.alert_thresholds.items():
                if percentage >= threshold and not self.alert_state[period][level]:
                    # Generate alert
                    alert = {
                        'timestamp': datetime.now().isoformat(),
                        'period': period,
                        'level': level,
                        'spent': data['spent'],
                        'budget': data['budget'],
                        'percentage': data['percentage'],
                        'message': f"{level.upper()}: {period} spending at {data['percentage']:.1f}% of budget (${data['spent']:.2f}/${data['budget']:.2f})"
                    }
                    
                    alerts.append(alert)
                    self.alert_state[period][level] = True
                    self._log_alert(alert)
        
        return alerts
    
    def _log_alert(self, alert: Dict):
        """
        Log alert to file
        
        Args:
            alert: Alert dict
        """
        try:
            with open(self.alerts_log, 'a') as f:
                f.write(json.dumps(alert) + '\n')
        except Exception as e:
            print(f"⚠️ Warning: Failed to log alert: {e}")
    
    def get_recent_alerts(self, hours: int = 24) -> List[Dict]:
        """
        Get recent alerts
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            List of alerts
        """
        if not self.alerts_log.exists():
            return []
        
        cutoff = datetime.now() - timedelta(hours=hours)
        alerts = []
        
        try:
            with open(self.alerts_log, 'r') as f:
                for line in f:
                    alert = json.loads(line)
                    alert_time = datetime.fromisoformat(alert['timestamp'])
                    
                    if alert_time > cutoff:
                        alerts.append(alert)
        except Exception as e:
            print(f"⚠️ Warning: Failed to load alerts: {e}")
        
        return alerts
    
    def get_spending_by_operation(self, hours: int = 24) -> Dict:
        """
        Get spending breakdown by operation
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            Dict with spending by operation
        """
        costs = self._load_costs(hours=hours)
        
        by_operation = defaultdict(lambda: {'cost': 0.0, 'saved': 0.0, 'count': 0, 'tokens': 0})
        
        for entry in costs:
            op = entry['operation']
            by_operation[op]['cost'] += entry['cost']
            by_operation[op]['saved'] += entry.get('saved', 0)
            by_operation[op]['count'] += 1
            by_operation[op]['tokens'] += entry.get('tokens', 0)
        
        return dict(by_operation)
    
    def reset_daily_alerts(self):
        """Reset daily alert state (call at midnight)"""
        self.alert_state['daily'] = {'warning': False, 'critical': False, 'exceeded': False}
    
    def reset_weekly_alerts(self):
        """Reset weekly alert state (call on Monday)"""
        self.alert_state['weekly'] = {'warning': False, 'critical': False, 'exceeded': False}
    
    def reset_monthly_alerts(self):
        """Reset monthly alert state (call on 1st of month)"""
        self.alert_state['monthly'] = {'warning': False, 'critical': False, 'exceeded': False}
    
    def generate_dashboard(self) -> str:
        """
        Generate monitoring dashboard
        
        Returns:
            Dashboard string
        """
        spending = self.get_current_spending()
        alerts = self.get_recent_alerts(hours=24)
        by_operation = self.get_spending_by_operation(hours=24)
        
        dashboard = "╔" + "="*68 + "╗\n"
        dashboard += "║" + " "*20 + "COST MONITORING DASHBOARD" + " "*23 + "║\n"
        dashboard += "╠" + "="*68 + "╣\n"
        
        # Budget status
        dashboard += "║ BUDGET STATUS" + " "*54 + "║\n"
        dashboard += "╠" + "-"*68 + "╣\n"
        
        for period, data in spending.items():
            status = "✅" if data['percentage'] < 75 else "⚠️" if data['percentage'] < 90 else "🔴"
            bar_length = 30
            filled = int(bar_length * min(data['percentage'] / 100, 1.0))
            bar = "█" * filled + "░" * (bar_length - filled)
            
            dashboard += f"║ {status} {period.capitalize():8s} "
            dashboard += f"${data['spent']:6.2f}/${data['budget']:6.2f} "
            dashboard += f"[{bar}] {data['percentage']:5.1f}% ║\n"
        
        dashboard += "╠" + "="*68 + "╣\n"
        
        # Spending by operation (top 5)
        dashboard += "║ TOP OPERATIONS (24h)" + " "*47 + "║\n"
        dashboard += "╠" + "-"*68 + "╣\n"
        
        sorted_ops = sorted(by_operation.items(), key=lambda x: x[1]['cost'], reverse=True)[:5]
        
        if sorted_ops:
            for op, data in sorted_ops:
                dashboard += f"║   {op[:30]:30s} ${data['cost']:6.2f}  ({data['count']:3d} calls) "
                dashboard += " " * (68 - 52 - len(op[:30])) + "║\n"
        else:
            dashboard += "║   No operations recorded" + " "*42 + "║\n"
        
        dashboard += "╠" + "="*68 + "╣\n"
        
        # Recent alerts
        dashboard += "║ RECENT ALERTS (24h)" + " "*48 + "║\n"
        dashboard += "╠" + "-"*68 + "╣\n"
        
        if alerts:
            for alert in alerts[-5:]:  # Show last 5
                level_icon = "🔴" if alert['level'] == 'exceeded' else "⚠️" if alert['level'] == 'critical' else "⚡"
                dashboard += f"║ {level_icon} {alert['message'][:62]:62s} ║\n"
        else:
            dashboard += "║   No alerts" + " "*55 + "║\n"
        
        dashboard += "╚" + "="*68 + "╝\n"
        
        return dashboard
    
    def generate_report(self, period: str = 'daily') -> str:
        """
        Generate detailed cost report
        
        Args:
            period: Report period ('daily', 'weekly', 'monthly')
            
        Returns:
            Report string
        """
        if period == 'daily':
            hours = 24
        elif period == 'weekly':
            hours = 24 * 7
        elif period == 'monthly':
            hours = 24 * 30
        else:
            hours = 24
        
        costs = self._load_costs(hours=hours)
        by_operation = self.get_spending_by_operation(hours=hours)
        spending = self.get_current_spending()
        
        report = "="*70 + "\n"
        report += f"COST REPORT - {period.upper()}\n"
        report += "="*70 + "\n\n"
        
        period_data = spending[period]
        
        report += f"Period:               {period}\n"
        report += f"Total Spent:          ${period_data['spent']:.2f}\n"
        report += f"Total Saved:          ${period_data['saved']:.2f}\n"
        report += f"Budget:               ${period_data['budget']:.2f}\n"
        report += f"Remaining:            ${period_data['remaining']:.2f}\n"
        report += f"Budget Used:          {period_data['percentage']:.1f}%\n"
        report += f"Total Operations:     {period_data['operations']}\n"
        report += "\n"
        
        report += "Spending by Operation:\n"
        report += "-"*70 + "\n"
        
        sorted_ops = sorted(by_operation.items(), key=lambda x: x[1]['cost'], reverse=True)
        
        for op, data in sorted_ops:
            report += f"  {op:30s} ${data['cost']:7.2f}  "
            report += f"({data['count']:4d} calls, {data['tokens']:6d} tokens)\n"
        
        report += "="*70 + "\n"
        
        return report


def main():
    """Test the cost monitor"""
    monitor = CostMonitor()
    
    print("Testing Cost Monitor...")
    print()
    
    # Test 1: Get current spending
    print("Test 1: Current spending")
    spending = monitor.get_current_spending()
    for period, data in spending.items():
        print(f"  {period}: ${data['spent']:.2f}/${data['budget']:.2f} ({data['percentage']:.1f}%)")
    print()
    
    # Test 2: Check budgets
    print("Test 2: Budget check")
    alerts = monitor.check_budgets()
    if alerts:
        for alert in alerts:
            print(f"  {alert['level'].upper()}: {alert['message']}")
    else:
        print("  No alerts")
    print()
    
    # Test 3: Generate dashboard
    print("Test 3: Dashboard")
    print(monitor.generate_dashboard())
    print()
    
    # Test 4: Generate report
    print("Test 4: Report")
    print(monitor.generate_report('daily'))


if __name__ == "__main__":
    main()
