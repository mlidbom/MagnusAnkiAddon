# jaslib → JAStudio.Core Migration Status

## Goal

Replace all usages of `jaslib` (Python business logic library) with equivalent types from `JAStudio.Core` (.NET), then **delete jaslib entirely** (this will wait, keeping the code around will let us debug issues in the ported .NET code much easier, so we will probably keep it for months, just not use it...).

See [PORTING_STATUS.md](PORTING_STATUS.md) for the C# porting status of jaslib itself.
See [UI_PORTING_STATUS.md](UI_PORTING_STATUS.md) for the UI porting status.

## Context

Every Python file in `jastudio/` (the Anki addon) that imports from `jaslib` needs to be updated to import the equivalent .NET type from `JAStudio.Core` (via pythonnet). Files that don't import jaslib may still need review if they interact with jaslib types indirectly.

## Legend
- **NOT_STARTED** - Not yet migrated, still uses jaslib
- **IN_PROGRESS** - Migration started but not complete
- **DONE** - All jaslib usages replaced with JAStudio.Core equivalents
- **NO_JASLIB** - File has no jaslib imports (may still need review for indirect usage)
- **DELETE** - File will be deleted entirely (functionality moved to C#)
- **KEEP_AS_IS** - File is Anki/Python-specific, no jaslib to replace

---

## anki_extentions/ — Anki API Wrappers

| Status | File | Lines | jaslib imports | Description |
|--------|------|-------|----------------|-------------|
| NOT_STARTED | card_ex.py | 71 | 1 | Extended wrapper around Anki Card with deck/note/scheduling helpers |
| NO_JASLIB | config_manager_ex.py | 10 | 0 | Wrapper to set Anki config values like timebox seconds |
| NO_JASLIB | deck_configdict_ex.py | 11 | 0 | Typed accessor for deck config settings |
| NO_JASLIB | deck_ex.py | 14 | 0 | Wrapper around Anki DeckDict with name, id, config access |
| NOT_STARTED | note_bulk_loader.py | 42 | 2 | Bulk-loads all notes of a given note type via raw SQL query |
| NOT_STARTED | note_ex.py | 35 | 1 | Wrapper around Anki Note with note-type and card accessors |
| NO_JASLIB | notetype_ex/note_type_ex.py | 73 | 0 | Typed representation of an Anki note type (model) |
| NO_JASLIB | notetype_ex/note_type_field.py | 43 | 0 | Typed representation of a single note type field definition |
| NO_JASLIB | notetype_ex/note_type_template.py | 36 | 0 | Typed representation of a single note type card template |
| NO_JASLIB | sheduling_states_ex.py | 27 | 0 | Wrapper around Anki scheduling states for interval manipulation |

---

## ankiutils/ — Anki Utilities

| Status | File | Lines | jaslib imports | Description |
|--------|------|-------|----------------|-------------|
| KEEP_AS_IS | anki_module_import_issues_fix_...py | 1 | 0 | Single-line import to fix Anki module loading order |
| NOT_STARTED | app.py | 113 | 2 | Central application singleton: collection, config, UI, scheduler |
| NO_JASLIB | audio_suppressor.py | 18 | 0 | Temporarily suppresses Anki audio playback |
| NOT_STARTED | query_builder.py | 111 | 7 | Builds Anki search query strings for note/card lookups |
| NO_JASLIB | search_executor.py | 18 | 0 | Opens Anki browser with a search query |
| NO_JASLIB | ui_utils_interface.py | 13 | 0 | Abstract interface for UI operations (refresh, tooltip, preview) |
| NOT_STARTED | ui_utils.py | 117 | 1 | Concrete PyQt implementation of UI utilities |

---

## batches/ — Batch Operations

| Status | File | Lines | jaslib imports | Description |
|--------|------|-------|----------------|-------------|
| NOT_STARTED | local_note_updater.py | 23 | 1 | Batch converts Immersion Kit sentences to native sentence notes |

---

## configuration/ — Settings & Dialogs

| Status | File | Lines | jaslib imports | Description |
|--------|------|-------|----------------|-------------|
| NOT_STARTED | configuration_value.py | 27 | 3 | Bridges Anki addon config storage with C# ConfigurationValue |
| NOT_STARTED | configuration.py | 140 | 1 | PyQt dialog for editing Japanese study options |
| NOT_STARTED | readings_mapping_dialog.py | 120 | 1 | PyQt dialog for editing custom readings mappings |

---

## dotnet/ — .NET Runtime Loading

| Status | File | Lines | jaslib imports | Description |
|--------|------|-------|----------------|-------------|
| NOT_STARTED | load_dotnet_runtime.py | 41 | 1 | Loads .NET CoreCLR runtime and JAStudio C# assemblies |

---

## language_services/ — Language Processing

| Status | File | Lines | jaslib imports | Description |
|--------|------|-------|----------------|-------------|
| NO_JASLIB | english_dictionary/english_dict_search.py | 65 | 0 | Loads and searches English dictionary file for word lookups |

---

## Root Files

| Status | File | Lines | jaslib imports | Description |
|--------|------|-------|----------------|-------------|
| NOT_STARTED | mylog.py | 63 | 1 | Configures rotating file-based logging for the Anki addon |

---

## note/ — Note Type Wrappers (Anki ↔ Domain Bridge)

| Status | File | Lines | jaslib imports | Description |
|--------|------|-------|----------------|-------------|
| NOT_STARTED | anki_backend_note_creator.py | 32 | 6 | Creates new Anki backend notes from JPNote domain objects |
| NOT_STARTED | ankijpnote.py | 30 | 5 | Converts Anki Card/Note into typed JPNote (Vocab/Kanji/Sentence) |
| NOT_STARTED | cardutils.py | 24 | 1 | Card utility methods: is-new check, note-type priority |
| NOT_STARTED | collection/anki_collection_sync_runner.py | 92 | 1 | Orchestrates background syncing of note types to cache |
| NOT_STARTED | collection/anki_jp_collection_syncer.py | 117 | 10 | Main collection syncer: bulk-loads and caches all JP note types |
| NOT_STARTED | collection/anki_single_collection_syncer.py | 74 | 4 | Syncs a single note type's cache with adds/deletes/updates |
| NOT_STARTED | jpnotedata_shim.py | 19 | 2 | Converts between Anki Note fields and JPNoteData domain objects |
| NO_JASLIB | queue_manager.py | 18 | 0 | Manages card queue: prioritize selected cards, refresh browser |
| NOT_STARTED | sentences/ankisentencenote.py | 21 | 3 | Imports Immersion Kit notes into native SentenceNote format |
| NOT_STARTED | studing_status_helper.py | 50 | 4 | Updates card studying status cache (suspend/unsuspend/new state) |

---

## qt_utils/ — PyQt Utilities

| Status | File | Lines | jaslib imports | Description |
|--------|------|-------|----------------|-------------|
| NO_JASLIB | ex_qmenu.py | 24 | 0 | Recursively disables empty QMenu submenus |
| NOT_STARTED | qt_task_progress_runner.py | 99 | 2 | PyQt progress dialog for long-running tasks with cancel support |

---

## sysutils/ — System Utilities

| Status | File | Lines | jaslib imports | Description |
|--------|------|-------|----------------|-------------|
| NO_JASLIB | app_thread_pool.py | 25 | 0 | Thread pool and UI-thread synchronous execution utilities |
| NO_JASLIB | collections/recent_items.py | 11 | 0 | Fixed-size deque tracking recently seen items |
| NOT_STARTED | ex_gc.py | 14 | 1 | Helpers to run garbage collection with user feedback |
| NO_JASLIB | ex_thread.py | 4 | 0 | Simple thread sleep helper |
| NOT_STARTED | memory_usage/ex_trace_malloc.py | 42 | 1 | Optional tracemalloc wrapper for memory usage tracking |
| NO_JASLIB | object_instance_tracker.py | 63 | 0 | Tracks live object instance counts and diffs between snapshots |

---

## testutils/

| Status | File | Lines | jaslib imports | Description |
|--------|------|-------|----------------|-------------|
| NO_JASLIB | ex_pytest.py | 3 | 0 | Detects whether code is running under pytest |

---

## ui/ — User Interface

### Core UI Infrastructure

| Status | File | Lines | jaslib imports | Description |
|--------|------|-------|----------------|-------------|
| NOT_STARTED | avalonia_host.py | 222 | 1 | Initializes Avalonia UI subsystem and wraps C# dialog show functions |
| NOT_STARTED | avalonia_menu_helper.py | 66 | 1 | Adds hover-triggered Avalonia popup menus to PyQt menu actions |
| NO_JASLIB | garbage_collection_fixes.py | 30 | 0 | Monkey-patches Anki to prevent GC hangs on dialog close |
| NO_JASLIB | timing_hacks.py | 25 | 0 | Tracks editor/reviewer timing to suppress audio on rapid interactions |
| NOT_STARTED | tools_menu.py | 120 | 3 | Builds the addon's top-level Tools menu (refresh, config, batch ops) |

### Dialogs

| Status | File | Lines | jaslib imports | Description |
|--------|------|-------|----------------|-------------|
| NO_JASLIB | english_dict/find_english_words_dialog.py | 94 | 0 | Singleton PyQt dialog for searching English dictionary words |
| NOT_STARTED | open_note/open_note_dialog.py | 264 | 6 | Singleton quick-search dialog to find and navigate to notes |

### Hooks (Anki Event Handlers)

| Status | File | Lines | jaslib imports | Description |
|--------|------|-------|----------------|-------------|
| NO_JASLIB | hooks/clear_studying_cache_on_card_suspend_unsuspend.py | 34 | 0 | Updates studying cache on card suspend/unsuspend |
| NO_JASLIB | hooks/convert_immersion_kit_sentences_on_import.py | 12 | 0 | Auto-converts Immersion Kit sentences after Anki import |
| NO_JASLIB | hooks/copy_sort_field_to_clipboard.py | 30 | 0 | Copies note sort field to clipboard on card show |
| NOT_STARTED | hooks/custom_auto_advance_timings.py | 70 | 5 | Overrides auto-advance timings per note type and difficulty |
| NO_JASLIB | hooks/custom_short_term_scheduling.py | 20 | 0 | Reduces "again" interval for same-day failed cards |
| NOT_STARTED | hooks/custom_timebox_lengths.py | 35 | 1 | Adjusts timebox duration based on deck's card type |
| NO_JASLIB | hooks/global_shortcuts.py | 39 | 0 | Registers global keyboard shortcuts |
| NO_JASLIB | hooks/history_navigator.py | 93 | 0 | Back/forward navigation through reviewed card history |
| NO_JASLIB | hooks/no_accidental_double_click.py | 31 | 0 | Anti-double-click guard for answer/show-answer |
| NOT_STARTED | hooks/note_view_shortcuts.py | 105 | 4 | Context-aware keyboard shortcuts for the reviewer |
| NO_JASLIB | hooks/timebox_end_sound.py | 29 | 0 | Plays sound and shows stats at timebox end |

### Menus

| Status | File | Lines | jaslib imports | Description |
|--------|------|-------|----------------|-------------|
| NOT_STARTED | menus/browser/main.py | 72 | 3 | Context menu actions for the Anki browser |
| NOT_STARTED | menus/common.py | 148 | 8 | Shared reviewer context menu: lookup, copy, web search |
| NOT_STARTED | menus/menu_utils/ex_qmenu.py | 63 | 4 | Helper functions for creating menu actions |
| NO_JASLIB | menus/menu_utils/shortcutfinger.py | 31 | 0 | Keyboard shortcut mnemonics to accelerators |
| NOT_STARTED | menus/notes/kanji/main.py | 38 | 2 | Kanji note context menu |
| NOT_STARTED | menus/notes/kanji/string_menu.py | 36 | 2 | String-specific submenu for kanji notes |
| NOT_STARTED | menus/notes/sentence/main.py | 36 | 2 | Sentence note context menu |
| NOT_STARTED | menus/notes/sentence/string_menu.py | 52 | 4 | String-specific submenu for sentence notes |
| NOT_STARTED | menus/notes/vocab/common.py | 26 | 1 | Shared vocab menu: create prefix/suffix note variations |
| NO_JASLIB | menus/notes/vocab/counter.py | 8 | 0 | Simple integer counter for sequential numbering |
| NOT_STARTED | menus/notes/vocab/create_note_menu.py | 52 | 2 | Menu for cloning vocab to forms, noun variations |
| NOT_STARTED | menus/notes/vocab/main.py | 69 | 4 | Vocab note context menu |
| NOT_STARTED | menus/notes/vocab/require_forbid_widget.py | 61 | 1 | Radio button widget for require/forbid flag editing |
| NOT_STARTED | menus/notes/vocab/string_menu.py | 52 | 2 | String-specific submenu for vocab notes |
| NOT_STARTED | menus/notes/vocab/string_set_widget.py | 130 | 1 | Chip-style widget for editing a set of strings |
| NOT_STARTED | menus/notes/vocab/vocab_flags_dialog.py | 237 | 4 | Full dialog for editing all vocab note flags |
| NOT_STARTED | menus/open_in_anki.py | 33 | 1 | "Open in Anki" submenu with search options |
| NO_JASLIB | menus/qt_menu_adapter.py | 95 | 0 | Converts C# MenuItem specs into PyQt QMenu objects |
| NO_JASLIB | menus/web_search.py | 48 | 0 | Web search submenu (kanji sites, sentence sites) |

### Web Renderers

| Status | File | Lines | jaslib imports | Description |
|--------|------|-------|----------------|-------------|
| NOT_STARTED | web/kanji/kanji_note_renderer.py | 9 | 2 | Hooks kanji note HTML rendering into Anki display pipeline |
| NOT_STARTED | web/sentence/sentence_note_renderer.py | 9 | 2 | Hooks sentence note HTML rendering into Anki display pipeline |
| NOT_STARTED | web/vocab/vocab_note_renderer.py | 9 | 2 | Hooks vocab note HTML rendering into Anki display pipeline |
| NOT_STARTED | web/web_utils/pre_rendering_content_renderer_anki_shim.py | — | 3 | Generic shim that pre-renders note HTML by note type |

---

## Summary Statistics

| Category | Files with jaslib | Files without jaslib | Total |
|----------|-------------------|----------------------|-------|
| anki_extentions/ | 3 | 7 | 10 |
| ankiutils/ | 3 | 4 | 7 |
| batches/ | 1 | 0 | 1 |
| configuration/ | 3 | 0 | 3 |
| dotnet/ | 1 | 0 | 1 |
| language_services/ | 0 | 1 | 1 |
| Root (mylog.py) | 1 | 0 | 1 |
| note/ | 9 | 1 | 10 |
| qt_utils/ | 1 | 1 | 2 |
| sysutils/ | 2 | 4 | 6 |
| testutils/ | 0 | 1 | 1 |
| ui/ (core + dialogs) | 4 | 4 | 8 |
| ui/hooks/ | 3 | 8 | 11 |
| ui/menus/ | 14 | 4 | 18 |
| ui/web/ | 4 | 0 | 4 |
| **Total** | **49** | **35** | **84** |

**49 files** need jaslib → JAStudio.Core migration.
**35 files** have no jaslib imports (NO_JASLIB / KEEP_AS_IS).

---

## Migration Notes

- **`__init__.py` files** are excluded (22 files, all empty or trivial).
- **jaslib imports** column shows the count of `from jaslib...` / `import jaslib...` lines in each file.
- Files marked **NO_JASLIB** may still reference jaslib types indirectly (e.g., via function parameters). Review during migration of their callers.
- The **note/** and **note/collection/** directories are the heaviest jaslib consumers — these bridge Anki's data model to the domain model and will need the most careful migration.
- **ui/menus/** files mostly use jaslib for note type access — many already have C# menu spec equivalents that could replace them (see UI_PORTING_STATUS.md).
