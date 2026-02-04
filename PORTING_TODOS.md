# JAStudio C# Porting - TODO Items

This document catalogs TODO items that were added during the Python-to-C# porting process and need to be addressed.

## Summary

- **Total C# TODOs**: 23 porting-related items (excluding "todo" in class/variable names)
- **Python TODOs**: 22 items (many are design/performance notes, not porting issues)
- **New C# Porting TODOs**: 15 items that represent incomplete implementations

---

## Porting-Related TODOs (Need Implementation)

### 1. String Auto-Interning ✅ COMPLETED
**File**: [NoteTags.cs](src/src_dotnet/JAStudio.Core/Note/NoteTags.cs#L81)
**Status**: RESOLVED - Python uses `string_auto_interner.auto_intern_qlist()` but per porting rules, string interning is a Python-specific optimization not needed in C#. Comment updated to explain why C# doesn't use it.

---

### 2. VocabNote - Dictionary Lookup
**File**: [VocabNote.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNote.cs#L91)
```csharp
// TODO: Implement when DictLookup is ported
// var dictLookup = DictLookup.LookupVocabWordOrName(this);
// if (dictLookup.FoundWords())
// {
//     var generated = dictLookup.FormatAnswer();
//     SourceAnswer.Set(generated);
// }
```
**Status**: Dictionary lookup functionality not yet ported
**Action**: Need to port DictLookup functionality

---

### 3. VocabNoteQuestion - Mine.VocabPrefixSuffixMarker ✅ COMPLETED
**File**: [VocabNoteQuestion.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNoteQuestion.cs#L76)
**Status**: RESOLVED - Implemented `WithoutNoiseCharacters` property to use `Raw.Replace(Mine.VocabPrefixSuffixMarker, "")`. The Mine class with VocabPrefixSuffixMarker constant already exists and was ready to use.

---

### 4. VocabNoteMetaTag - Ichidan/Godan Potential Check ✅ COMPLETED
**File**: [VocabNoteMetaTag.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNoteMetaTag.cs#L132)
**Status**: RESOLVED - Implemented the ichidan hiding godan potential check using `IchidanGodanPotentialOrImperativeHybridSplitter.TryGetGodanHiddenByIchidan()`, matching Python's implementation. The class was already ported and available.

---

### 5. VocabNoteSentences - SentenceNote.IsStudying ✅ COMPLETED
**File**: [VocabNoteSentences.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNoteSentences.cs#L41)
**File**: [VocabNoteSentences.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNoteSentences.cs#L78)
**Status**: RESOLVED - Implemented calls to `IsStudying()` in both `GetStudyingSentenceCount()` and `Studying()` methods. The `IsStudying()` method already exists in the base `JPNote` class and was ready to use.

---

### 6. VocabNoteSentences - NoteFields Constants ✅ COMPLETED
**File**: [VocabNoteSentences.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNoteSentences.cs#L49-L50)
**Status**: RESOLVED - Replaced hard-coded strings "Reading" and "Listening" with `NoteFieldsConstants.VocabNoteType.Card.Reading` and `NoteFieldsConstants.VocabNoteType.Card.Listening`, matching Python's `NoteFields.VocabNoteType.Card.Reading` and `NoteFields.VocabNoteType.Card.Listening`.

---

### 7. VocabNoteSentences - WithVocabMarkedInvalid ✅ COMPLETED
**File**: [VocabNoteSentences.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNoteSentences.cs#L89)
**Status**: RESOLVED - Implemented `InvalidIn()` to call `App.Col().Sentences.WithVocabMarkedInvalid(Vocab)`. The `WithVocabMarkedInvalid()` method already exists in SentenceCollection and was ready to use.

---

### 8. VocabNoteSentences - WithVocabOwnedForm ✅ COMPLETED
**File**: [VocabNoteSentences.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNoteSentences.cs#L95)
**Status**: RESOLVED - Implemented `WithOwnedForm()` to call `App.Col().Sentences.WithVocabOwnedForm(Vocab)`. The `WithVocabOwnedForm()` method already exists in SentenceCollection and was ready to use.

---

### 9. KanjiNote - Katakana to Hiragana Conversion ✅ COMPLETED
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L64)
**Status**: RESOLVED - Used existing `KanaUtils.KatakanaToHiragana()` method to convert katakana to hiragana in `UpdateGeneratedData()`, matching Python implementation.

---

### 10. KanjiNote - Vocab System Integration ✅ COMPLETED
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L69)
**Status**: RESOLVED - Implemented primary vocab audio functionality in `UpdatePrimaryAudios()`. Gets vocab notes from `GetPrimaryVocab()`, retrieves their audio using `Audio.GetPrimaryAudio()`, and concatenates them, matching Python's implementation.

---

### 11. KanjiNote - StripHtmlMarkup ✅ COMPLETED
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L135)
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L142)
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L149)
**Status**: RESOLVED - Applied `StringExtensions.StripHtmlMarkup()` to all three primary reading methods (`GetPrimaryReadingsOn`, `GetPrimaryReadingsKun`, `GetPrimaryReadingsNan`), matching Python's use of `ex_str.strip_html_markup()`.

---

### 12. KanjiNote - ReplaceWord ✅ COMPLETED
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L170)
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L181)
**Status**: RESOLVED - Updated `StringExtensions.ReplaceWord()` to use word boundary detection with regex (matching Python's `ex_str.replace_word()` which uses `\b` word boundaries). Applied to `AddPrimaryOnReading` and `AddPrimaryKunReading` methods.

---

### 13. KanjiNote - ExtractCommaSeparatedValues ✅ COMPLETED
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L192)
**Status**: RESOLVED - Method `StringExtensions.ExtractCommaSeparatedValues` already exists and is used elsewhere in the same file. Updated `GetRadicals()` to use it, matching Python's `ex_str.extract_comma_separated_values()`.

---

### 14. KanjiNote - Config and Mnemonic Maker ✅ COMPLETED
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L345)
**Status**: RESOLVED - Integrated `KanjiNoteMnemonicMaker.CreateDefaultMnemonic()` in `GetActiveMnemonic()` method with config check for `PreferDefaultMnemonicsToSourceMnemonics`, matching Python's implementation.

---

### 15. KanjiNote - VocabCollection Integration ✅ COMPLETED
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L377)
**Status**: RESOLVED - Implemented `GetVocabNotes()` to use `App.Col().Vocab.WithKanjiInAnyForm(this)`, matching Python's `app.col().vocab.with_kanji_in_any_form(self)`. VocabCollection is fully ported and integrated.

