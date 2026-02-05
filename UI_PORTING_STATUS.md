# JAStudio UI Porting Status (Python PyQt6 → C# Avalonia)

## Current Status

**Infrastructure: COMPLETE**
- JAStudio.UI project created with Avalonia 11.2.5
- DialogHost.cs provides Python → C# entry point
- Type stubs auto-generated for Python type checking
- Runtime binaries copied to `src/runtime_binaries/` (~23 MB)
- Integration tests verify Initialize/Shutdown cycle

**First Dialog: AboutDialog (Test/Demo)**
- Simple "About JAStudio" window in Avalonia
- Accessible from Anki: Japanese → Debug → Test Avalonia Dialog
- Validates the full Python → C# → Avalonia pipeline works

**VocabFlagsDialog: COMPLETE**
- Full-featured dialog for editing vocab matching flags, register & string rules
- 231 lines of Python UI ported to C# Avalonia
- Includes reusable RequireForbidControl (radio button group)
- Includes reusable StringSetControl (editable string chips)
- Reparse prompt with Python integration for batch updates
- Accessible from vocab context menu → Edit

**OptionsDialog: COMPLETE**
- Full Japanese addon configuration dialog
- Two-way binding to JapaneseConfig
- All settings from Python version ported
- Accessible from Japanese → Config → Options (Ctrl+Shift+S)

**ReadingsMappingsDialog: COMPLETE**
- Text editor for readings mappings
- Search functionality
- Deduplication and sorting on save
- Calls AnkiFacade.Refresh() to update note display
- Accessible from Japanese → Config → Readings mappings (Ctrl+Shift+M)

**NoteSearchDialog: COMPLETE**
- Search all notes (Kanji, Vocab, Sentence)
- Multi-condition search with && separator
- Prefixed search (r:, a:, q:)
- Async background search
- Opens notes in Anki browser on double-click
- Singleton pattern with toggle visibility
- Accessible from Japanese → Lookup → Open note (Ctrl+O)

**Menu Architecture: REVOLUTIONARY NEW APPROACH**

**Problem Solved:** Python callbacks from C# don't work with pythonnet

**Solution:** UI-agnostic menu specifications in C# + UI adapters

```
C# Menu Spec Builder (JAStudio.UI/Menus/)
    → Produces MenuItem tree (pure data)
        ↓
    ┌───────────────┴────────────────┐
    ↓                                ↓
PyQt Adapter              Avalonia Adapter
(30 lines)                (future: 30 lines)
    ↓                                ↓
Native PyQt Menu          Native Avalonia Menu
```

**Architecture Benefits:**
- Menu logic 100% in C#
- Actions call JAStudio.Core directly (no Python callbacks)
- PyQt adapter converts C# specs → PyQt menus (simple, thin)
- Python is just a rendering layer
- Future: Same specs work for Avalonia menus

**Menus COMPLETE:**
- ✅ OpenInAnkiMenus.cs - All Anki browser search menus
- ✅ WebSearchMenus.cs - All web search menus (uses BrowserLauncher directly)
- ✅ JapaneseMainMenu.cs - Main menu with Config, Lookup, Local Actions
- ✅ NoteContextMenu.cs - Right-click context menu (scaffolding)
- ✅ ShortcutFinger.cs - Keyboard accelerator utilities
- ✅ QueryBuilder.cs - 21 Anki search query methods

**AnkiFacade - Minimal Python Bridge:**
Reduced from 17 methods (370 lines) to 4 methods (~120 lines):
1. ExecuteLookup(query) - Opens Anki browser
2. ShowTooltip(msg) - Shows Anki tooltip
3. Refresh() - Refreshes note display
4. ConvertImmersionKitSentences() converts between kanji note types

Everything else uses JAStudio.Core directly!

