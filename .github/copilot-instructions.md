# JAStudio Workspace Instructions for AI Assistants

### How to Build

```powershell
dotnet build src\src_dotnet\JAStudio.slnx -c Debug # Fast build: compiles .NET only

.\full-build.ps1                                    # Full build: compiles .NET + regenerates Python type stubs + runs basedpyright
```

**Use the full build** when you are done making changes and need to validate everything (Definition of Done).
The fast build is for quick iteration — the Anki addon copies .NET binaries on its own startup, and stubs only need regenerating when the .NET API surface changes.

### How to Test

```powershell
dotnet test src\src_dotnet\JAStudio.slnx --verbosity quiet  # Run .NET tests
pytest src\tests                                             # Run Python tests
```

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

✅ **CORRECT - Just don't catch it at all or Re-throw or wrap:**


Only catch exceptions when you have a **specific recovery strategy**:

✅ Retry logic with backoff
✅ Wrapping with more context and re-throwing
✅ Cleanup operations followed by re-throw

**Bottom line**: If you can't handle the error meaningfully, don't catch it. Let it propagate.