---

### 16. VocabCollection - Disambiguation Name Access ✅ COMPLETED
**File**: [VocabCollection.cs](src/src_dotnet/JAStudio.Core/Note/Collection/VocabCollection.cs#L143)
**Status**: RESOLVED - Enabled recursive call to `FetchParts(vocab.Question.DisambiguationName)` in `WithCompoundPart()` method. The `DisambiguationName` property exists and is accessible, matching Python's `vocab.question.disambiguation_name`.

---

### 17. CachingSentenceConfigurationField - Review Test Method ✅ COMPLETED
**File**: [CachingSentenceConfigurationField.cs](src/src_dotnet/JAStudio.Core/Note/Sentences/CachingSentenceConfigurationField.cs#L67)
**Status**: RESOLVED - Reviewed and confirmed correct. This is a test-only helper method that doesn't exist in Python. It directly sets `_value` without triggering Save(), which is appropriate for test scenarios. The `[Obsolete("For testing only")]` attribute properly warns against production use. Implementation is correct.

---

## TODOs That Exist in Both Python and C# (Design Issues, Not Porting Issues)

These are preserved from Python and represent original design concerns, not porting incompleteness:

1. **AnalysisConstants.cs / analysis_constants.py**: Full-width exclamation mark question
2. **DictEntry.cs / dict_entry.py** (2 instances): Katakana to hiragana conversion concerns
3. **SplitToken.cs / split_token.py**: Replace jack-of-all-trades class
4. **TextLocation.cs / text_location.py**: Compound inflecting word check placement
5. **ForbidsHasDisplayedOverlappingFollowingCompound.cs / forbids_has_displayed_overlapping_following_compound.py**: Problematic display_words reference
6. **GodanDictionaryFormStem.cs / godan_dictionary_form_stem.py** (2 instances): Token classification concerns
7. **SentenceCollection.cs / sentence_collection.py**: Redundant check question
8. **Synonyms.cs / Synonyms.py**: Cleanup after bug (can be removed soon)

---

## Action Plan

### High Priority (Blocking Functionality)
1. Port/implement SentenceNote.IsStudying (#5)
2. Port SentenceCollection.WithVocabMarkedInvalid (#7)
3. Port SentenceCollection.WithVocabOwnedForm (#8)
4. Implement DictLookup functionality (#2)

### Medium Priority (Incomplete Features)
5. Integrate KanjiNoteMnemonicMaker (#14)
6. Implement VocabCollection integration in KanjiNote (#15)
7. Implement ichidan/godan potential check (#4)
8. Implement primary vocab audio (#10)
9. Port Mine class for VocabPrefixSuffixMarker (#3)

### Low Priority (Cleanup/Refactoring)
10. Replace hard-coded strings with NoteFields constants (#6)
11. Remove string interning TODO (#1)
12. Remove ExtractCommaSeparatedValues TODO (#13)
13. Apply StripHtmlMarkup to regex results (#11)
14. Verify DisambiguationName access (#16)
15. Review test method (#17)
16. Determine if ReplaceWord is needed (#12)
17. Verify KatakanaToHiragana usage (#9)

---

## Notes

- Many TODOs marked "when X is ported" can now be addressed since X has been ported
- Several TODOs reference functionality that already exists and just needs to be wired up
- The design-level TODOs preserved from Python should be addressed in a refactoring phase, not during porting
