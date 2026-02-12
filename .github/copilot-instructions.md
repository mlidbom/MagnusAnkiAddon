# JAStudio Workspace Instructions for AI Assistants

## Tech Stack

**Languages & Frameworks:**
- **C# / .NET 10** - Primary language for UI (Avalonia) and business logic
- **Python 3.13** - Thin integration layer with Anki, minimal usage preferred
- **Avalonia UI** - Cross-platform .NET UI framework
- **PyQt6** - Legacy UI (being phased out in favor of Avalonia)

**Key Tools:**
- **basedpyright** - Python type checker (strict, zero errors required)
- **pytest** - Python testing framework
- **dotnet test** - .NET testing framework
- **pythonnet** - Python ↔ C# interop bridge

**Dependencies:**
- Janome, jamdict, pykakasi, python-romkan-ng (Japanese language processing)
- beartype, typing_extensions, deepdiff, pyperclip, autoslot (Python utilities)

## Boundaries & Constraints

**DO NOT:**
- Edit auto-generated files: `runtime_binaries/`, `typings/`
- Modify `.github/agents/` directory (contains instructions for other agents)
- Suppress type errors with `# pyright: ignore` or `# type: ignore` without explicit permission
- Swallow exceptions without re-throwing (see Exception Handling section)
- Add significant Python logic (prefer C# unless interfacing with Anki)
- Touch build artifacts: `bin/`, `obj/`, `venv/`, `.vs/`, `CopilotIndices/`

**DO:**
- Put UI logic in C# (`JAStudio.UI`)
- Put business logic in C# (`JAStudio.Core`)
- Use Python only as thin Anki integration layer
- Re-throw or wrap exceptions with context
- Fix type errors properly rather than suppressing them

## How to Build

```powershell
dotnet build src\src_dotnet\JAStudio.slnx -c Debug # Fast build: compiles .NET only

.\full-build.ps1                                    # Full build: compiles .NET + regenerates Python type stubs + runs basedpyright
```

**Use the full build** when you are done making changes and need to validate everything (Definition of Done).
The fast build is for quick iteration — the Anki addon copies .NET binaries on its own startup, and stubs only need regenerating when the .NET API surface changes.

### How to Test

**Run all tests (Definition of Done):**
```bash
# .NET tests (on Linux/CI - set JASTUDIO_VENV_PATH for pythonnet)
JASTUDIO_VENV_PATH="$(pwd)/venv" dotnet test src/src_dotnet/JAStudio.slnx --verbosity quiet

# Exclude BulkLoaderTests (requires test database not available in CI)
JASTUDIO_VENV_PATH="$(pwd)/venv" dotnet test src/src_dotnet/JAStudio.slnx --verbosity quiet --filter "FullyQualifiedName!~BulkLoaderTests"

# Python tests
source venv/bin/activate && pytest src/tests/jaspythonutils_tests -v
```

**On Windows (PowerShell):**
```powershell
dotnet test src\src_dotnet\JAStudio.slnx --verbosity quiet
pytest src\tests
```

**Test Guidelines:**
- Write tests for new C# features in the appropriate test project
- Write Python tests in `src/tests/jaspythonutils_tests/`
- Follow existing test patterns and naming conventions
- Run relevant tests after making changes, not just at the end

### Definition of Done

No task should be considered complete until:
- `.\full-build.ps1` succeeds (compiles .NET, regenerates stubs, **0 basedpyright errors**)
- All .NET tests pass
- All Python tests pass

### Python Type Errors

Do **not** suppress type errors with `# pyright: ignore` or `# type: ignore` comments. The code should almost always be fixed or restructured to satisfy the type checker. If you cannot find a way to make the type checker understand the code, ask for permission before adding a suppression.

## Linux / CI Agent Setup

When developing on Linux (e.g. GitHub Actions runners, Copilot coding agents):

```bash
./setup-dev.sh                      # One-time: creates venv, installs deps, builds .NET

# Run .NET tests (set JASTUDIO_VENV_PATH so pythonnet can find the venv)
JASTUDIO_VENV_PATH="$(pwd)/venv" dotnet test src/src_dotnet/JAStudio.slnx --verbosity quiet

# Run Python tests
source venv/bin/activate && pytest src/tests/jaspythonutils_tests -v
```

**Note:** The `BulkLoaderTests` require a test Anki database (`src/tests/collection.anki2`) that is not currently available in CI.
Exclude them with: `--filter "FullyQualifiedName!~BulkLoaderTests"`

## Project Architecture

### Python as Thin Layer
This project is actively porting UI from Python/PyQt6 to C#/Avalonia. **Use Python as little as possible:**

- ✅ Menu logic, definitions, and handlers belong in C# (`JAStudio.UI`)
- ✅ Business logic belongs in C# (`JAStudio.Core`)
- ❌ Python should only be a thin integration layer with Anki

### Directory Structure
- `dev_docs/` - Development progress notes and porting status documents
- `src/src_dotnet/` - C# source code (Avalonia UI, Core logic, Python interop)
  - `JAStudio.UI/` - Avalonia UI (porting target)
  - `JAStudio.Core/` - Domain logic (already ported)
  - `JAStudio.PythonInterop/` - Python ↔ C# bridge
- `src/jastudio_src/` - Python source (Anki addon, thin wrapper)
- `src/runtime_binaries/` - Compiled .NET DLLs (auto-generated, don't edit)
- `typings/` - Python type stubs for C# (auto-generated, don't edit)

### UI Porting Status
Essentially done now.

## Python Environment

The project uses a virtual environment at `venv/`. Python dependencies are managed via `requirements.txt`.
On Linux, run `./setup-dev.sh` to create the venv and install all dependencies.

## Exception Handling

### CRITICAL: Never Swallow Exceptions

❌ **FORBIDDEN - Silent failure:**
```csharp
try
{
    CriticalOperation();
}
catch (Exception ex)
{
    JALogger.Log($"Error: {ex.Message}");  // WRONG - exception is swallowed
}
```

✅ **CORRECT - Re-throw or wrap:**
```csharp
// Option 1: Don't catch at all (preferred)
CriticalOperation();

// Option 2: Re-throw after logging
try
{
    CriticalOperation();
}
catch (Exception ex)
{
    JALogger.Log($"Error: {ex.Message}");
    throw; // CRITICAL: Must re-throw
}

// Option 3: Wrap with context
try
{
    CriticalOperation();
}
catch (Exception ex)
{
    throw new InvalidOperationException("Failed during critical operation", ex);
}
```

**Only catch exceptions when you have a specific recovery strategy:**
- ✅ Retry logic with backoff
- ✅ Wrapping with more context and re-throwing
- ✅ Cleanup operations followed by re-throw
- ✅ Converting to a different exception type (still re-throwing)

**Bottom line**: If you can't handle the error meaningfully, don't catch it. Let it propagate.

## Coding Standards

### C# Style
- Use modern C# idioms (record types, pattern matching, LINQ)
- Prefer immutability where practical
- Use meaningful variable and method names
- Keep methods focused and small

### Python Style
- Follow PEP 8
- Use type hints for all function signatures
- Maintain compatibility with existing code patterns

### Comments
- Don't add comments unless they match existing style or explain complex logic
- Prefer self-documenting code over comments
- Update comments when changing code

## Development Workflow

### Making Changes
1. **Understand first**: Explore the codebase before making changes
2. **Small iterations**: Make minimal, focused changes
3. **Test early**: Run relevant tests after each change, not just at the end
4. **Verify builds**: Use `dotnet build` for quick feedback during iteration
5. **Full validation**: Run `./full-build.ps1` (or `./setup-dev.sh` on Linux) before considering work complete

### Working on Linux/CI
When working in GitHub Actions or coding agent environments:
```bash
# First-time setup
./setup-dev.sh

# Activate Python environment for any Python work
source venv/bin/activate

# Run tests with proper environment
JASTUDIO_VENV_PATH="$(pwd)/venv" dotnet test src/src_dotnet/JAStudio.slnx --verbosity quiet --filter "FullyQualifiedName!~BulkLoaderTests"
pytest src/tests/jaspythonutils_tests -v
```

### Dependencies
- **Use existing libraries** whenever possible
- **Only add/update libraries** if absolutely necessary
- **Don't update versions** unless required for the task
- **Install via package managers**: `dotnet add package`, `pip install`
