# Project Problems Analysis

Analysis of all warnings and suggestions reported across the JAStudio workspace, grouped by type.

**Total: ~81 reported problems across 13 files**

---

## 1. Unnecessary Whitespace (22 occurrences)

Trailing or extraneous whitespace in code lines. All occur in menu builder files using multi-line `SpecMenuItem.Command(...)` calls.

| File | Line(s) |
|------|---------|
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Kanji/KanjiNoteMenus.cs` | 31, 38, 42, 44, 46, 56, 58, 60, 62, 65 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Sentence/SentenceNoteMenus.cs` | 44, 46, 48, 50, 76, 78, 80, 82, 97, 99, 101 |
| `src/src_dotnet/JAStudio.Core/Note/Sentences/SentenceNote.cs` | 153 |

---

## 2. Dead Code — Never Used Members (21 occurrences)

Methods, properties, constants, and fields that are declared but never referenced.

### Never-Used Methods (14)

| File | Member | Line |
|------|--------|------|
| `src/src_dotnet/JAStudio.UI/AppDialogs.cs` | `ShowDialog<T>()` | 26 |
| `src/src_dotnet/JAStudio.UI/AppDialogs.cs` | `ShowVocabFlagsDialog()` | 38 |
| `src/src_dotnet/JAStudio.UI/AppDialogs.cs` | `ShowVocabEditorDialog()` | 59 |
| `src/src_dotnet/JAStudio.UI/AppDialogs.cs` | `ShowKanjiEditorDialog()` | 79 |
| `src/src_dotnet/JAStudio.UI/AppDialogs.cs` | `ShowSentenceEditorDialog()` | 99 |
| `src/src_dotnet/JAStudio.UI/AppDialogs.cs` | `ShowAboutDialog()` | 119 |
| `src/src_dotnet/JAStudio.UI/AppDialogs.cs` | `ToggleEnglishWordSearchDialog()` | 176 |
| `src/src_dotnet/JAStudio.Core/App.cs` | `AddInitHook()` | 28 |
| `src/src_dotnet/JAStudio.Core/Note/NoteConstants.cs` | `FromType()` | 59 |
| `src/src_dotnet/JAStudio.Core/Note/NoteConstants.cs` | `IdFactoryFromType()` | 61 |
| `src/src_dotnet/JAStudio.Core/Note/JPNote.cs` | `GetDependenciesRecursive()` | 160 |
| `src/src_dotnet/JAStudio.Core/Note/JPNote.cs` | `GetMediaReferences()` | 169 |
| `src/src_dotnet/JAStudio.Core/Note/Sentences/SentenceNote.cs` | `AddSentence()` | 189 |
| `src/src_dotnet/JAStudio.Core/Note/NoteFields/MutableStringField.cs` | `GetImageReferences()` | 36 |

### Never-Used Properties (2)

| File | Member | Line |
|------|--------|------|
| `src/src_dotnet/JAStudio.Core/Storage/FileSystemNoteRepository.cs` | `Serializer` | 20 |
| `src/src_dotnet/JAStudio.Core/App.cs` | `AnkiMediaDir` | 63 |

### Never-Used Constants/Fields (4)

| File | Member | Line |
|------|--------|------|
| `src/src_dotnet/JAStudio.Core/Note/NoteConstants.cs` | `SentenceFields.Audio` | 15 |
| `src/src_dotnet/JAStudio.Core/Note/NoteConstants.cs` | `SentenceFields.Screenshot` | 17 |
| `src/src_dotnet/JAStudio.Core/Note/NoteConstants.cs` | `VocabCards.Listening` | 106 |
| `src/src_dotnet/JAStudio.Core/Note/NoteConstants.cs` | `AppStillLoadingMessage` | 174 |

### Collection Updated But Never Read (1)

| File | Member | Line |
|------|--------|------|
| `src/src_dotnet/JAStudio.Core/App.cs` | `_initHooks` | 26 |

**Note:** `AppDialogs` methods may be called from Python via pythonnet at runtime — verify before removing.

---

## 3. Method Can Be Made Static (11 occurrences)

Instance methods that don't access `this` and could be `static`.

