#!/usr/bin/env python3.11
"""
Automatic API Key Monitoring
Runs periodic health checks and sends alerts
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from key_manager import APIKeyManager
from datetime import datetime
import json

class AutoMonitor:
    """Automatic monitoring system for API keys"""
    
    def __init__(self):
        self.manager = APIKeyManager()
        self.alert_log_path = Path.home() / ".api_keys" / "alerts.json"
    
    def check_and_alert(self):
        """Run health check and generate alerts if needed"""
        print(f"🔍 Auto Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        results = self.manager.validate_all()
        alerts = []
        
        for service, result in results.items():
            if not result.get("valid"):
                alert = {
                    "service": service,
                    "timestamp": datetime.now().isoformat(),
                    "status": "CRITICAL",
                    "message": f"{service} API key is invalid or expired",
                    "details": result.get("details", "Unknown error")
                }
                alerts.append(alert)
                self.print_alert(alert)
        
        if alerts:
            self.save_alerts(alerts)
            return False
        else:
            print("✅ All API keys are healthy!")
            return True
    
    def print_alert(self, alert):
        """Print formatted alert"""
        print(f"\n🚨 ALERT: {alert['service'].upper()}")
        print(f"   Status: {alert['status']}")
        print(f"   Message: {alert['message']}")
        print(f"   Details: {alert['details']}")
        print(f"   Time: {alert['timestamp']}")
    
    def save_alerts(self, alerts):
        """Save alerts to log file"""
        all_alerts = []
        if self.alert_log_path.exists():
            with open(self.alert_log_path) as f:
                all_alerts = json.load(f)
        
        all_alerts.extend(alerts)
        all_alerts = all_alerts[-100:]  # Keep last 100 alerts
        
        with open(self.alert_log_path, 'w') as f:
            json.dump(all_alerts, f, indent=2)
    
    def get_recent_alerts(self, count=10):
        """Get recent alerts"""
        if not self.alert_log_path.exists():
            return []
        
        with open(self.alert_log_path) as f:
            alerts = json.load(f)
        
        return alerts[-count:]


def main():
    """Run automatic monitoring"""
    monitor = AutoMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == "recent":
        alerts = monitor.get_recent_alerts()
        if alerts:
            print("Recent Alerts:")
            for alert in alerts:
                monitor.print_alert(alert)
        else:
            print("No recent alerts")
    else:
        monitor.check_and_alert()


if __name__ == "__main__":
    main()
