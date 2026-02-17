---
applyTo: "**/*.Tests/**/*.cs;**/*.Tests/**/*.cs"
---

# C# Specifications (Tests) Guidelines

**Scope:** All test specification code

## Specification Philosophy: Black-Box specifications

Specifications verify that things **actually work correctly together**. They are **not** unit tests that isolate a single component — they are black-box tests that exercise the real wiring.


## Test Infrastructure

### Base Classes
All tests touching the domain **must** inherit from one of these (at the outermost class level):

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
