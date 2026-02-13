---
applyTo: "**/*.Tests/**/*.cs"
---

# C# Test Guidelines

**Scope:** All test code in `JAStudio.Core.Tests` and `JAStudio.UI.Tests`.

## BDD-Style Specification Tests (Preferred)

Write tests as **nested, inheritable classes** that read like executable specifications. Use `[XF]` (from `Compze.Utilities.Testing.XUnit.BDD`) instead of `[Fact]`.

### When adding tests to an existing test class that uses the older flat style:

- If it's relatively easy, refactor the existing test class to BDD-style nested structure, then add the new tests in that structure.
- If refactoring would be complex or risky, create a new test class using BDD-style structure for the new tests instead.
- Do NOT add new tests to the old flat structure — this only adds to the technical debt

### How it works
- Each nested class **inherits from its parent**, gaining access to shared setup
- Each level's **constructor** adds context (the "act" step)
- **`[XF]`** runs a test only in the class that declares it — inherited tests are silently excluded at discovery time
- Class names describe the scenario, method names describe the expected behavior

### Example with domain base class
```csharp
using Compze.Utilities.Testing.XUnit.BDD;

public class After_adding_a_kanji_note : TestStartingWithEmptyCollection
{
   readonly KanjiNote _note;
   public After_adding_a_kanji_note() => _note = CreateKanji("人", "person");

   [XF] public void note_is_in_collection() => Assert.Contains(_note, NoteServices.Collection.KanjiNotes);

   public class and_adding_a_vocab_note_using_that_kanji : After_adding_a_kanji_note
   {
      readonly VocabNote _vocab;
      public and_adding_a_vocab_note_using_that_kanji() => _vocab = CreateVocab("人間", "にんげん", "human");

      [XF] public void vocab_is_in_collection() => Assert.Contains(_vocab, NoteServices.Collection.VocabNotes);
      [XF] public void kanji_is_still_accessible() => Assert.NotNull(_note);
   }
}
```

This produces a readable specification tree in Test Explorer:
```
After_adding_a_kanji_note
├── note_is_in_collection
└── and_adding_a_vocab_note_using_that_kanji
    ├── vocab_is_in_collection
    └── kanji_is_still_accessible
```

### Naming conventions for BDD tests
- **Class names**: `snake_case` describing context — `When_...`, `After_...`, `with_...`, `and_...`, `that_...`
- **Method names**: `snake_case` describing the assertion — `registration_is_rejected`, `error_mentions_email`
- Only the **outermost class** inherits the domain base class (`CollectionUsingTest` / `TestStartingWithEmptyCollection`)
- Inner classes inherit from their **immediate parent**

### `[XF]` vs `[Fact]`
- Use **`[XF]`** for all new tests — it enables BDD nesting without duplicated runs
- `[Fact]` still works but **must not** be used in nested/inherited test hierarchies (causes exponential duplication)
- `[Theory]` / `[InlineData]` remain available for parameterised tests

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

## No Mocking
This project deliberately uses **no mock/stub frameworks** (no Moq, NSubstitute, etc.). Tests use the real DI container and real services. Each test gets a fresh `App` instance so there is no shared state.

## Parallel Execution
Tests run in parallel. Each test creates its own `App` instance through the base class.

## No noisy comments that are always the same
- Never use `// Arrange`, `// Act`, `// Assert` comments. We know how tests are structured.

## xunit
All test projects use **xunit v3**. Use `[XF]` for new tests, `[Theory]` / `[InlineData]` for parameterised tests.

## Filesystem Tests
For tests that write to disk:
```csharp
var tempDir = Path.Combine(Path.GetTempPath(), $"JAStudio_test_{Guid.NewGuid():N}");
// ... use tempDir ...
// Clean up in Dispose()
```
