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
| `Storage/AllNotesData.cs` | Groups all notes (kanji, vocab, sentences), sorted by ID on construction |
| `Storage/NoteSerializer.cs` | Public API — `Serialize`/`Deserialize` per note type + `AllNotesData`, registered in DI |
| `Storage/FileSystemNoteRepository.cs` | File-based persistence — individual files per note + single-file mode, registered in DI |
| `Storage/Dto/*` | Internal DTOs (transitional, hidden behind `NoteSerializer`) |
| `Storage/Converters/*` | Internal converters (transitional, hidden behind `NoteSerializer`) |

### File System Layout

```
jas_database/
├── kanji/{jas_note_id}.json
├── vocab/{jas_note_id}.json
├── sentences/{jas_note_id}.json
└── all_notes.json              (single-file mode)
```

### DI Registration

- `NoteSerializer` — singleton, injected with `NoteServices`
- `FileSystemNoteRepository` — singleton, injected with `NoteSerializer`, root dir = `App.DatabaseDir`

### Addon Root Dir

At runtime, `App.AddonRootDir` calls `AnkiFacade.GetAddonRootDir()` which delegates to `anki_facade_backend.addon_root_dir()` in Python. During tests, falls back to assembly-based path resolution. `App.DatabaseDir` is `{AddonRootDir}/jas_database`.

## Known Limitations

- Sentence count `"0"` vs empty string is treated as equivalent in field comparisons.
- DTOs store comma-separated fields as `List<string>` and rejoin with `", "` on roundtrip. This normalizes whitespace around separators, which is acceptable.

## Next Steps

- Build the thin Anki sync layer: map `jas_note_id` to Anki note IDs for SRS scheduling
- Migrate existing Anki note data into the git-based storage
- Set up `src/jas_database/` as an independent git repo (gitignored by the parent repo, separate remote for data)
