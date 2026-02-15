# Encapsulation Refactoring Status

## Goal

Cleanly separate Anki data/code from corpus (domain) data/code, with mapping code as the only bridge. Encapsulate the raw field dictionary inside the note class hierarchy so no external code can bypass typed properties.

## What Was Done

### 1. Removed `//Remove` constants from `AnkiFieldNames`

Removed 37 Anki field constants marked `//Remove` across `AnkiFieldNames.Vocab` (17), `AnkiFieldNames.Kanji` (13), `AnkiFieldNames.Sentence` (7).

**Kept 5 constants** that `QueryBuilder` still uses for Anki search queries (with comments explaining why):
- `Vocab.Reading`, `Vocab.Forms`
- `Kanji.ReadingOn`, `Kanji.ReadingKun`
- `Sentence.ParsingResult`

### 2. Removed corresponding `AnkiNoteWrapper` properties

All properties on `AnkiVocabNote`, `AnkiKanjiNote`, `AnkiSentenceNote` that referenced deleted constants were removed.

### 3. Simplified `FromAnki()` methods on `*Data` classes

`VocabData.FromAnki()`, `KanjiData.FromAnki()`, `SentenceData.FromAnki()` now only read fields that still have Anki constants (sync-to/from-anki fields). Domain data gets its defaults when constructed from Anki — the real data lives in the filesystem store.

### 4. Made `GetField`/`SetField` protected on `JPNote`

Changed from `public` → `protected`. Only `JPNote` and its subclasses (`VocabNote`, `KanjiNote`, `SentenceNote`) can call these methods. This is enforced at compile time.

### 5. Refactored field wrapper types to use delegates

Since `MutableStringField` and `CachingMutableStringField` aren't subclasses of `JPNote`, they can't access `protected` members. They were refactored to accept `Func<string, string>` getter and `Action<string, string>` setter delegates instead of a `JPNote` reference. The note subclasses pass `GetField` and `SetField` as method groups (accessible because they're `protected`). Nobody outside the hierarchy can create these delegates.

**Changed field wrapper constructors:**
- `MutableStringField(string fieldName, Func<string, string> getter, Action<string, string> setter)`
- `CachingMutableStringField(string fieldName, Func<string, string> getter, Action<string, string> setter)`

**Composed field types now take pre-built wrappers:**
- `AudioField`, `WritableAudioField`, `ImageField`, `WritableImageField` → take `MutableStringField`
- `IntegerField`, `MutableSerializedObjectField<T>` → take `MutableStringField`
- `MutableCommaSeparatedStringsListField` → takes `CachingMutableStringField`
- `MutableCommaSeparatedStringsListFieldDeDuplicated` → takes `CachingMutableStringField`

**JPNote provides factory methods** for concise property declarations:
- `protected MutableStringField StringField(string fieldName)`
- `protected CachingMutableStringField CachingStringField(string fieldName)`

### 6. Updated all sub-objects to receive delegates from parent note

Sub-objects like `VocabNoteAudio`, `VocabNoteUserFields`, `VocabNoteForms`, `VocabNotePartsOfSpeech`, `VocabNoteQuestion`, `VocabNoteMetaData`, `VocabNoteUserCompoundParts`, `VocabNoteMatchingRules`, `VocabNoteMatchingConfiguration`, `RelatedVocab`, `SentenceUserFields` — all now receive `Func<string, string> getField, Action<string, string> setField` in their constructors, passed from the parent note where `GetField`/`SetField` are accessible.

### 7. Fixed all external callers to use public API

- `VocabNoteFactory` → uses `SourceAnswer.Set()`, `SourceAnswer.Value`, `SourceAnswer.Empty()`
- `VocabNoteGeneratedData` → uses `ActiveAnswer.Set()`
- `VocabNote.GetAnswer()` → uses `SourceAnswer.Value`
- `VocabNoteConverter` → uses `References.Value`
- `KanjiNoteConverter` → uses `PrimaryReadingsTtsAudio.Value`, `KanjiReferences.Value`
- Tests → use `SetRadicals()`, `SourceAnswer.Set()` instead of `SetField()`

### 8. Added missing typed properties

- `VocabNote.References` (MutableStringField)
- `KanjiNote.PrimaryReadingsTtsAudio` (MutableStringField)
- `KanjiNote.KanjiReferences` (MutableStringField)

## Current Architecture

### Separation of Concerns

| Layer | References Anki types? | References corpus types? |
|---|---|---|
| Domain notes (VocabNote, KanjiNote, SentenceNote) | No | Uses NoteFieldsConstants |
| Converters (VocabNoteConverter etc.) | No | Reads domain notes → writes *Data |
| Anki wrappers (AnkiVocabNote etc.) | Yes (AnkiFieldNames) | No |
| *Data classes (VocabData etc.) | **Yes** — FromAnki() bridge only | N/A (they ARE corpus) |
| AnkiFieldNames | N/A (they ARE Anki) | No |
| NoteFieldsConstants | No | N/A (they ARE corpus) |
| QueryBuilder | Yes (AnkiFieldNames) | No |

The one cross-boundary point is the `FromAnki()` methods on `*Data` — the mapping bridge.

### Field Access Encapsulation

- `GetField`/`SetField` on `JPNote` are `protected` — compile-time enforced
- All external access goes through typed properties (MutableStringField, ImageField, etc.)
- Field wrappers use delegates, not JPNote references — only note subclasses can provide these delegates
- Tests, converters, factories all use the public typed API

## Verification

- `dotnet build` — zero errors, zero warnings
- `dotnet test` — all 424 tests pass (411 Core + 13 UI)
- No `GetField`/`SetField` calls exist outside the note hierarchy and its internal field wrappers
