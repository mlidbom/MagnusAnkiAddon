# JAStudio Menu Porting Status

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
- Dict**COMPLETE** Anki (see OpenInAnkiMenus.cs)
      - **COMPLETE** Exact matches
        - **COMPLETE** Open Exact matches | no sentences | reading cards
        - **COMPLETE** Open Exact matches with sentences
      - **COMPLETE** Kanji
        - **COMPLETE** All kanji in string
        - **COMPLETE** By reading part
        - **COMPLETE** By reading exact
        - **COMPLETE** With radicals
        - **COMPLETE** With meaning
      - **COMPLETE** Vocab
        - **COMPLETE** form -
        - **COMPLETE** form - read card only
        - **COMPLETE** form, reading or answer
        - **COMPLETE** Wildcard
        - **COMPLETE** Text words
      - **COMPLETE** Sentence
        - **COMPLETE** Parse Vocabulary
        - **COMPLETE** Exact String
    - **COMPLETE** Web (see WebSearchMenus.cs)
      - **COMPLETE** Kanji
        - **COMPLETE** Kanji explosion
        - **COMPLETE** Kanshudo
        - **COMPLETE** Kanji map
      - **COMPLETE** Sentences
        - **COMPLETE** Sentences: Immersion Kit
        - **COMPLETE** Sentences: Tatoeba
      - **COMPLETE** Misc
        - **COMPLETE** Conjugate
          - **COMPLETE** Conjugate: Japanese verb conjugator
          - **COMPLETE** Conjugate: Verbix
        - **COMPLETE** Translate
          - **COMPLETE** Translate: Deepl
          - **COMPLETE** Translate: Kanshudo
        - **COMPLETE** Grammar
          - **COMPLETE** Grammar: Google
          - **COMPLETE** Grammar: Japanese with anime
          - **COMPLETE** Grammar: Wiktionary
        - **COMPLETE** Images
          - **COMPLETE** Images: Google
          - **COMPLETE** Images: Bing
      - **COMPLETE** Lookup
        - **COMPLETE** English: Merriam Webster
        - **COMPLETE** Wiktionary
        - **COMPLETE** Lookup: Takoboto
        - **COMPLETE** Lookup: Jisho
        - **COMPLETE** Lookup: Wanikani
        - **COMPLETE**anji
        - MISSING All kanji in string
        - MISSING By reading part
        - MISSING By reading exact
        - MISSING With radicals
        - MISSING With meaning
      - MISSING Vocab
        - MISSING form -
        - MISSING form - read card only
        - MISSING form, reading or answer
        - MISSING Wildcard
        - MISSING Text words
      - MISSING Sentence
        - MISSING Parse Vocabulary
        - MISSING Exact String
    - MISSING Web
      - MISSING Kanji
        - MISSING Kanji explosion
        - MISSING Kanshudo
        - MISSING Kanji map
      - MISSING Sentences
        - MISSING Sentences: Immersion Kit
        - MISSING Sentences: Tatoeba
      - MISSING Misc
        - MISSING Conjugate
          - MISSING Conjugate: Japanese verb conjugator
          - MISSING Conjugate: Verbix
        - MISSING Translate
          - MISSING Translate: Deepl
          - MISSING Translate: Kanshudo
        - MISSING Grammar
          - MISSING Grammar: Google
          - MISSING Grammar: Japanese with anime
          - MISSING Grammar: Wiktionary
        - MISSING Images
          - MISSING Images: Google
          - MISSING Images: Bing
      - MISSING Lookup
        - MISSING English: Merriam Webster
        - MISSING Wiktionary
        - MISSING Lookup: Takoboto
        - MISSING Lookup: Jisho
        - MISSING Lookup: Wanikani
        - MISSING Lookup: Word Kanshudo
  - MISSING Local Actions
    - MISSING Update
      - MISSING Vocab
      - MISSING Kanji
      - MISSING Sentences
      - MISSING Tag note metadata
      - MISSING All the above
      - MISSING Reparse sentences
      - MISSING All the above: Full rebuild
    - MISSING Convert Immersion Kit sentences
    - MISSING Update everything except reparsing sentences
    - MISSING Create vocab notes for parsed words with no vocab notes
    - MISSING Regenerate vocab source answers from jamdict
  - MISSING Debug
    - MISSING Show instance report
    - MISSING Take Snapshot
    - MISSING Show current snapshot diff
    - MISSING Show diff against first snapshot
    - MISSING Show diff against current snapshot
    - MISSING Run GC and report
    - MISSING Reset
    - MISSING Refresh UI (F5)
  - MISSING About JA Studio

