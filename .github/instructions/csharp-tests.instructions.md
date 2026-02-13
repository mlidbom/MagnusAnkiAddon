---
applyTo: "**/*.Tests/**/*.cs"
---

# C# Test Guidelines

**Scope:** All test code in `JAStudio.Core.Tests` and `JAStudio.UI.Tests`.

## JAStudio BDD Test Example

General BDD-style test conventions are in the shared instructions. Here is an example using this project's domain base classes:

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

Only the **outermost class** inherits the domain base class (`CollectionUsingTest` / `TestStartingWithEmptyCollection`).

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
