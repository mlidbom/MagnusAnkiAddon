# JAStudio Menu Porting Status

---

## ⚠️ CRITICAL ARCHITECTURAL CONSTRAINT: ALL-AT-ONCE SWITCH

**Why C# Cannot Call Python (jaslib):**

This project manages massive in-memory state:
- ~30,000 vocabulary entries with metadata
- ~50,000+ sentences with metadata
- Complex synchronization with Anki's database

In Python, this state consumes **gigabytes of RAM** and causes severe performance degradation.

**The Problem:**
- Maintaining this state in BOTH Python (jaslib) and C# (JAStudio.Core) would require **three-way synchronization** (Python ↔ C# ↔ Anki)
- The Python and C# types are **incompatible and do not interoperate**
- This is architecturally impossible to maintain
- We cannot have two copies of this massive state

**The Solution:**
- We CANNOT switch gradually from jaslib → JAStudio.Core
- When we switch, we must **remove ALL of jaslib** and replace it **ALL AT ONCE** with JAStudio.Core
- This switch will happen **SOON** - as soon as remaining menu code is ported

**What This Means for Menu Porting:**
- ✅ C# menus MUST call JAStudio.Core directly (no Python business logic callbacks)
- ✅ C# can ONLY call minimal Anki APIs (via AnkiFacade: ExecuteLookup, ShowTooltip, Refresh)
- ✅ All menu actions must be implemented in C# using existing JAStudio.Core types
- ❌ NEVER create menu callbacks to Python business logic - it will be deleted soon

**This is why:**
- Menu architecture uses pure data specs (MenuItem trees)
- Actions are lambdas calling JAStudio.Core methods
- PyQt adapter is a thin 30-line renderer
- We can't gradually migrate - it's all or nothing

---

## IMPORTANT: Business Logic Already in C#

**VIRTUALLY EVERYTHING EXCEPT FOR UI CODE IS ALREADY PORTED TO C#.**

