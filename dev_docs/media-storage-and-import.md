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
│  free-vocab/                                        │
│    tts/                                             │
│      3c/                                            │
│        3c4d5e6f-....mp3                             │
│        3c4d5e6f-....audio.json                      │
│    user/                                            │
│      ...                                            │
│                                                     │
│  free-sentence/                                     │
│    tts/                                             │
│      ...                                            │
│                                                     │
│  free-kanji/                                        │
│    ...                                              │
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

The `noteSourceTag` field is a `SourceTag` value — a structured, `::` -separated hierarchical identifier (e.g. `source::anime::natsume::s1::01`). `SourceTag` is a domain type that supports hierarchical containment checks (`IsContainedIn`, `Contains`), proper equality, and rejects invalid values (empty strings, empty segments). This enables filtering, bulk updates, and re-routing by source without re-parsing note data.

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

A manually maintained config maps **source tag prefix → storage directory**. Routing uses `SourceTag` — a hierarchical `::` -separated domain type. Each `MediaRoutingRule` has a `SourceTag Prefix` and a `TargetDirectory`. At import time, the source tag is matched against rules by hierarchical containment (`sourceTag.IsContainedIn(rule.Prefix)`), longest prefix first.

**There are no defaults or catch-all rules.** If no rule matches a source tag, import fails with an error. This is by design — if we don't know where to put something, we cannot import it. The routing config must be explicitly configured for every source before import.

```csharp
// Domain type — hierarchical, ::‑separated, validated
var tag = SourceTag.Parse("source::anime::natsume::s1::01");
tag.IsContainedIn(SourceTag.Parse("source::anime::natsume")); // true
tag.IsContainedIn(SourceTag.Parse("source::anime"));          // true
tag.IsContainedIn(SourceTag.Parse("source::wani"));           // false

// Routing config — explicit rules only, no fallback
var config = new MediaRoutingConfig([
    new MediaRoutingRule(SourceTag.Parse("source::anime::natsume"), "commercial-001"),
    new MediaRoutingRule(SourceTag.Parse("source::anime"),          "commercial-002"),
    new MediaRoutingRule(SourceTag.Parse("source::wani"),           "commercial-003")
]);

config.ResolveDirectory(SourceTag.Parse("source::anime::natsume::s1::01")); // "commercial-001"
config.ResolveDirectory(SourceTag.Parse("source::anime::mushishi::s1"));    // "commercial-002"
config.ResolveDirectory(SourceTag.Parse("source::forvo::ja"));              // throws InvalidOperationException
```

The full routing config will also incorporate note type and field name (see Architecture Overview), but the current implementation routes by source tag only.

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
free-vocab/tts/3c/3c4d5e6f-a7b8-9012-cdef-123456789012.mp3
free-vocab/tts/3c/3c4d5e6f-a7b8-9012-cdef-123456789012.audio.json
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

// SourceTag — hierarchical, ::‑separated, validated domain type
// Supports containment: tag.IsContainedIn(ancestor), tag.Contains(descendant)
// Serialized to/from JSON as a plain string
public sealed class SourceTag : IEquatable<SourceTag>
{
    public static SourceTag Parse(string value);
    public IReadOnlyList<string> Segments { get; }
    public bool IsContainedIn(SourceTag ancestor);
    public bool Contains(SourceTag descendant);
}

