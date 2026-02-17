#!/usr/bin/env python3
"""
Automated Deployment Script
Deploys Phase 1 cost optimization to all Apollo production scripts

Author: Manus AI
Date: 2026-02-16
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime


class ProductionDeployer:
    """
    Automated deployment of cost optimization to production scripts
    """
    
    def __init__(self, apollo_dir: str = "/home/ubuntu/ProjetoApollo"):
        """
        Initialize deployer
        
        Args:
            apollo_dir: Directory containing Apollo scripts
        """
        self.apollo_dir = Path(apollo_dir)
        self.backup_dir = Path("/home/ubuntu/backups") / f"apollo_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        self.stats = {
            'total_files': 0,
            'updated_files': 0,
            'skipped_files': 0,
            'errors': []
        }
    
    def find_apollo_scripts(self) -> list:
        """
        Find all Apollo Python scripts
        
        Returns:
            List of script paths
        """
        if not self.apollo_dir.exists():
            print(f"⚠️ Warning: Apollo directory not found: {self.apollo_dir}")
            return []
        
        scripts = []
        for py_file in self.apollo_dir.rglob("*.py"):
            # Skip __pycache__ and test files
            if '__pycache__' in str(py_file) or 'test' in py_file.name.lower():
                continue
            scripts.append(py_file)
        
        return scripts
    
    def backup_file(self, file_path: Path):
        """
        Backup a file before modification
        
        Args:
            file_path: Path to file to backup
        """
        relative_path = file_path.relative_to(self.apollo_dir)
        backup_path = self.backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
    
    def update_script(self, script_path: Path) -> bool:
        """
        Update a script to use Phase 1 optimizer
        
        Args:
            script_path: Path to script
            
        Returns:
            True if updated, False if skipped
        """
        try:
            # Read script
            content = script_path.read_text()
            
            # Check if already using optimizer
            if 'unified_cost_optimizer_v2' in content:
                print(f"  ⏭️  Already updated: {script_path.name}")
                self.stats['skipped_files'] += 1
                return False
            
            # Check if uses requests
            if 'import requests' not in content and 'from requests' not in content:
                print(f"  ⏭️  No requests import: {script_path.name}")
                self.stats['skipped_files'] += 1
                return False
            
            # Backup original
            self.backup_file(script_path)
            
            # Modify content
            modified = self._modify_script_content(content, script_path.stem)
            
            # Write back
            script_path.write_text(modified)
            
            print(f"  ✅ Updated: {script_path.name}")
            self.stats['updated_files'] += 1
            return True
            
        except Exception as e:
            error_msg = f"Error updating {script_path.name}: {e}"
            print(f"  ❌ {error_msg}")
            self.stats['errors'].append(error_msg)
            return False
    
    def _modify_script_content(self, content: str, script_name: str) -> str:
        """
        Modify script content to use Phase 1 optimizer
        
        Args:
            content: Original script content
            script_name: Name of script (for operation naming)
            
        Returns:
            Modified content
        """
        lines = content.split('\n')
        modified_lines = []
        
        # Track if we've added imports
        imports_added = False
        requests_import_found = False
        
        for i, line in enumerate(lines):
            # Add optimizer import after requests import
            if not imports_added and ('import requests' in line or 'from requests' in line):
                modified_lines.append(line)
                requests_import_found = True
                
                # Add optimizer imports
                modified_lines.append('')
                modified_lines.append('# Cost Optimization - Phase 1')
                modified_lines.append('import sys')
                modified_lines.append('from pathlib import Path')
                modified_lines.append('sys.path.insert(0, "/home/ubuntu/manus_global_knowledge/core")')
                modified_lines.append('from unified_cost_optimizer_v2 import optimized_post, print_optimization_stats')
                modified_lines.append('')
                
                imports_added = True
                continue
            
            # Replace requests.post with optimized_post
            if 'requests.post(' in line and not line.strip().startswith('#'):
                # Extract the requests.post call
                modified_line = line.replace('requests.post(', f'optimized_post(')
                
                # Try to add operation parameter
                # This is a simple heuristic - may need manual adjustment
                if 'operation=' not in modified_line:
                    # Insert operation parameter after URL
                    modified_line = re.sub(
                        r'optimized_post\(([^,]+),',
                        f'optimized_post(\\1, operation="{script_name}",',
                        modified_line
                    )
                
                modified_lines.append(modified_line)
                continue
            
            # Add stats printing at the end of main execution
            if line.strip().startswith('if __name__') and i < len(lines) - 1:
                modified_lines.append(line)
                # Find the end of the main block and add stats
                # This is simplified - may need adjustment
                continue
            
            modified_lines.append(line)
        
        # Add stats printing at the very end if not already added
        if imports_added:
            modified_lines.append('')
            modified_lines.append('# Print cost optimization statistics')
            modified_lines.append('try:')
            modified_lines.append('    print("\\n" + "="*70)')
            modified_lines.append('    print_optimization_stats()')
            modified_lines.append('except:')
            modified_lines.append('    pass  # Stats not available')
        
        return '\n'.join(modified_lines)
    
    def deploy(self):
        """
        Deploy Phase 1 to all Apollo scripts
        """
        print("="*70)
        print("APOLLO SCRIPTS - PHASE 1 DEPLOYMENT")
        print("="*70)
        print()
        
        # Find scripts
        print("Finding Apollo scripts...")
        scripts = self.find_apollo_scripts()
        self.stats['total_files'] = len(scripts)
        
        if not scripts:
            print("⚠️ No Apollo scripts found!")
            return
        
        print(f"Found {len(scripts)} Python scripts")
        print()
        
        # Update each script
        print("Updating scripts...")
        print("-"*70)
        
        for script in scripts:
            self.update_script(script)
        
        print("-"*70)
        print()
        
        # Print summary
        print("="*70)
        print("DEPLOYMENT SUMMARY")
        print("="*70)
        print(f"Total Files:          {self.stats['total_files']}")
        print(f"Updated Files:        {self.stats['updated_files']}")
        print(f"Skipped Files:        {self.stats['skipped_files']}")
        print(f"Errors:               {len(self.stats['errors'])}")
        print()
        
        if self.stats['errors']:
            print("Errors:")
            for error in self.stats['errors']:
                print(f"  - {error}")
            print()
        
        print(f"Backup Location:      {self.backup_dir}")
        print()
        
        if self.stats['updated_files'] > 0:
            print("✅ DEPLOYMENT SUCCESSFUL")
            print(f"   {self.stats['updated_files']} scripts updated with Phase 1 optimization")
        else:
            print("⚠️ NO FILES UPDATED")
            print("   All scripts may already be using the optimizer")
        
        print("="*70)
    
    def rollback(self):
        """
        Rollback deployment (restore from backup)
        """
        print("="*70)
        print("ROLLBACK DEPLOYMENT")
        print("="*70)
        print()
        
        if not self.backup_dir.exists():
            print("❌ No backup found!")
            return
        
        print(f"Restoring from: {self.backup_dir}")
        print()
        
        restored = 0
        for backup_file in self.backup_dir.rglob("*.py"):
            relative_path = backup_file.relative_to(self.backup_dir)
            original_path = self.apollo_dir / relative_path
            
            try:
                shutil.copy2(backup_file, original_path)
                print(f"  ✅ Restored: {relative_path}")
                restored += 1
            except Exception as e:
                print(f"  ❌ Error restoring {relative_path}: {e}")
        
        print()
        print(f"✅ Rollback complete: {restored} files restored")
        print("="*70)


def main():
    """Main deployment function"""
    deployer = ProductionDeployer()
    
    # Check if Apollo directory exists
    if not deployer.apollo_dir.exists():
        print("="*70)
        print("APOLLO DIRECTORY NOT FOUND")
        print("="*70)
        print()
        print(f"Expected location: {deployer.apollo_dir}")
        print()
        print("Please ensure the Apollo scripts are in the correct location.")
        print("="*70)
        return
    
    # Deploy
    deployer.deploy()


if __name__ == "__main__":
    main()
