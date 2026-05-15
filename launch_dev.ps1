# ProjSkep Startup Orchestrator

Write-Host "🚀 Initializing ProjSkep Neural Observatory..." -ForegroundColor Cyan

# 1. Start Backend
Write-Host "[1/4] Starting Backend Server..." -ForegroundColor Gray
Start-Process -NoNewWindow -FilePath "uvicorn" -ArgumentList "projskep_server.main:app --reload --port 8000"

# Wait for backend to warm up
Start-Sleep -Seconds 3

# 2. Start Orchestrator
Write-Host "[2/4] Starting Event Orchestrator..." -ForegroundColor Gray
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "scripts/event_orchestrator.py"

# 3. Start Frontend
Write-Host "[3/4] Starting Frontend Control Surface..." -ForegroundColor Gray
Set-Location projskep_ui
Start-Process -NoNewWindow -FilePath "npm" -ArgumentList "run dev"
Set-Location ..

# 4. Verification
Write-Host "[4/4] Verifying System Readiness..." -ForegroundColor Gray
python projskep_server/services/health_check.py

Write-Host "`n✨ ProjSkep is now ONLINE." -ForegroundColor Green
Write-Host "Observatory UI: http://localhost:5173" -ForegroundColor Cyan

# Auto-open browser
Start-Process "http://localhost:5173"
