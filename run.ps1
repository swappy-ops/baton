# Baton v1.0 Runner — Windows

Write-Host "=== Baton v1.0 ===" -ForegroundColor Cyan

# Check .env
if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
    Write-Host "Created .env from .env.example" -ForegroundColor Gray
}

# Check venv
if (-not (Test-Path ".venv")) {
    Write-Host "ERROR: Virtual environment not found. Run .\install.ps1 first." -ForegroundColor Red
    exit 1
}

& .\.venv\Scripts\Activate.ps1

# Check dependencies
try {
    python -c "import fastapi" 2>$null
} catch {
    Write-Host "ERROR: Dependencies not installed. Run .\install.ps1 first." -ForegroundColor Red
    exit 1
}

Write-Host "Starting Baton Server on http://0.0.0.0:8000" -ForegroundColor Green
Write-Host "Observatory UI: http://localhost:8000"
Write-Host "API Status: http://localhost:8000/api/status"
Write-Host "Press Ctrl+C to stop"
Write-Host ""

uvicorn baton_server.main:app --host 0.0.0.0 --port 8000 --reload
