# Missing Editor Fields Report

Fields present in Anki notes but **not displayed in the Avalonia edit dialogs**.
Format: `AnkiFieldName` (C# property name)

## Summary

### Sentence

| # | Anki Field | C# Property | In Logic | In Web | Editor Status | Recommendation |
|---|-----------|-------------|----------|--------|---------------|----------------|
| 1 | `Audio Sentence` | `Audio` (WritableAudioField) | Yes | Yes | Missing | Read-only display |
| 2 | `Source` | — | No | No | Missing | Not handled at all |
| 3 | `Screenshot` | `Screenshot` (private) | Yes | Yes | Missing | Read-only display |
| 4 | `ID` | `Id` (MutableStringField) | Yes (storage) | No | Missing | Read-only display |

### Kanji

| # | Anki Field | C# Property | In Logic | In Web | Editor Status | Recommendation |
|---|-----------|-------------|----------|--------|---------------|----------------|
| 5 | `__references` | — | No | Yes (template) | Missing | Not handled in C# |
| 6 | `__explanation` | — | No | Yes (template) | Missing | Not handled in C# |
| 7 | `__audio` | (private write) | Yes (computed) | No | Missing | Auto-generated, read-only display |
| 8 | `_image` | — | No | Commented out | Missing | Not handled at all |
| 9 | `_primary_readings_tts_audio` | — | No | Yes (template) | Missing | Not handled in C# |

### Vocab

| # | Anki Field | C# Property | In Logic | In Web | Editor Status | Recommendation |
|---|-----------|-------------|----------|--------|---------------|----------------|
| 12 | `__technical_notes` | — | No | Yes (template) | Missing | Not handled in C# |
| 13 | `__related_vocab` | `RelatedNotes` (complex) | Yes | Yes (renderers) | Missing | Complex structure, read-only? |
| 14 | `__references` | — | No | — | Missing | Not handled in C# |
| 15 | `Audio_b` | `Audio.First` (WritableAudioField) | Yes | Yes | Missing | Read-only display |
| 16 | `Audio_g` | `Audio.Second` (WritableAudioField) | Yes | Yes | Missing | Read-only display |
| 17 | `Audio_TTS` | `Audio.Tts` (WritableAudioField) | Yes | Yes | Missing | Read-only display |
| 18 | `Image` | — | No | No | Missing | Not handled at all |
| 19 | `__image` | — | No | No | Missing | Not handled at all |
| 20 | `sentence_count` | `MetaData.SentenceCount` (computed) | Yes | Yes (CSS) | Missing | Auto-generated, read-only display |

## Detailed Findings

### Sentence Fields

#### `Audio Sentence` → `SentenceNote.Audio` (WritableAudioField)
- **Constant:** `SentenceNoteFields.Audio`
- **Used in:** `AddSentence()` when creating notes; `Audio.FirstAudioFilePath()` in web renderers
- **Web:** `{{Audio Sentence}}` in sentence card templates (listening front, reading back)
- **DTO:** Persisted in `SentenceNoteDto`
- **Editor:** Not in `SentenceEditorViewModel` or AXAML
- **Verdict:** Fully handled in logic. Could show as read-only in editor.

#### `Source` → No C# representation
- **No constant, no property, no usage anywhere in C#**
- **Tags handle source concepts** (`Tags.Source.Folder`, `Tags.Source.Jamdict`) but there's no standalone `Source` field
- **Verdict:** Not handled at all. Investigate whether this Anki field is still in use.

#### `Screenshot` → `SentenceNote.Screenshot` (private MutableStringField)
- **Constant:** `SentenceNoteFields.Screenshot`
- **Used in:** `AddSentence()` when creating notes
- **Web:** `{{Screenshot}}` in sentence back template
- **DTO:** Persisted in `SentenceNoteDto`
- **Editor:** Not exposed — property is **private**
- **Verdict:** Used in logic + web rendering. Could show as read-only in editor.

#### `ID` → `SentenceNote.Id` (MutableStringField)
- **Constant:** `SentenceNoteFields.Id`
- **Used in:** Persisted as `ExternalId` in `SentenceNoteDto`; converter maps it in `SentenceNoteConverter`
- **Editor:** Not in ViewModel or AXAML
- **Verdict:** Storage/identity field. Could show as read-only in editor for reference.

---

### Kanji Fields

#### `__references` → No C# representation
- **No constant, no property**
- **Explicitly ignored** in `AnkiVsFileSystemComparisonTests`
- **Web:** `{{__references}}` rendered by Anki's native mustache templating in kanji template
- **Verdict:** Template-only field. Would need C# property to display in editor.

#### `__mnemonic` → `KanjiNote.UserMnemonic` ✅ Already in editor
- **Constant:** `NoteFieldsConstants.Kanji.UserMnemonic`
- **ViewModel:** Exposed in `KanjiEditorViewModel`
- **AXAML:** Displayed as "Mnemonic" TextBox in `KanjiEditorDialog.axaml`
- **Logic:** `ActiveMnemonic`, `BootstrapMnemonicFromRadicals()`, `PopulateRadicalsFromMnemonicTags()`
- **Verdict:** Fully handled. No action needed.

#### `__explanation` → No C# representation (for Kanji)
- **Note:** `NoteFieldsConstants.Vocab.UserExplanation = "__explanation"` exists for **Vocab**, not Kanji
- **No Kanji constant, no Kanji property**
- **Web:** `{{__explanation}}` in kanji template
- **Verdict:** Template-only field for Kanji. Would need C# property to display in editor.

#### `__audio` → Auto-generated (private write)
- **Constant:** `NoteFieldsConstants.Kanji.Audio`
- **Written by:** `SetPrimaryVocabAudio()` private method, called from `UpdateGeneratedData()`
- **Logic:** Audio is **auto-populated** from `PrimaryVocab` notes' audio files
- **DTO:** Persisted in `KanjiNoteDto`
- **Verdict:** Computed field. Could show as read-only in editor.

#### `_image` → No C# representation
- **No constant, no property**
- **Explicitly ignored** in comparison tests
- **Web:** Template usage is **commented out**: `<!--<div id="userImage">{{_image}}</div>-->`
- **Verdict:** Not handled at all. Appears to be a deprecated/unused field.

#### `_primary_readings_tts_audio` → No C# representation
- **No constant, no property, no C# code references**
- **Web:** `{{_primary_readings_tts_audio}}` at top of kanji template for audio playback
- **Verdict:** Template-only field. Not handled in C#.

#### `__primary_Vocab` → `KanjiNote.PrimaryVocab` ✅ Already in editor
- **Constant:** `NoteFieldsConstants.Kanji.PrimaryVocab`
- **ViewModel:** Exposed in `KanjiEditorViewModel`
- **AXAML:** Displayed as "Primary Vocab" TextBox
- **Logic:** Extensive — `PositionPrimaryVocab()`, `RemovePrimaryVocab()`, `GenerateDefaultPrimaryVocab()`, menu actions
- **Verdict:** Fully handled. No action needed.

---

### Vocab Fields

#### `__technical_notes` → No C# representation
- **No constant, no property**
- **Explicitly ignored** in comparison tests
- **Web:** `{{__technical_notes}}` in vocab back template
- **Verdict:** Template-only field. Would need C# property to display in editor.

#### `__related_vocab` → `VocabNote.RelatedNotes` (complex RelatedVocab object)
- **Constant:** `NoteFieldsConstants.Vocab.RelatedVocab`
- **Property:** Complex structure with sub-fields: `ErgativeTwin`, `Synonyms`, `PerfectSynonyms`, `Antonyms`, `SeeAlso`, `DerivedFrom`, `ConfusedWith`
- **Logic:** Extensive — `RelatedVocabsRenderer` generates web sections for homophones, synonyms, antonyms, see-also, confused-with, compounds, stems; `GetDirectDependencies()`
- **Web:** Rendered via dedicated C# renderers (not raw mustache)
- **DTO:** Full serialization/deserialization via `VocabNoteConverter`
- **Editor:** Not in ViewModel or AXAML
- **Verdict:** Fully handled in logic + web rendering. Complex structure — would need specialized editor UI.

#### `__references` (Vocab) → No C# representation
- **No constant, no property** (unlike Kanji which also lacks it)
- **Not in comparison test ignore list for vocab specifically**
- **Verdict:** Not handled at all.

#### `Audio_b` → `VocabNote.Audio.First` (WritableAudioField)
- **Constant:** `NoteFieldsConstants.Vocab.AudioB`
- **Logic:** First priority in `PrimaryAudio`/`PrimaryAudioPath` chain
- **Web:** `{{Audio_b}}` in vocab listening front and reading back templates
- **DTO:** Persisted in `VocabNoteDto`
- **Verdict:** Used in logic + web. Could show as read-only in editor.

#### `Audio_g` → `VocabNote.Audio.Second` (WritableAudioField)
- **Constant:** `NoteFieldsConstants.Vocab.AudioG`
- **Logic:** Second priority in `PrimaryAudio` chain
- **Web:** `{{Audio_g}}` in vocab listening front template
- **DTO:** Persisted in `VocabNoteDto`
- **Verdict:** Used in logic + web. Could show as read-only in editor.

#### `Audio_TTS` → `VocabNote.Audio.Tts` (WritableAudioField)
- **Constant:** `NoteFieldsConstants.Vocab.AudioTTS`
- **Logic:** Third/fallback priority in `PrimaryAudio` chain
- **Web:** `{{Audio_TTS}}` in vocab listening front template
- **DTO:** Persisted in `VocabNoteDto`
- **Verdict:** Used in logic + web. Could show as read-only in editor.

#### `Image` → No C# representation
- **No constant, no property**
- **Explicitly ignored** in comparison tests
- **Not in vocab mustache templates** (only referenced in `basic.mustache`)
- **Verdict:** Not handled at all for vocab notes.

#### `__image` → No C# representation
- **No constant, no property**
- **Explicitly ignored** in comparison tests
- **Not in any vocab mustache template**
- **Verdict:** Not handled at all.

#### `sentence_count` → `VocabNote.MetaData.SentenceCount` (IntegerField, computed)
- **Constant:** `NoteFieldsConstants.Vocab.SentenceCount`
- **Logic:** **Auto-computed** in `VocabNoteGeneratedData.UpdateGeneratedData()` — set to `vocab.Sentences.All().Count`
- **DTO:** Persisted in `VocabNoteDto`
- **Verdict:** Computed field. Could show as read-only in editor.

---

## Categories

### ✅ Already Displayed in Editor (2)
- Kanji: `__mnemonic` (UserMnemonic)
- Kanji: `__primary_Vocab` (PrimaryVocab)

### 📊 Has C# Property, Used in Logic — Could Add to Editor (10)
- Sentence: `Audio Sentence` — read-only display
- Sentence: `Screenshot` — read-only display (private property, needs exposure)
- Sentence: `ID` — read-only display
- Kanji: `__audio` — read-only display (auto-generated)
- Vocab: `__related_vocab` — complex structure, needs specialized UI
- Vocab: `Audio_b` — read-only display
- Vocab: `Audio_g` — read-only display
- Vocab: `Audio_TTS` — read-only display
- Vocab: `sentence_count` — read-only display (auto-generated)

### 🌐 Template-Only (Anki Native Rendering, No C# Code) (5)
- Kanji: `__references`
- Kanji: `__explanation`
- Kanji: `_primary_readings_tts_audio`
- Vocab: `__technical_notes`
- Vocab: `__references`

### ❌ Not Handled At All (3)
- Sentence: `Source`
- Kanji: `_image` (commented out in template)
- Vocab: `Image`
- Vocab: `__image`
