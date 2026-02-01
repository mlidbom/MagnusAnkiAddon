from __future__ import annotations

import random
from typing import TYPE_CHECKING

from ankiutils import app
from language_services.janome_ex.tokenizing.pre_processing_stage.ichidan_godan_potential_or_imperative_hybrid_splitter import IchidanGodanPotentialOrImperativeHybridSplitter
from note.tags import Tags
from qt_utils.task_progress_runner import TaskRunner
from sysutils import ex_str

if TYPE_CHECKING:
    from note.kanjinote import KanjiNote
    from note.sentences.sentencenote import SentenceNote
    from note.vocabulary.vocabnote import VocabNote

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

def tag_note_metadata() -> None:
    with TaskRunner.current("Tagging notes"):
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
        vocab.tags.toggle(Tags.Vocab.Matching.Uses.required_prefix, not vocab.matching_configuration.configurable_rules.required_prefix.none())
        vocab.tags.toggle(Tags.Vocab.Matching.Uses.prefix_is_not, not vocab.matching_configuration.configurable_rules.prefix_is_not.none())
        vocab.tags.toggle(Tags.Vocab.Matching.Uses.suffix_is_not, not vocab.matching_configuration.configurable_rules.suffix_is_not.none())
        vocab.tags.toggle(Tags.Vocab.Matching.Uses.surface_is_not, not vocab.matching_configuration.configurable_rules.surface_is_not.none())
        vocab.tags.toggle(Tags.Vocab.is_ichidan_hiding_godan_potential, IchidanGodanPotentialOrImperativeHybridSplitter.is_ichidan_hiding_godan(vocab))

    with TaskRunner.current("Tagging vocab") as runner:
        runner.process_with_progress(app.col().vocab.all(), tag_note, "Tag vocab notes")


def reparse_all_sentences() -> None:
    with TaskRunner.current("Reparse all sentences"):
        reparse_sentences(app.col().sentences.all())

# noinspection PyUnusedFunction
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


# noinspection PyUnusedFunction
def regenerate_jamdict_vocab_answers() -> None:
    with TaskRunner.current("Regenerating vocab source answers from jamdict") as runner:
        vocab_notes: list[VocabNote] = list(app.col().vocab.all())
        runner.process_with_progress(vocab_notes, lambda vocab: vocab.generate_and_set_answer(), "Regenerating vocab source answers from jamdict")
