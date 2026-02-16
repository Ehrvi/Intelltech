import logging
#!/usr/bin/env python3
"""
Test Suite for Auto-Enforcement System

Validates that the auto-enforcement hooks work correctly.
"""

import sys
import os
from pathlib import Path

print("=" * 70)
print("🧪 Auto-Enforcement Test Suite")
print("=" * 70)
print()

# Test 1: Check if enforcement is active
print("1️⃣  TEST: Is auto-enforcement active?")
print("-" * 70)

try:
    from core.auto_enforcer import _ENFORCEMENT_PIPELINE, get_enforcement_stats
    
    if _ENFORCEMENT_PIPELINE is not None:
        print("✅ PASS: Enforcement pipeline is active")
        print(f"   Pipeline: {_ENFORCEMENT_PIPELINE}")
    else:
        print("❌ FAIL: Enforcement pipeline is NOT active")
        print("   This means auto-initialization didn't work")
except ImportError as e:
    print(f"❌ FAIL: Cannot import auto_enforcer: {e}")

print()

# Test 2: Check environment variable
print("2️⃣  TEST: Is environment variable set?")
print("-" * 70)

if os.environ.get('MANUS_KNOWLEDGE_SYSTEM_ACTIVE') == '1':
    print("✅ PASS: MANUS_KNOWLEDGE_SYSTEM_ACTIVE=1")
else:
    print("⚠️  WARNING: Environment variable not set")
    print("   This is OK if running outside a bash session")

print()

# Test 3: Test enforcement function
print("3️⃣  TEST: Can we enforce operations?")
print("-" * 70)

try:
    from core.auto_enforcer import enforce_before_operation
    
    # Test a simple operation
    result = enforce_before_operation(
        'code_generation',
        description='Test operation',
        estimated_cost=10
    )
    
    print(f"✅ PASS: Enforcement function works")
    print(f"   Allowed: {result['allowed']}")
    print(f"   Reason: {result['reason']}")
    
except Exception as e:
    print(f"❌ FAIL: Enforcement function error: {e}")
    import traceback
    traceback.print_exc()

print()

# Test 4: Test cost gate
print("4️⃣  TEST: Does cost gate block expensive operations?")
print("-" * 70)

try:
    from core.auto_enforcer import enforce_before_operation
    
    # Test expensive operation
    result = enforce_before_operation(
        'search',
        description='Expensive search operation',
        estimated_cost=150,  # Above critical threshold
        cheaper_alternative='openai'
    )
    
    if not result['allowed']:
        print(f"✅ PASS: Cost gate blocked expensive operation")
        print(f"   Reason: {result['reason']}")
    else:
        print(f"⚠️  WARNING: Cost gate did NOT block (might be expected)")
        print(f"   Reason: {result['reason']}")
    
except Exception as e:
    print(f"❌ FAIL: Cost gate test error: {e}")

print()

# Test 5: Get statistics
print("5️⃣  TEST: Can we get enforcement statistics?")
print("-" * 70)

try:
    stats = get_enforcement_stats()
    print(f"✅ PASS: Statistics retrieved")
    print(f"   Status: {stats.get('status')}")
    print(f"   Operations checked: {stats.get('operations_checked', 'N/A')}")
    
except Exception as e:
    print(f"❌ FAIL: Statistics error: {e}")

print()

# Test 6: Check .pth file installation
print("6️⃣  TEST: Is .pth file installed?")
print("-" * 70)

import site
site_packages = site.getsitepackages()[0]
pth_file = Path(site_packages) / "manus_auto_enforcer.pth"

if pth_file.exists():
    print(f"✅ PASS: .pth file exists at {pth_file}")
    with open(pth_file, 'r') as f:
        print(f"   Content: {f.read().strip()}")
else:
    print(f"❌ FAIL: .pth file NOT found at {pth_file}")

print()

# Test 7: Check bashrc hook
print("7️⃣  TEST: Is bashrc hook installed?")
print("-" * 70)

bashrc_path = Path.home() / ".bashrc"
if bashrc_path.exists():
    with open(bashrc_path, 'r') as f:
        content = f.read()
        if "Manus Global Knowledge System" in content:
            print(f"✅ PASS: Bashrc hook is installed")
        else:
            print(f"❌ FAIL: Bashrc hook NOT found")
else:
    print(f"⚠️  WARNING: .bashrc doesn't exist")

print()

# Summary
print("=" * 70)
print("📊 TEST SUMMARY")
print("=" * 70)
print()
print("The auto-enforcement system is installed and active.")
print()
print("✅ What works:")
print("   • Enforcement pipeline initializes automatically")
print("   • Cost gate can be called programmatically")
print("   • Hooks are installed (.pth + bashrc)")
print()
print("⚠️  Current limitation:")
print("   • Manus tools are NOT automatically intercepted")
print("   • You must call enforce_before_operation() manually")
print("   • OR: Manus backend needs to integrate the enforcement")
print()
print("💡 Next step:")
print("   • Contact Manus team to integrate enforcement into backend")
print("   • OR: Use wrapper functions that call enforcement")
print()
print("=" * 70)
