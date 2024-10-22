import re

from anki.notes import NoteId

from ankiutils import app, query_builder
from language_services.janome_ex.tokenizing import janome_ex
from note.kanjinote import KanjiNote
from note.note_constants import Mine
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote

from sysutils import progress_display_runner

def update_all() -> None:
    update_sentences()
    update_kanji()
    update_vocab()
    #update_vocab_parsed_parts_of_speech()


#todo: I don't think this is reliable at the moment. Review it.
def update_vocab_parsed_parts_of_speech() -> None:
    def update(vocab: VocabNote) -> None:
        vocab.set_parsed_type_of_speech(janome_ex.get_word_parts_of_speech(vocab.get_question()))

    progress_display_runner.process_with_progress(app.col().vocab.all(), update, "Update vocab parsed parts of speech")

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

def tag_kanji_metadata() -> None:
    primary_reading = re.compile(r'<primary>(.*?)</primary>')

    def tag_kanji(kanji: KanjiNote) -> None:
        vocab_with_kanji_in_main_form = app.col().vocab.with_kanji_in_main_form(kanji)
        vocab_with_kanji_in_any_form = app.col().vocab.with_kanji_in_any_form(kanji)

        kanji_with_this_kanji_as_a_radical = app.col().kanji.with_radical(kanji.get_question())
        kanji.toggle_tag(Mine.Tags.kanji_not_in_any_vocab_main_form, bool(not vocab_with_kanji_in_main_form and kanji_with_this_kanji_as_a_radical))
        kanji.toggle_tag(Mine.Tags.kanji_not_in_any_vocab_form, bool(not vocab_with_kanji_in_any_form and kanji_with_this_kanji_as_a_radical))

        studying_vocab = [voc for voc in vocab_with_kanji_in_main_form if voc.is_studying()]
        kanji.toggle_tag(Mine.Tags.kanji_with_no_studying_vocab, not studying_vocab)

        primary_readings: list[str] = primary_reading.findall(f"{kanji.get_reading_on_html()} {kanji.get_reading_kun()} {kanji.get_reading_nan()}")
        kanji.toggle_tag(Mine.Tags.kanji_with_no_primary_readings, not primary_readings)

        primary_on_readings:list[str] = primary_reading.findall(kanji.get_reading_on_html())
        kanji.toggle_tag(Mine.Tags.kanji_with_no_primary_on_readings, not primary_on_readings)
        if primary_on_readings:
            first_primary_on_reading = primary_on_readings[0]
            vocab_with_first_primary_on_reading = [voc for voc in studying_vocab if any(reading for reading in voc.get_readings() if first_primary_on_reading in reading)]
            kanji.toggle_tag(Mine.Tags.kanji_with_no_studying_vocab_with_primary_on_reading, not vocab_with_first_primary_on_reading)


        kanji.toggle_tag(Mine.Tags.kanji_is_radical, any(app.col().kanji.with_radical(kanji.get_question())))
        kanji.toggle_tag(Mine.Tags.kanji_is_radical_purely, not any(vocab_with_kanji_in_any_form) and any(app.col().kanji.with_radical(kanji.get_question())))
        kanji.toggle_tag(Mine.Tags.kanji_is_radical_silent, not any(primary_readings) and any(app.col().kanji.with_radical(kanji.get_question())))






    def tag_has_single_kanji_vocab_with_reading_different_from_kanji_primary_reading(kanji: KanjiNote) -> None:
        vocabs = app.col().vocab.with_kanji_in_main_form(kanji)
        single_kanji_vocab = [v for v in vocabs if v.get_question() == kanji.get_question()]
        if single_kanji_vocab:
            kanji.set_tag(Mine.Tags.kanji_with_single_kanji_vocab)
            primary_readings: list[str] = primary_reading.findall(f"{kanji.get_reading_on_html()} {kanji.get_reading_kun()} {kanji.get_reading_nan()}")

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
    def reparse_sentence(sentence: SentenceNote) ->None:
        sentence.update_parsed_words(force=True)

    progress_display_runner.process_with_progress(app.col().sentences.all(), reparse_sentence, "Reparsing sentences.")