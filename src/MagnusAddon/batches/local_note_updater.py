import re

from anki.notes import NoteId

from ankiutils import app, query_builder
from note.kanjinote import KanjiNote
from note.note_constants import CardTypes, Mine
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote

from sysutils import ex_str, progress_display_runner

def update_all() -> None:
    update_sentences()
    update_kanji()
    update_vocab()
    #update_vocab_parsed_parts_of_speech()


def update_sentences() -> None:
    def update_sentence(sentence: SentenceNote) -> None:
        sentence.update_generated_data()

    progress_display_runner.process_with_progress(app.col().sentences.all(), update_sentence, "Updating sentences")


def update_kanji() -> None:
    def _update_kanji(kanji: KanjiNote) -> None:
        kanji.update_generated_data()

    progress_display_runner.process_with_progress(app.col().kanji.all(), _update_kanji, "Updating kanji")

def update_vocab() -> None:
    def _update_vocab(vocab: VocabNote) -> None:
        vocab.update_generated_data()

    progress_display_runner.process_with_progress(app.col().vocab.all(), _update_vocab, "Updating vocab")


def generate_sentences_for_context_sentences_with_audio() -> None:
    def generate_sentences(vocab: VocabNote) -> None:
        vocab.generate_sentences_from_context_sentences(require_audio=True)

    progress_display_runner.process_with_progress(app.col().vocab.all(), generate_sentences, "Generating sentence notes from context sentences")

def convert_immersion_kit_sentences() -> None:
    def convert_note(note_id: NoteId) -> None:
        immersion_kit_note = app.anki_collection().get_note(note_id)
        SentenceNote.import_immersion_kit_sentence(immersion_kit_note)
        app.anki_collection().remove_notes([note_id])

    immersion_kit_sences = list(app.anki_collection().find_notes(query_builder.immersion_kit_sentences()))
    progress_display_runner.process_with_progress(immersion_kit_sences, convert_note, "Converting immersion kit sentences")

def tag_note_metadata() -> None:
    tag_kanji_metadata()
    tag_vocab_metadata()

def tag_vocab_metadata() -> None:
    def tag_note(vocab:VocabNote) -> None:
        vocab.toggle_tag(Mine.Tags.vocab_has_no_studying_sentences, not any(vocab.get_sentences_studying()))

    progress_display_runner.process_with_progress(app.col().vocab.all(), tag_note, "Tag vocab notes")

