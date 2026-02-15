#!/usr/bin/env python3
"""
Mandatory Initialization Hook - Fix 1
MUST run before ANY other action
Blocks execution until complete
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

class MandatoryInit:
    """Enforces mandatory initialization sequence"""
    
    def __init__(self):
        self.base_path = Path("/home/ubuntu/manus_global_knowledge")
        self.init_log = self.base_path / "metrics" / "init_log.json"
        self.errors = []
        
    def log_init(self, status, details):
        """Log initialization attempt"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "details": details,
            "errors": self.errors
        }
        
        self.init_log.parent.mkdir(parents=True, exist_ok=True)
        
        # Append to log
        logs = []
        if self.init_log.exists():
            with open(self.init_log) as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(self.init_log, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def check_file_exists(self, filepath, description):
        """Verify critical file exists"""
        if not filepath.exists():
            error = f"CRITICAL: {description} not found at {filepath}"
            self.errors.append(error)
            return False
        return True
    
    def run(self):
        """Execute mandatory initialization sequence"""
        
        print("="*70)
        print("🔒 MANDATORY INITIALIZATION - FIX 1")
        print("="*70)
        print("This MUST complete before any other action.\n")
        
        # Step 1: Verify critical files exist
        print("Step 1: Verifying critical files...")
        
        critical_files = {
            self.base_path / "INITIALIZER.md": "INITIALIZER",
            self.base_path / "MASTER_INDEX.md": "MASTER_INDEX",
            self.base_path / "core" / "adaptive_router.py": "Adaptive Router",
            self.base_path / "core" / "SCIENTIFIC_METHODOLOGY_REQUIREMENTS.md": "Scientific Methodology"
        }
        
        all_exist = True
        for filepath, description in critical_files.items():
            if self.check_file_exists(filepath, description):
                print(f"  ✅ {description}")
            else:
                print(f"  ❌ {description}")
                all_exist = False
        
        if not all_exist:
            print("\n❌ INITIALIZATION FAILED: Critical files missing")
            self.log_init("FAILED", "Critical files missing")
            return EXIT_FAILURE
        
        # Step 2: Run optimized sync
        print("\nStep 2: Running optimized sync...")
        
        sync_script = self.base_path / "optimized_sync.sh"
        if sync_script.exists():
            import subprocess
            result = subprocess.run(
                ["bash", str(sync_script), "pull"],
                cwd=str(self.base_path),
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("  ✅ Knowledge base synced")
            else:
                print(f"  ⚠️  Sync warning: {result.stderr[:100]}")
                # Don't fail on sync warning, just log it
        else:
            print("  ⚠️  optimized_sync.sh not found, skipping")
        
        # Step 3: Load INITIALIZER.md
        print("\nStep 3: Loading INITIALIZER.md...")
        
        initializer_path = self.base_path / "INITIALIZER.md"
        try:
            with open(initializer_path) as f:
                initializer_content = f.read()
            print(f"  ✅ INITIALIZER loaded ({len(initializer_content)} bytes)")
        except Exception as e:
            error = f"Failed to load INITIALIZER: {e}"
            self.errors.append(error)
            print(f"  ❌ {error}")
            self.log_init("FAILED", "Could not load INITIALIZER")
            return EXIT_FAILURE
        
        # Step 4: Initialize adaptive router
        print("\nStep 4: Initializing adaptive router...")
        
        sys.path.insert(0, str(self.base_path / "core"))
        try:
            from adaptive_router import AdaptiveRouter
            router = AdaptiveRouter()
            stats = router.get_statistics()
            print(f"  ✅ Router initialized")
            print(f"     - OpenAI routing: {stats.get('openai_percentage', 0)}%")
            print(f"     - Learning: {'ENABLED' if stats.get('learning_enabled') else 'Collecting data'}")
        except Exception as e:
            error = f"Failed to initialize router: {e}"
            self.errors.append(error)
            print(f"  ⚠️  {error}")
            # Don't fail on router error, just warn
        
        # Step 5: Load scientific methodology
        print("\nStep 5: Loading scientific methodology...")
        
        methodology_path = self.base_path / "core" / "SCIENTIFIC_METHODOLOGY_REQUIREMENTS.md"
        try:
            with open(methodology_path) as f:
                methodology = f.read()
            print(f"  ✅ Scientific methodology loaded")
        except Exception as e:
            error = f"Failed to load methodology: {e}"
            self.errors.append(error)
            print(f"  ⚠️  {error}")
        
        # Step 6: Set environment flags
        print("\nStep 6: Setting environment flags...")
        
        os.environ['MANUS_INITIALIZED'] = 'true'
        os.environ['MANUS_INIT_TIMESTAMP'] = datetime.now().isoformat()
        print("  ✅ Environment flags set")
        
        # Success
        print("\n" + "="*70)
        print("✅ MANDATORY INITIALIZATION COMPLETE")
        print("="*70)
        print("Agent is now ready to process tasks.\n")
        
        self.log_init("SUCCESS", "All steps completed")
        return EXIT_SUCCESS

def main():
    """Entry point"""
    init = MandatoryInit()
    exit_code = init.run()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
