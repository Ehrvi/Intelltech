#!/usr/bin/env python3
"""
Clean Duplicate Imports from Apollo Scripts
Removes old optimization imports and keeps only the new ones

Author: Manus AI
Date: 2026-02-16
"""

import os
import re
from pathlib import Path


def clean_duplicate_imports(file_path: Path) -> tuple[bool, str]:
    """
    Clean duplicate optimization imports from a Python file
    
    Args:
        file_path: Path to Python file
        
    Returns:
        (success, message) tuple
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        original_content = content
        
        # Patterns to remove (old imports)
        patterns_to_remove = [
            r'# Cost Optimization Integration\s*\n',
            r'sys\.path\.insert\(0, str\(Path\(__file__\)\.parent\.parent / [\'"]manus_global_knowledge[\'"] / [\'"]core[\'"]\)\)\s*\n',
            r'from optimized_api_wrapper import optimized_post, print_optimization_stats\s*\n',
            r'from aggressive_cost_optimizer import AggressiveCostOptimizer\s*\n',
        ]
        
        # Remove old patterns
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content)
        
        # Check if we made changes
        if content == original_content:
            return True, "No duplicate imports found"
        
        # Write back
        with open(file_path, 'w') as f:
            f.write(content)
        
        return True, "Cleaned duplicate imports"
        
    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    print("="*70)
    print("CLEAN DUPLICATE IMPORTS")
    print("="*70)
    print()
    
    apollo_dir = Path("/home/ubuntu/ProjetoApollo")
    
    if not apollo_dir.exists():
        print("❌ Apollo directory not found")
        print(f"   Expected: {apollo_dir}")
        return
    
    # Find all Python files
    python_files = list(apollo_dir.glob("*.py"))
    
    if not python_files:
        print("❌ No Python files found in Apollo directory")
        return
    
    print(f"Found {len(python_files)} Python files")
    print()
    
    cleaned = 0
    skipped = 0
    errors = 0
    
    for file_path in python_files:
        success, message = clean_duplicate_imports(file_path)
        
        if success:
            if "No duplicate" in message:
                skipped += 1
            else:
                cleaned += 1
                print(f"✅ {file_path.name}: {message}")
        else:
            errors += 1
            print(f"❌ {file_path.name}: {message}")
    
    print()
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total files:     {len(python_files)}")
    print(f"Cleaned:         {cleaned}")
    print(f"Skipped:         {skipped}")
    print(f"Errors:          {errors}")
    print()
    
    if cleaned > 0:
        print("✅ Duplicate imports cleaned successfully")
    else:
        print("✅ No duplicate imports found")


if __name__ == "__main__":
    main()
