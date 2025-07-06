# Tennis Serve Analyzer - System Status Check
Write-Host "=== Tennis Serve Analyzer System Check ===" -ForegroundColor Green
Write-Host ""

# Python Check
Write-Host "Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion) {
        Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Python not found" -ForegroundColor Red
        Write-Host "Please install Python from: https://www.python.org/downloads/" -ForegroundColor Red
    }
} catch {
    Write-Host "[ERROR] Python not found" -ForegroundColor Red
}

Write-Host ""

# Node.js Check
Write-Host "Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>$null
    if ($nodeVersion) {
        Write-Host "[OK] Node.js found: $nodeVersion" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Node.js not found" -ForegroundColor Red
        Write-Host "Please install Node.js from: https://nodejs.org/" -ForegroundColor Red
    }
} catch {
    Write-Host "[ERROR] Node.js not found" -ForegroundColor Red
}

Write-Host ""

# Port Check
Write-Host "Checking ports..." -ForegroundColor Yellow
$port5000 = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
$port5173 = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue

if ($port5000) {
    Write-Host "[OK] Port 5000 is in use (Backend server running)" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Port 5000 not in use (Backend server not running)" -ForegroundColor Red
}

if ($port5173) {
    Write-Host "[OK] Port 5173 is in use (Frontend server running)" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Port 5173 not in use (Frontend server not running)" -ForegroundColor Red
}

Write-Host ""

# Process Check
Write-Host "Checking processes..." -ForegroundColor Yellow
$pythonProcesses = Get-Process -Name "python*" -ErrorAction SilentlyContinue
$nodeProcesses = Get-Process -Name "node*" -ErrorAction SilentlyContinue

if ($pythonProcesses) {
    Write-Host "[OK] Python processes running: $($pythonProcesses.Count)" -ForegroundColor Green
} else {
    Write-Host "[INFO] No Python processes found" -ForegroundColor Yellow
}

if ($nodeProcesses) {
    Write-Host "[OK] Node processes running: $($nodeProcesses.Count)" -ForegroundColor Green
} else {
    Write-Host "[INFO] No Node processes found" -ForegroundColor Yellow
}

Write-Host ""

# File Check
Write-Host "Checking files..." -ForegroundColor Yellow
if (Test-Path "backend\app\main.py") {
    Write-Host "[OK] Backend files exist" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Backend files not found" -ForegroundColor Red
}

if (Test-Path "frontend\package.json") {
    Write-Host "[OK] Frontend files exist" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Frontend files not found" -ForegroundColor Red
}

if (Test-Path "frontend\node_modules") {
    Write-Host "[OK] Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Frontend dependencies not installed" -ForegroundColor Red
    Write-Host "Run 'npm install' in frontend folder" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Recommendations ===" -ForegroundColor Green

if (-not $port5000 -and -not $port5173) {
    Write-Host "1. Start both servers:" -ForegroundColor Yellow
    Write-Host "   - Double-click start_system.bat" -ForegroundColor White
    Write-Host "   - Double-click start_frontend.bat" -ForegroundColor White
} elseif (-not $port5000) {
    Write-Host "1. Start backend server:" -ForegroundColor Yellow
    Write-Host "   - Double-click start_system.bat" -ForegroundColor White
} elseif (-not $port5173) {
    Write-Host "1. Start frontend server:" -ForegroundColor Yellow
    Write-Host "   - Double-click start_frontend.bat" -ForegroundColor White
} else {
    Write-Host "1. Both servers are running!" -ForegroundColor Green
    Write-Host "   - Access: http://localhost:5173" -ForegroundColor White
}

Write-Host ""
Read-Host "Press Enter to exit"

