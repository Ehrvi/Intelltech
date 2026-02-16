#!/bin/bash
# Manus Global Knowledge System - SIMPLIFIED Bootstrap
# Version: 3.5
# Purpose: Minimal, reliable initialization

set -e  # Exit on error

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 MOTHER SYSTEM BOOTSTRAP V3.5"
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

# Step 3: Display system version
echo ""
if [ -f "VERSION" ]; then
  VERSION=$(cat VERSION)
  echo "📌 MOTHER Version: $VERSION"
else
  echo "📌 MOTHER Version: Unknown"
fi

# Step 4: Display enforcement reminder
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚠️  MANDATORY: READ PRE_TASK_ENFORCEMENT.md BEFORE STARTING"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 ENFORCEMENT CHECKLIST:"
echo "   1. Identify task type (research/decision/implementation)"
echo "   2. If RESEARCH → Use browser for Google Scholar/Anna's Archive"
echo "   3. If DECISION → Decide autonomously (don't ask user)"
echo "   4. Optimize costs (but CORRECTNESS > COST)"
echo "   5. Generate honest cost report at end"
echo "   6. Be 100% truthful about actions"
echo ""
echo "🚨 VIOLATIONS = CRITICAL FAILURE"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ BOOTSTRAP COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Repository: https://github.com/Ehrvi/Intelltech"
echo "Motto: 'Somente unidos seremos mais fortes!'"
echo ""