def tag_kanji_metadata() -> None:
    primary_reading = re.compile(r'<primary>(.*?)</primary>')

    known_kanji = {kanji.get_question() for kanji in app.col().kanji.all() if kanji.is_studying()}

    def tag_kanji(kanji: KanjiNote) -> None:
        vocab_with_kanji_in_main_form = app.col().vocab.with_kanji_in_main_form(kanji)
        vocab_with_kanji_in_any_form = app.col().vocab.with_kanji_in_any_form(kanji)

        is_radical = any(app.col().kanji.with_radical(kanji.get_question()))
        kanji.toggle_tag(Mine.Tags.kanji_in_vocab_main_form, any(vocab_with_kanji_in_main_form))
        kanji.toggle_tag(Mine.Tags.kanji_in_any_vocab_form, any(vocab_with_kanji_in_any_form))

        studying_reading_vocab = [voc for voc in vocab_with_kanji_in_main_form if voc.is_studying(CardTypes.reading)]
        kanji.toggle_tag(Mine.Tags.kanji_with_studying_vocab, any(studying_reading_vocab))

        primary_readings: list[str] = primary_reading.findall(f"{kanji.get_reading_on_html()} {kanji.get_reading_kun_html()} {kanji.get_reading_nan_html()}")
        kanji.toggle_tag(Mine.Tags.kanji_with_no_primary_readings, not primary_readings)

        primary_on_readings:list[str] = primary_reading.findall(kanji.get_reading_on_html())
        non_primary_on_readings:list[str] = [reading for reading in kanji.get_readings_on() if reading not in primary_readings]

        kanji.toggle_tag(Mine.Tags.kanji_with_no_primary_on_readings, not primary_on_readings)

        def reading_is_in_vocab_readings(kanji_reading: str, voc:VocabNote) -> bool: return any(vocab_reading for vocab_reading in voc.get_readings() if reading_in_vocab_reading(kanji, kanji_reading, vocab_reading, voc.get_question()))
        def has_vocab_with_reading(kanji_reading: str) -> bool: return any(voc for voc in vocab_with_kanji_in_main_form if any(vocab_reading for vocab_reading in voc.get_readings() if reading_in_vocab_reading(kanji, kanji_reading, vocab_reading, voc.get_question())))

        def vocab_has_only_known_kanji(voc:VocabNote) -> bool: return not any(kan for kan in voc.extract_all_kanji() if kan not in known_kanji)
        def has_vocab_with_reading_and_no_unknown_kanji(kanji_reading: str) -> bool: return any(voc for voc in vocab_with_kanji_in_main_form if reading_is_in_vocab_readings(kanji_reading, voc) and vocab_has_only_known_kanji(voc))

        kanji.toggle_tag(Mine.Tags.kanji_with_vocab_with_primary_on_reading, any(primary_on_readings) and has_vocab_with_reading(primary_on_readings[0]))

        def has_studying_vocab_with_reading(kanji_reading:str) -> bool: return any(voc for voc in studying_reading_vocab if any(vocab_reading for vocab_reading in voc.get_readings() if reading_in_vocab_reading(kanji, kanji_reading, vocab_reading, voc.get_question())))
        kanji.toggle_tag(Mine.Tags.kanji_with_studying_vocab_with_primary_on_reading, any(primary_on_readings) and has_studying_vocab_with_reading(primary_on_readings[0]))
        kanji.toggle_tag(Mine.Tags.kanji_has_studying_vocab_for_each_primary_reading, any(primary_readings) and not any(reading for reading in primary_readings if not has_studying_vocab_with_reading(reading)))
        kanji.toggle_tag(Mine.Tags.kanji_has_primary_reading_with_no_studying_vocab, any(primary_readings) and any(studying_reading_vocab) and any(reading for reading in primary_readings if not has_studying_vocab_with_reading(reading)))
        kanji.toggle_tag(Mine.Tags.kanji_has_non_primary_on_reading_vocab, any(reading for reading in non_primary_on_readings if has_vocab_with_reading(reading)))
        kanji.toggle_tag(Mine.Tags.kanji_has_non_primary_on_reading_vocab_with_only_known_kanji, any(reading for reading in non_primary_on_readings if has_vocab_with_reading_and_no_unknown_kanji(reading)))

        all_readings = kanji.get_readings_clean()

        def vocab_matches_primary_reading(_vocab:VocabNote) -> bool:
            return any(_primary_reading for _primary_reading in primary_readings if any(_vocab_reading for _vocab_reading in _vocab.get_readings() if _primary_reading in _vocab_reading))

        def vocab_matches_reading(_vocab:VocabNote) -> bool:
            return any(_reading for _reading in all_readings if any(_vocab_reading for _vocab_reading in _vocab.get_readings() if _reading in _vocab_reading))

        kanji.toggle_tag(Mine.Tags.kanji_has_studying_vocab_with_no_matching_primary_reading, any(_vocab for _vocab in studying_reading_vocab if (not vocab_matches_primary_reading(_vocab) and vocab_matches_reading(_vocab))))


        kanji.toggle_tag(Mine.Tags.kanji_is_radical, is_radical)
        kanji.toggle_tag(Mine.Tags.kanji_is_radical_purely, is_radical and not any(vocab_with_kanji_in_any_form))
        kanji.toggle_tag(Mine.Tags.kanji_is_radical_silent, is_radical and not any(primary_readings))

    def tag_has_single_kanji_vocab_with_reading_different_from_kanji_primary_reading(kanji: KanjiNote) -> None:
        vocabs = app.col().vocab.with_kanji_in_main_form(kanji)
        single_kanji_vocab = [v for v in vocabs if v.get_question() == kanji.get_question()]
        kanji.toggle_tag(Mine.Tags.kanji_with_single_kanji_vocab, any(single_kanji_vocab))
        if single_kanji_vocab:
            primary_readings: list[str] = primary_reading.findall(f"{kanji.get_reading_on_html()} {kanji.get_reading_kun_html()} {kanji.get_reading_nan_html()}")

            kanji.remove_tag(Mine.Tags.kanji_with_single_kanji_vocab_with_different_reading)
            kanji.remove_tag(Mine.Tags.kanji_with_studying_single_kanji_vocab_with_different_reading)

            for vocab in single_kanji_vocab:
                for reading in vocab.get_readings():
                    if reading not in primary_readings:
                        kanji.set_tag(Mine.Tags.kanji_with_single_kanji_vocab_with_different_reading)
                        if vocab.is_studying(reading):
                            kanji.set_tag(Mine.Tags.kanji_with_studying_single_kanji_vocab_with_different_reading)

    all_kanji = app.col().kanji.all()
    progress_display_runner.process_with_progress(all_kanji, tag_kanji, "Tagging kanji with studying metadata")
    progress_display_runner.process_with_progress(all_kanji, tag_has_single_kanji_vocab_with_reading_different_from_kanji_primary_reading, "Tagging kanji with single kanji vocab")

def reparse_sentence_words() -> None:
    def reparse_sentence(sentence: SentenceNote) -> None:
        sentence.update_parsed_words(force=True)

    progress_display_runner.process_with_progress(app.col().sentences.all(), reparse_sentence, "Reparsing sentences.")

def reading_in_vocab_reading(kanji:KanjiNote, kanji_reading: str, vocab_reading: str, vocab_form: str) -> bool:
    vocab_form = ex_str.strip_html_and_bracket_markup_and_noise_characters(vocab_form)
    if vocab_form.startswith(kanji.get_question()):
        return vocab_reading.startswith(kanji_reading)
    elif vocab_form.endswith(kanji.get_question()):
        return vocab_reading.endswith(kanji_reading)
    else:
        return kanji_reading in vocab_reading[1:-1]