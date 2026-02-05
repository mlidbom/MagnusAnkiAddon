# Porting Gap Analysis: Python jaslib → C# JAStudio.Core

## Current Status

### ✅ PORTED (Core Foundation)
- **JPNote.cs** ← jpnote.py
- **JPNoteData.cs** ← jpnote_data.py  
- **VocabNote.cs** ← vocabnote.py
- **KanjiNote.cs** ← kanjinote.py
- **SentenceNote.cs** ← sentencenote.py
- **Tags/NoteTags** ← tags.py / note_tags.py
- **NoteRecursiveFlushGuard.cs** ← note_flush_guard.py
- **BackendNoteCreator.cs** ← backend_note_creator.py
- **DifficultyCalculator.cs** ← difficulty_calculator.py
- **Collection classes** ← collection/*.py (VocabCollection, KanjiCollection, SentenceCollection, NoteCache, JPCollection)
- **VocabNoteQuestion.cs** ← vocabnote_question.py
- **VocabNoteForms.cs** ← vocabnote_forms.py
- **VocabNoteUserFields.cs** ← vocabnote_userfields.py
- **ParsingResult.cs** ← parsing_result.py
- **SentenceConfiguration.cs** ← sentence_configuration.py

### ❌ NOT YET PORTED

#### Vocabulary Components (18 files missing)
- ❌ **vocabnote_audio.py** - Audio field management
- ❌ **vocabnote_cloner.py** - Cloning vocab notes
- ❌ **vocabnote_conjugator.py** - Verb/adjective conjugation
- ❌ **vocabnote_factory.py** - Factory for creating vocab notes
- ❌ **vocabnote_generated_data.py** - Auto-generated data
- ❌ **vocabnote_kanji.py** - Kanji extraction from vocab
- ❌ **vocabnote_matching_rules.py** - Matching configuration
- ❌ **vocabnote_matching_rules_is_inflecting_word.py**
- ❌ **vocabnote_matching_rules_yield_last_token_to_next_compound.py**
- ❌ **vocabnote_metadata.py** - Metadata management
- ❌ **vocabnote_meta_tag.py** - Meta tag system
- ❌ **vocabnote_parts_of_speech.py** - POS management
- ❌ **vocabnote_register.py** - Register (formality) tracking
- ❌ **vocabnote_sentences.py** - Sentences using this vocab
- ❌ **vocabnote_sorting.py** - Sorting logic
- ❌ **vocabnote_usercompoundparts.py** - User compound parts
- ❌ **pos.py** - Part of speech enum/types
- ❌ **pos_set_interner.py** - POS set optimization
- ❌ **related_vocab/** subfolder - Related vocab tracking
- ❌ **serialization/** subfolder - Vocab serialization

#### Sentence Components (4 files missing)
- ❌ **caching_sentence_configuration_field.py** - Caching wrapper
- ❌ **parsed_match.py** - Match result structure
- ❌ **user_fields.py** - User-editable sentence fields
- ❌ **word_exclusion_set.py** - Excluded words
- ❌ **serialization/** subfolder - Sentence serialization

#### Kanji Components (1 file missing)
- ❌ **kanjinote_mnemonic_maker.py** - Mnemonic generation

#### NoteFields Components (Multiple files missing)
- ✅ **IntegerField.cs** ← integer_field.py
- ✅ **MutableStringField.cs** ← mutable_string_field.py
- ✅ **CachingMutableStringField.cs** ← caching_mutable_string_field.py
- ✅ **CommaSeparatedStringsListField.cs** ← comma_separated_strings_list_field.py
- ✅ **FallbackStringField.cs** ← fallback_string_field.py
- ✅ **TagFlagField.cs** ← tag_flag_field.py
- ✅ **SerializedObjectField.cs** ← json_object_field.py
- ❌ **comma_separated_strings_list_field_de_duplicated.py**
- ❌ **audio_field.py**
- ❌ **require_forbid_flag_field.py**
- ❌ **sentence_question_field.py**
- ❌ **strip_html_on_read_fallback_string_field.py**
- ❌ **auto_save_wrappers/** subfolder

---

## RECOMMENDED NEXT STEPS

### Priority 1: VocabNote Foundation (CRITICAL)
These are heavily used by VocabNote and need to be ported next:

1. **VocabNoteQuestion** - Already ported ✅
2. **vocabnote_kanji.py** → **VocabNoteKanji.cs** - Extract kanji from vocab
3. **vocabnote_parts_of_speech.py** + **pos.py** → **VocabNotePartsOfSpeech.cs** + **PartOfSpeech.cs**
4. **vocabnote_conjugator.py** → **VocabNoteConjugator.cs** - Verb/adjective conjugation
5. **vocabnote_generated_data.py** → **VocabNoteGeneratedData.cs** - Auto-generation

### Priority 2: VocabNote Features
6. **vocabnote_sentences.py** → **VocabNoteSentences.cs** - Sentences using vocab
7. **vocabnote_matching_rules.py** → **VocabNoteMatchingRules.cs** - Matching config
8. **vocabnote_metadata.py** → **VocabNoteMetadata.cs**
9. **vocabnote_usercompoundparts.py** → **VocabNoteUserCompoundParts.cs**
10. **related_vocab/** → **RelatedVocab/** subfolder

### Priority 3: Sentence Components
11. **parsed_match.py** → **ParsedMatch.cs**
12. **user_fields.py** → **SentenceUserFields.cs**
13. **word_exclusion_set.py** → **WordExclusionSet.cs**

### Priority 4: Additional Fields
14. Missing notefields components as needed

---

## SUGGESTION FOR NEXT ACTION

**Start with Priority 1, item #2: Port `vocabnote_kanji.py` → `VocabNoteKanji.cs`**

Why this order?
- VocabNoteKanji is referenced in VocabSnapshot (forms, kanji extraction)
- It's foundational for vocab caching
- It's relatively self-contained
- Tests already expect kanji extraction to work

Would you like me to start porting VocabNoteKanji.cs?
