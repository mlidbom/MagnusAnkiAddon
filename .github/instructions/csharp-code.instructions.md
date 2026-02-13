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

## Code Quality

### Modern C# Features
```csharp
// ✅ GOOD - Modern C# idioms
public record UserData(string Name, int Age);

var result = items switch
{
    [] => "empty",
    [var single] => $"one: {single}",
    _ => "multiple"
};

var filtered = data
    .Where(x => x.IsValid)
    .Select(x => x.Name)
    .ToList();

// ❌ AVOID - Old-style verbose code
public class UserData
{
    public string Name { get; set; }
    public int Age { get; set; }
}

string result;
if (items.Length == 0)
    result = "empty";
else if (items.Length == 1)
    result = $"one: {items[0]}";
else
    result = "multiple";
```

### Exception Handling
See main copilot-instructions.md for critical exception handling rules.

**Key point:** Never catch and log without re-throwing, unless you have a specific recovery strategy.

### Naming Conventions
- PascalCase for public members, types, methods
- camelCase for private fields, local variables
- Prefix private fields with `_` (e.g., `_repository`)
- Use meaningful names; avoid abbreviations unless standard (ID, UI, etc.)

## Testing

See `csharp-tests.instructions.md` for detailed test conventions (base classes, fixture patterns, no-mocking policy, AI test conventions).

Test framework: **xunit v3** (all test projects use `[Fact]`/`[Theory]` attributes).

### Test Location
- Unit tests: Same namespace as code under test, in `*.Tests` project
- Keep tests close to the code they test
- UI tests go in `JAStudio.UI.Tests`

## Build & Verification

See the main `copilot-instructions.md` for full build, test, and Definition of Done details.

## Comments
- Don't add comments unless they match existing style or explain complex logic
- Prefer self-documenting code over comments
- Update comments when changing code
