#!/usr/bin/env python3
"""
Automated Cost Optimization Integration Tool
Integrates cost optimization wrapper into existing Python scripts

Author: Manus AI + MOTHER V5
Date: 2026-02-16
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

class CostOptimizationIntegrator:
    """Automatically integrates cost optimization into Python scripts"""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.stats = {
            'processed': 0,
            'modified': 0,
            'skipped': 0,
            'errors': 0
        }
    
    def integrate_script(self, script_path: Path) -> Tuple[bool, str]:
        """
        Integrate cost optimization into a single script
        
        Returns:
            (success, message)
        """
        try:
            # Read script
            content = script_path.read_text()
            original_content = content
            
            # Check if already integrated
            if 'optimized_api_wrapper' in content or 'optimized_post' in content:
                return (False, "Already integrated")
            
            # Check if script uses requests
            if 'requests.post' not in content and 'requests.get' not in content:
                return (False, "No API calls found")
            
            # Step 1: Add imports
            content = self._add_imports(content)
            
            # Step 2: Replace requests.post with optimized_post
            content = self._replace_api_calls(content)
            
            # Step 3: Add cost reporting at end
            content = self._add_cost_reporting(content)
            
            # Check if anything changed
            if content == original_content:
                return (False, "No changes needed")
            
            # Write back (if not dry run)
            if not self.dry_run:
                # Backup original
                backup_path = script_path.with_suffix('.py.backup')
                backup_path.write_text(original_content)
                
                # Write modified
                script_path.write_text(content)
            
            return (True, "Integrated successfully")
            
        except Exception as e:
            return (False, f"Error: {str(e)}")
    
    def _add_imports(self, content: str) -> str:
        """Add optimization imports"""
        
        # Find the import section
        lines = content.split('\n')
        
        # Find last import line
        last_import_idx = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                last_import_idx = i
        
        if last_import_idx == -1:
            # No imports found, add after shebang/docstring
            insert_idx = 0
            if lines[0].startswith('#!'):
                insert_idx = 1
            if insert_idx < len(lines) and (lines[insert_idx].startswith('"""') or lines[insert_idx].startswith("'''")):
                # Skip docstring
                for i in range(insert_idx + 1, len(lines)):
                    if lines[i].strip().endswith('"""') or lines[i].strip().endswith("'''"):
                        insert_idx = i + 1
                        break
        else:
            insert_idx = last_import_idx + 1
        
        # Add optimization imports
        new_imports = [
            "import sys",
            "from pathlib import Path",
            "",
            "# Cost Optimization Integration",
            "sys.path.insert(0, str(Path(__file__).parent.parent / 'manus_global_knowledge' / 'core'))",
            "from optimized_api_wrapper import optimized_post, print_optimization_stats",
            ""
        ]
        
        # Insert imports
        for imp in reversed(new_imports):
            lines.insert(insert_idx, imp)
        
        return '\n'.join(lines)
    
    def _replace_api_calls(self, content: str) -> str:
        """Replace requests.post with optimized_post"""
        
        # Replace requests.post(
        content = re.sub(
            r'\brequests\.post\(',
            'optimized_post(',
            content
        )
        
        return content
    
    def _add_cost_reporting(self, content: str) -> str:
        """Add cost reporting at end of script"""
        
        # Check if main block exists
        if 'if __name__' in content:
            # Add before the final closing of main block
            lines = content.split('\n')
            
            # Find the main block
            main_idx = -1
            for i, line in enumerate(lines):
                if 'if __name__' in line:
                    main_idx = i
                    break
            
            if main_idx != -1:
                # Find last non-empty line in main block
                last_line_idx = len(lines) - 1
                for i in range(len(lines) - 1, main_idx, -1):
                    if lines[i].strip():
                        last_line_idx = i
                        break
                
                # Add cost reporting
                report_lines = [
                    "",
                    "    # Cost Optimization Report",
                    "    print()",
                    "    print_optimization_stats()"
                ]
                
                for line in reversed(report_lines):
                    lines.insert(last_line_idx + 1, line)
                
                content = '\n'.join(lines)
        else:
            # No main block, add at end
            content += "\n\n# Cost Optimization Report\nprint()\nprint_optimization_stats()\n"
        
        return content
    
    def integrate_directory(self, directory: Path, pattern: str = "*.py") -> None:
        """
        Integrate cost optimization into all scripts in directory
        
        Args:
            directory: Directory to process
            pattern: File pattern to match
        """
        scripts = list(directory.glob(pattern))
        
        print(f"Found {len(scripts)} scripts to process")
        print("="*70)
        print()
        
        for script in scripts:
            self.stats['processed'] += 1
            
            success, message = self.integrate_script(script)
            
            if success:
                self.stats['modified'] += 1
                status = "✅ MODIFIED"
            elif "Already integrated" in message or "No API calls" in message:
                self.stats['skipped'] += 1
                status = "⏭️  SKIPPED"
            else:
                self.stats['errors'] += 1
                status = "❌ ERROR"
            
            print(f"{status:12s} {script.name:50s} {message}")
        
        print()
        print("="*70)
        print("INTEGRATION SUMMARY")
        print("="*70)
        print(f"Total processed: {self.stats['processed']}")
        print(f"Modified:        {self.stats['modified']}")
        print(f"Skipped:         {self.stats['skipped']}")
        print(f"Errors:          {self.stats['errors']}")
        print("="*70)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Integrate cost optimization into Python scripts")
    parser.add_argument("directory", type=str, help="Directory containing scripts")
    parser.add_argument("--pattern", type=str, default="*.py", help="File pattern (default: *.py)")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (don't modify files)")
    parser.add_argument("--production-only", action="store_true", help="Only process production scripts")
    
    args = parser.parse_args()
    
    directory = Path(args.directory)
    
    if not directory.exists():
        print(f"Error: Directory {directory} does not exist")
        sys.exit(1)
    
    # Adjust pattern for production-only
    if args.production_only:
        pattern = "*production*.py"
    else:
        pattern = args.pattern
    
    print("="*70)
    print("COST OPTIMIZATION INTEGRATION TOOL")
    print("="*70)
    print(f"Directory:       {directory}")
    print(f"Pattern:         {pattern}")
    print(f"Dry run:         {args.dry_run}")
    print(f"Production only: {args.production_only}")
    print("="*70)
    print()
    
    integrator = CostOptimizationIntegrator(dry_run=args.dry_run)
    integrator.integrate_directory(directory, pattern)
    
    if args.dry_run:
        print()
        print("⚠️  DRY RUN - No files were modified")
        print("   Run without --dry-run to apply changes")
