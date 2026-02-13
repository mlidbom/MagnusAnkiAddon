$repoRoot = (git -C "$PSScriptRoot" rev-parse --show-toplevel) -replace '/', '\'
Push-Location $repoRoot
try { git subtree push --prefix .github/instructions/shared-instructions https://github.com/mlidbom/copilot-code-standards-and-instructions.git main }
finally { Pop-Location }
