# Note Serialization Layer

> **Purpose**: This document captures the current state and next steps for the note serialization work. It is a continuation point, not a history log — completed items are removed.

## Vision

The git-based `jas_database/` is the **source of truth** for all note data. All data is already serialized to JSON — we can stop loading from Anki at any time.

The Anki integration layer becomes very thin: look up the `jas_note_id`, render the menus provided by our code, render the card view by calling our code, open dialogs in our code. Anki is just an SRS scheduler.

### Benefits

- Full version history of all note edits via git
- No dependency on Anki's SQLite database for data integrity
- Clean separation: our code owns all data and rendering, Anki is just an SRS scheduler
- Enables offline editing, backup, and collaboration via standard git workflows

## Architecture

### Serialization & Construction

Notes are constructed from DTOs. Each note type has a corresponding DTO class that represents the serialized JSON shape. The DTO is a dumb data bag — no logic, just the fields as they appear in JSON.

```
JSON string
    ↓ System.Text.Json
NoteDto
    ↓ Note constructor
JPNote (domain object)
    ↓ DtoMapper.ToDto()
NoteDto
    ↓ System.Text.Json
JSON string
```

Each note type has a **DtoMapper** class (e.g. `VocabDtoMapper`) responsible for extracting data from a live Note into the current DTO shape for serialization.

### Format Migration Strategy

**No per-file auto-migration.** Format migration is a **batch operation**:

1. Load the entire collection using the **old** serializer/DTO format → fully populated Note objects in memory
2. The mapper has access to the full collection, so cross-note resolution (e.g. string → NoteId) works
3. **New DtoMapper** extracts data from live Notes into the **new** DTO shape
4. **New serializer** writes the new DTOs to disk
5. Switch Note constructors to accept the new DTO type, delete old DTOs/mapper
6. Commit both code and data

This is explicitly a batch tool that runs once per migration. There is only ever one format at a time — old serialization code is deleted after migration.

**Why batch, not per-file:**
- Data migrations (string → NoteId, denormalized → normalized) require **global knowledge** of the entire collection
- Cross-note references can't be resolved without the full dataset loaded
- A one-time batch is simpler, testable, and avoids permanent migration infrastructure

### Components

| File | Role |
|------|------|
| `Storage/INoteRepository.cs` | Interface for note persistence — `Save` per type + `LoadAll` |
| `Storage/AllNotesData.cs` | Groups all notes (kanji, vocab, sentences), sorted by ID on construction |
| `Storage/NoteSerializer.cs` | Public API — `Serialize`/`Deserialize` per note type + `AllNotesData`, registered in DI |
| `Storage/FileSystemNoteRepository.cs` | Production `INoteRepository` — individual files per note (bucketed), bulk save with progress, single-file mode |
| `Storage/InMemoryNoteRepository.cs` | Test `INoteRepository` — in-memory dictionaries, no I/O |
| `Storage/Dto/*` | DTO classes matching the current JSON format |
| `Storage/Converters/*` | Converters: Note→DTO (for save) and DTO→NoteData (for load) |

### File System Layout

```
jas_database/
├── kanji/{2-char-hex-bucket}/{jas_note_id}.json
├── vocab/{2-char-hex-bucket}/{jas_note_id}.json
├── sentences/{2-char-hex-bucket}/{jas_note_id}.json
└── all_notes.json              (single-file mode)
```

Notes are bucketed into 256 subdirectories (00–ff) based on the first 2 hex chars of the GUID to keep directory sizes manageable.

### Auto-Save on Flush

When a note is flushed (`NoteFlushGuard.Flush()` → `UpdateInCache()`), the cache's `OnNoteUpdated` listener fires and calls `INoteRepository.Save(note)`. This is wired up in `JPCollection`'s constructor — each cache gets a listener that delegates to the injected `INoteRepository`.

### DI Registration

- `INoteRepository` — registered first (before `JPCollection`); `InMemoryNoteRepository` for tests, `FileSystemNoteRepository` for production
- `NoteSerializer` — singleton, injected with `NoteServices`
- `FileSystemNoteRepository` — singleton, injected with `NoteSerializer` + `TaskRunner`
- `JPCollection` — receives `INoteRepository`, registers cache update listeners

### Data Repository

`src/jas_database/` is an independent git repo (gitignored by JAStudio, remote: `https://github.com/mlidbom/JAStudioData.git`). Code and data commits are fully decoupled.

### Addon Root Dir

At runtime, `App.AddonRootDir` calls `AnkiFacade.GetAddonRootDir()` which delegates to `anki_facade_backend.addon_root_dir()` in Python. During tests, falls back to assembly-based path resolution. `App.DatabaseDir` is `{AddonRootDir}/jas_database`.

## Known Limitations

- Sentence count `"0"` vs empty string is treated as equivalent in field comparisons.
- DTOs store comma-separated fields as `List<string>` and rejoin with `", "` on roundtrip. This normalizes whitespace around separators, which is acceptable.

## Next Steps

- Design the V2 DTO format: typed IDs, proper structure (no more flat string fields)
- Build batch migration tool: load V1 → full collection in memory → resolve cross-note references → write V2
- Switch to loading from `jas_database/` instead of Anki (all data is already there)
- Build the thin Anki sync layer: map `jas_note_id` to Anki note IDs for SRS scheduling
