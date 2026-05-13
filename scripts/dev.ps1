param(
  [switch]$Docker
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path "$PSScriptRoot\.."
$RootPath = $Root.Path

if ($Docker) {
  Set-Location $Root
  docker compose up --build
  exit
}

$BackendPython = Join-Path $RootPath "backend\.venv\Scripts\python.exe"
if (-not (Test-Path $BackendPython)) {
  $BackendPython = "python"
}

$AiPython = Join-Path $RootPath "ai-engine\.venv\Scripts\python.exe"
if (-not (Test-Path $AiPython)) {
  $AiPython = "python"
}

Write-Host "Starting SmartRecycleAI services in separate PowerShell windows..."

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$RootPath\backend'; & '$BackendPython' -m uvicorn app.main:app --reload --port 8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$RootPath\ai-engine'; & '$AiPython' -m uvicorn ai_engine.api.main:app --reload --port 8100"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$RootPath\frontend'; npm run dev"

Write-Host "Frontend:  http://localhost:5173"
Write-Host "Backend:   http://localhost:8000/health"
Write-Host "AI Engine: http://localhost:8100/health"
