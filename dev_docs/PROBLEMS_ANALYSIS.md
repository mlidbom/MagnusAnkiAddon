# Project Problems Analysis

Analysis of all warnings and suggestions reported across the JAStudio workspace, grouped by type.

**Total: 38 problems across 12 files** (2 suppressed as used from Python)

---

## 1. Dead Code — Never Used Members (15 unsuppressed + 2 suppressed)

Methods, properties, constants, and fields that are declared but never referenced.

### Never-Used Methods (10 + 1 suppressed)

| File | Member | Line |
|------|--------|------|
| `src/src_dotnet/JAStudio.UI/AppDialogs.cs` | `ShowDialog<T>()` | 24 |
| `src/src_dotnet/JAStudio.UI/AppDialogs.cs` | `ShowVocabFlagsDialog()` | 36 |
| `src/src_dotnet/JAStudio.UI/AppDialogs.cs` | `ShowVocabEditorDialog()` | 57 |
| `src/src_dotnet/JAStudio.UI/AppDialogs.cs` | `ShowKanjiEditorDialog()` | 77 |
| `src/src_dotnet/JAStudio.UI/AppDialogs.cs` | `ShowSentenceEditorDialog()` | 97 |
| `src/src_dotnet/JAStudio.UI/AppDialogs.cs` | `ShowAboutDialog()` | 117 |
| `src/src_dotnet/JAStudio.UI/AppDialogs.cs` | ~~`ToggleEnglishWordSearchDialog()`~~ **SUPPRESSED** — called from Python (`global_shortcuts.py`) | 175 |
| `src/src_dotnet/JAStudio.Core/App.cs` | `AddInitHook()` | 26 |
| `src/src_dotnet/JAStudio.Core/Note/NoteConstants.cs` | `FromType()` | 61 |
| `src/src_dotnet/JAStudio.Core/Note/NoteConstants.cs` | `IdFactoryFromType()` | 63 |
| `src/src_dotnet/JAStudio.Core/Note/Sentences/SentenceNote.cs` | `AddSentence()` | 182 |

### Never-Used Properties (2)

| File | Member | Line |
|------|--------|------|
| `src/src_dotnet/JAStudio.Core/Storage/FileSystemNoteRepository.cs` | `Serializer` | 21 |
| `src/src_dotnet/JAStudio.Core/App.cs` | `AnkiMediaDir` | 61 |

### Never-Used Constants/Fields (3 + 1 suppressed)

| File | Member | Line |
|------|--------|------|
| `src/src_dotnet/JAStudio.Core/Note/NoteConstants.cs` | `SentenceFields.Audio` | 17 |
| `src/src_dotnet/JAStudio.Core/Note/NoteConstants.cs` | `SentenceFields.Screenshot` | 19 |
| `src/src_dotnet/JAStudio.Core/Note/NoteConstants.cs` | `VocabCards.Listening` | 108 |
| `src/src_dotnet/JAStudio.Core/Note/NoteConstants.cs` | ~~`AppStillLoadingMessage`~~ **SUPPRESSED** — used from Python (`dotnet_rendering_content_renderer_anki_shim.py`, `common.py`) | 177 |

### Virtual Methods Never Used (2)

| File | Member | Line |
|------|--------|------|
| `src/src_dotnet/JAStudio.Core/Note/JPNote.cs` | `GetDependenciesRecursive()` | 141 |
| `src/src_dotnet/JAStudio.Core/Note/JPNote.cs` | `GetMediaReferences()` | 150 |

### Collection Updated But Never Read (1)

| File | Member | Line |
|------|--------|------|
| `src/src_dotnet/JAStudio.Core/App.cs` | `_initHooks` | 24 |

**Note:** `AppDialogs` methods may be called from Python via pythonnet at runtime — verify before removing.

---

## 2. Method Can Be Made Static (10 occurrences)

Instance methods that don't access `this` and could be `static`.

| File | Method | Line |
|------|--------|------|
| `src/src_dotnet/JAStudio.Core/Storage/FileSystemNoteRepository.cs` | `FindChangesSinceSnapshot` | 113 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Vocab/VocabNoteMenus.cs` | `BuildCreateNounVariationsMenuSpec` | 167 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Vocab/VocabNoteMenus.cs` | `BuildCreateVerbVariationsMenuSpec` | 182 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Vocab/VocabNoteMenus.cs` | `BuildCreateMiscMenuSpec` | 202 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Vocab/VocabNoteMenus.cs` | `BuildCopyMenuSpec` | 217 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Vocab/VocabNoteMenus.cs` | `BuildRemoveMenuSpec` | 256 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Vocab/VocabNoteMenus.cs` | `OnEditVocab` | 295 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Vocab/VocabNoteMenus.cs` | `FormatVocabMeaning` | 321 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Kanji/KanjiNoteMenus.cs` | `OnEditKanji` | 74 |
| `src/src_dotnet/JAStudio.UI/Menus/Notes/Sentence/SentenceNoteMenus.cs` | `OnEditSentence` | 54 |

