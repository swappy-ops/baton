#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Baton: Starting Baton Server ==="

# Create .env from example if missing
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from .env.example — edit if needed"
fi

# Check Python
command -v python3 >/dev/null 2>&1 || { echo "Need python3"; exit 1; }

# Install dependencies if missing
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -q -r requirements.txt

echo "Starting server on http://0.0.0.0:8000"
uvicorn baton_server.main:app --host 0.0.0.0 --port 8000 --reload
