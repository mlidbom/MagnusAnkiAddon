from __future__ import annotations

import gc
import random
import re
from typing import TYPE_CHECKING

from ankiutils import app, query_builder
from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.janome_ex.tokenizing.pre_processing_stage.ichidan_godan_potential_or_imperative_hybrid_splitter import IchidanGodanPotentialOrImperativeHybridSplitter
from note.note_constants import CardTypes
from note.sentences.parsed_match import ParsedMatch
from note.sentences.sentencenote import SentenceNote
from note.tags import Tags
from note.vocabulary.vocabnote import VocabNote
from qt_utils.task_progress_runner import TaskRunner
from sysutils import ex_str

if TYPE_CHECKING:
    from anki.notes import NoteId
    from language_services.jamdict_ex.dict_lookup_result import DictLookupResult
    from note.kanjinote import KanjiNote
    from typed_linq_collections.collections.q_list import QList

def update_all() -> None:
    with TaskRunner.current("Updating everything but sentence reparsing"):
        update_sentences()
        update_kanji()
        update_vocab()
        tag_note_metadata()
        # update_vocab_parsed_parts_of_speech()

def full_rebuild() -> None:
    with TaskRunner.current("Full rebuild"):
        reparse_all_sentences()
        update_all()

def update_sentences() -> None:
    def update_sentence(sentence: SentenceNote) -> None:
        sentence.update_generated_data()

    with TaskRunner.current("Updating sentences") as runner:
        runner.process_with_progress(app.col().sentences.all(), update_sentence, "Updating sentences")

def update_kanji() -> None:
    def _update_kanji(kanji: KanjiNote) -> None:
        kanji.update_generated_data()

    with TaskRunner.current("Updating kanji") as runner:
        runner.process_with_progress(app.col().kanji.all(), _update_kanji, "Updating kanji")

def update_vocab() -> None:
    def _update_vocab(vocab: VocabNote) -> None:
        vocab.update_generated_data()

    with TaskRunner.current("Updating vocab") as runner:
        runner.process_with_progress(app.col().vocab.all(), _update_vocab, "Updating vocab")

def convert_immersion_kit_sentences() -> None:
    def convert_note(note_id: NoteId) -> None:
        immersion_kit_note = app.anki_collection().get_note(note_id)
        SentenceNote.import_immersion_kit_sentence(immersion_kit_note)
        app.anki_collection().remove_notes([note_id])

    with TaskRunner.current("Converting immersion kit sentences", inhibit_gc=True) as runner:
        immersion_kit_sences = list(app.anki_collection().find_notes(query_builder.immersion_kit_sentences()))
        runner.process_with_progress(immersion_kit_sences, convert_note, "Converting immersion kit sentences", run_gc=True, minimum_items_to_gc=100)

def tag_note_metadata() -> None:
    with TaskRunner.current("Tagging notes"):
        tag_kanji_metadata()
        tag_vocab_metadata()
        tag_sentence_metadata()

def tag_sentence_metadata() -> None:
    def tag_sentence(sentence: SentenceNote) -> None:
        sentence.tags.toggle(Tags.Sentence.Uses.incorrect_matches, any(sentence.configuration.incorrect_matches.get()))
        sentence.tags.toggle(Tags.Sentence.Uses.hidden_matches, any(sentence.configuration.hidden_matches.get()))

    with TaskRunner.current("Tagging sentence notes") as runner:
        runner.process_with_progress(app.col().sentences.all(), tag_sentence, "Tagging sentence notes")

