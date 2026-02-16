# Media Storage — Design & Architecture

## Goals & Motivations

We are building a corpus of analyzed Japanese sentences/vocab for language study. Most sentences come from copyrighted material (anime, textbooks, learning platforms). Using them for study with linguistic breakdowns is fair use, but rights holders can be aggressive, so we need to:

1. **Isolate media from the core corpus.** The core corpus is pure language analysis — text, breakdowns, grammar, readings. No media files, no media references, no source-identifying data.
2. **Partition media by copyright regime.** Media lives in separate git repositories organized so that a takedown for one source (e.g. one anime) can be handled by deleting files without touching the core data or other media.
3. **Keep git repos at manageable size.** Binary media files (audio, images) are large. Separating them from the text corpus keeps the core repo small and fast.

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│  Core Corpus (git repo)                             │
│  jas_database/                                      │
│    kanji/{bucket}/{id}.json     ← pure language     │
│    vocab/{bucket}/{id}.json        analysis data    │
│    sentences/{bucket}/{id}.json    NO media refs    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  Media Repos (one or more separate git repos)       │
│                                                     │
│  commercial-001/                                    │
│    natsume/                                         │
│      a1/                                            │
│        a1b2c3d4-....mp3          ← media file       │
│        a1b2c3d4-....json         ← sidecar metadata │
│      f7/                                            │
│        f7e6d5c4-....png                             │
│        f7e6d5c4-....json                            │
│    mushishi/                                        │
│      ...                                            │
│                                                     │
│  commercial-002/                                    │
│    wanikani/                                        │
│      ...                                            │
│                                                     │
│  general/                                           │
│    tts/                                             │
│      3c/                                            │
│        3c4d5e6f-....mp3                             │
│        3c4d5e6f-....json                            │
│    forvo/                                           │
│      ...                                            │
└─────────────────────────────────────────────────────┘
```

### Key Principles

- **Core corpus stores no media data.** Not even MediaFileIds. The note JSON is purely about language analysis.
- **All note↔media association lives in the media layer.** Each media file's sidecar JSON declares which note it belongs to.
- **Directory structure is organizational, not semantic.** The routing config determines where files land at import time, but the path encodes no meaning — all metadata is in the sidecar JSON.
- **Sidecar JSON per media file.** Every media file has a companion `.json` file with the same GUID name containing all metadata about that file.

## Sidecar Metadata Format

Each media file is stored as a pair: `{guid}.{ext}` + `{guid}.json`. Different media types have **separate sidecar schemas** — audio and image are fundamentally different data and will diverge further over time (e.g. audio has duration, TTS engine; image has resolution; video will have frame range, subtitles track, etc.).

### JSON Serialization

The serializer is configured with `DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingDefault`. This means properties with `null`, `0`, `false`, or other default values are omitted from the JSON output. Benefits:

- **Smaller files** — most sidecar fields are optional; no need to write `"tts": null` on every non-TTS audio file
- **Clean git diffs** — when new optional properties are added to the schema, existing files don't change (no new `"newField": null` lines appearing across thousands of files)
- **Readable** — opening a sidecar shows only what's relevant to that specific file

The `noteSourceTag` field preserves the full source tag from the note at import time (e.g. `source::anime::natsume::s1::01`). This enables filtering, bulk updates, and re-routing by source without re-parsing note data.

### Shared media files

A single media file (e.g. pronunciation audio for 走る) may be referenced by multiple notes — the vocab note for 走る and every sentence note containing 走る. The sidecar uses `noteIds` (plural) to track all associated notes. During import, when a file is encountered that already exists (by original filename), its sidecar is updated to append the new note ID rather than creating a duplicate file.

### `ankiFieldName` — preserving the source field

The `ankiFieldName` field records which Anki note field the media came from (e.g. `"Audio.First"`, `"Audio.Tts"`, `"Screenshot"`). This is critical because the same note can have multiple audio fields with different copyright status — e.g. a vocab note's `Audio.First` is commercial (WaniKani) while `Audio.Tts` is free.

### Audio Sidecar (`{guid}.audio.json`)

**Copyrighted anime audio (sentence):**
```json
{
  "noteIds": ["9f8e7d6c-5b4a-3210-fedc-ba9876543210"],
  "noteSourceTag": "source::anime::natsume::s1::01",
  "ankiFieldName": "Audio",
  "originalFileName": "natsume_ep01_03m22s.mp3",
  "copyright": "Commercial"
}
```

**TTS-generated audio (wani sentence):**
```json
{
  "noteIds": ["9f8e7d6c-5b4a-3210-fedc-ba9876543210"],
  "noteSourceTag": "source::wani::level05",
  "ankiFieldName": "Audio",
  "copyright": "Free",
  "tts": {
    "engine": "azure-neural",
    "voice": "ja-JP-NanamiNeural",
    "version": "2025.1"
  }
}
```

**WaniKani vocabulary audio:**
```json
{
  "noteIds": ["abc12345-6789-0abc-def0-123456789abc"],
  "noteSourceTag": "source::wani::level05",
  "ankiFieldName": "Audio.First",
  "originalFileName": "走る_audio_b.mp3",
  "copyright": "Commercial"
}
```

**Shared pronunciation audio (vocab + multiple sentences):**
```json
{
  "noteIds": [
    "abc12345-6789-0abc-def0-123456789abc",
    "9f8e7d6c-5b4a-3210-fedc-ba9876543210",
    "11223344-5566-7788-99aa-bbccddeeff00"
  ],
  "noteSourceTag": "source::core2000::step01",
  "ankiFieldName": "Audio.First",
  "originalFileName": "走る_core2k.mp3",
  "copyright": "Commercial"
}
```

### Image Sidecar (`{guid}.image.json`)

**Screenshot from anime:**
```json
{
  "noteIds": ["9f8e7d6c-5b4a-3210-fedc-ba9876543210"],
  "noteSourceTag": "source::anime::natsume::s1::01",
  "ankiFieldName": "Screenshot",
  "originalFileName": "natsume_ep01_03m22s.png",
  "copyright": "Commercial"
}
```

### File naming convention

The sidecar extension encodes the media type, so the media type is knowable from the filename alone without reading the JSON:

```
a1b2c3d4-e5f6-7890-abcd-ef1234567890.mp3          ← audio file
a1b2c3d4-e5f6-7890-abcd-ef1234567890.audio.json   ← audio sidecar

