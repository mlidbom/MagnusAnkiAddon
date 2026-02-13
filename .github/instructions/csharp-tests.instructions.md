---
applyTo: "**/*.Tests/**/*.cs"
---

# C# Test Guidelines

**Scope:** All test code in `JAStudio.Core.Tests` and `JAStudio.UI.Tests`.

## Test Infrastructure

### Base Classes (Mandatory)
All tests touching the domain **must** inherit from one of these:

- **`CollectionUsingTest`** — For tests that need sample data. Pass a `DataNeeded` flags enum to the constructor specifying the minimum data needed:
  ```csharp
  public class MyTests : CollectionUsingTest
  {
      public MyTests() : base(DataNeeded.Vocabulary) {}
  }
  ```
- **`TestStartingWithEmptyCollection`** — Shorthand for `DataNeeded.None`. Use when tests create all their own data.

`DataNeeded` flags: `None`, `Kanji`, `Vocabulary`, `Sentences`, `All`. **Use the minimum needed** — `All` when you only need kanji wastes setup time.

### Resolving Services
Use `GetService<T>()` from the base class to get services from the real DI container:
```csharp
var analyzer = GetService<TextAnalyzer>();
```
Do **not** construct service objects directly.

### Creating Test Notes
Use the available factory methods or the note will not be in the collection — **never call note constructors directly**:

## No Mocking
This project deliberately uses **no mock/stub frameworks** (no Moq, NSubstitute, etc.). Tests use the real DI container and real services. Each test gets a fresh `App` instance so there is no shared state.

## Parallel Execution
Tests run in parallel. Each test creates its own `App` instance through the base class.

## No noisy comments that are always the same
- Never Use `// Arrange`, `// Act`, `// Assert` comments. We know how tests are structured

## xunit
All test projects use **xunit v3** (`[Fact]` / `[Theory]` / `[InlineData]`).

## Test Naming
- Prefer short, descriptive names: `KanjiAddedCorrectly`, `EmptyObjectSerializesToEmptyString`
- `[Theory]` + `[InlineData]` for parameterised tests; `params` arrays for variable-length data

## Filesystem Tests
For tests that write to disk:
```csharp
var tempDir = Path.Combine(Path.GetTempPath(), $"JAStudio_test_{Guid.NewGuid():N}");
// ... use tempDir ...
// Clean up in Dispose()
```
