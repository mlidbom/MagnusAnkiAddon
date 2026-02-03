# JAStudio Python to C# Porting Status

## Legend
- **CREATED WIP** - C# equivalent exists but needs verification for equivalence
- **MISSING** - No C# equivalent exists yet

---

## Root Level
- CREATED WIP app.py
- CREATED WIP mylog.py

## batches/
- MISSING batches/local_note_updater.py

## configuration/
- MISSING configuration/configuration_value.py
- MISSING configuration/settings.py

## dotnet/
- MISSING dotnet/load_dotnet_runtime.py

## language_services/
- CREATED WIP language_services/conjugator.py
- CREATED WIP language_services/hiragana_chart.py
- CREATED WIP language_services/katakana_chart.py

### language_services/jamdict_ex/
- MISSING language_services/jamdict_ex/dict_entry.py
- MISSING language_services/jamdict_ex/dict_lookup.py
- MISSING language_services/jamdict_ex/dict_lookup_result.py
- MISSING language_services/jamdict_ex/jamdict_threading_wrapper.py
- MISSING language_services/jamdict_ex/priority_spec.py

### language_services/janome_ex/tokenizing/
- MISSING language_services/janome_ex/tokenizing/analysis_token.py
- MISSING language_services/janome_ex/tokenizing/godan_dictionary_form_stem.py
- MISSING language_services/janome_ex/tokenizing/inflection_forms.py
- MISSING language_services/janome_ex/tokenizing/inflection_types.py
- MISSING language_services/janome_ex/tokenizing/jn_parts_of_speech.py
- MISSING language_services/janome_ex/tokenizing/jn_token.py
- MISSING language_services/janome_ex/tokenizing/jn_tokenized_text.py
- MISSING language_services/janome_ex/tokenizing/jn_tokenizer.py
- MISSING language_services/janome_ex/tokenizing/split_token.py

#### language_services/janome_ex/tokenizing/pre_processing_stage/
- MISSING language_services/janome_ex/tokenizing/pre_processing_stage/dictionary_form_verb_splitter.py
- MISSING language_services/janome_ex/tokenizing/pre_processing_stage/godan_imperative_splitter.py
- MISSING language_services/janome_ex/tokenizing/pre_processing_stage/ichidan_godan_potential_or_imperative_hybrid_splitter.py
- MISSING language_services/janome_ex/tokenizing/pre_processing_stage/ichidan_imperative_splitter.py
- MISSING language_services/janome_ex/tokenizing/pre_processing_stage/pre_processing_stage.py
- MISSING language_services/janome_ex/tokenizing/pre_processing_stage/word_info.py
- MISSING language_services/janome_ex/tokenizing/pre_processing_stage/word_info_entry.py

### language_services/janome_ex/word_extraction/
- MISSING language_services/janome_ex/word_extraction/analysis_constants.py
- MISSING language_services/janome_ex/word_extraction/candidate_word.py
- MISSING language_services/janome_ex/word_extraction/candidate_word_variant.py
- MISSING language_services/janome_ex/word_extraction/text_analysis.py
- MISSING language_services/janome_ex/word_extraction/text_location.py
- CREATED WIP language_services/janome_ex/word_extraction/word_exclusion.py

#### language_services/janome_ex/word_extraction/matches/
- MISSING language_services/janome_ex/word_extraction/matches/dictionary_match.py
- CREATED WIP language_services/janome_ex/word_extraction/matches/match.py
- MISSING language_services/janome_ex/word_extraction/matches/missing_match.py
- CREATED WIP language_services/janome_ex/word_extraction/matches/vocab_match.py

##### language_services/janome_ex/word_extraction/matches/requirements/
- MISSING language_services/janome_ex/word_extraction/matches/requirements/custom_forbids_no_cache.py
- MISSING language_services/janome_ex/word_extraction/matches/requirements/match_inspector.py
- MISSING language_services/janome_ex/word_extraction/matches/requirements/requirement.py
- MISSING language_services/janome_ex/word_extraction/matches/requirements/vocab_match_inspector.py

