#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Baton v1.0 ==="

# Create .env from example if missing
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
fi

# Check Python
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 required. Run ./install.sh first."; exit 1; }

# Check venv
if [ ! -d ".venv" ]; then
    echo "ERROR: Virtual environment not found. Run ./install.sh first."
    exit 1
fi

source .venv/bin/activate

# Check dependencies
python3 -c "import fastapi" 2>/dev/null || { echo "ERROR: Dependencies not installed. Run ./install.sh first."; exit 1; }

echo "Starting Baton Server on http://0.0.0.0:8000"
echo "Observatory UI: http://localhost:8000"
echo "API Status: http://localhost:8000/api/status"
echo "Press Ctrl+C to stop"
echo ""

uvicorn baton_server.main:app --host 0.0.0.0 --port 8000 --reload
