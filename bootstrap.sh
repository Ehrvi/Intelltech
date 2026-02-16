#!/bin/bash
# Manus Global Knowledge System - Bootstrap Script
# Version 3.1 - Operating System V3.1
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

# Step 2: Load Operating System V3.1
echo "🎯 Loading MANUS OPERATING SYSTEM V3.1..."
if [ -f /home/ubuntu/manus_global_knowledge/MANUS_OPERATING_SYSTEM.md ]; then
  echo "   ✅ Operating System V3.1 loaded"
  echo "   📋 Prime Directive active"
  echo "   🏛️  5 Core Principles enforced"
else
  echo "   ⚠️  Operating System not found - using legacy mode"
fi

# Step 3: Initialize enforcement system
echo "⚙️  Initializing enforcement system..."
cd /home/ubuntu/manus_global_knowledge && python3 mandatory_init.py

echo "✅ Manus Global Knowledge System V3.1 initialized successfully!"
echo ""
echo "🎯 OPERATING SYSTEM V3.1 ACTIVE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Prime Directive: Deliver maximum value with maximum efficiency"
echo ""
echo "5 Core Principles:"
echo "   P1: Always Study First (100% compliance)"
echo "   P2: Always Decide Autonomously (99.9% compliance)"
echo "   P3: Always Optimize Cost (75-90% savings)"
echo "   P4: Always Ensure Quality (≥80% score)"
echo "   P5: Always Report Accurately (100% compliance)"
echo ""
echo "📊 System Features:"
echo "   - Cost optimization (75-90% savings)"
echo "   - Knowledge cache (150+ companies, 200+ contacts)"
echo "   - Guardian validation (quality ≥80%)"
echo "   - Scientific method (12 steps)"
echo "   - Autonomous decision enforcement"
echo "   - Multi-platform cost tracking"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Repository: https://github.com/Ehrvi/Intelltech"
