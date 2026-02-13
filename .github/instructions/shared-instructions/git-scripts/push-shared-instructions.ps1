# git-scripts/ → shared-instructions/ → instructions/ → .github/ → repo root
$repoRoot = $PSScriptRoot | Split-Path | Split-Path | Split-Path | Split-Path
Push-Location $repoRoot
try {
   # Split with --rejoin caches the split point so future pushes only process new commits.
   # Without this, git subtree push walks the entire repo history every time.
   $branch = git subtree split --prefix .github/instructions/shared-instructions --rejoin
   if ($LASTEXITCODE -ne 0) { throw "git subtree split failed (exit code $LASTEXITCODE)" }
   git push https://github.com/mlidbom/copilot-code-standards-and-instructions.git "${branch}:main"
   if ($LASTEXITCODE -ne 0) { throw "git push failed (exit code $LASTEXITCODE)" }
}
finally { Pop-Location }
