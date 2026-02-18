#!/usr/bin/env pwsh
# Copy .NET binaries to runtime folder for use by Python/Anki
# Gracefully skips locked files without failing the build

param(
    [Parameter(Mandatory=$true)]
    [string]$SourceDir,
    
    [Parameter(Mandatory=$true)]
    [string]$DestDir
)

# Ensure destination exists
if (-not (Test-Path $DestDir)) {
    New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
}

$filesToCopy = @("*.dll", "*.deps.json", "*.runtimeconfig.json", "*.staticwebassets.runtime.json", "*.staticwebassets.endpoints.json")
$copied = 0
$skipped = 0

foreach ($pattern in $filesToCopy) {
    $files = Get-ChildItem -Path $SourceDir -Filter $pattern -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        $destFile = Join-Path $DestDir $file.Name
        try {
            # Check if destination file exists and is different
            if (Test-Path $destFile) {
                $srcHash = (Get-FileHash $file.FullName -Algorithm MD5).Hash
                $dstHash = (Get-FileHash $destFile -Algorithm MD5).Hash
                if ($srcHash -eq $dstHash) {
                    # File unchanged, skip
                    continue
                }
            }
            
            Copy-Item -Path $file.FullName -Destination $destFile -Force -ErrorAction Stop
            $copied++
        }
        catch {
            # File likely locked - skip gracefully
            Write-Host "  Skipped (locked): $($file.Name)" -ForegroundColor Yellow
            $skipped++
        }
    }
}

if ($skipped -gt 0) {
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Red
    Write-Host "==================== FAILED TO UPDATE ASSEMBLIES FOR ANKI ==================" -ForegroundColor Red
    Write-Host "============================================================================" -ForegroundColor Red
    Write-Host "  $skipped file(s) were locked and could not be updated." -ForegroundColor Red
    Write-Host "  Anki is probably running and has the DLLs loaded." -ForegroundColor Red
    Write-Host "  1. CLOSE ANKI" -ForegroundColor Red
    Write-Host "  2. REBUILD THE SOLUTION to copy the updated assemblies" -ForegroundColor Red
    Write-Host "  3. Start Anki to load the new assemblies" -ForegroundColor Red
    Write-Host "============================================================================" -ForegroundColor Red
    Write-Host ""
}

# Always print status
if ($copied -gt 0 -or $skipped -gt 0) {
    Write-Host "Runtime binaries: $copied copied, $skipped skipped (locked)" -ForegroundColor $(if ($skipped -gt 0) { "Yellow" } else { "Green" })
} else {
    Write-Host "Runtime binaries: All files up to date (no changes detected)" -ForegroundColor Cyan
}

# Always exit successfully
exit 0
