Push-Location (git -C "$PSScriptRoot" rev-parse --show-toplevel)
try { git subtree push --prefix .github/instructions/shared-instructions https://github.com/mlidbom/copilot-code-standards-and-instructions.git main }
finally { Pop-Location }