**Python Integration:**
- `jastudio/ui/avalonia_host.py` - Python wrapper for C# dialogs
- `show_about_dialog()` - Opens the About dialog from Python
- `show_context_menu_popup()` - Shows context menu at (x, y) coordinates
- `show_vocab_flags_dialog()` - Opens VocabFlagsDialog (now C# Avalonia)

---

## Porting Strategy

Port the Anki addon's UI from PyQt6 to Avalonia, keeping the domain logic in JAStudio.Core and creating a clean ViewModel layer.

### Architecture

```
Python (Anki addon)
    ↓ pythonnet call
JAStudio.UI.dll (Avalonia)
    ↓ binds to
JAStudio.ViewModels.dll (MVVM, INotifyPropertyChanged)
    ↓ uses
JAStudio.Core.dll (Domain logic - already ported)
```

### Porting Rules

- **ViewModels are UI-agnostic** - No Avalonia types in ViewModels, only standard .NET (INotifyPropertyChanged, ICommand)
- **Views are thin** - XAML bindings to ViewModel properties, minimal code-behind

---

## Legend
- **MISSING** - No C# equivalent exists yet
- **WIP** - Work in progress
- **COMPLETE** - C# equivalent verified as functionally equivalent

---

## Dialogs (PORT TO AVALONIA)

| Status | File | Lines | Description |
|--------|------|-------|-------------|
| COMPLETE | ui/menus/notes/vocab/vocab_flags_dialog.py | 231 | Edit vocab matching flags, register, string rules |
| COMPLETE | ui/open_note/open_note_dialog.py | 264 | Search and open notes dialog |
| MISSING | ui/english_dict/find_english_words_dialog.py | 94 | English dictionary search |
| COMPLETE | configuration/readings_mapping_dialog.py | 120 | Configure reading mappings |
| COMPLETE | configuration/configuration.py | 140 | Japanese addon options dialog |

**Subtotal: 755 lines ported / 849 total (89% complete)**

---

## Widgets (PORT TO AVALONIA)

| Status | File | Lines | Description |
|--------|------|-------|-------------|
| MISSING | ui/menus/notes/vocab/string_set_widget.py | 130 | Editable string set widget |
| MISSING | ui/menus/notes/vocab/require_forbid_widget.py | 61 | Require/Forbid radio button group |
| MISSING | qt_utils/qt_task_progress_runner.py | 99 | Progress dialog for batch operations |

**Subtotal: 290 lines**

---

## Menus (NEW APPROACH: C# MENU SPECS + ADAPTERS)

**Architecture:** Menu logic in C# → UI-agnostic MenuItem specs → PyQt/Avalonia adapters

| Status | Python File | C# File | Lines | Description |
|--------|-------------|---------|-------|-------------|
| COMPLETE | ui/menus/common.py | Menus/NoteContextMenu.cs | 102 | Right-click menu builder (scaffolded) |
| COMPLETE | ui/tools_menu.py | Menus/JapaneseMainMenu.cs | 74 | Main "Japanese" menu (Config ✅, Lookup ✅, Local Actions ✅) |
| SCAFFOLDED | ui/menus/notes/vocab/main.py | (in NoteContextMenu.cs) | 69 | Vocab note context menu |
| N/A | ui/menus/menu_utils/ex_qmenu.py | (not needed) | 63 | Menu helpers (obsolete with new approach) |
| TODO | ui/menus/notes/sentence/string_menu.py | (future) | 52 | Sentence string context menu |
| TODO | ui/menus/notes/vocab/string_menu.py | (future) | 52 | Vocab string context menu |
| TODO | ui/menus/notes/vocab/create_note_menu.py | (future) | 52 | Create note submenu |
| COMPLETE | ui/menus/web_search.py | Menus/WebSearchMenus.cs | 48 | Web search menu items |
| MISSING | ui/menus/browser/main.py | (future) | 45 | Browser context menu additions |
| TODO | ui/menus/notes/kanji/main.py | (future) | 38 | Kanji note context menu |
| TODO | ui/menus/notes/kanji/string_menu.py | (future) | 36 | Kanji string context menu |
| TODO | ui/menus/notes/sentence/main.py | (future) | 36 | Sentence note context menu |
| COMPLETE | ui/menus/open_in_anki.py | Menus/OpenInAnkiMenus.cs | 33 | "Open in Anki" menu items |
| COMPLETE | ui/menus/menu_utils/shortcutfinger.py | Utils/ShortcutFinger.cs | 31 | Keyboard shortcut text helpers |
| N/A | ui/menus/notes/vocab/common.py | (integrated) | 26 | Vocab menu utilities |
| N/A | ui/menus/notes/vocab/counter.py | (not needed) | 8 | Simple counter |
| N/A | qt_utils/ex_qmenu.py | (not needed) | 24 | QMenu utilities |

**Subtotal: ~300 lines ported / 789 total (38% complete, but main infrastructure done)**

**Note:** New architecture means less code! Many Python menu utilities are obsolete.
Main menus work, note-specific actions remain to be ported.

---

## Summary Statistics

| Category | Status | Lines Ported | Total Lines | % Complete |
|----------|--------|--------------|-------------|------------|
| Dialogs | 4/5 complete | 755 | 849 | 89% |
| Widgets | 2/3 complete | 191 | 290 | 66% |
| Menus | Infrastructure ✅ | ~300 | 789 | 38% |
| **Total** | **Good progress** | **~1,246** | **1,928** | **65%** |

**Key Achievement:** Main infrastructure complete, menus use C# business logic directly!

---

## Porting Order (Recommended)

### Phase 1: Infrastructure ✅ COMPLETE
1. ~~Create JAStudio.UI project with Avalonia~~ ✅
2. ~~Set up Python → C# dialog invocation pattern~~ ✅
3. ~~Add integration tests~~ ✅
4. ~~AboutDialog as proof of concept~~ ✅
5. ~~Context menu positioning infrastructure~~ ✅
   - Window-based menu with submenu pattern
   - DPI-aware coordinate positioning
   - Python → C# coordinate passing

### Phase 2: Dialogs ✅ MOSTLY COMPLETE
1. ~~`vocab_flags_dialog.py` → `VocabFlagsDialog.axaml`~~ ✅ (most complex, good test)
2. ~~`open_note_dialog.py` → `NoteSearchDialog.axaml`~~ ✅ (search with async background)
3. `find_english_words_dialog.py` → `EnglishWordSearchDialog.axaml` ⚠️ TODO
4. ~~`readings_mapping_dialog.py` → `ReadingsMappingsDialog.axaml`~~ ✅
5. ~~`configuration.py` → `OptionsDialog.axaml`~~ ✅

### Phase 3: Widgets ✅ COMPLETE
1. ~~`string_set_widget.py` → `StringSetControl.axaml`~~ ✅ (reused in VocabFlagsDialog)
2. ~~`require_forbid_widget.py` → `RequireForbidControl.axaml`~~ ✅ (radio group)
3. `qt_task_progress_runner.py` → `TaskProgressDialog.axaml` ⚠️ TODO (low priority)

### Phase 4: Menus ✅ INFRASTRUCTURE COMPLETE
1. ~~Create UI-agnostic MenuItem specification classes~~ ✅
2. ~~Build main menus in C# (JapaneseMainMenu, NoteContextMenu)~~ ✅
3. ~~Build shared menus (OpenInAnki, WebSearch)~~ ✅
4. ~~Create PyQt adapter to render C# specs~~ ✅ (`qt_menu_adapter.py`)
5. ~~Wire up Python to call C# menu builders~~ ✅
6. ~~Integrate AnkiFacade for minimal Python API calls~~ ✅
7. **TODO**: Port note-specific actions (Kanji/Vocab/Sentence main.py and string_menu.py)

**Current Status:**
- Main menu (Japanese) - Config ✅, Lookup ✅, Local Actions ✅
- Context menu - Scaffolding ✅, Lookup submenus ✅
- ~120 note-specific actions remain (Kanji, Vocab, Sentence menus)
- Architecture allows incremental porting without breaking existing functionality

### Phase 5: Complete Avalonia Migration (Future)
1. Replace PyQt adapter with Avalonia menu rendering
2. Remove Python UI layer entirely
3. Run JAStudio as standalone Avalonia app (no Anki dependency)