##### language_services/janome_ex/word_extraction/matches/state_tests/
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/another_match_owns_the_form.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/forbids_compositionally_transparent_compound.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/forbids_compounds.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/forbids_dictionary_form_verb_inflection.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/forbids_dictionary_form_verb_stem_surface_as_compound_end.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/forbids_yields_to_surface.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/is_configured_hidden.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/is_configured_incorrect.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/is_exact_match.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/is_godan_imperative_surface_with_base.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/is_godan_potential_surface_with_base.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/is_ichidan_imperative.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/is_inflected_surface_with_valid_base.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/is_poison_word.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/is_shadowed.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/is_single_token.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/starts_with_godan_imperative_stem_or_inflection.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/starts_with_godan_potential_stem_or_inflection.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/surface_is_in.py

###### language_services/janome_ex/word_extraction/matches/state_tests/head/
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/head/failed_match_requirement.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/head/generic_forbids.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/head/has_godan_imperative_prefix.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/head/has_past_tense_stem.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/head/has_te_form_stem.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/head/is_sentence_start.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/head/prefix_is_in.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/head/requires_forbids_adverb_stem.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/head/requires_forbids_masu_stem.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/head/requires_or_forbids_dictionary_form_prefix.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/head/requires_or_forbids_dictionary_form_stem.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/head/requires_or_forbids_generic.py

###### language_services/janome_ex/word_extraction/matches/state_tests/tail/
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/tail/forbids_has_displayed_overlapping_following_compound.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/tail/is_sentence_end.py
- MISSING language_services/janome_ex/word_extraction/matches/state_tests/tail/suffix_is_in.py

## note/
- MISSING note/backend_note_creator.py
- MISSING note/difficulty_calculator.py
- CREATED WIP note/jpnote.py
- CREATED WIP note/jpnote_data.py
- MISSING note/kanjinote.py
- MISSING note/kanjinote_mnemonic_maker.py
- CREATED WIP note/note_constants.py
- MISSING note/note_flush_guard.py
- CREATED WIP note/note_tags.py
- CREATED WIP note/tag.py
- CREATED WIP note/tags.py

### note/collection/
- MISSING note/collection/card_studying_status.py
- CREATED WIP note/collection/jp_collection.py
- MISSING note/collection/kanji_collection.py
- CREATED WIP note/collection/note_cache.py
- MISSING note/collection/sentence_collection.py
- MISSING note/collection/vocab_collection.py

### note/notefields/
- CREATED WIP note/notefields/audio_field.py
- CREATED WIP note/notefields/caching_mutable_string_field.py
- CREATED WIP note/notefields/comma_separated_strings_list_field.py
- CREATED WIP note/notefields/comma_separated_strings_list_field_de_duplicated.py
- CREATED WIP note/notefields/fallback_string_field.py
- CREATED WIP note/notefields/integer_field.py
- CREATED WIP note/notefields/json_object_field.py
- CREATED WIP note/notefields/mutable_string_field.py
- CREATED WIP note/notefields/require_forbid_flag_field.py
- CREATED WIP note/notefields/sentence_question_field.py
- CREATED WIP note/notefields/strip_html_on_read_fallback_string_field.py
- CREATED WIP note/notefields/tag_flag_field.py

#### note/notefields/auto_save_wrappers/
- MISSING note/notefields/auto_save_wrappers/field_wrapper.py
- MISSING note/notefields/auto_save_wrappers/set_wrapper.py
- MISSING note/notefields/auto_save_wrappers/value_wrapper.py

### note/sentences/
- CREATED WIP note/sentences/caching_sentence_configuration_field.py
- CREATED WIP note/sentences/parsed_match.py
- CREATED WIP note/sentences/parsing_result.py
- CREATED WIP note/sentences/sentence_configuration.py
- CREATED WIP note/sentences/sentencenote.py
- CREATED WIP note/sentences/user_fields.py
- CREATED WIP note/sentences/word_exclusion_set.py