f7e6d5c4-b3a2-1098-7654-321fedcba098.png           ← image file
f7e6d5c4-b3a2-1098-7654-321fedcba098.image.json    ← image sidecar
```

Each sidecar schema is independently extensible — adding audio-specific fields (duration, bitrate) or image-specific fields (resolution, format) doesn't affect the other type.

## Import-Time Routing

A manually maintained config maps **(note type, source tag prefix, field name)** to a storage directory and copyright status. The routing is **per note type** because the same source tag can have entirely different copyright implications depending on whether it's a vocab note or a sentence note.

```json
{
  "vocab": {
    "source::wani::": {
      "Audio.First":  { "directory": "commercial-002/wanikani", "copyright": "Commercial" },
      "Audio.Second": { "directory": "commercial-002/wanikani", "copyright": "Commercial" },
      "Audio.Tts":    { "directory": "general/tts",             "copyright": "Free" },
      "Image":        { "directory": "commercial-002/wanikani", "copyright": "Commercial" },
      "UserImage":    { "directory": "general/user",            "copyright": "Free" }
    },
    "source::core2000::": {
      "Audio.First":  { "directory": "commercial-003/core2000", "copyright": "Commercial" },
      "Audio.Tts":    { "directory": "general/tts",             "copyright": "Free" }
    }
  },
  "sentence": {
    "source::anime::natsume::": {
      "Audio":      { "directory": "commercial-001/natsume", "copyright": "Commercial" },
      "Screenshot": { "directory": "commercial-001/natsume", "copyright": "Commercial" }
    },
    "source::anime::mushishi::": {
      "Audio":      { "directory": "commercial-001/mushishi", "copyright": "Commercial" },
      "Screenshot": { "directory": "commercial-001/mushishi", "copyright": "Commercial" }
    },
    "source::wani::": {
      "Audio":      { "directory": "general/tts",             "copyright": "Free" }
    },
    "source::core2000::": {
      "Audio":      { "directory": "commercial-003/core2000", "copyright": "Commercial" }
    }
  },
  "kanji": {
    "default": {
      "Audio": { "directory": "general/kanji", "copyright": "Free" },
      "Image": { "directory": "general/kanji", "copyright": "Free" }
    }
  },
  "default": { "directory": "general/uncategorized", "copyright": "Free" }
}
```

At import time, the lookup is: find the note type section → match source tag by longest prefix → find the field name → get directory + copyright. Unmatched combinations fall through to `"default"`.

**This config is import-time only.** Once files are stored, the routing config is not consulted again. The `MediaFileIndex` discovers files by scanning the filesystem.

This mapping is specific to the initial Anki import. Future imports will specify source/copyright at import time directly, not via magical source tags.

## Storage Path Structure

Files are stored at:
```
{media-repo}/{routed-directory}/{guid-bucket}/{guid}.{ext|json}
```

The GUID bucket is the first two hex characters of the GUID, keeping any single directory to ~1/256th of total files:

```
commercial-001/natsume/a1/a1b2c3d4-e5f6-7890-abcd-ef1234567890.mp3
commercial-001/natsume/a1/a1b2c3d4-e5f6-7890-abcd-ef1234567890.audio.json
commercial-001/natsume/f7/f7e6d5c4-b3a2-1098-7654-321fedcba098.png
commercial-001/natsume/f7/f7e6d5c4-b3a2-1098-7654-321fedcba098.image.json
general/tts/3c/3c4d5e6f-a7b8-9012-cdef-123456789012.mp3
general/tts/3c/3c4d5e6f-a7b8-9012-cdef-123456789012.audio.json
```

## Runtime: Building the Domain Model

At startup, `MediaFileIndex` scans all media repositories, reading every `*.audio.json` and `*.image.json` sidecar to build an in-memory index.

**Index lookups:**
- `NoteId → NoteMedia` — all media for a note, typed (a single media file appears in the results for every note in its `NoteIds` list)
- `MediaFileId → AudioAttachment | ImageAttachment` — single file by GUID
- `OriginalFileName → MediaAttachment` — for dedup during import

**Runtime domain objects (built from sidecar data at index time):**
```csharp
public enum CopyrightStatus
{
    Commercial,    // requires verified account or license
    Free           // freely redistributable (TTS, CC-licensed, etc.)
}

