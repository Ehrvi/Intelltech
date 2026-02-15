#!/bin/bash
#
# Install Hooks for Manus Global Knowledge System Auto-Enforcement
#
# This script installs hooks that make the enforcement system activate
# automatically without manual intervention.
#

set -e

echo "======================================================================="
echo "🔧 Installing Manus Global Knowledge System Auto-Enforcement Hooks"
echo "======================================================================="
echo ""

BASE_DIR="/home/ubuntu/manus_global_knowledge"

# Hook 1: Bashrc initialization
echo "1️⃣  Installing bashrc hook..."

BASHRC_HOOK="
# Manus Global Knowledge System - Auto-Initialization
if [ -f \"$BASE_DIR/mandatory_init.py\" ]; then
    export MANUS_KNOWLEDGE_SYSTEM_ACTIVE=1
    # Silent initialization (errors only)
    python3 \"$BASE_DIR/mandatory_init.py\" 2>&1 | grep -E '(ERROR|FAILED|✅ SYSTEM)' || true
fi
"

# Check if hook already exists
if grep -q "Manus Global Knowledge System" ~/.bashrc 2>/dev/null; then
    echo "   ⚠️  Hook already exists in ~/.bashrc, skipping..."
else
    echo "$BASHRC_HOOK" >> ~/.bashrc
    echo "   ✅ Added hook to ~/.bashrc"
fi

# Hook 2: Python site-packages (.pth file)
echo ""
echo "2️⃣  Installing Python import hook..."

sudo python3 "$BASE_DIR/core/auto_enforcer.py"

# Hook 3: Create systemd user service (optional, for persistent enforcement)
echo ""
echo "3️⃣  Creating systemd user service (optional)..."

SYSTEMD_DIR="$HOME/.config/systemd/user"
mkdir -p "$SYSTEMD_DIR"

cat > "$SYSTEMD_DIR/manus-enforcement.service" << EOF
[Unit]
Description=Manus Global Knowledge System Enforcement Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $BASE_DIR/mandatory_init.py
Restart=on-failure
RestartSec=10
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=default.target
EOF

echo "   ✅ Systemd service created at: $SYSTEMD_DIR/manus-enforcement.service"
echo "   To enable: systemctl --user enable manus-enforcement.service"
echo "   To start:  systemctl --user start manus-enforcement.service"

# Hook 4: Create initialization flag
echo ""
echo "4️⃣  Creating state directory..."

mkdir -p "$BASE_DIR/state"
date > "$BASE_DIR/state/hooks_installed.flag"
echo "   ✅ State directory created"

echo ""
echo "======================================================================="
echo "✅ INSTALLATION COMPLETE"
echo "======================================================================="
echo ""
echo "The enforcement system will now activate automatically when:"
echo "  • You open a new shell session"
echo "  • Python interpreter starts (via .pth hook)"
echo "  • (Optional) As a systemd service"
echo ""
echo "To verify installation:"
echo "  source ~/.bashrc"
echo "  echo \$MANUS_KNOWLEDGE_SYSTEM_ACTIVE"
echo ""
echo "======================================================================="
