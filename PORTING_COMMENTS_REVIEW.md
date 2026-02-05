# Porting-Related Comments Review

This document lists code comments that appear to be related to porting or might indicate incomplete implementations.

## Design Issues (Not Porting Blockers)

### 1. SentenceCollection - Redundant Check
**File**: [SentenceCollection.cs](src/src_dotnet/JAStudio.Core/Note/Collection/SentenceCollection.cs#L60)
```csharp
// TODO: isn't this check redundant, won't the match have been removed during indexing?
```
**Status**: Design question preserved from Python source. Not a porting issue - this is questioning the Python logic itself.

### 2. DictEntry - Hiragana Conversion Concerns
**File**: [DictEntry.cs](src/src_dotnet/JAStudio.Core/LanguageServices/JamdictEx/DictEntry.cs#L171)
**File**: [DictEntry.cs](src/src_dotnet/JAStudio.Core/LanguageServices/JamdictEx/DictEntry.cs#L178)
```csharp
// TODO: this converting to hiragana is worrisome. Is this really the behavior we want? What false positives might we run into?
```
**Status**: Design concern preserved from Python source. Both Python and C# have this same concern.

### 3. TextLocation - Compound Inflection Check
**File**: [TextLocation.cs](src/src_dotnet/JAStudio.Core/LanguageServices/JanomeEx/WordExtraction/TextLocation.cs#L155)
```csharp
// todo: having this check here only means that marking a compound as an inflecting word has no effect, and figuring out why things are not working can be quite a pain
```
**Status**: Design concern preserved from Python source. Not a porting issue.

### 4. ForbidsHasDisplayedOverlappingFollowingCompound - Problematic Reference
**File**: [ForbidsHasDisplayedOverlappingFollowingCompound.cs](src/src_dotnet/JAStudio.Core/LanguageServices/JanomeEx/WordExtraction/Matches/StateTests/Tail/ForbidsHasDisplayedOverlappingFollowingCompound.cs#L23)
```csharp
// todo: this is a problematic reference to display_words. That collection is initialized using this class,
// so this class will return different results depending on whether it is used after or before display_words is first initialized. Ouch
```
**Status**: Design concern preserved from Python source. Architectural issue that exists in both implementations.

## Potential Porting Issues

### 5. SplitToken - Needs Refactoring
**File**: [SplitToken.cs](src/src_dotnet/JAStudio.Core/LanguageServices/JanomeEx/Tokenizing/SplitToken.cs#L3)
```csharp
// TODO: replace this jack of all trades class with custom classes
```
**Status**: Design improvement needed. Python has the same TODO, so this is ported correctly but could be improved in both versions.

### 6. GodanDictionaryFormStem - Odd Behavior
**File**: [GodanDictionaryFormStem.cs](src/src_dotnet/JAStudio.Core/LanguageServices/JanomeEx/Tokenizing/GodanDictionaryFormStem.cs#L32)
```csharp
// TODO: this feels odd, but without it it seems that things go haywire...
```
**Status**: Preservation of Python uncertainty. Needs investigation but not a porting gap.

### 7. GodanDictionaryFormStem - Ichidan/Godan Ambiguity
**File**: [GodanDictionaryFormStem.cs](src/src_dotnet/JAStudio.Core/LanguageServices/JanomeEx/Tokenizing/GodanDictionaryFormStem.cs#L76)
```csharp
// TODO: this leaves us with these tokens claiming both to be an ichidan (via the base class) and a godan... We can't tell which, but still..
```
**Status**: Design issue preserved from Python. Both implementations have this ambiguity.

## Implementation Stubs/Placeholders

### 8. VocabNoteMatchingRules - Stub Implementation ✅ RESOLVED
**File**: [VocabNoteMatchingRules.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNoteMatchingRules.cs#L100)
```csharp
// Stub: Create empty data for now
```
**Status**: **RESOLVED** - Implemented full serialization/deserialization using `MutableSerializedObjectField<VocabNoteMatchingRulesData>` matching Python's implementation with `MutableSerializedObjectField[VocabNoteMatchingRulesData]`. The stub has been replaced with proper field loading and saving.

### 9. YieldLastTokenToOverlappingCompound - Settings Placeholder ✅ RESOLVED
**File**: [YieldLastTokenToOverlappingCompound.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/YieldLastTokenToOverlappingCompound.cs#L48)
```csharp
// Placeholder for Settings class
```
**Status**: **RESOLVED** - Removed placeholder Settings class and integrated with the real `Configuration.Settings` singleton class that was already ported. Added using directive for `JAStudio.Core.Configuration`.

### 10. KanjiNote - Placeholder Comment ✅ RESOLVED
**File**: [KanjiNote.cs](src/src_dotnet/JAStudio.Core/Note/KanjiNote.cs#L373)
```csharp
// Placeholder methods for vocab-related functionality
```
**Status**: **RESOLVED** - Comment removed. The methods are fully implemented and no longer placeholders.

### 11. VocabNoteAudio - Field Consolidation Question ✅ RESOLVED
**File**: [VocabNoteAudio.cs](src/src_dotnet/JAStudio.Core/Note/Vocabulary/VocabNoteAudio.cs#L16)
```csharp
Second = new WritableAudioField(vocab, NoteFieldsConstants.Vocab.Audio);  // Using same field - Python has Audio_b/Audio_g but C# might consolidate
```
**Status**: **RESOLVED** - Python DOES have separate Audio_b, Audio_g, and Audio_TTS fields. Added these constants to NoteFieldsConstants.Vocab and updated VocabNoteAudio to use the correct separate fields instead of consolidating to one field.

## Documentation Comments (Not Issues)

The following are informational comments explaining porting decisions:

- **JAAssert.cs:6** - "porting comment: renamed to avoid collision with assertion libraries assert class"
- **NoteTags.cs:81-82** - Explains why Python's string interning is not needed in C#
- **JNToken.cs:16** - "Standard references instead of WeakRef (C# has better GC)"
- **JNToken.cs:33** - "Python defaults to '*' when not provided"
- **StringExtensions.cs:44** - "Use word boundary detection to match whole words only (matching Python's implementation)"

These are correct and document intentional differences between Python and C#.

## Summary

**Action Items - All Resolved**:
1. ✅ Review VocabNoteMatchingRules stub implementation (#8) - Fixed to use MutableSerializedObjectField
2. ✅ Investigate Settings class placeholder (#9) - Integrated with Configuration.Settings
3. ✅ Remove outdated placeholder comment from KanjiNote (#10) - Comment removed
4. ✅ Check VocabNoteAudio field consolidation (#11) - Separated into three distinct fields

**Total Potential Issues**: 4 (All Resolved)
**Design Concerns (Not Blockers)**: 7
**Documentation Only**: 6

All porting-related comment issues have been addressed!