// Base — common storage/identity data shared by all media types
public abstract record MediaAttachment
{
    // Persisted in sidecar JSON
    public required MediaFileId Id { get; init; }
    public required List<NoteId> NoteIds { get; init; }   // all notes that reference this file
    public required string NoteSourceTag { get; init; }   // full tag, e.g. "source::anime::natsume::s1::01"
    public string? AnkiFieldName { get; init; }           // which Anki field this came from, e.g. "Audio.First"
    public string? OriginalFileName { get; init; }
    public required CopyrightStatus Copyright { get; init; }

    // Runtime only — resolved by MediaFileIndex from the filesystem, not serialized
    [JsonIgnore] public string FilePath { get; internal set; } = string.Empty;
}

// Audio — extends with audio-specific fields
public record AudioAttachment : MediaAttachment
{
    public TtsInfo? Tts { get; init; }                    // non-null if TTS-generated
}

public record TtsInfo(string Engine, string Voice, string Version);

// Image — extends with image-specific fields (none yet, but will diverge)
public record ImageAttachment : MediaAttachment;

// Aggregated per note
public record NoteMedia(
    IReadOnlyList<AudioAttachment> Audio,
    IReadOnlyList<ImageAttachment> Images
);
```

The base `MediaAttachment` gives shared storage/serialization/index logic a single type to work with. `MediaFileIndex` can store all attachments as `MediaAttachment` internally, while typed accessors return `AudioAttachment` or `ImageAttachment`.
```

**Domain notes expose typed media from the index:**
```csharp
// SentenceNote — assembled at load time
public NoteMedia Media { get; }    // .Audio, .Images

// VocabNote — same
public NoteMedia Media { get; }
```

Multiple audio sources per note is the norm — copyrighted original audio, TTS from multiple engines, human recordings from free sources. The access/preference layer selects which to present.

## Core Corpus Data (Source-Blind)

The note JSON stored in the core corpus contains **no media references at all**:

```csharp
// SentenceData — what's on disk in core corpus
// NO AudioId, NO ScreenshotId, NO MediaIds
// Just: text, breakdown, grammar, readings, translation, etc.

// VocabData — same
// NO audio fields, NO image fields
// Just: word, readings, meanings, pitch accent, usage notes, etc.
```

The association `note ↔ media` exists only in the media layer's sidecar files (via `noteId`).

## Access Gating (Future)

Media access is controlled at runtime based on the user's verified accounts:

