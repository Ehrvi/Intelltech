#!/usr/bin/env python3
"""
Real-Time Monitoring Dashboard
Continuous monitoring and reporting for cost optimization system

Features:
- Real-time cost tracking
- Live dashboard updates
- Automated daily/weekly reports
- Alert notifications

Author: Manus AI
Date: 2026-02-16
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent))

from unified_cost_optimizer_v2 import get_optimizer
from cost_monitor import CostMonitor
from anomaly_detector import AnomalyDetector


class MonitoringDashboard:
    """
    Real-time monitoring dashboard
    """
    
    def __init__(self):
        """Initialize dashboard"""
        self.optimizer = get_optimizer()
        self.monitor = CostMonitor()
        self.anomaly_detector = AnomalyDetector()
        
        self.reports_dir = Path("/home/ubuntu/manus_global_knowledge/reports")
        self.reports_dir.mkdir(exist_ok=True)
    
    def display_dashboard(self):
        """Display real-time dashboard"""
        # Clear screen (works on Unix-like systems)
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("╔" + "="*78 + "╗")
        print("║" + " "*20 + "COST OPTIMIZATION MONITORING DASHBOARD" + " "*20 + "║")
        print("║" + " "*25 + f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + " "*24 + "║")
        print("╠" + "="*78 + "╣")
        print()
        
        # Budget status
        print(self.monitor.generate_dashboard())
        print()
        
        # Optimizer stats
        stats = self.optimizer.get_stats()
        
        print("╔" + "="*78 + "╗")
        print("║" + " "*25 + "OPTIMIZATION PERFORMANCE" + " "*28 + "║")
        print("╠" + "="*78 + "╣")
        print(f"║ Total API Calls:        {stats['total_calls']:8d}                                        ║")
        print(f"║ Cache Hit Rate:         {stats.get('cache_hit_rate', 0):7.1f}%                                        ║")
        print(f"║ Optimization Rate:      {stats.get('optimization_rate', 0):7.1f}%                                        ║")
        print(f"║ Anomaly Rate:           {stats.get('anomaly_rate', 0):7.1f}%                                        ║")
        print(f"║ Estimated Savings:      ${stats.get('estimated_cost_savings_usd', 0):7.2f}                                      ║")
        print("╚" + "="*78 + "╝")
        print()
        
        # Recent anomalies
        anomalies = self.anomaly_detector.get_recent_anomalies(hours=1)
        
        if anomalies:
            print("╔" + "="*78 + "╗")
            print("║" + " "*28 + "RECENT ANOMALIES (1h)" + " "*29 + "║")
            print("╠" + "="*78 + "╣")
            
            for anomaly in anomalies[-5:]:
                severity_icon = "🔴" if anomaly['severity'] > 0.7 else "⚠️"
                timestamp = anomaly['timestamp'][11:19]  # HH:MM:SS
                print(f"║ {severity_icon} [{timestamp}] {anomaly['operation'][:30]:30s} ${anomaly['cost']:6.4f}           ║")
            
            print("╚" + "="*78 + "╝")
            print()
        
        # Recent alerts
        alerts = self.monitor.get_recent_alerts(hours=1)
        
        if alerts:
            print("╔" + "="*78 + "╗")
            print("║" + " "*30 + "RECENT ALERTS (1h)" + " "*31 + "║")
            print("╠" + "="*78 + "╣")
            
            for alert in alerts[-5:]:
                level_icon = "🔴" if alert['level'] == 'exceeded' else "⚠️" if alert['level'] == 'critical' else "⚡"
                timestamp = alert['timestamp'][11:19]  # HH:MM:SS
                print(f"║ {level_icon} [{timestamp}] {alert['message'][:60]:60s} ║")
            
            print("╚" + "="*78 + "╝")
            print()
        
        print("Press Ctrl+C to exit monitoring")
    
    def generate_daily_report(self):
        """Generate daily cost report"""
        report_file = self.reports_dir / f"daily_report_{datetime.now().strftime('%Y%m%d')}.md"
        
        report = f"# Daily Cost Report - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        # Get spending data
        spending = self.monitor.get_current_spending()
        daily = spending['daily']
        
        report += "## Summary\n\n"
        report += f"- **Total Spent:** ${daily['spent']:.2f}\n"
        report += f"- **Budget:** ${daily['budget']:.2f}\n"
        report += f"- **Remaining:** ${daily['remaining']:.2f}\n"
        report += f"- **Budget Used:** {daily['percentage']:.1f}%\n"
        report += f"- **Operations:** {daily['operations']}\n"
        report += f"- **Savings:** ${daily['saved']:.2f}\n\n"
        
        # Get optimizer stats
        stats = self.optimizer.get_stats()
        
        report += "## Performance\n\n"
        report += f"- **Cache Hit Rate:** {stats.get('cache_hit_rate', 0):.1f}%\n"
        report += f"- **Optimization Rate:** {stats.get('optimization_rate', 0):.1f}%\n"
        report += f"- **Anomaly Rate:** {stats.get('anomaly_rate', 0):.1f}%\n"
        report += f"- **Estimated Savings:** ${stats.get('estimated_cost_savings_usd', 0):.2f}\n\n"
        
        # Top operations
        by_operation = self.monitor.get_spending_by_operation(hours=24)
        
        if by_operation:
            report += "## Top Operations\n\n"
            report += "| Operation | Cost | Calls | Tokens |\n"
            report += "|---|---|---|---|\n"
            
            sorted_ops = sorted(by_operation.items(), key=lambda x: x[1]['cost'], reverse=True)[:10]
            for op, data in sorted_ops:
                report += f"| {op} | ${data['cost']:.2f} | {data['count']} | {data['tokens']} |\n"
            
            report += "\n"
        
        # Anomalies
        anomalies = self.anomaly_detector.get_recent_anomalies(hours=24)
        
        if anomalies:
            report += "## Anomalies Detected\n\n"
            report += f"Total: {len(anomalies)}\n\n"
            
            critical = [a for a in anomalies if a['severity'] > 0.7]
            if critical:
                report += f"### Critical ({len(critical)})\n\n"
                for anomaly in critical[:10]:
                    report += f"- **{anomaly['operation']}** (${anomaly['cost']:.4f}): {anomaly['reason']}\n"
                report += "\n"
        
        # Alerts
        alerts = self.monitor.get_recent_alerts(hours=24)
        
        if alerts:
            report += "## Budget Alerts\n\n"
            for alert in alerts:
                report += f"- **{alert['level'].upper()}** ({alert['period']}): {alert['message']}\n"
            report += "\n"
        
        report += "---\n"
        report += f"*Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        # Save report
        report_file.write_text(report)
        
        return report_file
    
    def generate_weekly_report(self):
        """Generate weekly cost report"""
        report_file = self.reports_dir / f"weekly_report_{datetime.now().strftime('%Y%m%d')}.md"
        
        report = f"# Weekly Cost Report - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        # Get spending data
        spending = self.monitor.get_current_spending()
        weekly = spending['weekly']
        
        report += "## Summary\n\n"
        report += f"- **Total Spent:** ${weekly['spent']:.2f}\n"
        report += f"- **Budget:** ${weekly['budget']:.2f}\n"
        report += f"- **Remaining:** ${weekly['remaining']:.2f}\n"
        report += f"- **Budget Used:** {weekly['percentage']:.1f}%\n"
        report += f"- **Operations:** {weekly['operations']}\n"
        report += f"- **Savings:** ${weekly['saved']:.2f}\n\n"
        
        # Get optimizer stats
        stats = self.optimizer.get_stats()
        
        report += "## Performance\n\n"
        report += f"- **Cache Hit Rate:** {stats.get('cache_hit_rate', 0):.1f}%\n"
        report += f"- **Optimization Rate:** {stats.get('optimization_rate', 0):.1f}%\n"
        report += f"- **Anomaly Rate:** {stats.get('anomaly_rate', 0):.1f}%\n"
        report += f"- **Estimated Savings:** ${stats.get('estimated_cost_savings_usd', 0):.2f}\n\n"
        
        # Top operations
        by_operation = self.monitor.get_spending_by_operation(hours=24*7)
        
        if by_operation:
            report += "## Top Operations\n\n"
            report += "| Operation | Cost | Calls | Tokens |\n"
            report += "|---|---|---|---|\n"
            
            sorted_ops = sorted(by_operation.items(), key=lambda x: x[1]['cost'], reverse=True)[:20]
            for op, data in sorted_ops:
                report += f"| {op} | ${data['cost']:.2f} | {data['count']} | {data['tokens']} |\n"
            
            report += "\n"
        
        report += "---\n"
        report += f"*Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        # Save report
        report_file.write_text(report)
        
        return report_file
    
    def run_continuous_monitoring(self, refresh_interval: int = 60):
        """
        Run continuous monitoring with periodic updates
        
        Args:
            refresh_interval: Seconds between updates
        """
        print("Starting continuous monitoring...")
        print(f"Refresh interval: {refresh_interval} seconds")
        print()
        
        try:
            while True:
                self.display_dashboard()
                time.sleep(refresh_interval)
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")
            print()
    
    def run_scheduled_reports(self):
        """Run scheduled daily and weekly reports"""
        last_daily = None
        last_weekly = None
        
        print("Starting scheduled reporting...")
        print("Daily reports: Every day at midnight")
        print("Weekly reports: Every Monday at midnight")
        print()
        
        try:
            while True:
                now = datetime.now()
                
                # Check if we should generate daily report
                if last_daily is None or now.date() > last_daily:
                    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Generating daily report...")
                    report_file = self.generate_daily_report()
                    print(f"  ✅ Saved to: {report_file}")
                    last_daily = now.date()
                
                # Check if we should generate weekly report (Monday)
                if now.weekday() == 0 and (last_weekly is None or now.date() > last_weekly):
                    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Generating weekly report...")
                    report_file = self.generate_weekly_report()
                    print(f"  ✅ Saved to: {report_file}")
                    last_weekly = now.date()
                
                # Sleep for 1 hour
                time.sleep(3600)
        
        except KeyboardInterrupt:
            print("\n\nScheduled reporting stopped by user")
            print()


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Cost Optimization Monitoring Dashboard')
    parser.add_argument('--mode', choices=['dashboard', 'daily', 'weekly', 'scheduled'], 
                       default='dashboard', help='Monitoring mode')
    parser.add_argument('--refresh', type=int, default=60, 
                       help='Dashboard refresh interval in seconds')
    
    args = parser.parse_args()
    
    dashboard = MonitoringDashboard()
    
    if args.mode == 'dashboard':
        dashboard.run_continuous_monitoring(refresh_interval=args.refresh)
    elif args.mode == 'daily':
        report_file = dashboard.generate_daily_report()
        print(f"✅ Daily report generated: {report_file}")
    elif args.mode == 'weekly':
        report_file = dashboard.generate_weekly_report()
        print(f"✅ Weekly report generated: {report_file}")
    elif args.mode == 'scheduled':
        dashboard.run_scheduled_reports()


if __name__ == "__main__":
    main()