#### note/sentences/serialization/
- CREATED WIP note/sentences/serialization/parsed_word_serializer.py
- CREATED WIP note/sentences/serialization/parsing_result_serializer.py
- CREATED WIP note/sentences/serialization/sentence_configuration_serializer.py

### note/vocabulary/
- MISSING note/vocabulary/pos.py
- MISSING note/vocabulary/pos_set_interner.py
- CREATED WIP note/vocabulary/vocabnote.py
- MISSING note/vocabulary/vocabnote_audio.py
- MISSING note/vocabulary/vocabnote_cloner.py
- CREATED WIP note/vocabulary/vocabnote_conjugator.py
- MISSING note/vocabulary/vocabnote_factory.py
- CREATED WIP note/vocabulary/vocabnote_forms.py
- MISSING note/vocabulary/vocabnote_generated_data.py
- MISSING note/vocabulary/vocabnote_kanji.py
- MISSING note/vocabulary/vocabnote_matching_rules.py
- MISSING note/vocabulary/vocabnote_matching_rules_is_inflecting_word.py
- MISSING note/vocabulary/vocabnote_matching_rules_yield_last_token_to_next_compound.py
- MISSING note/vocabulary/vocabnote_meta_tag.py
- MISSING note/vocabulary/vocabnote_metadata.py
- MISSING note/vocabulary/vocabnote_parts_of_speech.py
- MISSING note/vocabulary/vocabnote_question.py
- MISSING note/vocabulary/vocabnote_register.py
- MISSING note/vocabulary/vocabnote_sentences.py
- MISSING note/vocabulary/vocabnote_sorting.py
- CREATED WIP note/vocabulary/vocabnote_usercompoundparts.py
- MISSING note/vocabulary/vocabnote_userfields.py

#### note/vocabulary/related_vocab/
- MISSING note/vocabulary/related_vocab/Antonyms.py
- MISSING note/vocabulary/related_vocab/ergative_twin.py
- MISSING note/vocabulary/related_vocab/perfect_synonyms.py
- MISSING note/vocabulary/related_vocab/related_vocab.py
- MISSING note/vocabulary/related_vocab/related_vocab_data.py
- MISSING note/vocabulary/related_vocab/related_vocab_data_serializer.py
- MISSING note/vocabulary/related_vocab/SeeAlso.py
- MISSING note/vocabulary/related_vocab/Synonyms.py

#### note/vocabulary/serialization/
- MISSING note/vocabulary/serialization/matching_rules_serializer.py

## task_runners/
- MISSING task_runners/i_task_progress_runner.py
- MISSING task_runners/invisible_task_progress_runner.py
- MISSING task_runners/task_progress_runner.py

## testutils/
- MISSING testutils/ex_pytest.py

## ui/
### ui/web/sentence/
- MISSING ui/web/sentence/candidate_word_variant_viewmodel.py
- MISSING ui/web/sentence/compound_part_viewmodel.py
- MISSING ui/web/sentence/match_viewmodel.py
- MISSING ui/web/sentence/sentence_viewmodel.py
- MISSING ui/web/sentence/text_analysis_viewmodel.py

### ui/web/vocab/
- MISSING ui/web/vocab/vocab_sentences_vocab_sentence_view_model.py

## viewmodels/
### viewmodels/kanji_list/
- MISSING viewmodels/kanji_list/kanji_list_viewmodel.py
- MISSING viewmodels/kanji_list/sentence_kanji_list_viewmodel.py
- MISSING viewmodels/kanji_list/sentence_kanji_viewmodel.py

---

## Summary Statistics
- **CREATED WIP**: 30 files
- **MISSING**: 135 files
- **Total Python files**: 165 files
- **Completion**: ~18%
