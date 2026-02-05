# JAStudio Workspace Instructions for AI Assistants

## Build Process

### C# / .NET Build Automation

**IMPORTANT**: The build process is fully automated. When you build the C# solution, it automatically:

1. **Copies runtime assemblies** - DLLs are automatically copied to `src\runtime_binaries\`
2. **Regenerates Python type stubs** - Type stubs are automatically generated in `typings\`

**DO NOT manually run these scripts after building:**
- ❌ `src\src_dotnet\copy-runtime-binaries.ps1`
- ❌ `src\src_dotnet\regenerate-stubs.ps1`

These are invoked automatically as part of the MSBuild process.

### How to Build

```powershell
# Build the entire solution (automatically updates binaries and stubs)
dotnet build src\src_dotnet\JAStudio.slnx -c Release
```

## Project Architecture

### Python as Thin Layer
This project is actively porting UI from Python/PyQt6 to C#/Avalonia. **Use Python as little as possible:**

- ✅ Menu logic, definitions, and handlers belong in C# (`JAStudio.UI`)
- ✅ Business logic belongs in C# (`JAStudio.Core`)
- ❌ Python should only be a thin integration layer with Anki
- ❌ Do not build menus or UI logic in Python

### Directory Structure
- `src\src_dotnet\` - C# source code (Avalonia UI, Core logic, Python interop)
  - `JAStudio.UI\` - Avalonia UI (porting target)
  - `JAStudio.Core\` - Domain logic (already ported)
  - `JAStudio.PythonInterop\` - Python ↔ C# bridge
- `src\jastudio_src\` - Python source (Anki addon, thin wrapper)
- `src\runtime_binaries\` - Compiled .NET DLLs (auto-generated, don't edit)
- `typings\` - Python type stubs for C# (auto-generated, don't edit)

### UI Porting Status
See [UI_PORTING_STATUS.md](../UI_PORTING_STATUS.md) for current porting progress.

## Python Environment

The project uses a virtual environment at `.venv\`. Python dependencies are managed via `requirements.txt`.

## Exception Handling

### CRITICAL: Never Swallow Exceptions

**NEVER, EVER swallow exceptions with empty catch blocks or logging-only handlers.**

❌ **FORBIDDEN - Silent failure:**
```python
try:
    critical_operation()
except Exception as e:
    logger.error(f"Error: {e}")  # WRONG - exception is swallowed
    # Execution continues as if nothing happened
```

```csharp
try
{
    CriticalOperation();
}
catch (Exception ex)
{
    JALogger.Log($"Error: {ex.Message}");  // WRONG - exception is swallowed
    // Execution continues as if nothing happened
}
```

✅ **CORRECT - Re-throw or wrap:**
```python
try:
    critical_operation()
except Exception as e:
    logger.error(f"Context: Operation failed: {e}")
    raise  # Re-throw the original exception
```

```python
try:
    critical_operation()
except SpecificError as e:
    # Add context and re-throw as a more specific error
    raise RuntimeError(f"Failed during initialization step X: {e}") from e
```

```csharp
try
{
    CriticalOperation();
}
catch (Exception ex)
{
    JALogger.Log($"Context: Operation failed: {ex.Message}");
    throw;  // Re-throw the original exception
}
```

### When Catching is Acceptable

Only catch exceptions when you have a **specific recovery strategy**:

✅ Retry logic with backoff
✅ Fallback to default values (for non-critical operations)
✅ Wrapping with more context and re-throwing
✅ Cleanup operations followed by re-throw

**Bottom line**: If you can't handle the error meaningfully, don't catch it. Let it propagate.
