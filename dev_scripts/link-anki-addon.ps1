#!/usr/bin/env pwsh
# Repoints the Anki addon symlink to the src/ folder of the current worktree.
# Run from any worktree root (or it auto-detects from script location).
# Requires elevated permissions (symlinks on Windows need admin or Developer Mode).

$ErrorActionPreference = "Stop"

# Resolve the workspace root from the script's own location
$WorkspaceRoot = Split-Path -Parent $PSScriptRoot  # script is in dev_scripts/, so parent is workspace root

# If the script somehow ends up at the workspace root itself, use $PSScriptRoot
if (-not (Test-Path (Join-Path $WorkspaceRoot "src"))) {
    $WorkspaceRoot = $PSScriptRoot
}

$SourceDir = Join-Path $WorkspaceRoot "src"
$AnkiAddonsDir = Join-Path $env:APPDATA "Anki2\addons21"
$LinkPath = Join-Path $AnkiAddonsDir "jastudio_module"

if (-not (Test-Path $SourceDir)) {
    Write-Error "Source directory not found: $SourceDir"
    exit 1
}

if (-not (Test-Path $AnkiAddonsDir)) {
    Write-Error "Anki addons directory not found: $AnkiAddonsDir"
    exit 1
}

# Remove existing symlink or directory
if (Test-Path $LinkPath) {
    $item = Get-Item $LinkPath -Force
    if ($item.LinkType -eq "SymbolicLink") {
        $currentTarget = $item.Target
        if ($currentTarget -eq $SourceDir) {
            Write-Host "Symlink already points to: $SourceDir" -ForegroundColor Green
            exit 0
        }
        Write-Host "Removing existing symlink: $LinkPath -> $currentTarget" -ForegroundColor Yellow
        $item.Delete()
    } else {
        Write-Error "$LinkPath exists but is not a symlink. Remove it manually."
        exit 1
    }
}

New-Item -ItemType SymbolicLink -Path $LinkPath -Target $SourceDir | Out-Null
Write-Host "Symlink created: $LinkPath -> $SourceDir" -ForegroundColor Green
