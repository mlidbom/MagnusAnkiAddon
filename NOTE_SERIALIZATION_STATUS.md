# Note Serialization Layer

> **Purpose**: This document captures the current state and next steps for the note serialization work. It is a continuation point, not a history log — completed items are removed.

## Vision

This git repository becomes the **source of truth** for all note data. Anki notes will be stripped down to very few fields `jas_note_id`, audio fields required for anki to play audio, and likely the question and answer fields so that the user can search and find notes in anki. All all other data lives in the git repository.

The Anki integration layer becomes very thin: look up the `jas_note_id` render the menus provided by our code, render the card view by calling our code,  open dialogs in our code

### Benefits

- Full version history of all note edits via git
- No dependency on Anki's SQLite database for data integrity
- Clean separation: our code owns all data and rendering, Anki is just an SRS scheduler
- Enables offline editing, backup, and collaboration via standard git workflows

## Architecture

### Current Architecture (transitional)

```
JPNote (domain object)
    ↓ Converter.ToDto()
JSON string
    ↓ System.Text.Json
NoteDto
    ↓ Converter.FromDto()
NoteData (existing transfer object → note constructor)
```

The DTOs and `NoteData` are **temporary artifacts** of the current migration. They exist because the note types still expect to be constructed from `NoteData` (the Anki-era transfer object).

### Target Architecture

```
JPNote (domain object)
    ↔ System.Text.Json
JSON string
```

Once we fully migrate away from Anki as the data store, the note types will serialize directly to/from JSON — no intermediate DTOs or `NoteData`. The converters and DTO classes will be removed.

### Components

| File | Role |
|------|------|
| `Storage/Dto/KanjiNoteDto.cs` | Plain DTO for kanji notes |
| `Storage/Dto/VocabNoteDto.cs` | Plain DTO for vocab notes (includes `VocabMatchingRulesDto`, `VocabRelatedDataDto`) |
| `Storage/Dto/SentenceNoteDto.cs` | Plain DTO for sentence notes (includes `SentenceConfigurationDto`, `ParsingResultDto`, `ParsedMatchDto`, `WordExclusionDto`) |
| `Storage/Converters/KanjiNoteConverter.cs` | Kanji ↔ DTO conversion |
| `Storage/Converters/VocabNoteConverter.cs` | Vocab ↔ DTO conversion (handles matching rules & related vocab serialization) |
| `Storage/Converters/SentenceNoteConverter.cs` | Sentence ↔ DTO conversion (handles configuration & parsing result) |
| `Storage/NoteSerializer.cs` | Public API — `Serialize`/`Deserialize` per note type, registered in DI container |

### DI Registration

`NoteSerializer` is registered as a singleton in `AppBootStrapper.cs`, injected with `NoteServices`.

## Known Limitations

- Sentence count `"0"` vs empty string is treated as equivalent in field comparisons.
- DTOs store comma-separated fields as `List<string>` and rejoin with `", "` on roundtrip. This normalizes whitespace around separators, which is acceptable.

## Next Steps

- Implement file-based storage: persist each note as a JSON file keyed by `jas_note_id`
- Build the thin Anki sync layer: map `jas_note_id` to Anki note IDs for SRS scheduling
- Migrate existing Anki note data into the git-based storage