---

## Right-Click Context Menu (common.py)

### Context Menu Structure
- MISSING Selection: "{text}" (dynamic, when text is selected)
  - MISSING Current note actions (see Note-Type Specific Actions below)
  - **COMPLETE** Open in Anki (same structure as Main Menu > Lookup > Anki)
  - **COMPLETE** Search Web (same structure as Main Menu > Lookup > Web)
  - MISSING Exactly matching notes
    - MISSING Vocab Actions
    - MISSING Sentence Actions
    - MISSING Kanji Actions
  - MISSING Create: {text}
    - MISSING vocab
    - MISSING sentence
    - MISSING kanji
  - MISSING Reparse matching sentences
- MISSING Clipboard: "{text}" (dynamic, when clipboard has content)
  - (Same structure as Selection menu - **Anki/Web lookups COMPLETE**)
- MISSING Note actions (see Note-Type Specific Actions below)
- MISSING Universal note actions
  - MISSING Open in previewer
  - MISSING Note actions (nested, note-type specific)
  - MISSING Unsuspend all cards
  - MISSING Suspend all cards
- MISSING View (see Note-Type Specific Actions below)

---

## Note-Type Specific Actions

### Kanji Note Actions (notes/kanji/main.py)
- MISSING Note actions
  - MISSING Open
    - MISSING Primary Vocabs
    - MISSING Vocabs
    - MISSING Radicals
    - MISSING Kanji
    - MISSING Sentences
  - MISSING Reset Primary Vocabs
  - MISSING Accept meaning (conditional: only if no user answer)
  - MISSING Populate radicals from mnemonic tags
  - MISSING Bootstrap mnemonic from radicals
  - MISSING Reset mnemonic
- MISSING View
  - (Empty in Python)

### Kanji String Menu Actions (notes/kanji/string_menu.py)
- MISSING Highlighted Vocab
  - MISSING {vocab} (dynamic: one per primary vocab, positioned)
  - MISSING [Last]
  - MISSING Remove (conditional: if string is in primary vocab)
- MISSING Add
  - MISSING Similar meaning
  - MISSING Confused with
- MISSING Make primary Onyomi Reading (conditional: if katakana string in readings)
- MISSING Remove primary Onyomi Reading (conditional: if katakana string in primary readings)
- MISSING Make primary Kunyomi reading (conditional: if hiragana string in readings)
- MISSING Remove primary Kunyomi reading (conditional: if hiragana string in primary readings)

