---
applyTo: "**/*.cs"
---

# C# Code Guidelines

**Scope:** This applies to all C# code:

## Architecture Rules

### UI Code (JAStudio.UI)
- Use **Avalonia UI** for all new UI components
- Follow **MVVM pattern**: Views (XAML) + ViewModels (C#)
- ViewModels should not reference Avalonia types (maintain testability and the ability to use them with other UI frameworks)
- Use **CommunityToolkit.Mvvm** for property change notifications (`[ObservableProperty]`) and commands (`RelayCommand`, `AsyncRelayCommand`)
- `[ObservableProperty]` fields use `_camelCase` naming — the source generator creates a PascalCase property without the underscore:
  ```csharp
  // Field: _isInflectingWord → Generated property: IsInflectingWord
  [ObservableProperty] bool _isInflectingWord;
  ```

### Business Logic (JAStudio.Core)
- Keep pure domain logic in Core - no UI dependencies
- Make code testable: prefer dependency injection
- Use immutable types where practical (record types, readonly properties)
- No direct Anki/Python dependencies in Core

### Python Interop (JAStudio.PythonInterop)
- This is the **only** layer that should bridge C# ↔ Python
- Expose clean C# APIs that hide pythonnet complexity
- Handle Python exceptions and convert to appropriate C# exceptions
- Document Python type mappings clearly

### Anki Integration (JAStudio.Anki)
- C#-side utilities for interacting with Anki concepts
- No direct Python/pythonnet dependencies here — that belongs in PythonInterop
- Provides C# abstractions that the rest of the solution can consume

## Testing

### Test Location
- Unit tests: Same namespace as code under test, in `*.Tests` project
- Keep tests close to the code they test
- UI tests go in `JAStudio.UI.Tests`

## Build & Verification

See the main `copilot-instructions.md` for full build, test, and Definition of Done details.