def tag_vocab_metadata() -> None:
    def tag_note(vocab: VocabNote) -> None:
        vocab.tags.toggle(Tags.Vocab.has_no_studying_sentences, not any(vocab.sentences.studying()))
        vocab.tags.toggle(Tags.Vocab.Matching.Uses.required_prefix, not vocab.matching_configuration.configurable_rules.required_prefix.none())
        vocab.tags.toggle(Tags.Vocab.Matching.Uses.prefix_is_not, not vocab.matching_configuration.configurable_rules.prefix_is_not.none())
        vocab.tags.toggle(Tags.Vocab.Matching.Uses.suffix_is_not, not vocab.matching_configuration.configurable_rules.suffix_is_not.none())
        vocab.tags.toggle(Tags.Vocab.Matching.Uses.surface_is_not, not vocab.matching_configuration.configurable_rules.surface_is_not.none())
        vocab.tags.toggle(Tags.Vocab.is_ichidan_hiding_godan_potential, IchidanGodanPotentialOrImperativeHybridSplitter.is_ichidan_hiding_godan(vocab))

    with TaskRunner.current("Tagging vocab") as runner:
        runner.process_with_progress(app.col().vocab.all(), tag_note, "Tag vocab notes")

def tag_kanji_metadata() -> None:
    primary_reading = re.compile(r"<primary>(.*?)</primary>")

    known_kanji = {kanji.get_question() for kanji in app.col().kanji.all() if kanji.is_studying()}

    def tag_kanji(kanji: KanjiNote) -> None:
        vocab_with_kanji_in_main_form = app.col().vocab.with_kanji_in_main_form(kanji)
        vocab_with_kanji_in_any_form = app.col().vocab.with_kanji_in_any_form(kanji)

        is_radical = any(app.col().kanji.with_radical(kanji.get_question()))
        kanji.tags.toggle(Tags.Kanji.in_vocab_main_form, any(vocab_with_kanji_in_main_form))
        kanji.tags.toggle(Tags.Kanji.in_any_vocab_form, any(vocab_with_kanji_in_any_form))

        studying_reading_vocab = [voc for voc in vocab_with_kanji_in_main_form if voc.is_studying(CardTypes.reading)]
        kanji.tags.toggle(Tags.Kanji.with_studying_vocab, any(studying_reading_vocab))

        primary_readings: list[str] = primary_reading.findall(f"{kanji.get_reading_on_html()} {kanji.get_reading_kun_html()} {kanji.get_reading_nan_html()}")
        kanji.tags.toggle(Tags.Kanji.with_no_primary_readings, not primary_readings)

        primary_on_readings: list[str] = primary_reading.findall(kanji.get_reading_on_html())
        non_primary_on_readings: list[str] = [reading for reading in kanji.get_readings_on() if reading not in primary_readings]

        kanji.tags.toggle(Tags.Kanji.with_no_primary_on_readings, not primary_on_readings)

        def reading_is_in_vocab_readings(kanji_reading: str, voc: VocabNote) -> bool: return any(vocab_reading for vocab_reading in voc.readings.get() if reading_in_vocab_reading(kanji, kanji_reading, vocab_reading, voc.get_question()))
        def has_vocab_with_reading(kanji_reading: str) -> bool: return any(voc for voc in vocab_with_kanji_in_main_form if any(vocab_reading for vocab_reading in voc.readings.get() if reading_in_vocab_reading(kanji, kanji_reading, vocab_reading, voc.get_question())))

        def vocab_has_only_known_kanji(voc: VocabNote) -> bool: return not any(kan for kan in voc.kanji.extract_all_kanji() if kan not in known_kanji)
        def has_vocab_with_reading_and_no_unknown_kanji(kanji_reading: str) -> bool: return any(voc for voc in vocab_with_kanji_in_main_form if reading_is_in_vocab_readings(kanji_reading, voc) and vocab_has_only_known_kanji(voc))

        kanji.tags.toggle(Tags.Kanji.with_vocab_with_primary_on_reading, any(primary_on_readings) and has_vocab_with_reading(primary_on_readings[0]))

        def has_studying_vocab_with_reading(kanji_reading: str) -> bool: return any(voc for voc in studying_reading_vocab if any(vocab_reading for vocab_reading in voc.readings.get() if reading_in_vocab_reading(kanji, kanji_reading, vocab_reading, voc.get_question())))
        kanji.tags.toggle(Tags.Kanji.with_studying_vocab_with_primary_on_reading, any(primary_on_readings) and has_studying_vocab_with_reading(primary_on_readings[0]))
        kanji.tags.toggle(Tags.Kanji.has_studying_vocab_for_each_primary_reading, any(primary_readings) and not any(reading for reading in primary_readings if not has_studying_vocab_with_reading(reading)))
        kanji.tags.toggle(Tags.Kanji.has_primary_reading_with_no_studying_vocab, any(primary_readings) and any(studying_reading_vocab) and any(reading for reading in primary_readings if not has_studying_vocab_with_reading(reading)))
        kanji.tags.toggle(Tags.Kanji.has_non_primary_on_reading_vocab, any(reading for reading in non_primary_on_readings if has_vocab_with_reading(reading)))
        kanji.tags.toggle(Tags.Kanji.has_non_primary_on_reading_vocab_with_only_known_kanji, any(reading for reading in non_primary_on_readings if has_vocab_with_reading_and_no_unknown_kanji(reading)))

        all_readings = kanji.get_readings_clean()

        def vocab_matches_primary_reading(_vocab: VocabNote) -> bool:
            return any(_primary_reading for _primary_reading in primary_readings if any(_vocab_reading for _vocab_reading in _vocab.readings.get() if _primary_reading in _vocab_reading))

        def vocab_matches_reading(_vocab: VocabNote) -> bool:
            return any(_reading for _reading in all_readings if any(_vocab_reading for _vocab_reading in _vocab.readings.get() if _reading in _vocab_reading))

        kanji.tags.toggle(Tags.Kanji.has_studying_vocab_with_no_matching_primary_reading, any(_vocab for _vocab in studying_reading_vocab if (not vocab_matches_primary_reading(_vocab) and vocab_matches_reading(_vocab))))

        kanji.tags.toggle(Tags.Kanji.is_radical, is_radical)
        kanji.tags.toggle(Tags.Kanji.is_radical_purely, is_radical and not any(vocab_with_kanji_in_any_form))
        kanji.tags.toggle(Tags.Kanji.is_radical_silent, is_radical and not any(primary_readings))

    def tag_has_single_kanji_vocab_with_reading_different_from_kanji_primary_reading(kanji: KanjiNote) -> None:
        vocabs = app.col().vocab.with_kanji_in_main_form(kanji)
        single_kanji_vocab = [v for v in vocabs if v.get_question() == kanji.get_question()]
        kanji.tags.toggle(Tags.Kanji.with_single_kanji_vocab, any(single_kanji_vocab))
        if single_kanji_vocab:
            primary_readings: list[str] = primary_reading.findall(f"{kanji.get_reading_on_html()} {kanji.get_reading_kun_html()} {kanji.get_reading_nan_html()}")

            kanji.tags.unset(Tags.Kanji.with_single_kanji_vocab_with_different_reading)
            kanji.tags.unset(Tags.Kanji.with_studying_single_kanji_vocab_with_different_reading)

            for vocab in single_kanji_vocab:
                for reading in vocab.readings.get():
                    if reading not in primary_readings:
                        kanji.tags.set(Tags.Kanji.with_single_kanji_vocab_with_different_reading)
                        if vocab.is_studying(reading):  # todo: Bug: this code looks nuts. You cannot pass a reading to is_studying.
                            kanji.tags.set(Tags.Kanji.with_studying_single_kanji_vocab_with_different_reading)

    with TaskRunner.current("Tagging kanji") as runner:
        all_kanji = app.col().kanji.all()
        runner.process_with_progress(all_kanji, tag_kanji, "Tagging kanji with studying metadata")
        runner.process_with_progress(all_kanji, tag_has_single_kanji_vocab_with_reading_different_from_kanji_primary_reading, "Tagging kanji with single kanji vocab")