### Vocab Note Actions (notes/vocab/main.py)
- MISSING Note actions
  - MISSING Open
    - MISSING Vocab
      - MISSING Forms
      - MISSING Compound parts
      - MISSING In compounds
      - MISSING Synonyms
      - MISSING See also
      - MISSING Homonyms
        - MISSING Homonyms: {reading} (dynamic: one per reading)
      - MISSING Dependencies
    - MISSING Sentences
      - MISSING Sentences I'm Studying
      - MISSING Sentences
      - MISSING Sentences with primary form
      - MISSING Sentences with this word highlighted
      - MISSING Potentially matching sentences
      - MISSING Marked invalid in sentences
    - MISSING Kanji
    - MISSING Ergative twin (conditional: if twin exists)
  - MISSING Edit
  - MISSING Create
    - MISSING Clone to form
      - MISSING {form} (dynamic: one per form with no vocab)
    - MISSING Noun variations
      - MISSING する-verb
      - MISSING します-verb
      - MISSING な-adjective
      - MISSING の-adjective
      - MISSING に-adverb
      - MISSING と-adverb
    - MISSING Verb variations
      - MISSING ます-form
      - MISSING て-form
      - MISSING た-form
      - MISSING ない-form
      - MISSING え-stem/godan-imperative
      - MISSING ば-form
      - MISSING {receptive/passive}-form
      - MISSING causative
      - MISSING imperative
      - MISSING Potential-godan
    - MISSING Misc
      - MISSING く-form-of-い-adjective
      - MISSING さ-form-of-い-adjective
      - MISSING て-prefixed
      - MISSING お-prefixed
      - MISSING ん-suffixed
      - MISSING か-suffixed
    - MISSING Selection (conditional: if selection exists)
      - MISSING Prefix-onto
        - MISSING Dictionary form
        - MISSING chop-1
        - MISSING chop-2
        - MISSING chop-3
      - MISSING Suffix-onto
        - MISSING dictionary-form
        - MISSING い-stem
        - MISSING て-stem
        - MISSING え-stem
        - MISSING あ-stem
        - MISSING chop-1
        - MISSING chop-2
        - MISSING chop-3
        - MISSING chop-4
    - MISSING Clipboard (conditional: if clipboard has content)
      - (Same structure as Selection)
  - MISSING Copy
    - MISSING Question
    - MISSING Answer
    - MISSING Definition (question:answer)
    - MISSING Sentences: max 30
  - MISSING Misc
    - MISSING Accept meaning (conditional: if no user answer)
    - MISSING Generate answer
    - MISSING Reparse potentially matching sentences
    - MISSING Repopulate TOS
    - MISSING Autogenerate compounds
  - MISSING Remove
    - MISSING User explanation (conditional: if has value)
    - MISSING User explanation long (conditional: if has value)
    - MISSING User mnemonic (conditional: if has value)
    - MISSING User answer (conditional: if has value)
- MISSING View
  - (Empty in Python)

### Vocab String Menu Actions (notes/vocab/string_menu.py)
- MISSING Add
  - MISSING Synonym (conditional: if not already a synonym)
  - MISSING Synonyms transitively one level
  - MISSING Confused with (conditional: if not already confused with)
  - MISSING Antonym (conditional: if not already an antonym)
  - MISSING Form (conditional: if not already a form)
  - MISSING See also (conditional: if not already see also)
  - MISSING Perfect synonym, automatically synchronize answers (conditional: if not already perfect synonym)
- MISSING Set
  - MISSING Ergative twin
  - MISSING Derived from
- MISSING Remove
  - MISSING Synonym (conditional: if is a synonym)
  - MISSING Confused with (conditional: if is confused with)
  - MISSING Antonym (conditional: if is an antonym)
  - MISSING Ergative twin (conditional: if string is ergative twin)
  - MISSING Form (conditional: if is a form)
  - MISSING See also (conditional: if is see also)
  - MISSING Perfect synonym (conditional: if is perfect synonym)
  - MISSING Derived from (conditional: if string is derived from)
- MISSING Sentence
  - MISSING Add Highlight (conditional: if not already highlighted)
  - MISSING Remove highlight (conditional: if is highlighted)
  - MISSING Remove-sentence: Mark as incorrect match in sentence
- MISSING Create combined {string}
  - MISSING Prefix-onto
    - MISSING Dictionary form
    - MISSING chop-1
    - MISSING chop-2
    - MISSING chop-3
  - MISSING Suffix-onto
    - MISSING dictionary-form
    - MISSING い-stem
    - MISSING て-stem
    - MISSING え-stem
    - MISSING あ-stem
    - MISSING chop-1
    - MISSING chop-2
    - MISSING chop-3
    - MISSING chop-4

### Sentence Note Actions (notes/sentence/main.py)
- MISSING Note actions
  - MISSING Open
    - MISSING Highlighted Vocab
    - MISSING Highlighted Vocab Read Card
    - MISSING Kanji
    - MISSING Parsed words
  - MISSING Remove
    - MISSING All highlighted (conditional: if any highlighted)
    - MISSING All incorrect matches (conditional: if any incorrect matches)
    - MISSING All hidden matches (conditional: if any hidden matches)
    - MISSING Source comments (conditional: if has source comments)
  - MISSING Remove User
    - MISSING comments (conditional: if has user comments)
    - MISSING answer (conditional: if has user answer)
    - MISSING question (conditional: if has user question)
