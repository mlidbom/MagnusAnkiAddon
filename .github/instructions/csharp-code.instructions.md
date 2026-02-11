# C# Code Guidelines

**Scope:** This applies to all C# code in `src/src_dotnet/`:
- `JAStudio.Core/` - Core business logic, domain models
- `JAStudio.UI/` - Avalonia UI components and view models
- `JAStudio.PythonInterop/` - Python ↔ C# bridge
- `JAStudio.Anki/` - Anki integration utilities
- `*.Tests/` - Test projects

## Architecture Rules

### UI Code (JAStudio.UI)
- Use **Avalonia UI** for all new UI components
- Follow **MVVM pattern**: Views (XAML) + ViewModels (C#)
- ViewModels should not reference Avalonia types (maintain testability)
- Use ReactiveUI for property change notifications and commands

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

### Test Structure
```csharp
// ✅ GOOD - Clear, focused test
[Fact]
public void ProcessItems_WithValidInput_ReturnsFilteredResults()
{
    // Arrange
    var service = new ItemService();
    var items = new[] { "valid", "invalid", "valid" };
    
    // Act
    var results = service.ProcessItems(items);
    
    // Assert
    Assert.Equal(2, results.Count);
    Assert.All(results, item => Assert.Equal("valid", item));
}
```

### Test Naming
- Use descriptive names: `MethodName_Scenario_ExpectedResult`
- Group related tests in nested classes if helpful
- Use `[Theory]` with `[InlineData]` for parameterized tests

### Test Location
- Unit tests: Same namespace as code under test, in `*.Tests` project
- Keep tests close to the code they test
- UI tests go in `JAStudio.UI.Tests`

## Build & Verification

### Before Committing
```bash
# Quick build (iteration)
dotnet build src/src_dotnet/JAStudio.slnx -c Debug

# Run affected tests
JASTUDIO_VENV_PATH="$(pwd)/venv" dotnet test src/src_dotnet/JAStudio.slnx --verbosity quiet

# Full validation (before PR)
./full-build.ps1  # or ./setup-dev.sh on Linux
```

### Common Issues
- If tests fail due to missing venv, ensure `JASTUDIO_VENV_PATH` is set
- If build fails with pythonnet errors, run `./setup-dev.sh` first
- Exclude BulkLoaderTests in CI: `--filter "FullyQualifiedName!~BulkLoaderTests"`
