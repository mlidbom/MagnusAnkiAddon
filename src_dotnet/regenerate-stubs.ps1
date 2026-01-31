#!/usr/bin/env pwsh
# Regenerate Python type stubs for JAStudio .NET assemblies
#
# Usage:
#   .\regenerate-stubs.ps1              # Default - includes all System.* types (slow)
#   .\regenerate-stubs.ps1 -OnlyTargetTypes  # Fast - only JAStudio types

param(
    [switch]$OnlyTargetTypes
)

Write-Host "Building stub generator..." -ForegroundColor Cyan
dotnet build pythonnet-stub-generator\csharp\PythonNetStubTool\PythonNetStubGenerator.Tool.csproj

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`nCleaning old JAStudio stubs..." -ForegroundColor Cyan
$jastudioPath = "..\typings\JAStudio"
if (Test-Path $jastudioPath) {
    Remove-Item -Recurse -Force $jastudioPath
    Write-Host "Removed old JAStudio stubs" -ForegroundColor Yellow
}

$globalPath = "..\typings\global_"
if (Test-Path $globalPath) {
    Remove-Item -Recurse -Force $globalPath
    Write-Host "Removed broken global_ stubs" -ForegroundColor Yellow
}

Write-Host "`nGenerating stubs..." -ForegroundColor Cyan

$args = @(
    "pythonnet-stub-generator\csharp\PythonNetStubTool\bin\Debug\net10.0\PythonNetStubGenerator.Tool.dll",
    "--dest-path", "..\typings",
    "--target-dlls", "JAStudio.Core\bin\Debug\net10.0\JAStudio.Core.dll,JAStudio.PythonInterop\bin\Debug\net10.0\JAStudio.PythonInterop.dll"
)

if ($OnlyTargetTypes) {
    Write-Host "Only generating JAStudio types (faster)..." -ForegroundColor Yellow
    $args += "--only-target-types"
} else {
    Write-Host "Generating all types including System.* (this will be slow)..." -ForegroundColor Yellow
}

dotnet @args

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nStubs regenerated successfully!" -ForegroundColor Green
} else {
    Write-Host "`nStub generation failed!" -ForegroundColor Red
    exit 1
}
