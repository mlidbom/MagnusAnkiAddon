---
applyTo: "**/*.cs"
---

# C# Code Guidelines

**Scope:** This applies to all C# code:

## Architecture Rules

### UI Code
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
- Use immutable types where practical (readonly properties, private setters)
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


This pattern is pervasive in Compze and throughout this project's code.

## NuGet Packages

JAStudio is an end-user application, not a library. **Freely add NuGet packages** when they are the right tool for the job. The goal is the best, most maintainable code and result — not minimal dependencies. If a package solves the problem well, use it.

(This does NOT apply to the Compze submodule, which is a library and must minimize its dependency footprint.)