- MISSING View
  - MISSING {toggle} (dynamic: one per sentence view toggle)
  - MISSING Toggle all sentence auto yield compound last token flags (Ctrl+Shift+Alt+D)

### Sentence String Menu Actions (notes/sentence/string_menu.py)
- MISSING Add
  - MISSING Highlighted Vocab (conditional: if not already highlighted)
  - MISSING Hidden matches (dynamic: one or more based on matched words)
  - MISSING Incorrect matches (dynamic: one or more based on matched words)
- MISSING Remove
  - MISSING Highlighted vocab (conditional: if is highlighted)
  - MISSING Hidden matches (dynamic: one or more based on existing exclusions)
  - MISSING Incorrect matches (dynamic: one or more based on existing exclusions)
- MISSING Split with word-break tag in question (conditional: if string is in question)

---

## Summary Statistics
- **Total menu items tracked**: ~200+ items
- **COMPLETE**: ~50+ items (all shared lookup menus)
- **MISSING**: ~150+ items (note-specific actions, local actions, debug, config)
- **Porting completion**: ~25%

### Phase 1 Complete ✅
- QueryBuilder (21 methods)
- OpenInAnkiMenus (17 menu items)
- WebSearchMenus (22 menu items) ✅
- The C# scaffolding exists in:
  - `JAStudio.UI/Menus/JapaneseMainMenu.cs` (scaffolding + shared menus integrated)
  - `JAStudio.UI/Menus/NoteContextMenu.cs` (scaffolding + shared menus integrated)
  - `JAStudio.UI/Menus/OpenInAnkiMenus.cs` ✅ COMPLETE
  - `JAStudio.UI/Menus/WebSearchMenus.cs` ✅ COMPLETE
  - `JAStudio.UI/PopupMenuHost.cs`
  - `JAStudio.UI/DialogHost.cs` (updated with callbacks)
- Python integration layer in:
  - `jastudio/ui/avalonia_host.py` (updated with callbacks)
  - `jastudio/ui/tools_menu.py` (see `_add_avalonia_main_menu()`)
  - `jastudio/ui/menus/common.py` (see `_add_avalonia_menu_entry()`)

## Implementation Patterns Established

### Callback Pattern for Anki Browser Searches
```csharp
// C# generates query using QueryBuilder
var query = QueryBuilder.KanjiInString(text);
// Invokes Python callback which uses search_executor.do_lookup()
_executeLookup(query);
```

### Web URL Opening (Pure C#)
```csharp
// Direct C# call, no Python callback needed
BrowserLauncher.OpenUrl("https://jisho.org/search/" + encodedText);
```

### Menu Creation Pattern
```csharp
// Menu items use Func<string> for lazy text evaluation
OpenInAnkiMenus.BuildOpenInAnkiMenu(() => _searchText, _executeLookup)
WebSearchMenus.BuildWebSearchMenu(() => _searchText, BrowserLauncher.OpenUrl)
``Vocab, Kanji, Parsed words
2. **Note-specific string menus** - Context menu actions on selected text
   - Kanji string menu (add/remove readings, primary vocab)
   - Vocab string menu (add synonym, form, confused with, etc.)
   - Sentence string menu (add/remove highlights, hidden matches)
3. **Note manipulation actions** - Create, edit, copy, remove operations
   - Will need more Python callbacks for note modification
4. **Config/Debug/Local Actions** - Lower priority, Python UI dialogs needed

## Notes
- Menu items marked as "conditional" only appear when certain conditions are met
- Menu items marked as "dynamic" are generated at runtime based on data
- Submenu structures under "Open in Anki" and "Search Web" are shared between main menu and context menu
- The C# scaffolding exists in:
  - `JAStudio.UI/Menus/JapaneseMainMenu.cs`
  - `JAStudio.UI/Menus/NoteContextMenu.cs`
  - `JAStudio.UI/PopupMenuHost.cs`
  - `JAStudio.UI/DialogHost.cs`
- Python integration layer in:
  - `jastudio/ui/avalonia_host.py`
  - `jastudio/ui/tools_menu.py`
  - `jastudio/ui/menus/common.py`
