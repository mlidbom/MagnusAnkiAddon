Push-Location (git -C "$PSScriptRoot" rev-parse --show-toplevel)
try { git subtree add --prefix .github/instructions/shared-instructions https://github.com/mlidbom/copilot-code-standards-and-instructions.git main --squash }
finally { Pop-Location }
