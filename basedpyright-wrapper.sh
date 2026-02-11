#!/usr/bin/env bash
# Cross-platform basedpyright wrapper for Linux/macOS.
# Equivalent of basedpyright-wrapper.bat for Windows.
set -euo pipefail
cd "$(dirname "$0")"

source venv/bin/activate
basedpyright --project basedpyright-wrapper-config.json
