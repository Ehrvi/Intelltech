#!/bin/bash
#
# MOTHER V4 Bootstrap Script
#
# This is the new bootstrap that uses MOTHER V4 with V3 compatibility.
# It can be used as a drop-in replacement for the old bootstrap.sh
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                    MOTHER V4 BOOTSTRAP                            ║"
echo "║              Manus Operating System - Version 4.0                 ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Detect base directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MOTHER_V4_DIR="$SCRIPT_DIR/mother_v4"

# Check if V4 exists
if [ ! -d "$MOTHER_V4_DIR" ]; then
    echo -e "${RED}✗ ERROR: MOTHER V4 not found at $MOTHER_V4_DIR${NC}"
    echo "  Please ensure MOTHER V4 is properly installed."
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ ERROR: Python 3 not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python 3 found"

# Run V4 bootstrap via compatibility layer
echo ""
echo "Initializing MOTHER V4..."
echo ""

cd "$MOTHER_V4_DIR"

# Use V3 compatibility layer for backward compatibility
python3 << 'EOF'
import sys
from pathlib import Path

# Add mother_v4 to path
sys.path.insert(0, str(Path.cwd()))

from integration.v3_compatibility import create_v3_compatible_bootstrap

# Run bootstrap
exit_code = create_v3_compatible_bootstrap()
sys.exit(exit_code)
EOF

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║              ✓ MOTHER V4 BOOTSTRAP COMPLETE                      ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "${GREEN}System ready for use.${NC}"
    echo ""
else
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║              ✗ MOTHER V4 BOOTSTRAP FAILED                        ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "${RED}Please check the error messages above.${NC}"
    echo ""
    exit $EXIT_CODE
fi
