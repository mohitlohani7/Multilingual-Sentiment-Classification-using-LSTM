# NeuroSenti 2.0 - PowerShell Startup Script for Windows
# Usage: powershell -ExecutionPolicy Bypass -File start.ps1

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║      NeuroSenti 2.0 - Startup Script             ║" -ForegroundColor Cyan
Write-Host "║      Hybrid CNN-BiLSTM Sentiment Engine           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if virtual environment exists
$venvPath = Join-Path $scriptDir "venv\Scripts\Activate.ps1"
if (-not (Test-Path $venvPath)) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Expected path: $venvPath" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& $venvPath

# Check if ports are available
$port8000 = netstat -ano | findstr ":8000 " 
$port8501 = netstat -ano | findstr ":8501 "

if ($port8000) {
    Write-Host "WARNING: Port 8000 is already in use!" -ForegroundColor Yellow
}
if ($port8501) {
    Write-Host "WARNING: Port 8501 is already in use!" -ForegroundColor Yellow
}

# Start Backend
Write-Host ""
Write-Host "Starting FastAPI Backend (Port 8000)..." -ForegroundColor Green
$backendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir'; python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload" -PassThru
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "Starting Streamlit Frontend (Port 8501)..." -ForegroundColor Green
$frontendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir'; streamlit run frontend/app.py --server.port 8501 --server.address 127.0.0.1" -PassThru

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║              NeuroSenti 2.0 Started!              ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "Frontend (Streamlit): " -ForegroundColor Cyan -NoNewline
Write-Host "http://127.0.0.1:8501" -ForegroundColor White
Write-Host "Backend (FastAPI):   " -ForegroundColor Cyan -NoNewline
Write-Host "http://127.0.0.1:8000" -ForegroundColor White
Write-Host "API Docs (Swagger):  " -ForegroundColor Cyan -NoNewline
Write-Host "http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Both applications are running in separate windows." -ForegroundColor Yellow
Write-Host "Close the windows to stop the applications." -ForegroundColor Yellow
Write-Host ""

# Wait for processes
Wait-Process -Id $backendProcess.Id
Wait-Process -Id $frontendProcess.Id