```
noteSourceTag starts with "source::anime::natsume"  →  requires Crunchyroll (or relevant licensor)
noteSourceTag starts with "source::wani::"           →  requires verified WaniKani account
copyright == "free"                                  →  always available
tts != null                                          →  always available
```

A note might have 5 audio attachments. The access layer filters to what the user is entitled to, then the preference layer selects the best one (community-ranked, student-overridable, curator-pinned).

## Takedown Handling

If a rights holder demands removal of media from a source:

1. Identify all sidecar files matching the source (e.g. `noteSourceTag` starts with `source::anime::natsume::`)
2. Delete the media files and their sidecars
3. Commit the deletion to the media repo
4. Core corpus is untouched — notes still load, they just have fewer (or no) audio/image options

Because media repos are separate git repositories, an entire repo can be deleted without affecting the core corpus or other media repos.

## Source-Revealing Tags (Future)

Note tags like `source::anime::natsume::s1::01` on sentence notes in the core corpus reveal the source. This is a separate concern from media storage but related to the same copyright goal. Eventually these tags should move out of the core corpus — possibly into the media repo's sidecar data or a separate metadata layer. Deferred for now.

## Deduplication Strategy

During import, `MediaFileIndex.TryGetByOriginalFileName()` checks if a file with the same original name is already stored:

- **First encounter:** file is copied, sidecar created with `noteIds: [currentNoteId]`
- **Subsequent encounters (same filename, different note):** file is NOT copied again; the existing sidecar's `noteIds` list is updated to include the new note ID
- The check is case-insensitive

This is name-based dedup, not content-based. Acceptable because Anki media files are essentially immutable once created.

## Current Implementation Status

The existing code (`JAStudio.Core.Storage.Media` namespace) implements an earlier version of this design where:

- Notes stored raw Anki markup (`[sound:file.mp3]`, `<img src="file.jpg">`) in the corpus JSON
- Media association was embedded in the note data
- All metadata was encoded in the filesystem path structure
- No sidecar JSON files

This needs to be evolved to match the architecture described above.

### Existing components to evolve:

| Component | Current | Target |
|---|---|---|
| Note corpus data (DTOs) | Contains Anki markup audio/image fields | No media fields at all |
| `MediaStorageService` | Encodes metadata in path | Stores typed sidecar JSON (`*.audio.json` / `*.image.json`) alongside media files |
| `MediaFileIndex` | Recovers original filename from directory structure | Reads typed sidecars; supports `NoteId → NoteMedia` lookup |
| `AnkiMediaSyncService` | Hardcodes `anki::audio`/`anki::image` tags | Uses routing config + note source tags to determine storage location and sidecar content |
| `MediaFileInfo` | `(Id, FullPath, OriginalFileName, Extension)` | Replaced by typed `AudioAttachment` / `ImageAttachment` records built from sidecar data |
| `MediaRoutingConfig` | Routes by source tag prefix → directory | Same role, but import-time only |
| `WritableAudioValue` / `WritableImageValue` | Wraps raw Anki markup, parses media refs | Still needed for Anki interop; not used in corpus storage |
| `JPNote.MediaReferences` | Aggregates media fields from the note | No longer needed on the note — media discovered via index |

### Existing tests to adapt:

- `When_creating_a_MediaFileId` — unchanged
- `When_building_a_MediaFileIndex` — adapt to read sidecar JSON
- `When_configuring_media_routing` — unchanged
- `When_storing_a_media_file` — adapt to write/read sidecar JSON
- `When_querying_MediaFileIndex_by_original_filename` — adapt to sidecar-based lookup
- `When_syncing_media_from_anki` — adapt to new routing + sidecar writing

## Import Plan (Fresh from Anki)

The import always runs from scratch — wipe the media output folder and re-import everything from Anki. No incremental or crash-recovery logic needed.

1. Delete all existing media files in the target directories (clean slate)
2. Load all notes from the corpus; for each note, parse Anki markup fields → extract original filenames and field names
3. For each media reference, look up `(noteType, sourceTag, fieldName)` in the routing config → get target directory + copyright
4. Check if file already stored (by original filename — dedup): if so, append noteId to existing sidecar's `noteIds`; if not, copy from Anki media dir
5. Write typed sidecar JSON (`*.audio.json` or `*.image.json`) with `noteIds`, `noteSourceTag`, `ankiFieldName`, `originalFileName`, `copyright`, etc.

Stripping media fields from the corpus note JSON is a separate step (done when the corpus DTOs are updated to remove audio/image fields).
