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

**Context Menu Infrastructure: WIP**
- `ContextMenuPopup.axaml.cs` - Avalonia menu displayed at specific screen coordinates
- Uses Menu control with submenu to show at precise position
- Python integration via `jastudio/ui/avalonia_host.py`
- Positioning works correctly with DPI scaling (tested at 125%)
- Successfully displays vertical menu with multiple items
- Menu closes on selection or when focus is lost

**Python Integration:**
- `jastudio/ui/avalonia_host.py` - Python wrapper for C# dialogs
- `show_about_dialog()` - Opens the About dialog from Python
- `show_context_menu_popup()` - Shows context menu at (x, y) coordinates

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
| MISSING | ui/menus/notes/vocab/vocab_flags_dialog.py | 231 | Edit vocab matching flags, register, string rules |
| MISSING | ui/open_note/open_note_dialog.py | 264 | Search and open notes dialog |
| MISSING | ui/english_dict/find_english_words_dialog.py | 94 | English dictionary search |
| MISSING | configuration/readings_mapping_dialog.py | 120 | Configure reading mappings |
| 90% | configuration/configuration.py | 140 | Japanese addon options dialog |

**Subtotal: 849 lines**

---

## Widgets (PORT TO AVALONIA)

| Status | File | Lines | Description |
|--------|------|-------|-------------|
| MISSING | ui/menus/notes/vocab/string_set_widget.py | 130 | Editable string set widget |
| MISSING | ui/menus/notes/vocab/require_forbid_widget.py | 61 | Require/Forbid radio button group |
| MISSING | qt_utils/qt_task_progress_runner.py | 99 | Progress dialog for batch operations |

**Subtotal: 290 lines**

---

## Menus (PORT TO AVALONIA)

| Status | File | Lines | Description |
|--------|------|-------|-------------|
| MISSING | ui/menus/common.py | 102 | Right-click menu builder, dispatches by note type |
| MISSING | ui/tools_menu.py | 74 | Main "Japanese" menu in Anki menubar |
| MISSING | ui/menus/notes/vocab/main.py | 69 | Vocab note context menu |
| MISSING | ui/menus/menu_utils/ex_qmenu.py | 63 | Menu action helpers (add_ui_action, add_lookup_action) |
| MISSING | ui/menus/notes/sentence/string_menu.py | 52 | Sentence string context menu |
| MISSING | ui/menus/notes/vocab/string_menu.py | 52 | Vocab string context menu |
| MISSING | ui/menus/notes/vocab/create_note_menu.py | 52 | Create note submenu |
| MISSING | ui/menus/web_search.py | 48 | Web search menu items |
| MISSING | ui/menus/browser/main.py | 45 | Browser context menu additions |
| MISSING | ui/menus/notes/kanji/main.py | 38 | Kanji note context menu |
| MISSING | ui/menus/notes/kanji/string_menu.py | 36 | Kanji string context menu |
| MISSING | ui/menus/notes/sentence/main.py | 36 | Sentence note context menu |
| MISSING | ui/menus/open_in_anki.py | 33 | "Open in Anki" menu items |
| MISSING | ui/menus/menu_utils/shortcutfinger.py | 31 | Keyboard shortcut text helpers |
| MISSING | ui/menus/notes/vocab/common.py | 26 | Vocab menu common utilities |
| MISSING | ui/menus/notes/vocab/counter.py | 8 | Simple counter helper |
| MISSING | qt_utils/ex_qmenu.py | 24 | QMenu extension utilities |

**Subtotal: 789 lines**

---

## Summary Statistics

| Category | Files | Lines |
|----------|-------|-------|
| Dialogs | 5 | 849 |
| Widgets | 3 | 290 |
| Menus | 17 | 789 |
| **Total** | **25** | **1,928** |

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

### Phase 2: Dialogs (Highest Value)
1. `vocab_flags_dialog.py` → `VocabFlagsDialog.axaml` (most complex, good test)
2. `open_note_dialog.py` → `NoteSearchDialog.axaml` (search with table)
3. `find_english_words_dialog.py` → `EnglishWordSearchDialog.axaml`
4. `readings_mapping_dialog.py` → `ReadingsMappingDialog.axaml`
5. `configuration.py` → `OptionsDialog.axaml`

### Phase 3: Widgets
1. `string_set_widget.py` → `StringSetEditor.axaml` (reused in dialogs)
2. `require_forbid_widget.py` → `RequireForb ← **IN PROGRESS**
   - ✅ Context menu positioning infrastructure complete
   - Next: Port actual menu builders from PyQt to AvaloniaidSelector.axaml`
3. `qt_task_progress_runner.py` → `TaskProgressDialog.axaml`

### Phase 4: Menus
1. Port menu structure to Avalonia MenuItems
2. Wire up Python to call C# menu builder
3. Context menus integrate via Avalonia ContextMenu


