---
applyTo: "**/*.Tests/**/*.cs"
---

# C# Test Guidelines

**Scope:** All test code in `JAStudio.Core.Tests` and `JAStudio.UI.Tests`.

## Test Infrastructure

### Base Classes (Mandatory)
All tests touching the domain **must** inherit from one of these (at the outermost class level):

- **`CollectionUsingTest`** — For tests that need sample data. Pass a `DataNeeded` flags enum:
  ```csharp
  public class When_vocab_has_kanji : CollectionUsingTest
  {
      public When_vocab_has_kanji() : base(DataNeeded.Vocabulary) {}
  }
  ```
- **`TestStartingWithEmptyCollection`** — Shorthand for `DataNeeded.None`. Use when tests create all their own data.

`DataNeeded` flags: `None`, `Kanji`, `Vocabulary`, `Sentences`, `All`. **Use the minimum needed**.

### Resolving Services
Use `GetService<T>()` from the base class to get services from the real DI container:
```csharp
var analyzer = GetService<TextAnalyzer>();
```
Do **not** construct service objects directly.

### Creating Test Notes
Use the available factory methods or the note will not be in the collection — **never call note constructors directly**.

## Parallel Execution
Tests run in parallel. Each test creates its own `App` instance through the base class — no shared state.

## Filesystem Tests
For tests that write to disk:
```csharp
var tempDir = Path.Combine(Path.GetTempPath(), $"JAStudio_test_{Guid.NewGuid():N}");
// ... use tempDir ...
// Clean up in Dispose()
```
