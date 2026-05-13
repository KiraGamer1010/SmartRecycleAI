$ErrorActionPreference = "Stop"
$Root = (Resolve-Path "$PSScriptRoot\..").Path

function Invoke-Checked {
  param(
    [string]$FilePath,
    [string[]]$ArgumentList
  )

  & $FilePath @ArgumentList
  if ($LASTEXITCODE -ne 0) {
    throw "Command failed: $FilePath $($ArgumentList -join ' ')"
  }
}

$BackendPython = Join-Path $Root "backend\.venv\Scripts\python.exe"
if (-not (Test-Path $BackendPython)) {
  $BackendPython = "python"
}

$AiPython = Join-Path $Root "ai-engine\.venv\Scripts\python.exe"
if (-not (Test-Path $AiPython)) {
  $AiPython = "python"
}

Write-Host "Checking frontend build..."
Set-Location "$Root\frontend"
Invoke-Checked "npm" @("run", "build")

Write-Host "Checking backend tests..."
Set-Location "$Root\backend"
Invoke-Checked $BackendPython @("-m", "pytest")

Write-Host "Checking AI engine tests..."
Set-Location "$Root\ai-engine"
Invoke-Checked $AiPython @("-m", "pytest")

Write-Host "All checks completed."
