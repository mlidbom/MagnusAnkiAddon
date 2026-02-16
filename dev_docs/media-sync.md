# Media Storage — Design & Architecture

## Goals & Motivations

We are building a corpus of analyzed Japanese sentences/vocab for language study. Most sentences come from copyrighted material (anime, textbooks, learning platforms). Using them for study with linguistic breakdowns is fair use, but rights holders can be aggressive, so we need to:

1. **Isolate media from the core corpus.** The core corpus is pure language analysis — text, breakdowns, grammar, readings. No media files, no media references, no source-identifying filenames.
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

Each media file is stored as a pair: `{guid}.{ext}` + `{guid}.json`.

**Example: copyrighted anime audio**
```json
{
  "noteId": "9f8e7d6c-5b4a-3210-fedc-ba9876543210",
  "originalFileName": "natsume_ep01_03m22s.mp3",
  "mediaType": "audio",
  "copyright": "commercial",
  "source": {
    "type": "anime",
    "show": "natsume",
    "season": 1,
    "episode": 1
  }
}
```

**Example: TTS-generated audio**
```json
{
  "noteId": "9f8e7d6c-5b4a-3210-fedc-ba9876543210",
  "originalFileName": null,
  "mediaType": "audio",
  "copyright": "free",
  "generation": {
    "method": "tts",
    "engine": "azure-neural",
    "voice": "ja-JP-NanamiNeural",
    "version": "2025.1"
  }
}
```

**Example: screenshot from anime**
```json
{
  "noteId": "9f8e7d6c-5b4a-3210-fedc-ba9876543210",
  "originalFileName": "natsume_ep01_03m22s.png",
  "mediaType": "image",
  "copyright": "commercial",
  "source": {
    "type": "anime",
    "show": "natsume",
    "season": 1,
    "episode": 1
  }
}
```

The sidecar format is extensible — new fields can be added as needed without restructuring storage.

## Import-Time Routing

A manually maintained config maps Anki note source tags to storage directories:

```json
{
  "routing": {
    "source::anime::natsume::": "commercial-001/natsume",
    "source::anime::mushishi::": "commercial-001/mushishi",
    "source::wani::": "commercial-002/wanikani",
    "source::core2000::": "commercial-003/core2000"
  },
  "default": "general"
}
```

At import time, the note's tags are matched by longest prefix to determine the target directory. Unmatched files go to `"general"`.

**This config is import-time only.** Once files are stored, the routing config is not consulted again. The `MediaFileIndex` discovers files by scanning the filesystem.

### Copyright mapping from current Anki data

The copyright owner of a media file depends on the **note's source tag** and **which field** the media came from:

| Note source tag | Media field | Copyright | Storage target |
|---|---|---|---|
| `source::anime::natsume::*` | Audio | Commercial (show owner) | `commercial-001/natsume` |
| `source::anime::natsume::*` | Screenshot | Commercial (show owner) | `commercial-001/natsume` |
| `source::wani::*` | Audio_b, Audio_g | Commercial (WaniKani) | `commercial-002/wanikani` |
| `source::wani::*` (sentences) | Audio | Free (TTS) | `general/tts` |
| `source::core2000::*` | Audio | Commercial (Core 2000) | `commercial-003/core2000` |

This mapping is specific to the initial Anki import. Future imports will specify source/copyright at import time directly, not via magical source tags.

## Storage Path Structure

Files are stored at:
```
{media-repo}/{routed-directory}/{guid-bucket}/{guid}.{ext|json}
```

The GUID bucket is the first two hex characters of the GUID, keeping any single directory to ~1/256th of total files:

```
commercial-001/natsume/a1/a1b2c3d4-e5f6-7890-abcd-ef1234567890.mp3
commercial-001/natsume/a1/a1b2c3d4-e5f6-7890-abcd-ef1234567890.json
general/tts/3c/3c4d5e6f-a7b8-9012-cdef-123456789012.mp3
general/tts/3c/3c4d5e6f-a7b8-9012-cdef-123456789012.json
```

## Runtime: Building the Domain Model

At startup, `MediaFileIndex` scans all media repositories, reading every `.json` sidecar to build an in-memory index.

**Index lookups:**
- `NoteId → List<MediaAttachment>` — all media for a note
- `MediaFileId → MediaAttachment` — single file by GUID

**Runtime domain object (built from index at note load time):**
```csharp
// Rich object combining note data + media index
public record MediaAttachment(
    MediaFileId Id,
    string? OriginalFileName,
    string Extension,
    MediaType Type,           // Audio, Image — inferred from extension
    string Copyright,         // "commercial", "free"
    string FilePath           // absolute path to the media file
    // extensible: add TTS engine, source info, etc. as needed
);
```

**Domain notes expose media from the index:**
```csharp
// SentenceNote — assembled at load time
public IReadOnlyList<MediaAttachment> AllMedia { get; }
public IReadOnlyList<MediaAttachment> AudioOptions { get; }
public IReadOnlyList<MediaAttachment> Images { get; }

// VocabNote — same pattern
public IReadOnlyList<MediaAttachment> AudioOptions { get; }
public IReadOnlyList<MediaAttachment> Images { get; }
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
source.type "anime" on Crunchyroll  → requires verified Crunchyroll account
source.type "wanikani"              → requires verified WaniKani account
copyright "free"                    → always available
generation.method "tts"             → always available
```

A note might have 5 audio attachments. The access layer filters to what the user is entitled to, then the preference layer selects the best one (community-ranked, student-overridable, curator-pinned).

## Takedown Handling

If a rights holder demands removal of media from a source:

1. Identify all sidecar files matching the source (e.g. `source.show == "natsume"`)
2. Delete the media files and their sidecars
3. Commit the deletion to the media repo
4. Core corpus is untouched — notes still load, they just have fewer (or no) audio/image options

Because media repos are separate git repositories, an entire repo can be deleted without affecting the core corpus or other media repos.

## Source-Revealing Tags (Future)

Note tags like `source::anime::natsume::s1::01` on sentence notes in the core corpus reveal the source. This is a separate concern from media storage but related to the same copyright goal. Eventually these tags should move out of the core corpus — possibly into the media repo's sidecar data or a separate metadata layer. Deferred for now.

## Deduplication Strategy

`MediaFileIndex.ContainsByOriginalFileName()` checks if a file with the same original name is already stored before copying. This means:

- First import of a file: copied and indexed
- Subsequent imports of the same filename: skipped
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
| `MediaStorageService` | Encodes metadata in path | Stores sidecar JSON alongside media files |
| `MediaFileIndex` | Recovers original filename from directory structure | Reads sidecar JSON for full metadata; supports `NoteId → media` lookup |
| `AnkiMediaSyncService` | Hardcodes `anki::audio`/`anki::image` tags | Uses routing config + note source tags to determine storage location and sidecar content |
| `MediaFileInfo` | `(Id, FullPath, OriginalFileName, Extension)` | Richer record with all sidecar fields |
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

## Migration Plan (50k Sentence Import)

1. Parse existing Anki markup from current note JSON → extract original filenames
2. For each media reference, determine copyright/source from the note's tags using the routing config
3. Copy file from Anki media dir into the target media repo directory
4. Write sidecar JSON with `noteId`, `originalFileName`, `mediaType`, `copyright`, `source`, etc.
5. Strip media fields from corpus note JSON (remove `Audio`, `Screenshot`, `Image`, etc.)
6. Rebuild `MediaFileIndex` from the new sidecar-based storage
