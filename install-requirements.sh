#!/bin/sh
# install_requirements.sh - Install Python dependencies for Enhanced TV App
# Usage: Run this script from the enhanced-tv-app directory

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
else
    PYTHON=python
fi

$PYTHON -m pip install --upgrade pip
$PYTHON -m pip install -r requirements.txt