def reparse_all_sentences() -> None:
    with TaskRunner.current("Reparse all sentences"):
        reparse_sentences(app.col().sentences.all())

def reading_in_vocab_reading(kanji: KanjiNote, kanji_reading: str, vocab_reading: str, vocab_form: str) -> bool:
    vocab_form = ex_str.strip_html_and_bracket_markup_and_noise_characters(vocab_form)
    if vocab_form.startswith(kanji.get_question()):
        return vocab_reading.startswith(kanji_reading)
    if vocab_form.endswith(kanji.get_question()):
        return vocab_reading.endswith(kanji_reading)
    return kanji_reading in vocab_reading[1:-1]

def reparse_sentences(sentences: list[SentenceNote], run_gc_during_batch: bool = False) -> None:
    def reparse_sentence(sentence: SentenceNote) -> None:
        sentence.update_parsed_words(force=True)

    run_gc_during_batch = run_gc_during_batch and app.config().enable_garbage_collection_during_batches.get_value()
    random.shuffle(sentences)  # hopefully this will get us accurate time estimations by preventing all the long sentenences from turning up last

    with TaskRunner.current("Reparse Sentences", inhibit_gc=run_gc_during_batch) as runner:
        runner.process_with_progress(sentences, reparse_sentence, "Reparsing sentences.", run_gc=run_gc_during_batch, minimum_items_to_gc=500)

