# Missing Editor Fields Report

Fields present in Anki notes but **not displayed in the Avalonia edit dialogs**.
Format: `AnkiFieldName` (C# property name)

## Summary

### Sentence

| # | Anki Field | C# Property | In Logic | In Web | Editor Status | Recommendation |
|---|-----------|-------------|----------|--------|---------------|----------------|
| 1 | `Source` | — | No | No | Missing | Not handled at all |

### Kanji

| # | Anki Field | C# Property | In Logic | In Web | Editor Status | Recommendation |
|---|-----------|-------------|----------|--------|---------------|----------------|
| 2 | `__references` | — | No | Yes (template) | Missing | Not handled in C# |
| 3 | `__explanation` | — | No | Yes (template) | Missing | Not handled in C# |
| 4 | `_image` | — | No | Commented out | Missing | Not handled at all |
| 5 | `_primary_readings_tts_audio` | — | No | Yes (template) | Missing | Not handled in C# |

### Vocab

| # | Anki Field | C# Property | In Logic | In Web | Editor Status | Recommendation |
|---|-----------|-------------|----------|--------|---------------|----------------|
| 6 | `__references` | — | No | — | Missing | Not handled in C# |
| 7 | `Image` | — | No | No | Missing | Not handled at all |
| 8 | `__image` | — | No | No | Missing | Not handled at all |

## Detailed Findings

### Fields Now in Editor

The following fields have been added to the Avalonia edit dialogs (editable):

**Sentence:**
- `Audio Sentence` → `SentenceNote.Audio` (WritableAudioField)
- `Screenshot` → `SentenceNote.Screenshot` (via GetField/SetField)
- `ID` → `SentenceNote.Id` (MutableStringField)

**Kanji:**
- `__audio` → `KanjiNote` (via GetField/SetField with `NoteFieldsConstants.Kanji.Audio`)

**Vocab:**
- `Audio_b` → `VocabNote.Audio.First` (WritableAudioField)
- `Audio_g` → `VocabNote.Audio.Second` (WritableAudioField)
- `Audio_TTS` → `VocabNote.Audio.Tts` (WritableAudioField)
- `sentence_count` → `VocabNote.MetaData.SentenceCount` (IntegerField)
- `__related_vocab` → `VocabNote.RelatedNotes` (raw JSON string, editable)
- `__technical_notes` → `VocabNote.TechnicalNotes` (MutableStringField)

These were previously in the editor:
- Kanji: `__mnemonic` (UserMnemonic)
- Kanji: `__primary_Vocab` (PrimaryVocab)

---

### Remaining Missing Fields (No C# Property)

These fields have no C# constant or property. They would need to be added to the C# note model before they can appear in the editor. All can be accessed via `GetField`/`SetField` with the raw Anki field name string.

#### Sentence: `Source`
- No constant, no property, no usage anywhere in C#
- This usually contains the Anime Series the sentence is from

#### Kanji: `__references`
- Explicitly ignored in `AnkiVsFileSystemComparisonTests`
- Web: `{{__references}}` rendered by Anki's native mustache templating
- Contains links to articles abbout the kanji. An HTML string

#### Kanji: `__explanation`
- `NoteFieldsConstants.Vocab.UserExplanation = "__explanation"` exists for **Vocab**, not Kanji
- Web: `{{__explanation}}` in kanji template
- Some notes/explanations about the kanji

#### Kanji: `_image`
- Explicitly ignored in comparison tests
- Web: template usage is **commented out**: `<!--<div id="userImage">{{_image}}</div>-->`
- Appears to be deprecated/unused
- Still there are some images I don't want to lose.

#### Kanji: `_primary_readings_tts_audio`
- No C# code references at all
- Web: `{{_primary_readings_tts_audio}}` at top of kanji template for audio playback

#### Vocab: `__references`
- No constant, no property
- Not referenced in any vocab mustache template
- Links to articles dealing with the vocab in some way.

#### Vocab: `Image`
- Explicitly ignored in comparison tests
- Not in vocab mustache templates (only in `basic.mustache`)

#### Vocab: `__image`
- Explicitly ignored in comparison tests
- Not in any vocab mustache template
