#!/usr/bin/env pwsh
# Railway Environment Variables Auto-Setter
# Usage: ./railway_set_vars.ps1
# Requires: railway CLI installed and logged in (`railway login`)

param(
    [string]$EnvFile = ".env"
)

if (-not (Test-Path $EnvFile)) {
    Write-Error "Error: $EnvFile not found"
    exit 1
}

# Check if railway CLI is available
try {
    $railwayVersion = & railway --version 2>&1
    Write-Host "Railway CLI version: $railwayVersion" -ForegroundColor Green
} catch {
    Write-Error "Railway CLI not found. Install it: npm install -g railway"
    exit 1
}

Write-Host "Reading variables from $EnvFile..." -ForegroundColor Cyan

# Read .env file and parse key=value pairs
$envVars = @{}
Get-Content $EnvFile | Where-Object { $_ -match '^\s*[^#]' -and $_ -match '=' } | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith('#')) {
        $key, $value = $line -split '=', 2
        $key = $key.Trim()
        $value = $value.Trim().TrimStart('"').TrimEnd('"')
        if ($key) {
            $envVars[$key] = $value
        }
    }
}

Write-Host "Found $($envVars.Count) variables. Setting in Railway..." -ForegroundColor Cyan

# Variables to skip (DATABASE_URL is auto-set by Postgres plugin)
$skipVars = @('DATABASE_URL', 'APP_HOST', 'APP_PORT', 'APP_NAME')

$count = 0
$failed = 0

foreach ($key in $envVars.Keys) {
    if ($skipVars -contains $key) {
        Write-Host "⊘  Skipping $key (auto-managed by Railway)" -ForegroundColor Yellow
        continue
    }
    
    $value = $envVars[$key]
    
    # Escape quotes in values for CLI
    $value = $value -replace '"', '\"'
    
    try {
        Write-Host "Setting $key..." -NoNewline
        & railway variables set "$key=$value" 2>&1 | Out-Null
        Write-Host " ✓" -ForegroundColor Green
        $count++
    }
    catch {
        Write-Host " ✗" -ForegroundColor Red
        Write-Error "Failed to set $key : $_"
        $failed++
    }
}

Write-Host ""
Write-Host "Summary: $count variables set, $failed failed" -ForegroundColor Cyan

if ($failed -eq 0) {
    Write-Host "✓ All variables set successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Go to Railway Dashboard and verify variables"
    Write-Host "2. Trigger a Deploy/Redeploy"
    Write-Host "3. Once online, run migrations: railway run alembic upgrade head"
} else {
    Write-Host "⚠ Some variables failed. Check the errors above." -ForegroundColor Yellow
}