---

## 3. Captured Variable Modified in Outer Scope (2 occurrences)

A lambda captures a variable that is reassigned after the lambda is created, which can lead to unexpected behavior.

| File | Line | Variable |
|------|------|----------|
| `src/src_dotnet/JAStudio.Core/Storage/FileSystemNoteRepository.cs` | 101 | `container` |
| `src/src_dotnet/JAStudio.Core/Storage/FileSystemNoteRepository.cs` | 105 | `container` |

The `container` variable is captured in lambdas passed to `scope.RunIndeterminate()` and is also reassigned between calls.

---

## 4. Expression Always True (Nullable Reference Types) (2 occurrences)

Null checks on values that the nullable annotations indicate can never be null.

| File | Line | Expression |
|------|------|------------|
| `src/src_dotnet/JAStudio.Core/Note/Sentences/SentenceNote.cs` | 108 | `parsingResult != null` |
| `src/src_dotnet/JAStudio.Core/Note/Sentences/SentenceNote.cs` | 146 | `parsingResult != null` |

---

## 5. PowerShell Automatic Variable Overwrite (2 occurrences)

Assigning to `$args`, which is a built-in automatic variable in PowerShell.

| File | Line | Description |
|------|------|-------------|
| `src/src_dotnet/regenerate-stubs.ps1` | 54 | Assignment to `$args` |
| `src/src_dotnet/regenerate-stubs.ps1` | 61 | Appending to `$args` |

---

## 6. Unnecessary Whitespace (1 occurrence)

| File | Line |
|------|------|
| `src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNote.cs` | 142 |

---

## 7. Possible Unintended Reference Comparison (1 occurrence)

Using `!=` instead of `!Equals()` on reference types may compare identity rather than value.

| File | Line | Expression |
|------|------|------------|
| `src/src_dotnet/JAStudio.Core/Note/Vocabulary/RelatedVocab/RelatedVocab.cs` | 86 | `homophone != _vocab` |

Since `JPNote` overrides `Equals()` and `GetHashCode()`, this `!=` comparison may work correctly if the operator is also overloaded, but the analyzer flags it as potentially unintended.

---

## 8. Constant Hides Class from Outer Class (1 occurrence)

A nested constant has the same name as a class visible in the outer scope.

| File | Line | Member |
|------|------|--------|
| `src/src_dotnet/JAStudio.Core/Note/NoteConstants.cs` | 155 | Constant `Kanji` hides class `Kanji` |

---

## Summary by Severity

| Category | Count | Severity | Fix Effort |
|----------|-------|----------|------------|
| Dead Code (never used) | 15 (+2 suppressed) | Medium | Low (verify Python interop first) |
| Method Can Be Static | 10 | Low | Low (add `static` keyword) |
| Captured Variable in Outer Scope | 2 | Medium | Medium (restructure lambda captures) |
| Expression Always True | 2 | Low | Low (remove redundant checks) |
| PowerShell `$args` Overwrite | 2 | Low | Low (rename variable) |
| Unnecessary Whitespace | 1 | Low | Trivial (auto-format) |
| Possible Reference Comparison | 1 | Medium | Low (use Equals or verify operator overload) |
| Name Hiding | 1 | Low | Low (rename constant) |
| **Total** | **38** (+2 suppressed) | | |

## Files Most Affected

| File | Problem Count |
|------|---------------|
| `VocabNoteMenus.cs` | 7 |
| `AppDialogs.cs` | 7 |
| `NoteConstants.cs` | 7 |
| `FileSystemNoteRepository.cs` | 4 |
| `SentenceNote.cs` | 3 |
| `App.cs` | 3 |
| `JPNote.cs` | 2 |
| `regenerate-stubs.ps1` | 2 |
| `KanjiNoteMenus.cs` | 1 |
| `SentenceNoteMenus.cs` | 1 |
| `VocabNote.cs` | 1 |
| `RelatedVocab.cs` | 1 |
