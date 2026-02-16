#!/bin/bash
# Manus Global Knowledge System - Bootstrap Script
# Version 3.2 - Operating System V3.2
# Purpose: One-line initialization from GitHub

set -e  # Exit on error

# Step 1: Clone or update repository
if [ ! -d /home/ubuntu/manus_global_knowledge ]; then
  echo "📥 Cloning Manus Global Knowledge System from GitHub..."
  git clone https://github.com/Ehrvi/Intelltech.git /home/ubuntu/manus_global_knowledge
else
  echo "🔄 Updating Manus Global Knowledge System from GitHub..."
  cd /home/ubuntu/manus_global_knowledge && git pull origin main
fi

# Step 2: Load Operating System V3.2
echo "🎯 Loading MANUS OPERATING SYSTEM V3.2..."
if [ -f /home/ubuntu/manus_global_knowledge/MANUS_OPERATING_SYSTEM.md ]; then
  echo "   ✅ Operating System V3.2 loaded"
  echo "   📋 Prime Directive active"
  echo "   🏛️  5 Core Principles enforced"
else
  echo "   ⚠️  Operating System not found - using legacy mode"
fi

# Step 3: Initialize enforcement system
echo "⚙️  Initializing enforcement system..."
cd /home/ubuntu/manus_global_knowledge && python3 mandatory_init.py

# Step 4: CRITICAL ENFORCEMENT CHECK (NEW IN V3.2)
echo ""
echo "🔒 Running CRITICAL enforcement check..."
if ! python3 /home/ubuntu/manus_global_knowledge/core/critical_enforcement_check.py; then
  echo ""
  echo "╔════════════════════════════════════════════════════════════╗"
  echo "║                    ⛔ CRITICAL ERROR ⛔                     ║"
  echo "╠════════════════════════════════════════════════════════════╣"
  echo "║  MOTHER enforcement is NOT at 100% compliance.             ║"
  echo "║  Task execution is BLOCKED for safety.                     ║"
  echo "║                                                            ║"
  echo "║  This is a mandatory requirement in MOTHER V3.2.           ║"
  echo "║  All tasks MUST have full enforcement active.              ║"
  echo "║                                                            ║"
  echo "║  Please fix the missing files and re-run bootstrap.sh     ║"
  echo "╚════════════════════════════════════════════════════════════╝"
  echo ""
  exit 1  # Exit with error code to stop execution
fi

echo "✅ Manus Global Knowledge System V3.2 initialized successfully!"
echo ""

# Display MOTHER Status
python3 /home/ubuntu/manus_global_knowledge/core/mother_status_display.py detailed
echo ""
echo "Repository: https://github.com/Ehrvi/Intelltech"
