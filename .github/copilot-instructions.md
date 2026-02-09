# JAStudio Workspace Instructions for AI Assistants

### How to Build

```powershell
dotnet build src\src_dotnet\JAStudio.slnx -c Debug # Build solution, generates type stubs and copies stubs and dlls to where they need to be for the python integration

basedpyright-wrapper.bat # Check the python for typing errors.
```

### How to Test

```powershell
dotnet test src\src_dotnet\JAStudio.slnx --verbosity quiet  # Run .NET tests
pytest src\tests                                             # Run Python tests
```

### Definition of Done

No task should be considered complete until:
- `basedpyright-wrapper.bat` reports **0 errors**
- All .NET tests pass
- All Python tests pass

### Python Type Errors

Do **not** suppress type errors with `# pyright: ignore` or `# type: ignore` comments. The code should almost always be fixed or restructured to satisfy the type checker. If you cannot find a way to make the type checker understand the code, ask for permission before adding a suppression.

## Project Architecture

### Python as Thin Layer
This project is actively porting UI from Python/PyQt6 to C#/Avalonia. **Use Python as little as possible:**

- ✅ Menu logic, definitions, and handlers belong in C# (`JAStudio.UI`)
- ✅ Business logic belongs in C# (`JAStudio.Core`)
- ❌ Python should only be a thin integration layer with Anki

### Directory Structure
- `src\src_dotnet\` - C# source code (Avalonia UI, Core logic, Python interop)
  - `JAStudio.UI\` - Avalonia UI (porting target)
  - `JAStudio.Core\` - Domain logic (already ported)
  - `JAStudio.PythonInterop\` - Python ↔ C# bridge
- `src\jastudio_src\` - Python source (Anki addon, thin wrapper)
- `src\runtime_binaries\` - Compiled .NET DLLs (auto-generated, don't edit)
- `typings\` - Python type stubs for C# (auto-generated, don't edit)

### UI Porting Status
Essentially done now.

## Python Environment

The project uses a virtual environment at `venv\`. Python dependencies are managed via `requirements.txt`.

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
