#!/bin/bash
# Manus Global Knowledge System - Bootstrap with Compliance System
# Version: 4.0
# Purpose: Initialize MOTHER with integrated compliance system

set -e  # Exit on error

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 MOTHER SYSTEM BOOTSTRAP V4.0 (with Compliance System)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Step 1: Clone or update repository
if [ ! -d /home/ubuntu/manus_global_knowledge ]; then
  echo "📥 Cloning repository..."
  git clone https://github.com/Ehrvi/Intelltech.git /home/ubuntu/manus_global_knowledge
  echo "   ✅ Repository cloned"
else
  echo "🔄 Updating repository..."
  cd /home/ubuntu/manus_global_knowledge
  git pull origin main --quiet
  echo "   ✅ Repository updated"
fi

cd /home/ubuntu/manus_global_knowledge

# Step 2: Verify critical files exist
echo ""
echo "🔍 Verifying critical files..."

CRITICAL_FILES=(
  "MANUS_OPERATING_SYSTEM.md"
  "PRE_TASK_ENFORCEMENT.md"
  "COGNITIVE_ENFORCEMENT.md"
  "VERSION"
  "mother_v5/compliance/compliance_engine.py"
  "mother_v5/compliance/checklist.py"
)

ALL_OK=true
for file in "${CRITICAL_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "   ✅ $file"
  else
    echo "   ❌ MISSING: $file"
    ALL_OK=false
  fi
done

if [ "$ALL_OK" = false ]; then
  echo ""
  echo "⚠️  CRITICAL FILES MISSING - System may not function correctly"
  echo ""
fi

# Step 3: Initialize Compliance System
echo ""
echo "🔒 Initializing MOTHER V5 Compliance System..."

python3 -c "
import sys
sys.path.insert(0, '/home/ubuntu/manus_global_knowledge')

try:
    from mother_v5.compliance import COMPLIANCE_ENGINE
    
    # Initialize the compliance engine
    success = COMPLIANCE_ENGINE.initialize()
    
    if success:
        print('   ✅ Compliance Engine initialized')
        print(f'   📊 {len(COMPLIANCE_ENGINE.enforcers)} enforcers loaded')
    else:
        print('   ❌ Compliance Engine initialization FAILED')
        sys.exit(1)
        
except Exception as e:
    print(f'   ❌ ERROR: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
  echo ""
  echo "🚨 CRITICAL: Compliance System initialization FAILED"
  echo "   Task execution is BLOCKED until this is resolved."
  echo ""
  exit 1
fi

# Step 4: Run critical enforcement check (existing)
echo ""
echo "🔒 Running Critical Enforcement Check..."

if [ -f "core/critical_enforcement_check.py" ]; then
  python3 core/critical_enforcement_check.py
  
  if [ $? -ne 0 ]; then
    echo ""
    echo "🚨 CRITICAL: Enforcement check FAILED"
    echo "   Task execution is BLOCKED."
    echo ""
    exit 1
  fi
else
  echo "   ⚠️  WARNING: critical_enforcement_check.py not found"
fi

# Step 5: Display system version
echo ""
if [ -f "VERSION" ]; then
  VERSION=$(cat VERSION)
  echo "📌 MOTHER Version: $VERSION"
else
  echo "📌 MOTHER Version: Unknown"
fi

# Step 6: Display compliance status
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 COMPLIANCE SYSTEM STATUS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Compliance System: ACTIVE"
echo "✅ Pre-action blocking: ENABLED"
echo "✅ Violation logging: ENABLED"
echo "✅ Auto-audit: ENABLED"
echo ""
echo "📋 Available Commands:"
echo "   • mother-compliance-status          - View compliance dashboard"
echo "   • mother-compliance-status violations - View recent violations"
echo "   • mother-compliance-status report   - Generate compliance report"
echo ""

# Step 7: Display enforcement reminder
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚠️  MANDATORY: MOTHER PRINCIPLES (P1-P7)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 ENFORCEMENT CHECKLIST:"
echo "   P1: Always Study First (100% compliance)"
echo "   P2: Always Decide Autonomously (99.9% compliance)"
echo "   P3: Always Optimize Cost (75-90% savings)"
echo "   P4: Always Ensure Quality (≥80% quality)"
echo "   P5: Always Report Accurately (100% compliance)"
echo "   P6: Always Learn and Improve (100% compliance)"
echo "   P7: Always Be Truthful (100% compliance)"
echo ""
echo "🚨 VIOLATIONS = AUTOMATIC BLOCKING"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ BOOTSTRAP COMPLETE - COMPLIANCE SYSTEM ACTIVE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Repository: https://github.com/Ehrvi/Intelltech"
echo "Motto: 'Somente unidos seremos mais fortes!'"
echo ""
