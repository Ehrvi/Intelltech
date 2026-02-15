#!/bin/bash
# Manus Global Knowledge System - Bootstrap Script
# Version: 3.0
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

# Step 2: Initialize enforcement system
echo "⚙️  Initializing enforcement system..."
cd /home/ubuntu/manus_global_knowledge && python3 mandatory_init.py

echo "✅ Manus Global Knowledge System initialized successfully!"
echo "📊 System ready with:"
echo "   - Cost optimization (75-90% savings)"
echo "   - Knowledge cache (150+ companies, 200+ contacts)"
echo "   - Guardian validation (quality ≥80%)"
echo "   - Scientific method (12 steps)"
echo ""
echo "Repository: https://github.com/Ehrvi/Intelltech"
