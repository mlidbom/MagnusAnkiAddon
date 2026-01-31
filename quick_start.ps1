# Magnus Core POC - Quick Start Script

Write-Host "=== Magnus Core - Python.NET POC Quick Start ===" -ForegroundColor Cyan
Write-Host ""

# Check for .NET SDK
Write-Host "Checking for .NET 8 SDK..." -ForegroundColor Yellow
$dotnetVersion = dotnet --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ .NET SDK not found!" -ForegroundColor Red
    Write-Host "  Install from: https://dotnet.microsoft.com/download" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Found .NET SDK: $dotnetVersion" -ForegroundColor Green

# Check Python
Write-Host "Checking for Python..." -ForegroundColor Yellow
$pythonExe = ".\venv\Scripts\python.exe"
if (Test-Path $pythonExe) {
    $pythonVersion = & $pythonExe --version
    Write-Host "✓ Found Python: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Virtual environment not found at .\venv\" -ForegroundColor Red
    exit 1
}

# Install Python dependencies
Write-Host "`nInstalling Python dependencies..." -ForegroundColor Yellow
& $pythonExe -m pip install --quiet pythonnet janome
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install Python packages" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Python packages installed" -ForegroundColor Green

# Build the solution
Write-Host "`nBuilding C# projects..." -ForegroundColor Yellow
dotnet build --verbosity quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Build succeeded" -ForegroundColor Green

# Run tests
Write-Host "`nRunning tests..." -ForegroundColor Yellow
dotnet test --verbosity quiet --nologo
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Tests failed!" -ForegroundColor Red
    Write-Host "`nRun with verbose output to see details:" -ForegroundColor Yellow
    Write-Host "  dotnet test --logger 'console;verbosity=detailed'" -ForegroundColor Gray
    exit 1
}
Write-Host "✓ All tests passed" -ForegroundColor Green

# Run console example
Write-Host "`n=== Running Standalone .NET Example ===" -ForegroundColor Cyan
dotnet run --project MagnusCore.Console

# Run Python example
Write-Host "`n`n=== Running Python -> .NET Example ===" -ForegroundColor Cyan
& $pythonExe example_python_to_dotnet.py

Write-Host "`n=== Success! ===" -ForegroundColor Green
Write-Host ""
Write-Host "What to do next:" -ForegroundColor Yellow
Write-Host "  1. Open MagnusAnkiAddon.sln in Rider" -ForegroundColor Gray
Write-Host "  2. Read POC_SUMMARY.md for overview" -ForegroundColor Gray
Write-Host "  3. Read README_DOTNET_POC.md for details" -ForegroundColor Gray
Write-Host "  4. Explore the code in Rider" -ForegroundColor Gray
Write-Host ""
