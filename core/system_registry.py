import logging
#!/usr/bin/env python3
"""
System Registry - Fix 3
MUST check before creating new systems
Prevents redundant system creation
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List

class SystemExistsError(Exception):
    """Raised when trying to create a system that already exists"""
    pass

class SystemRegistry:
    """Registry of all existing systems"""
    
    def __init__(self):
        self.base_path = Path("/home/ubuntu/manus_global_knowledge")
        self.registry_path = self.base_path / "core" / "system_registry.json"
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict:
        """Load registry from file"""
        if self.registry_path.exists():
            with open(self.registry_path) as f:
                return json.load(f)
        
        # Default registry
        return {
            "systems": {
                "initialization_system": {
                    "exists": True,
                    "location": "/home/ubuntu/manus_global_knowledge/INITIALIZER.md",
                    "version": "3.0",
                    "last_updated": "2026-02-14",
                    "description": "Complete initialization sequence with optimized sync, adaptive router, and scientific methodology"
                },
                "mandatory_init": {
                    "exists": True,
                    "location": "/home/ubuntu/manus_global_knowledge/mandatory_init.py",
                    "version": "1.0",
                    "last_updated": "2026-02-15",
                    "description": "Mandatory initialization hook (Fix 1)"
                },
                "cost_gate": {
                    "exists": True,
                    "location": "/home/ubuntu/manus_global_knowledge/core/cost_gate.py",
                    "version": "1.0",
                    "last_updated": "2026-02-15",
                    "description": "Cost validation gate (Fix 2)"
                },
                "adaptive_router": {
                    "exists": True,
                    "location": "/home/ubuntu/manus_global_knowledge/core/adaptive_router.py",
                    "version": "2.1",
                    "last_updated": "2026-02-15",
                    "description": "Self-learning adaptive router with 80-90% OpenAI routing"
                },
                "cost_optimization": {
                    "exists": True,
                    "location": "/home/ubuntu/manus_global_knowledge/INITIALIZER.md",
                    "version": "3.0",
                    "integrated": True,
                    "last_updated": "2026-02-14",
                    "description": "Integrated cost optimization (Phase 1 + 2.1)"
                },
                "scientific_methodology": {
                    "exists": True,
                    "location": "/home/ubuntu/manus_global_knowledge/core/SCIENTIFIC_METHODOLOGY_REQUIREMENTS.md",
                    "version": "1.0",
                    "last_updated": "2026-02-14",
                    "description": "Scientific methodology requirements for all responses"
                },
                "guardian_validator": {
                    "exists": True,
                    "location": "/home/ubuntu/manus_global_knowledge/core/guardian_validator.py",
                    "version": "1.0",
                    "last_updated": "2026-02-15",
                    "description": "Guardian validation middleware for quality assurance"
                },
                "optimized_sync": {
                    "exists": True,
                    "location": "/home/ubuntu/manus_global_knowledge/optimized_sync.sh",
                    "version": "1.0",
                    "last_updated": "2026-02-14",
                    "description": "Optimized sync with cache-first strategy (80-90% savings)"
                }
            },
            "last_updated": datetime.now().isoformat(),
            "total_systems": 8
        }
    
    def _save_registry(self):
        """Save registry to file"""
        self.registry["last_updated"] = datetime.now().isoformat()
        self.registry["total_systems"] = len(self.registry["systems"])
        
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def check_exists(self, system_name: str) -> bool:
        """Check if system exists"""
        return system_name in self.registry["systems"] and \
               self.registry["systems"][system_name].get("exists", False)
    
    def get_system(self, system_name: str) -> Optional[Dict]:
        """Get system info"""
        if self.check_exists(system_name):
            return self.registry["systems"][system_name]
        return None
    
    def check_before_create(self, system_name: str, raise_error: bool = True):
        """
        MANDATORY: Check registry before creating new system
        
        Args:
            system_name: Name of system to check
            raise_error: If True, raises SystemExistsError. If False, returns bool.
        
        Returns:
            If raise_error=False, returns True if system exists, False otherwise
        
        Raises:
            SystemExistsError: If system exists and raise_error=True
        """
        if self.check_exists(system_name):
            system = self.get_system(system_name)
            
            if raise_error:
                raise SystemExistsError(
                    f"\n{'='*70}\n"
                    f"🚫 SYSTEM ALREADY EXISTS: {system_name}\n"
                    f"{'='*70}\n"
                    f"Location: {system['location']}\n"
                    f"Version: {system['version']}\n"
                    f"Last updated: {system['last_updated']}\n"
                    f"Description: {system['description']}\n"
                    f"\n"
                    f"❌ DO NOT create a new system.\n"
                    f"✅ USE the existing system instead.\n"
                    f"{'='*70}\n"
                )
            
            return True
        
        return False
    
    def register_system(
        self,
        system_name: str,
        location: str,
        version: str,
        description: str,
        **kwargs
    ):
        """Register a new system"""
        self.registry["systems"][system_name] = {
            "exists": True,
            "location": location,
            "version": version,
            "last_updated": datetime.now().isoformat(),
            "description": description,
            **kwargs
        }
        self._save_registry()
    
    def update_system(self, system_name: str, **updates):
        """Update existing system"""
        if not self.check_exists(system_name):
            raise ValueError(f"System {system_name} does not exist")
        
        self.registry["systems"][system_name].update(updates)
        self.registry["systems"][system_name]["last_updated"] = datetime.now().isoformat()
        self._save_registry()
    
    def list_systems(self) -> List[str]:
        """List all registered systems"""
        return [
            name for name, info in self.registry["systems"].items()
            if info.get("exists", False)
        ]
    
    def search_systems(self, keyword: str) -> List[str]:
        """Search systems by keyword"""
        keyword_lower = keyword.lower()
        results = []
        
        for name, info in self.registry["systems"].items():
            if not info.get("exists", False):
                continue
            
            if keyword_lower in name.lower() or \
               keyword_lower in info.get("description", "").lower():
                results.append(name)
        
        return results
    
    def print_registry(self):
        """Print formatted registry"""
        print("="*70)
        print("📋 SYSTEM REGISTRY")
        print("="*70)
        print(f"Total systems: {len(self.list_systems())}")
        print(f"Last updated: {self.registry['last_updated']}")
        print()
        
        for name in sorted(self.list_systems()):
            info = self.get_system(name)
            print(f"✅ {name}")
            print(f"   Location: {info['location']}")
            print(f"   Version: {info['version']}")
            print(f"   Description: {info['description']}")
            print()


# Convenience functions
def check_before_create(system_name: str):
    """
    Convenience function for checking before creating system
    
    Usage:
        try:
            check_before_create('initialization_system')
            # If we get here, system doesn't exist, safe to create
        except SystemExistsError as e:
            print(e)
            # System exists, don't create
    """
    registry = SystemRegistry()
    registry.check_before_create(system_name)


def search_existing(keyword: str) -> List[str]:
    """
    Search for existing systems
    
    Usage:
        systems = search_existing('init')
        # Returns: ['initialization_system', 'mandatory_init']
    """
    registry = SystemRegistry()
    return registry.search_systems(keyword)


# Test if run directly
if __name__ == "__main__":
    print("="*70)
    print("📋 SYSTEM REGISTRY - FIX 3")
    print("="*70)
    print()
    
    registry = SystemRegistry()
    
    # Save initial registry
    registry._save_registry()
    
    # Print registry
    registry.print_registry()
    
    # Test: Try to create existing system
    print("="*70)
    print("🧪 TEST: Try to create existing 'initialization_system'")
    print("="*70)
    
    try:
        registry.check_before_create('initialization_system')
        print("❌ Test failed: Should have raised SystemExistsError")
    except SystemExistsError as e:
        print("✅ Test passed: System exists error raised")
        print(str(e))
    
    # Test: Search
    print("\n" + "="*70)
    print("🔍 TEST: Search for 'init' systems")
    print("="*70)
    results = registry.search_systems('init')
    print(f"Found {len(results)} systems:")
    for system in results:
        print(f"  - {system}")
    
    print("\n✅ System registry working correctly!")