The business logic, note operations, parsing, lookups, and data manipulation are all in `JAStudio.Core`. The UI only needs to:
1. Create Avalonia dialogs/menus (in C#)
2. Call existing C# methods in `JAStudio.Core`
3. **DO NOT** create Python callbacks except for the thin Anki integration layer

When porting menus/dialogs:
- ✅ **DO**: Create Avalonia UI in C# that calls `JAStudio.Core` methods
- ✅ **DO**: Use existing C# types like `VocabNote`, `KanjiNote`, `SentenceNote`, `JPCollection`
- ❌ **DO NOT**: Create callbacks to Python UNLESS YOU HAVE BEEN EXPLICITLY INSTRUCTED TO
- ❌ **DO NOT**: Implement business logic in Python - it's already in C#

---

## Code Locations

### Python Source (What to Port From)
- **Main "Japanese" menu**: `src/jastudio_src/jastudio/ui/tools_menu.py`
- **Right-click context menu**: `src/jastudio_src/jastudio/ui/menus/common.py`
- **Kanji note menus**: `src/jastudio_src/jastudio/ui/menus/notes/kanji/main.py` and `string_menu.py`
- **Vocab note menus**: `src/jastudio_src/jastudio/ui/menus/notes/vocab/main.py` and `string_menu.py`
- **Sentence note menus**: `src/jastudio_src/jastudio/ui/menus/notes/sentence/main.py` and `string_menu.py`
- **Shared lookup menus**: ~~`src/jastudio_src/jastudio/ui/menus/open_in_anki.py`~~ ✅ PORTED and ~~`web_search.py`~~ ✅ PORTED

### C# Target (Where to Port To)
- **Main menu class**: `src/src_dotnet/JAStudio.UI/Menus/JapaneseMainMenu.cs`
- **Context menu class**: `src/src_dotnet/JAStudio.UI/Menus/NoteContextMenu.cs`
- **Shared lookup menus**: `src/src_dotnet/JAStudio.UI/Menus/OpenInAnkiMenus.cs` ✅ and `WebSearchMenus.cs` ✅
- **Query builder**: `src/src_dotnet/JAStudio.Core/AnkiUtils/QueryBuilder.cs` ✅
- **Menu host infrastructure**: `src/src_dotnet/JAStudio.UI/PopupMenuHost.cs`
- **Dialog host (entry points)**: `src/src_dotnet/JAStudio.UI/DialogHost.cs`
- **Utilities**: `src/src_dotnet/JAStudio.UI/Utils/BrowserLauncher.cs` ✅, `InputDialog.cs` ✅

### Python Integration Layer
- **Avalonia host wrapper**: `src/jastudio_src/jastudio/ui/avalonia_host.py` (updated)
- **Menu hooks**: `src/jastudio_src/jastudio/ui/tools_menu.py` (see `_add_avalonia_main_menu()`)
- **Context menu hooks**: `src/jastudio_src/jastudio/ui/menus/common.py` (see `_add_avalonia_menu_entry()`)

---

## Completed Infrastructure (Phase 1)

### ✅ QueryBuilder (JAStudio.Core/AnkiUtils/QueryBuilder.cs)
**Status**: 100% complete - all 21 methods fully implemented
- Vocab searches: wildcard, exact form, reading/answer, text analysis
- Kanji searches: all in string, by reading, with radicals, with meaning
- Sentence searches: vocabulary parsing, exact string, potential matches
- Combined searches: exact matches, dependencies, notes by ID
- Uses existing types: `VocabNote`, `KanjiNote`, `SentenceNote`, `TextAnalysis`, note collections

### ✅ OpenInAnkiMenus (JAStudio.UI/Menus/OpenInAnkiMenus.cs)
**Status**: Complete - all Anki browser search menus ported
- Exact matches (with/without sentences, reading cards)
- Kanji menu (all kanji in string, by reading, with radicals, with meaning)
- Vocab menu (form exact, reading cards, wildcard, text words)
- Sentence menu (parse vocabulary, exact string)
- Uses `QueryBuilder` for all query generation

### ✅ WebSearchMenus (JAStudio.UI/Menus/WebSearchMenus.cs)
**Status**: Complete - all web search menus ported
- Kanji lookups (Kanji explosion, Kanshudo, Kanji map)
- Sentences (Immersion Kit, Tatoeba)
- Conjugation (Japanese verb conjugator, Verbix)
- Translation (DeepL, Kanshudo)
- Grammar (Google, Japanese with anime, Wiktionary)
- Images (Google, Bing)
- Dictionary lookups (Merriam Webster, Wiktionary, Takoboto, Jisho, Wanikani, Word Kanshudo)

---

## Main Menu Structure (JapaneseMainMenu.cs)

### Status Overview
- **Config Menu**: ✅ COMPLETE
  - Options (Ctrl+Shift+S) - ✅ COMPLETE (Avalonia dialog with full two-way binding to JapaneseConfig)
  - Readings mappings (Ctrl+Shift+M) - ✅ COMPLETE (Avalonia dialog with text editor, search, deduplication)
  
- **Lookup Menu**: PARTIALLY COMPLETE
  - Open note (Ctrl+O) - TODO (Python dialog, needs porting to Avalonia)
  - ✅ Anki (all search menus complete, see OpenInAnkiMenus.cs)
  - ✅ Web (all search menus complete, see WebSearchMenus.cs)
  
- **Local Actions Menu**: ✅ COMPLETE (all operations use JAStudio.Core.Batches.LocalNoteUpdater directly)
  - Update submenu - ✅ COMPLETE (Vocab, Kanji, Sentences, Tag metadata, All, Reparse, Full rebuild)
  - Convert Immersion Kit sentences - TODO (not yet ported to C#, uses Python via AnkiFacade)
  - Update everything except reparsing sentences - ✅ COMPLETE
  - Create vocab notes for parsed words - ✅ COMPLETE
  - Regenerate vocab source answers from jamdict - ✅ COMPLETE
  
- **Debug Menu**: ❌ EXCLUDED (Python runtime diagnostics, not relevant to .NET)
  - ❌ Show instance report - EXCLUDED
  - ❌ Take Snapshot - EXCLUDED
  - ❌ Show current snapshot diff - EXCLUDED
  - ❌ Show diff against first snapshot - EXCLUDED
  - ❌ Show diff against current snapshot - EXCLUDED
  - ❌ Run GC and report - EXCLUDED
  - ❌ Reset - EXCLUDED
  - (NOTE: These are Python memory management diagnostics, addressing Python's poor performance with >100MB memory usage. Not needed in .NET. Remain in Python menu for now.)

---

## Right-Click Context Menu (NoteContextMenu.cs)

### Context Menu Structure
- SCAFFOLDED Selection: "{text}" (dynamic, when text is selected)
  - SCAFFOLDED Current note actions (menu entry exists, action is TODO stub)
  - ✅ COMPLETE Open in Anki (fully implemented via OpenInAnkiMenus.cs)
  - ✅ COMPLETE Search Web (fully implemented via WebSearchMenus.cs)
  - SCAFFOLDED Exactly matching notes (menu entry exists, action is TODO stub)
  - SCAFFOLDED Create: {text} (menu entries exist, actions are TODO stubs)
    - vocab - TODO stub
    - sentence - TODO stub
    - kanji - TODO stub
  - SCAFFOLDED Reparse matching sentences (menu entry exists, action is TODO stub)
- SCAFFOLDED Clipboard: "{text}" (dynamic, when clipboard has content)
  - (Same structure as Selection menu - Anki/Web lookups ✅ COMPLETE, other items SCAFFOLDED)
- SCAFFOLDED Note actions (menu entry exists, note-type specific, see below)
- SCAFFOLDED Universal note actions (menu entry exists, actions are TODO stubs)
  - Open in previewer - TODO stub
  - Note actions (nested, note-type specific) - TODO stub
  - Unsuspend all cards - TODO stub
  - Suspend all cards - TODO stub
- SCAFFOLDED View (menu entry exists, note-type specific, see below)

---

## Note-Type Specific Actions (Not Yet Started)

### Kanji Note Actions (notes/kanji/main.py)
- ✅ COMPLETE Note actions
  - ✅ COMPLETE Open
    - Primary Vocabs
    - Vocabs (all vocab with this kanji)
    - Radicals
    - Kanji (kanji containing this kanji as a radical)
    - Sentences
  - ✅ COMPLETE Reset Primary Vocabs
  - ✅ COMPLETE Accept meaning (conditional: only if no user answer)
  - ✅ COMPLETE Populate radicals from mnemonic tags
  - ✅ COMPLETE Bootstrap mnemonic from radicals
  - ✅ COMPLETE Reset mnemonic
- ✅ COMPLETE View (Empty in Python)

### Kanji String Menu Actions (notes/kanji/string_menu.py)
- NOT STARTED Highlighted Vocab
  - {vocab} (dynamic: one per primary vocab, positioned)
  - [Last]
  - Remove (conditional: if string is in primary vocab)
- NOT STARTED Add
  - Similar meaning
  - Confused with
- NOT STARTED Make primary Onyomi Reading (conditional: if katakana string in readings)
- NOT STARTED Remove primary Onyomi Reading (conditional: if katakana string in primary readings)
- NOT STARTED Make primary Kunyomi reading (conditional: if hiragana string in readings)
- NOT STARTED Remove primary Kunyomi reading (conditional: if hiragana string in primary readings)

### Vocab Note Actions (notes/vocab/main.py)
- ✅ COMPLETE Note actions
  - ✅ COMPLETE Open
    - Vocab (Forms, Compound parts, In compounds, Synonyms, See also, Homonyms, Dependencies)
    - Sentences (I'm Studying, All, Primary form, Highlighted, Potentially matching, Marked invalid)
    - Kanji
    - Ergative twin (conditional)
  - ✅ COMPLETE Edit (calls VocabFlagsDialog)
  - ✅ COMPLETE Create (Clone to form, Noun variations, Verb variations, Misc variations, Selection/Clipboard combinations)
  - ✅ COMPLETE Copy (Question, Answer, Definition, Sentences) - Note: clipboard integration via Python layer
  - ✅ COMPLETE Misc (Accept meaning, Generate answer, Reparse sentences, Repopulate TOS, Autogenerate compounds)
  - ✅ COMPLETE Remove (User explanation, User explanation long, User mnemonic, User answer - all conditional)
- ✅ COMPLETE View (Empty in Python)

### Vocab String Menu Actions (notes/vocab/string_menu.py)
- NOT STARTED Add (Synonym, Confused with, Antonym, Form, See also, Perfect synonym - conditional)
- NOT STARTED Set (Ergative twin, Derived from)
- NOT STARTED Remove (Synonym, Confused with, Antonym, Ergative twin, Form, See also, Perfect synonym, Derived from - all conditional)
- NOT STARTED Sentence (Add/Remove highlight, Mark as incorrect - conditional)
- NOT STARTED Create combined {string} (Prefix/Suffix variations)

### Sentence Note Actions (notes/sentence/main.py)
- NOT STARTED Note actions
  - NOT STARTED Open (Highlighted Vocab, Highlighted Vocab Read Card, Kanji, Parsed words)
  - NOT STARTED Remove (All highlighted, All incorrect matches, All hidden matches, Source comments - all conditional)
  - NOT STARTED Remove User (comments, answer, question - all conditional)
- NOT STARTED View ({toggle} dynamic, Toggle all auto yield flags)

### Sentence String Menu Actions (notes/sentence/string_menu.py)
- NOT STARTED Add (Highlighted Vocab, Hidden matches, Incorrect matches - conditional/dynamic)
- NOT STARTED Remove (Highlighted vocab, Hidden matches, Incorrect matches - conditional/dynamic)
- NOT STARTED Split with word-break tag (conditional)

---

## Summary Statistics
- **Total menu items tracked**: ~200+ items
- **COMPLETE**: ~77 items (QueryBuilder, OpenInAnki, WebSearch, Options/Readings dialogs, all Local Actions, **Vocab Note Actions complete**, **Kanji Note Actions complete**)
- **SCAFFOLDED**: ~20 items (menu structure exists, some actions still TODO)
- **EXCLUDED**: ~7 items (Debug menu - Python runtime diagnostics not relevant to .NET)
- **MISSING**: ~96+ items (Sentence note-specific actions, string menus not yet ported)
- **Porting completion**: ~38% complete, ~10% scaffolded, ~4% excluded, ~48% not started

### Phase 1 Complete ✅
- QueryBuilder (21 methods) - ✅ COMPLETE
- OpenInAnkiMenus (17 menu items) - ✅ COMPLETE
- WebSearchMenus (22 menu items) - ✅ COMPLETE
- ShortcutFinger utility (keyboard accelerators) - ✅ COMPLETE
- Menu integration into JapaneseMainMenu - ✅ COMPLETE
- Menu integration into NoteContextMenu - ✅ COMPLETE
- Python integration layer wiring - ✅ COMPLETE
- OptionsDialog (full configuration UI) - ✅ COMPLETE
- ReadingsMappingsDialog (Avalonia text editor) - ✅ COMPLETE
- Config Menu (Options + Readings Mappings) - ✅ COMPLETE
- Local Actions Menu (all update operations) - ✅ COMPLETE
- **Architecture cleanup**: Menus use JAStudio.Core directly instead of Python callbacks
- **AnkiFacade reduced**: From 17 methods (370 lines) to 4 methods (~110 lines) - 70% reduction

### Phase 2 Complete ✅
- ✅ Main menu Config actions (Options ✅, Readings mappings ✅)
- ✅ Main menu Local Actions (Update ✅, Create ✅, Regenerate ✅, Convert Immersion Kit TODO)
- ✅ **Vocab Note Actions Menu COMPLETE** (Open, Edit, Create, Copy, Misc, Remove - all 6 submenus fully implemented)
  - Open: 13 menu items (vocab lookups, sentence lookups, kanji, ergative twin)
  - Create: 30+ menu items (clone to form, noun/verb variations, misc conjugations)
  - Copy: 4 menu items (clipboard operations via Python layer)
  - Misc: 5 menu items (accept meaning, generate answer, reparse, repopulate TOS, autogenerate compounds)
  - Remove: 4 menu items (conditional enable/disable for user fields)
  - **All operations call JAStudio.Core directly - zero Python business logic dependencies!**
- ✅ **Kanji Note Actions Menu COMPLETE** (Open, Reset, Populate, Accept meaning - all operations fully implemented)
  - Open: 5 menu items (primary vocabs, all vocabs, radicals, kanji with this radical, sentences)
  - Reset/Populate: 4 menu items (reset primary vocabs, populate radicals, bootstrap mnemonic, reset mnemonic)
  - Accept meaning: Conditional menu item (only shown if no user answer)
  - **All operations call JAStudio.Core directly - KanjiNote methods used directly!**
- TODO Context menu Create actions (vocab, sentence, kanji)
- TODO Context menu Universal note actions (previewer, suspend/unsuspend)
- TODO Open Note dialog (currently Python dialog, needs Avalonia port)

### Excluded from Porting ❌
- **Debug Menu** (7 items) - Python runtime memory diagnostics used to manage Python's poor performance with >100MB memory. Not relevant to .NET which handles memory efficiently. These remain in the Python menu and may be removed entirely after full .NET migration.

### Phase 3 Not Started
- Sentence note-specific actions (Open, Remove, User fields, View)
- Sentence string menus (add/remove relationships, highlights, parse operations)
- Kanji string menus (add/remove relationships, highlighted vocab, primary readings)
- Vocab string menus (add/remove relationships, sentence highlighting)
- Conditional menu items based on note state
- Dynamic menu generation based on data

### Infrastructure Complete ✅
The C# infrastructure is in place:
  - `JAStudio.UI/Menus/JapaneseMainMenu.cs` ✅ COMPLETE (Config + Local Actions + Lookup menus)
  - `JAStudio.UI/Menus/NoteContextMenu.cs` ✅ VOCAB + KANJI COMPLETE (vocab + kanji note menus fully implemented, sentence TODO)
  - `JAStudio.UI/Menus/OpenInAnkiMenus.cs` ✅ COMPLETE
  - `JAStudio.UI/Menus/WebSearchMenus.cs` ✅ COMPLETE (uses BrowserLauncher directly)
  - `JAStudio.UI/Views/OptionsDialog.axaml` ✅ COMPLETE (Full configuration dialog)
  - `JAStudio.UI/ViewModels/OptionsDialogViewModel.cs` ✅ COMPLETE (Two-way binding to JapaneseConfig)
  - `JAStudio.UI/Views/ReadingsMappingsDialog.axaml` ✅ COMPLETE (Text editor with search)
  - `JAStudio.UI/ViewModels/ReadingsMappingsDialogViewModel.cs` ✅ COMPLETE (Edit/save mappings)
  - `JAStudio.UI/Utils/ShortcutFinger.cs` ✅ COMPLETE (keyboard accelerators)
  - `JAStudio.UI/Utils/BrowserLauncher.cs` ✅ COMPLETE (pure C# URL opening)
  - `JAStudio.UI/Utils/InputDialog.cs` ✅ COMPLETE
  - `JAStudio.UI/Anki/AnkiFacade.cs` ✅ MINIMIZED (4 methods, only true Anki API calls)
  - `JAStudio.UI/PopupMenuHost.cs` (infrastructure ready)
  - `JAStudio.UI/DialogHost.cs` (entry points for dialogs)
  
Python integration layer complete ✅:
  - `jastudio/ui/avalonia_host.py` (minimal - only dialogs not yet ported)
  - `jastudio/ui/tools_menu.py` (uses C# menus via PyQt adapter)
  - `jastudio/ui/menus/common.py` (uses C# menus via PyQt adapter)
  - `jastudio/ui/menus/qt_menu_adapter.py` ✅ COMPLETE (converts C# menu specs to PyQt)
  
**Architecture**: Menus are 100% C# → All business logic uses JAStudio.Core directly → Python is just a thin PyQt rendering layer

## Implementation Patterns Established

### Business Logic Uses C# Core Directly (NEW PATTERN)
```csharp
// Menus call JAStudio.Core directly - no Python callbacks!
private void OnUpdateVocab() => LocalNoteUpdater.UpdateVocab();
private void OnUpdateAll() => LocalNoteUpdater.UpdateAll();
private void OnCreateMissingVocab() => LocalNoteUpdater.CreateMissingVocabWithDictionaryEntries();
```

### Anki Browser Searches (Via AnkiFacade)
```csharp
// C# generates query using QueryBuilder
var query = QueryBuilder.KanjiInString(text);
// AnkiFacade calls Python's Anki browser API
AnkiFacade.ExecuteLookup(query);
```

### Web URL Opening (Pure C#)
```csharp
// Direct C# call, no Python needed
BrowserLauncher.OpenUrl("https://jisho.org/search/" + encodedText);
```

### Menu Creation Pattern
```csharp
// Menu specs are UI-agnostic, converted to PyQt or Avalonia
OpenInAnkiMenus.BuildOpenInAnkiMenuSpec(() => _searchText)
WebSearchMenus.BuildWebSearchMenuSpec(() => _searchText)
```

### AnkiFacade - Minimal Python Interop
```csharp
// Only 4 methods remain - true Anki API calls only:
- ExecuteLookup(query)     // Opens Anki browser
- ShowTooltip(msg)          // Shows Anki tooltip  
- ShowNoteSearchDialog()    // TODO: Port to Avalonia
- ConvertImmersionKit()     // TODO: Port to C#
```

### Keyboard Accelerators
```csharp
// Use ShortcutFinger for consistent accelerator keys
Header = ShortcutFinger.Home1("Config")  // Alt+U
Header = ShortcutFinger.Up1("Text")      // Alt+P
```

---

## Next Steps for Porting

### Immediate Priority (Phase 2A)
1. ✅ ~~**Port Readings Mappings dialog to Avalonia**~~ - COMPLETE
   - ✅ Readings mappings dialog with text editor, search box, save/cancel
2. **Port Open Note dialog to Avalonia** - Replace Python dialog with C# Avalonia UI
   - Note search dialog (needs search functionality and note browsing)

### Medium Priority (Phase 2B)  
1. **Implement Local Actions menu** - Wire up TODO stubs in JapaneseMainMenu.cs
   - Update operations (Python callbacks needed - Anki note operations)
   - Convert/Create/Regenerate operations (Python callbacks needed - Anki note operations)
2. **Implement Context menu Create actions** - Wire up TODO stubs in NoteContextMenu.cs
   - Create vocab note (Python callback needed - creates Anki note)
   - Create sentence note (Python callback needed - creates Anki note)
   - Create kanji note (Python callback needed - creates Anki note)
3. **Implement Universal note actions** - Wire up TODO stubs in NoteContextMenu.cs
   - Open in previewer (Python callback needed - Anki previewer)
   - Suspend/Unsuspend operations (Python callbacks needed - Anki operations)

### Large Effort (Phase 3)
1. **Note-specific main actions** - Port from Python note menu files
   - Vocab note "Open" submenu (forms, compounds, synonyms, sentences, kanji, etc.)
   - Vocab note "Create" submenu (clone forms, variations, prefixes/suffixes)
   - Vocab note "Copy" operations
   - Vocab note "Misc" operations  
   - Kanji note actions
   - Sentence note actions
2. **Note-specific string menus** - Context menu actions on selected text
   - Kanji string menu (primary vocab, readings)
   - Vocab string menu (add synonym, form, confused with, etc.)
   - Sentence string menu (highlights, hidden/incorrect matches)

---

## Notes
- Menu items marked as "TODO stub" have menu entries created but handler methods just log a message
- Menu items marked as "SCAFFOLDED" have structure in place but need implementation
- Menu items marked as "conditional" only appear when certain conditions are met
- Menu items marked as "dynamic" are generated at runtime based on data
- All ported menus use ShortcutFinger for keyboard accelerators matching the Python originals
