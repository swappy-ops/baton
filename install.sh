#!/usr/bin/env bash
set -euo pipefail

echo "=== Baton v1.0 Installer ==="

# Check prerequisites
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 required"; exit 1; }
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
REQUIRED="3.11"
if [ "$(printf '%s\n' "$REQUIRED" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED" ]; then
    echo "ERROR: Python 3.11+ required (found $PYTHON_VERSION)"
    exit 1
fi

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

# Install server dependencies (minimal runtime)
echo "Installing server dependencies..."
pip install -q -r requirements-server.txt

# Install full dependencies (optional — for baton/ package with ML stack)
read -p "Install full ML stack? (chromadb, langchain, sentence-transformers) [y/N]: " INSTALL_ML
if [[ "$INSTALL_ML" =~ ^[Yy]$ ]]; then
    echo "Installing full dependencies..."
    pip install -q -r requirements.txt
fi

# Create .env if missing
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
fi

echo ""
echo "=== Installation Complete ==="
echo "Run: ./run.sh"
echo "Or:  docker compose up -d"
