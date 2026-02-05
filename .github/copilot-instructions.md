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
