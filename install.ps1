# Baton v1.0 Installer — Windows

Write-Host "=== Baton v1.0 Installer ===" -ForegroundColor Cyan

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python 3.11+ required" -ForegroundColor Red
    exit 1
}

# Create virtual environment
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Gray
    python -m venv .venv
}

& .\.venv\Scripts\Activate.ps1

# Install server dependencies
Write-Host "Installing server dependencies..." -ForegroundColor Gray
pip install -q -r requirements-server.txt

# Install full dependencies (optional)
$installML = Read-Host "Install full ML stack? (chromadb, langchain, sentence-transformers) [y/N]"
if ($installML -match "^[Yy]") {
    Write-Host "Installing full dependencies..." -ForegroundColor Gray
    pip install -q -r requirements.txt
}

# Create .env if missing
if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
    Write-Host "Created .env from .env.example" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Installation Complete ===" -ForegroundColor Green
Write-Host "Run: .\run.ps1"
Write-Host "Or:  docker compose up -d"
