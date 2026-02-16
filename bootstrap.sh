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

# Display MOTHER Status
python3 /home/ubuntu/manus_global_knowledge/core/mother_status_display.py detailed
echo ""
echo "Repository: https://github.com/Ehrvi/Intelltech"
