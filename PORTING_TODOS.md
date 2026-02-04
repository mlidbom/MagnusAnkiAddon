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

### 3. VocabNoteQuestion - Mine.VocabPrefixSuffixMarker
**File**: [VocabNoteQuestion.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNoteQuestion.cs#L76)
```csharp
public string WithoutNoiseCharacters => Raw; // TODO: Use Mine.VocabPrefixSuffixMarker when Mine class is ported (currently empty string anyway)
```
**Status**: Mine class not yet ported
**Action**: Port Mine class or determine if this is still needed

---

### 4. VocabNoteMetaTag - Ichidan/Godan Potential Check ✅ COMPLETED
**File**: [VocabNoteMetaTag.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNoteMetaTag.cs#L132)
**Status**: RESOLVED - Implemented the ichidan hiding godan potential check using `IchidanGodanPotentialOrImperativeHybridSplitter.TryGetGodanHiddenByIchidan()`, matching Python's implementation. The class was already ported and available.

---

### 5. VocabNoteSentences - SentenceNote.IsStudying
**File**: [VocabNoteSentences.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNoteSentences.cs#L41)
```csharp
// TODO: Implement when SentenceNote.IsStudying is ported
return 0; // _parent().All().Count(it => it.IsStudying(card));
```
**File**: [VocabNoteSentences.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNoteSentences.cs#L78)
```csharp
// TODO: Implement when SentenceNote.IsStudying is ported
return All(); // All().Where(it => it.IsStudying()).ToList();
```
**Status**: SentenceNote.IsStudying not yet implemented
**Action**: Port IsStudying functionality from SentenceNote

---

### 6. VocabNoteSentences - NoteFields Constants ✅ COMPLETED
**File**: [VocabNoteSentences.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNoteSentences.cs#L49-L50)
**Status**: RESOLVED - Replaced hard-coded strings "Reading" and "Listening" with `NoteFieldsConstants.VocabNoteType.Card.Reading` and `NoteFieldsConstants.VocabNoteType.Card.Listening`, matching Python's `NoteFields.VocabNoteType.Card.Reading` and `NoteFields.VocabNoteType.Card.Listening`.

---

### 7. VocabNoteSentences - WithVocabMarkedInvalid
**File**: [VocabNoteSentences.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNoteSentences.cs#L89)
```csharp
// TODO: Implement when WithVocabMarkedInvalid is ported
return new List<SentenceNote>();
```
**Status**: SentenceCollection.WithVocabMarkedInvalid not yet ported
**Action**: Port this functionality from SentenceCollection

---

### 8. VocabNoteSentences - WithVocabOwnedForm
**File**: [VocabNoteSentences.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNoteSentences.cs#L95)
```csharp
// TODO: Implement when WithVocabOwnedForm is ported
return new List<SentenceNote>();
```
**Status**: SentenceCollection.WithVocabOwnedForm not yet ported  
**Action**: Port this functionality from SentenceCollection

---

### 9. KanjiNote - Katakana to Hiragana Conversion ✅ COMPLETED
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L64)
**Status**: RESOLVED - Used existing `KanaUtils.KatakanaToHiragana()` method to convert katakana to hiragana in `UpdateGeneratedData()`, matching Python implementation.

---

### 10. KanjiNote - Vocab System Integration
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L69)
```csharp
// TODO: Implement when vocab system is complete
SetPrimaryVocabAudio(string.Empty);
```
**Status**: Vocab system appears to be ported per PORTING_STATUS.md
**Action**: Implement primary vocab audio functionality

---

### 11. KanjiNote - StripHtmlMarkup ✅ COMPLETED
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L135)
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L142)
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L149)
**Status**: RESOLVED - Applied `StringExtensions.StripHtmlMarkup()` to all three primary reading methods (`GetPrimaryReadingsOn`, `GetPrimaryReadingsKun`, `GetPrimaryReadingsNan`), matching Python's use of `ex_str.strip_html_markup()`.

---

### 12. KanjiNote - ReplaceWord
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L170)
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L181)
```csharp
// TODO: Implement ReplaceWord when needed
SetReadingOn(GetReadingOnHtml().Replace(reading, $"<primary>{reading}</primary>"));
```
**Status**: Using simple string.Replace, but TODO suggests more sophisticated word replacement needed
**Action**: Determine if simple Replace is sufficient or if ReplaceWord utility is needed

---

### 13. KanjiNote - ExtractCommaSeparatedValues ✅ COMPLETED
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L192)
**Status**: RESOLVED - Method `StringExtensions.ExtractCommaSeparatedValues` already exists and is used elsewhere in the same file. Updated `GetRadicals()` to use it, matching Python's `ex_str.extract_comma_separated_values()`.

---

### 14. KanjiNote - Config and Mnemonic Maker
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L345)
```csharp
// TODO: Implement config and mnemonic maker
```
**Status**: KanjiNoteMnemonicMaker is 100% ported per PORTING_STATUS.md
**Action**: Integrate KanjiNoteMnemonicMaker into KanjiNote

---

### 15. KanjiNote - VocabCollection Integration
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L377)
```csharp
// TODO: Implement when VocabCollection is complete
```
**Status**: VocabCollection is 100% ported per PORTING_STATUS.md
**Action**: Implement the VocabCollection integration

---

### 16. VocabCollection - Disambiguation Name Access
**File**: [VocabCollection.cs](src/src_dotnet/JAStudio.Core/Note/Collection/VocabCollection.cs#L143)
```csharp
// TODO: Access vocab.question.disambiguation_name when implemented
// FetchParts(vocab.Question.DisambiguationName);
```
**Status**: VocabNoteQuestion exists, need to verify if DisambiguationName property exists
**Action**: Implement or enable access to disambiguation_name property

---

### 17. CachingSentenceConfigurationField - Review Test Method
**File**: [CachingSentenceConfigurationField.cs](src/src_dotnet/JAStudio.Core/Note/Sentences/CachingSentenceConfigurationField.cs#L67)
```csharp
public void SetValueDirectlyTestsOnly(SentenceConfiguration configuration)//TODO: Review
```
**Status**: Method marked for review
**Action**: Review whether this test-only method is properly implemented

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
