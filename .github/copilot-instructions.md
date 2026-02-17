# JAStudio Workspace Instructions for AI Assistants

JAStudio is a Japanese language learning tool that runs as an Anki addon. The core logic and UI are in C#/Avalonia, loaded into Anki's Python process via pythonnet. Python serves only as a thin integration layer with Anki's APIs.

## Quick Reference

```powershell
dotnet build src\src_dotnet\JAStudio.slnx -c Debug   # Fast .NET build (iteration)
dotnet test src\src_dotnet\JAStudio.slnx -v quiet     # .NET tests
pytest                                                 # Python tests
.\full-build.ps1                                       # Full validation (Definition of Done)
ruff check --fix                                       # Lint + autofix Python
ruff format                                            # Format Python
```

## Tech Stack

**Languages & Frameworks:**
- **C# / .NET 10** - Primary language for UI (Avalonia) and business logic
- **Python 3.13** - Thin integration layer with Anki, minimal usage preferred
- **Avalonia UI** - Cross-platform .NET UI framework
- **PyQt6** - Required for Anki addon integration (Anki's UI is Qt-based)

**Key Tools:**
- **basedpyright** - Python type checker (strict, zero errors required)
- **ruff** - Python linter and formatter (configured in `pyproject.toml`)
- **pytest** - Python testing framework
- **dotnet test** - .NET testing framework
- **pythonnet** - Python ↔ C# interop bridge

**Dependencies:**
- Janome, jamdict, pykakasi, python-romkan-ng (Japanese language processing)
- beartype, typing_extensions, deepdiff, pyperclip, autoslot (Python utilities)

## Boundaries & Constraints

**DO NOT:**
- Edit auto-generated files: `runtime_binaries/`, `typings/`
- Modify `.github/workflows/` directory (CI configuration)
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

**On Windows (PowerShell):**
```powershell
dotnet test src\src_dotnet\JAStudio.slnx --verbosity quiet
pytest
```

**On Linux/CI** (set `JASTUDIO_VENV_PATH` so pythonnet can find the venv):
```bash
JASTUDIO_VENV_PATH="$(pwd)/venv" dotnet test src/src_dotnet/JAStudio.slnx --verbosity quiet --filter "FullyQualifiedName!~BulkLoaderTests"
source venv/bin/activate && pytest
```

**Note:** `BulkLoaderTests` require a test Anki database (`src/tests/collection.anki2`) not available in CI. Exclude them with `--filter "FullyQualifiedName!~BulkLoaderTests"`.

**Test Guidelines:**
- Write tests for new C# features in the appropriate `*.Tests` project
- Python test directories: `src/tests/jaspythonutils_tests/`, `src/tests/jaslib_tests/`, `src/tests/jastudio_tests/` — choose based on what code is under test
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
```

Then use the test commands from the "How to Test" section above.

## Project Architecture

### Python as Thin Layer
This project is actively porting UI from Python/PyQt6 to C#/Avalonia. **Use Python as little as possible:**

- ✅ Menu logic, definitions, and handlers belong in C# (`JAStudio.UI`)
- ✅ Business logic belongs in C# (`JAStudio.Core`)
- ❌ Python should only be a thin integration layer with Anki

### Directory Structure
- `dev_docs/` - Development progress notes and porting status documents
- `src/src_dotnet/` - C# source code (Avalonia UI, Core logic, Python interop)
  - `JAStudio.UI/` - Avalonia UI
  - `JAStudio.UI.DesktopHost/` - Desktop entry point for running Avalonia UI outside Anki
  - `JAStudio.Core/` - Domain logic
  - `JAStudio.Anki/` - Anki integration utilities (C# side)
  - `JAStudio.PythonInterop/` - Python ↔ C# bridge
  - `JAStudio.Core.Specifications/`, `JAStudio.UI.Specifications/` - .NET test projects (xunit)
- `src/jastudio_src/` - Python source (Anki addon, thin integration layer)
- `src/jaspythonutils_src/` - Python utility libraries
- `src/jaslib_src/` - Python libraries (Japanese language processing)
- `src/tests/` - Python tests (`jaspythonutils_tests/`, `jaslib_tests/`, `jastudio_tests/`)
- `src/jas_database/` - Snapshot data for Japanese language database
- `src/web/` - HTML templates and styles for Anki card rendering
- `src/user_files/` - User-specific configuration files
- `src/runtime_binaries/` - Compiled .NET DLLs (auto-generated, don't edit)
- `typings/` - Python type stubs for C# (auto-generated, don't edit)

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

## Comments
- Don't add comments unless they match existing style or explain complex logic
- Prefer self-documenting code over comments
- Update comments when changing code

## Dependencies
- **Use existing libraries** whenever possible
- **Only add/update libraries** if absolutely necessary
- **Don't update versions** unless required for the task
- **Install via package managers**: `dotnet add package`, `pip install`