// Base — common storage/identity data shared by all media types
public abstract record MediaAttachment
{
    // Persisted in sidecar JSON
    public required MediaFileId Id { get; init; }
    public required List<NoteId> NoteIds { get; init; }     // all notes that reference this file
    public required SourceTag NoteSourceTag { get; init; }   // full tag, e.g. "source::anime::natsume::s1::01"
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

// Routing — source tag prefix → target directory, no defaults
public record MediaRoutingRule(SourceTag Prefix, string TargetDirectory)
{
    public bool Matches(SourceTag sourceTag) => sourceTag.IsContainedIn(Prefix);
}

public class MediaRoutingConfig(List<MediaRoutingRule> rules)
{
    // Ordered by segment count (longest prefix first)
    // ResolveDirectory throws if no rule matches — no silent fallback
    public string ResolveDirectory(SourceTag sourceTag);
}
```

The base `MediaAttachment` gives shared storage/serialization/index logic a single type to work with. `MediaFileIndex` can store all attachments as `MediaAttachment` internally, while typed accessors return `AudioAttachment` or `ImageAttachment`.

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
noteSourceTag.IsContainedIn("source::anime::natsume")  →  requires Crunchyroll (or relevant licensor)
noteSourceTag.IsContainedIn("source::wani")             →  requires verified WaniKani account
copyright == Free                                       →  always available
tts != null                                             →  always available
```

A note might have 5 audio attachments. The access layer filters to what the user is entitled to, then the preference layer selects the best one (community-ranked, student-overridable, curator-pinned).

## Takedown Handling

If a rights holder demands removal of media from a source:

1. Identify all sidecar files matching the source (e.g. `noteSourceTag.IsContainedIn(SourceTag.Parse("source::anime::natsume"))`)
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

The storage layer (`JAStudio.Core.Storage.Media`) is implemented and tested:

### Implemented

| Component | Status |
|---|---|
| `SourceTag` | Domain type with `::` hierarchy. `Parse()`, `IsContainedIn()`, `Contains()`, equality, JSON serialization. Rejects empty/invalid values. |
| `MediaAttachment` / `AudioAttachment` / `ImageAttachment` | Record types with typed `SourceTag NoteSourceTag` field. Audio has `TtsInfo?`, Image is a separate schema. |
| `SidecarSerializer` | Writes/reads typed sidecar JSON (`*.audio.json` / `*.image.json`). Omits defaults. Custom JSON converters for `NoteId`, `MediaFileId`, `SourceTag`. |
| `MediaFileId` | GUID-based value type with `Parse`, `TryParse`, `New`. |
| `MediaFileIndex` | Builds from filesystem scan of sidecar files. Lookups by ID, original filename (case-insensitive), note ID. In-memory `Register()` for newly stored files. |
| `MediaStorageService` | Stores files with GUID-bucket paths, writes typed sidecars, updates existing sidecars for shared files (dedup by original filename). |
| `MediaRoutingConfig` / `MediaRoutingRule` | Routes `SourceTag → directory` by hierarchical containment, longest prefix first. **No defaults — unmatched tags throw.** |
| `AnkiMediaSyncService` | Syncs media from Anki media folder. Builds `SourceTag` from note tags, deduplicates, skips missing files with warning. |

### Not yet implemented

| Component | Notes |
|---|---|
| `AnkiFieldName` on sidecar | Per-field routing (same note can have commercial audio + free TTS). Design exists in doc, not yet in code. |
| Note-type-aware routing | Config currently routes by source tag only; full design includes note type + field name dimensions. |
| `NoteMedia` aggregate | Per-note typed media view (`Audio`, `Images`). Not yet needed — media is currently accessed via the index directly. |
| Removal of media fields from corpus DTOs | Notes still contain Anki markup audio/image fields. These should be stripped. |
| Access gating | Runtime filtering by user's verified accounts / copyright status. |
| Import plan (Phase 1/2) | Dry-run planning with error collection before executing. Currently import is direct. |

### Test coverage

All components have BDD-style tests:

- `When_working_with_SourceTag` — parsing, containment, equality
- `When_configuring_media_routing` — rule matching, longest prefix, throw on no match
- `When_serializing_a_sidecar` — JSON roundtrip for audio/image, TTS, multiple note IDs, file read/write
- `When_building_a_MediaFileIndex` — filesystem scan, sidecar parsing, lookups
- `When_querying_MediaFileIndex_by_original_filename` — exact/case-insensitive lookup, registered attachments
- `When_storing_a_media_file` — routing, GUID-bucket paths, sidecar writing, index rebuilding
- `When_syncing_media_from_anki` — end-to-end sync with dedup, missing file warnings

## Import Plan (Fresh from Anki)

The import always runs from scratch — wipe the media output folder and re-import everything from Anki. No incremental or crash-recovery logic needed.

### Phase 1: Plan (no side effects)

Build the complete import plan in memory before touching any files:

1. Load all notes from the corpus; for each note, parse Anki markup fields → extract original filenames and field names
2. For each media reference, look up `(noteType, sourceTag, fieldName)` in the routing config → get target directory + copyright. **Collect all unmatched combinations as errors — don't stop at the first one.**
3. Deduplicate by original filename — group noteIds that reference the same file
4. Check that every referenced file exists in the Anki media folder — collect warnings for missing files
5. Build a complete `ImportPlan`: list of `PlannedFileCopy` (source path, target path, sidecar content) + summary statistics

**Import plan summary (always presented to user):**
- Total unique files to copy (audio / image breakdown)
- Total sidecar files to write
- Total notes with media / without media
- Files per target directory (shows distribution across repos)
- Missing source files (warnings — these will be skipped)
- Shared files (files referenced by multiple notes)
- **Unmatched routing combinations (errors) — listed with note type, source tag, and field name**

If there are any routing errors, the summary shows them all so the config can be fixed in one pass. **Phase 2 is blocked until there are zero routing errors.**

### Phase 2: Execute (after user confirms, only if plan is valid)

6. Delete all existing media files in the target directories (clean slate)
7. Execute the planned file copies and write sidecars

Stripping media fields from the corpus note JSON is a separate step (done when the corpus DTOs are updated to remove audio/image fields).
