#!/usr/bin/env pwsh
# Regenerate Python type stubs for JAStudio .NET assemblies
#
# Usage:
#   .\regenerate-stubs.ps1                          # Default Debug config
#   .\regenerate-stubs.ps1 -OnlyTargetTypes           # Fast - only JAStudio types
#   .\regenerate-stubs.ps1 -Configuration Release      # Use Release DLLs

param(
    [switch]$OnlyTargetTypes,
    [string]$Configuration = "Debug"
)

# Always work relative to script location
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $ScriptDir

$StubGenRoot = "..\..\src_dotnet\pythonnet-stub-generator"
$TypingsPath = "..\..\typings"
$StubGenDll = "$StubGenRoot\csharp\PythonNetStubTool\bin\Debug\net10.0\PythonNetStubGenerator.Tool.dll"

try {
    if (Test-Path $StubGenDll) {
        Write-Host "Stub generator already compiled, skipping build..." -ForegroundColor Gray
    } else {
        Write-Host "Building stub generator..." -ForegroundColor Cyan
        dotnet build "$StubGenRoot\csharp\PythonNetStubTool\PythonNetStubGenerator.Tool.csproj"

        if ($LASTEXITCODE -ne 0) {
            Write-Host "Build failed!" -ForegroundColor Red
            exit 1
        }
    }

Write-Host "`nCleaning old JAStudio stubs..." -ForegroundColor Cyan
$jastudioPath = "$TypingsPath\JAStudio"
if (Test-Path $jastudioPath) {
    Remove-Item -Recurse -Force $jastudioPath
    Write-Host "Removed old JAStudio stubs" -ForegroundColor Yellow
}

$globalPath = "$TypingsPath\global_"
if (Test-Path $globalPath) {
    Remove-Item -Recurse -Force $globalPath
    Write-Host "Removed broken global_ stubs" -ForegroundColor Yellow
}

Write-Host "`nGenerating stubs..." -ForegroundColor Cyan

$args = @(
    $StubGenDll,
    "--dest-path", $TypingsPath,
    "--target-dlls", "JAStudio.Core\bin\$Configuration\net10.0\JAStudio.Core.dll,JAStudio.PythonInterop\bin\$Configuration\net10.0\JAStudio.PythonInterop.dll,JAStudio.UI\bin\$Configuration\net10.0\win-x64\JAStudio.UI.dll"
)

if ($OnlyTargetTypes) {
    $args += "--only-target-types"
}

dotnet @args

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nStubs regenerated successfully!" -ForegroundColor Green
} else {
    Write-Host "`nStub generation failed!" -ForegroundColor Red
    exit 1
}
}
finally {
    Pop-Location
}