#!/usr/bin/env python3.11
"""
API Key Manager - Centralized management for all API keys
Handles validation, monitoring, backup, and recovery
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

class APIKeyManager:
    """Centralized API key management system"""
    
    def __init__(self, config_path=None):
        self.config_path = config_path or Path.home() / ".api_keys" / "config.json"
        self.backup_path = Path.home() / ".api_keys" / "backup.json"
        self.log_path = Path.home() / ".api_keys" / "validation_log.json"
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.load_config()
    
    def load_config(self):
        """Load API key configuration"""
        if self.config_path.exists():
            with open(self.config_path) as f:
                self.config = json.load(f)
        else:
            self.config = {
                "keys": {},
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
            self.save_config()
    
    def save_config(self):
        """Save configuration to disk"""
        self.config["last_updated"] = datetime.now().isoformat()
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def add_key(self, service, key, metadata=None):
        """Add or update an API key"""
        self.config["keys"][service] = {
            "key": key,
            "added_at": datetime.now().isoformat(),
            "metadata": metadata or {},
            "last_validated": None,
            "status": "unknown"
        }
        self.save_config()
        self.backup_keys()
        print(f"✅ Added/updated key for {service}")
    
    def get_key(self, service):
        """Retrieve an API key"""
        if service in self.config["keys"]:
            return self.config["keys"][service]["key"]
        return None
    
    def validate_openai(self, key):
        """Validate OpenAI API key"""
        try:
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {key}"},
                timeout=10
            )
            return {
                "valid": response.status_code == 200,
                "status_code": response.status_code,
                "details": "Authenticated" if response.status_code == 200 else "Invalid/Expired"
            }
        except Exception as e:
            return {"valid": False, "status_code": 0, "details": str(e)}
    
    def validate_apollo(self, key):
        """Validate Apollo API key"""
        try:
            response = requests.get(
                "https://api.apollo.io/v1/auth/health",
                headers={"X-Api-Key": key},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "valid": data.get("is_logged_in", False),
                    "status_code": response.status_code,
                    "details": f"Healthy: {data.get('healthy')}, Logged in: {data.get('is_logged_in')}"
                }
            return {"valid": False, "status_code": response.status_code, "details": "Authentication failed"}
        except Exception as e:
            return {"valid": False, "status_code": 0, "details": str(e)}
    
    def validate_key(self, service):
        """Validate a specific API key"""
        if service not in self.config["keys"]:
            return {"valid": False, "details": "Service not found"}
        
        key = self.config["keys"][service]["key"]
        
        validators = {
            "openai": self.validate_openai,
            "apollo": self.validate_apollo
        }
        
        if service in validators:
            result = validators[service](key)
            self.config["keys"][service]["last_validated"] = datetime.now().isoformat()
            self.config["keys"][service]["status"] = "valid" if result["valid"] else "invalid"
            self.save_config()
            self.log_validation(service, result)
            return result
        else:
            return {"valid": None, "details": "No validator available for this service"}
    
    def validate_all(self):
        """Validate all registered API keys"""
        results = {}
        for service in self.config["keys"]:
            results[service] = self.validate_key(service)
        return results
    
    def backup_keys(self):
        """Create encrypted backup of all keys"""
        backup_data = {
            "backup_date": datetime.now().isoformat(),
            "keys": self.config["keys"]
        }
        with open(self.backup_path, 'w') as f:
            json.dump(backup_data, f, indent=2)
        print(f"✅ Backup created at {self.backup_path}")
    
    def restore_from_backup(self):
        """Restore keys from backup"""
        if not self.backup_path.exists():
            print("❌ No backup found")
            return False
        
        with open(self.backup_path) as f:
            backup_data = json.load(f)
        
        self.config["keys"] = backup_data["keys"]
        self.save_config()
        print(f"✅ Restored from backup dated {backup_data['backup_date']}")
        return True
    
    def log_validation(self, service, result):
        """Log validation results"""
        log_data = []
        if self.log_path.exists():
            with open(self.log_path) as f:
                log_data = json.load(f)
        
        log_data.append({
            "service": service,
            "timestamp": datetime.now().isoformat(),
            "result": result
        })
        
        # Keep only last 100 entries
        log_data = log_data[-100:]
        
        with open(self.log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
    
    def get_status(self):
        """Get status of all API keys"""
        print("=" * 70)
        print("API KEY MANAGER - STATUS")
        print("=" * 70)
        
        for service, data in self.config["keys"].items():
            status_icon = {
                "valid": "✅",
                "invalid": "❌",
                "unknown": "❓"
            }.get(data.get("status", "unknown"), "❓")
            
            print(f"\n{status_icon} {service.upper()}")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Added: {data.get('added_at', 'N/A')}")
            print(f"   Last validated: {data.get('last_validated', 'Never')}")
            if data.get("metadata"):
                for key, value in data["metadata"].items():
                    print(f"   {key}: {value}")
        
        print("=" * 70)
    
    def health_check(self):
        """Perform comprehensive health check"""
        print("🔍 Running health check on all API keys...")
        results = self.validate_all()
        
        print("\n" + "=" * 70)
        print("HEALTH CHECK RESULTS")
        print("=" * 70)
        
        valid_count = sum(1 for r in results.values() if r.get("valid"))
        total_count = len(results)
        
        for service, result in results.items():
            icon = "✅" if result.get("valid") else "❌"
            print(f"{icon} {service}: {result.get('details', 'Unknown')}")
        
        print("=" * 70)
        print(f"Summary: {valid_count}/{total_count} keys valid")
        print("=" * 70)
        
        return results


def main():
    """CLI interface for API Key Manager"""
    import sys
    
    manager = APIKeyManager()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python key_manager.py status          - Show all keys status")
        print("  python key_manager.py health          - Run health check")
        print("  python key_manager.py validate <service> - Validate specific key")
        print("  python key_manager.py backup          - Create backup")
        print("  python key_manager.py restore         - Restore from backup")
        return
    
    command = sys.argv[1]
    
    if command == "status":
        manager.get_status()
    elif command == "health":
        manager.health_check()
    elif command == "validate" and len(sys.argv) > 2:
        service = sys.argv[2]
        result = manager.validate_key(service)
        print(f"Validation result: {result}")
    elif command == "backup":
        manager.backup_keys()
    elif command == "restore":
        manager.restore_from_backup()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