def print_gc_status_and_collect() -> None:
    from sysutils import object_instance_tracker
    object_instance_tracker.print_instance_counts()

    app.get_ui_utils().tool_tip(f"Gc.isenabled(): {gc.isenabled()}, Collecting ...", 10000)

    instances = gc.collect()
    app.get_ui_utils().tool_tip(f"collected: {instances} instances", 10000)
    object_instance_tracker.print_instance_counts()

def reparse_sentences_for_vocab(vocab: VocabNote) -> None:
    with TaskRunner.current("Fetching sentences to reparse") as runner:
        query = query_builder.potentially_matching_sentences_for_vocab(vocab)
        sentences: set[SentenceNote] = set(runner.run_on_background_thread_with_spinning_progress_dialog("Fetching sentences to reparse", lambda: app.col().sentences.search(query)))
        # noinspection PyAugmentAssignment
        sentences = sentences | set(vocab.sentences.all())
        reparse_sentences(list(sentences), run_gc_during_batch=True)

def reparse_matching_sentences(question_substring: str) -> None:
    sentences_to_update = app.col().sentences.search(query_builder.sentences_with_question_substring(question_substring))
    reparse_sentences(sentences_to_update, run_gc_during_batch=True)

def create_missing_vocab_with_dictionary_entries() -> None:
    with TaskRunner.current("Creating vocab notes for parsed words with no vocab notes") as runner:
        dictionary_words_with_no_vocab: QList[DictLookupResult] = (
                runner.
                run_on_background_thread_with_spinning_progress_dialog("Fetching parsed words with no vocab notes from parsing results",
                                                                       lambda: (app.col().sentences.all()
                                                                                .select_many(lambda it: it.parsing_result.get()
                                                                                             .parsed_words
                                                                                             .where(lambda word: word.vocab_id == ParsedMatch.missing_note_id)
                                                                                             .select(lambda word: word.parsed_form))
                                                                                .distinct()
                                                                                .select(DictLookup.lookup_word)
                                                                                .where(lambda it: it.found_words())
                                                                                .order_by(lambda it: it.priority_spec().priority)
                                                                                .to_list())))

        def create_vocab_if_not_already_created(result: DictLookupResult) -> None:
            if not any(app.col().vocab.with_form(result.word)):  # we may well have created a vocab that provides this form already...
                VocabNote.factory.create_with_dictionary(result.word)

        runner.process_with_progress(dictionary_words_with_no_vocab, create_vocab_if_not_already_created, "Creating vocab notes")