| File | Method | Line |
|------|--------|------|
| `src/src_dotnet/JAStudio.Core/Storage/FileSystemNoteRepository.cs` | `FindChangesSinceSnapshot` | 112 |
| `src/src_dotnet/JAStudio.Core.Tests/Storage/FileSystemNoteRepositoryTests.cs` | `AssertAllNotesDataMatch` | 220 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Vocab/VocabNoteMenus.cs` | `BuildCreateNounVariationsMenuSpec` | 172 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Vocab/VocabNoteMenus.cs` | `BuildCreateVerbVariationsMenuSpec` | 187 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Vocab/VocabNoteMenus.cs` | `BuildCreateMiscMenuSpec` | 207 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Vocab/VocabNoteMenus.cs` | `BuildCopyMenuSpec` | 222 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Vocab/VocabNoteMenus.cs` | `BuildRemoveMenuSpec` | 261 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Vocab/VocabNoteMenus.cs` | `OnEditVocab` | 300 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Vocab/VocabNoteMenus.cs` | `FormatVocabMeaning` | 326 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Kanji/KanjiNoteMenus.cs` | `OnEditKanji` | 84 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Sentence/SentenceNoteMenus.cs` | `OnEditSentence` | 57 |

---

## 4. Namespace Does Not Match File Location (4 occurrences)

The declared namespace doesn't reflect the file's directory path.

| File | Current Namespace | Expected Namespace |
|------|------------------|--------------------|
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Kanji/KanjiNoteMenus.cs` | `JAStudio.UI.Menus` | `JAStudio.UI.Menus.Notes.Kanji` |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Sentence/SentenceNoteMenus.cs` | `JAStudio.UI.Menus` | `JAStudio.UI.Menus.Notes.Sentence` |
| `src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNote.cs` | `JAStudio.Core.Note` | `JAStudio.Core.Note.Vocabulary` |
| `src/src_dotnet/JAStudio.Core/Note/Sentences/SentenceNote.cs` | `JAStudio.Core.Note` | `JAStudio.Core.Note.Sentences` |

**Note:** These may be intentional — the files were moved to subdirectories while keeping the original namespace to avoid breaking references. Fixing requires updating all `using` statements across the codebase.

---

## 5. Non-readonly Field Referenced in `GetHashCode()` (5 occurrences)

Mutable fields used in `GetHashCode()` can cause issues when objects are stored in hash-based collections if the field value changes after insertion.

| File | Line | Field |
|------|------|-------|
| `src/src_dotnet/JAStudio.Core/Note/JPNote.cs` | 116 | `_hashValue` |
| `src/src_dotnet/JAStudio.Core/Note/JPNote.cs` | 118 | `_hashValue`, `_id` |
| `src/src_dotnet/JAStudio.Core/Note/JPNote.cs` | 119 | `_hashValue` |
| `src/src_dotnet/JAStudio.Core/Note/JPNote.cs` | 125 | `_hashValue` |

All in the same `GetHashCode()` override. The `_hashValue` field is used as a lazy cache and `_id` is the identity field.

---

## 6. Captured Variable Modified in Outer Scope (2 occurrences)

A lambda captures a variable that is reassigned after the lambda is created, which can lead to unexpected behavior.

| File | Line | Variable |
|------|------|----------|
| `src/src_dotnet/JAStudio.Core/Storage/FileSystemNoteRepository.cs` | 100 | `container` |
| `src/src_dotnet/JAStudio.Core/Storage/FileSystemNoteRepository.cs` | 104 | `container` |

The `container` variable is captured in lambdas passed to `scope.RunIndeterminate()` and is also reassigned between calls.

---

## 7. Expression Always True (Nullable Reference Types) (2 occurrences)

Null checks on values that the nullable annotations indicate can never be null.

| File | Line | Expression |
|------|------|------------|
| `src/src_dotnet/JAStudio.Core/Note/Sentences/SentenceNote.cs` | 115 | `parsingResult != null` |
| `src/src_dotnet/JAStudio.Core/Note/Sentences/SentenceNote.cs` | 153 | `parsingResult != null` |

---

## 8. Possible Unintended Reference Comparison (1 occurrence)

Using `!=` instead of `!Equals()` on reference types may compare identity rather than value.

| File | Line | Expression |
|------|------|------------|
| `src/src_dotnet/JAStudio.Core/Note/Vocabulary/RelatedVocab/RelatedVocab.cs` | 86 | `homophone != _vocab` |

Since `JPNote` overrides `Equals()` and `GetHashCode()`, this `!=` comparison may work correctly if the operator is also overloaded, but the analyzer flags it as potentially unintended.

---

## 9. Constant Hides Class from Outer Class (1 occurrence)

A nested constant has the same name as a class visible in the outer scope.

| File | Line | Member |
|------|------|--------|
| `src/src_dotnet/JAStudio.Core/Note/NoteConstants.cs` | 153 | Constant `Kanji` hides class `Kanji` |

---

## Summary by Severity

| Category | Count | Severity | Fix Effort |
|----------|-------|----------|------------|
| Unnecessary Whitespace | 22 | Low | Trivial (auto-format) |
| Dead Code (never used) | 21 | Medium | Low (verify Python interop first) |
| Method Can Be Static | 11 | Low | Low (add `static` keyword) |
| Non-readonly Field in GetHashCode | 5 | Medium | Medium (make fields readonly or restructure) |
| Namespace Mismatch | 4 | Medium | Medium (update all references) |
| Captured Variable in Outer Scope | 2 | Medium | Medium (restructure lambda captures) |
| Expression Always True | 2 | Low | Low (remove redundant checks) |
| Possible Reference Comparison | 1 | Medium | Low (use Equals or verify operator overload) |
| Name Hiding | 1 | Low | Low (rename constant) |
| **Total** | **~69 unique** | | |

## Files Most Affected

| File | Problem Count |
|------|---------------|
| `KanjiNoteMenus.cs` | 12 |
| `SentenceNoteMenus.cs` | 13 |
| `VocabNoteMenus.cs` | 7 |
| `AppDialogs.cs` | 7 |
| `NoteConstants.cs` | 7 |
| `JPNote.cs` | 7 |
| `SentenceNote.cs` | 5 |
| `FileSystemNoteRepository.cs` | 4 |
| `App.cs` | 3 |
| `FileSystemNoteRepositoryTests.cs` | 1 |
| `VocabNote.cs` | 1 |
| `RelatedVocab.cs` | 1 |
| `MutableStringField.cs` | 1 |
