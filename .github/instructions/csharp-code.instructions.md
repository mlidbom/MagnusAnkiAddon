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

## Default Interface Methods (Mixins)

**Design rule:** Any method that can be defined in terms of other public methods on an interface SHOULD be implemented as a default method on the interface, because the implementation is identical for every implementing class and they should not be burdened with writing it over and over again.

This codebase uses **default interface methods extensively** as a mixin pattern. Interfaces often contain many convenience overloads and helper methods implemented as defaults that delegate to a small number of abstract members.

**Always check interfaces for default method implementations AND extension methods** before assuming a method doesn't exist or writing workarounds. If you only see a few abstract members on a class, look at the interface — it likely has many more methods available via defaults. Also check for extension method classes (often named `{TypeName}Extensions` or `{TypeName}CE`) that add convenience methods. Older code uses extension methods for the same mixin pattern; newer code uses default interface methods.

Example from Compze: `IMonitorCE` has ~10 abstract lock primitives (`TakeReadLock`, `TakeUpdateLock`, etc.) but provides ~12 default methods (`Read`, `Update`, `ReadWhen`, `Await`, etc.) that delegate to them — split across partial interface files:

```csharp
// Abstract — the only members implementors need to provide
IDisposable TakeReadLock(TimeSpan? timeout = null);
IDisposable TakeUpdateLock(TimeSpan? timeout = null);

// Default — delegates Action overload to Func overload
unit Read(Action action, TimeSpan? timeout = null) => Read(action.AsFunc(), timeout);

// Default — delegates to abstract TakeReadLock
TReturn Read<TReturn>(Func<TReturn> func, TimeSpan? timeout = null)
{
   using(TakeReadLock(timeout)) return func();
}
```

This pattern is pervasive in Compze and throughout this project's code.

## Build & Verification

See the main `copilot-instructions.md` for full build, test, and Definition of Done details.

## NuGet Packages

JAStudio is an end-user application, not a library. **Freely add NuGet packages** when they are the right tool for the job. The goal is the best, most maintainable code and result — not minimal dependencies. If a package solves the problem well, use it.

(This does NOT apply to the Compze submodule, which is a library and must minimize its dependency footprint.)
