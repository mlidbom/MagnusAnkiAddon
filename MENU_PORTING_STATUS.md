# JAStudio Menu Porting Status

## Code Locations

### Python Source (What to Port From)
- **Main "Japanese" menu**: `src/jastudio_src/jastudio/ui/tools_menu.py`
- **Right-click context menu**: `src/jastudio_src/jastudio/ui/menus/common.py`
- **Kanji note menus**: `src/jastudio_src/jastudio/ui/menus/notes/kanji/main.py` and `string_menu.py`
- **Vocab note menus**: `src/jastudio_src/jastudio/ui/menus/notes/vocab/main.py` and `string_menu.py`
- **Sentence note menus**: `src/jastudio_src/jastudio/ui/menus/notes/sentence/main.py` and `string_menu.py`
- **Shared lookup menus**: `src/jastudio_src/jastudio/ui/menus/open_in_anki.py` and `web_search.py`

### C# Target (Where to Port To)
- **Main menu class**: `src/src_dotnet/JAStudio.UI/Menus/JapaneseMainMenu.cs`
- **Context menu class**: `src/src_dotnet/JAStudio.UI/Menus/NoteContextMenu.cs`
- **Menu host infrastructure**: `src/src_dotnet/JAStudio.UI/PopupMenuHost.cs`
- **Dialog host (entry points)**: `src/src_dotnet/JAStudio.UI/DialogHost.cs`

### Python Integration Layer
- **Avalonia host wrapper**: `src/jastudio_src/jastudio/ui/avalonia_host.py`
- **Menu hooks**: `src/jastudio_src/jastudio/ui/tools_menu.py` (see `_add_avalonia_main_menu()`)
- **Context menu hooks**: `src/jastudio_src/jastudio/ui/menus/common.py` (see `_add_avalonia_menu_entry()`)

---

### Rules

- **Menu structure:** Maintain the same hierarchy, nesting, and organization as Python
- **Naming:** Keep the same menu item text/labels as Python
- **Functionality:** Each menu action must behave identically to its Python counterpart
- **Shortcuts:** Preserve keyboard shortcuts (Ctrl+Shift+S, etc.)
- **Dynamic menus:** Maintain dynamic menu creation (e.g., forms menu, readings menu)
- **Enabled/disabled states:** Match Python's logic for when menu items are enabled
- **Missing dependencies:** When ported code doesn't compile due to missing classes, create them. If too complex to implement immediately, create members throwing `NotImplementedException`
- **Implementation completeness:** Either fully implement a menu action or throw `NotImplementedException`. Do NOT create non-functional stubs

## Legend
- **MISSING** - No C# equivalent exists yet
- **COMPLETE** - C# equivalent verified as functionally equivalent to Python

---

## Main "Japanese" Menu (tools_menu.py)

### Top Level
- MISSING Japanese
  - MISSING Config
    - MISSING Options (Ctrl+Shift+S)
    - MISSING Readings mappings (Ctrl+Shift+M)
  - MISSING Lookup
    - MISSING Open note (Ctrl+O)
    - MISSING Anki
      - MISSING Exact matches
        - MISSING Open Exact matches | no sentences | reading cards
        - MISSING Open Exact matches with sentences
      - MISSING Kanji
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
  - MISSING Open in Anki (same structure as Main Menu > Lookup > Anki)
  - MISSING Search Web (same structure as Main Menu > Lookup > Web)
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
  - (Same structure as Selection menu)
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
- **MISSING**: ~200+ items
- **COMPLETE**: 0 items
- **Porting completion**: 0%

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
