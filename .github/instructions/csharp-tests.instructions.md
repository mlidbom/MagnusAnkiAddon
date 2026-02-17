---
applyTo: "**/*.Tests/**/*.cs"
---

# C# Test Guidelines

**Scope:** All test code in `JAStudio.Core.Tests` and `JAStudio.UI.Tests`.

## Testing Philosophy: Black-Box Integration Tests

Tests verify that things **actually work correctly together**. They are **not** unit tests that isolate a single component — they are black-box tests that exercise the real wiring.

**CRITICAL rules:**
- **Resolve components from the DI container** via `GetService<T>()`. Never construct services directly or duplicate the wiring logic from `AppBootstrapper` in tests.
- **Never make constructors, fields, or methods public just so tests can access them.** If a test can't reach something through the container, that's a design signal — fix the design, not the visibility.
- **Don't duplicate initialization details in tests.** Manually wiring up a component's dependencies in a test is fragile: it breaks when we refactor internals even though the domain code is correct, and it silently diverges from the real wiring over time.

The goal: if the domain code works, the tests pass. If the domain code breaks, the tests fail. Tests should not duplicate wiring details creating fragile implicit dependencies.

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
Do **not** construct service objects directly — this duplicates wiring, breaks encapsulation, and makes tests fragile.

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
