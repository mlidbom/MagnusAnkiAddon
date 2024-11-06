import re

from anki.notes import NoteId

from ankiutils import app, query_builder
from language_services.janome_ex.tokenizing import janome_ex
from note.jpnote import JPNote
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

        is_radical = any(app.col().kanji.with_radical(kanji.get_question()))
        kanji.toggle_tag(Mine.Tags.kanji_in_vocab_main_form, any(vocab_with_kanji_in_main_form))
        kanji.toggle_tag(Mine.Tags.kanji_in_any_vocab_form, any(vocab_with_kanji_in_any_form))

        studying_reading_vocab = [voc for voc in vocab_with_kanji_in_main_form if voc.is_studying(CardTypes.reading)]
        kanji.toggle_tag(Mine.Tags.kanji_with_studying_vocab, any(studying_reading_vocab))

        primary_readings: list[str] = primary_reading.findall(f"{kanji.get_reading_on_html()} {kanji.get_reading_kun_html()} {kanji.get_reading_nan()}")
        kanji.toggle_tag(Mine.Tags.kanji_with_no_primary_readings, not primary_readings)

        primary_on_readings:list[str] = primary_reading.findall(kanji.get_reading_on_html())
        kanji.toggle_tag(Mine.Tags.kanji_with_no_primary_on_readings, not primary_on_readings)

        def has_vocab_with_reading(kanji_reading: str) -> bool: return any(voc for voc in vocab_with_kanji_in_main_form if any(vocab_reading for vocab_reading in voc.get_readings() if kanji_reading in vocab_reading))
        kanji.toggle_tag(Mine.Tags.kanji_with_vocab_with_primary_on_reading, any(primary_on_readings) and has_vocab_with_reading(primary_on_readings[0]))

        def has_studying_vocab_with_reading(kanji_reading:str) -> bool: return any(voc for voc in studying_reading_vocab if any(vocab_reading for vocab_reading in voc.get_readings() if kanji_reading in vocab_reading))
        kanji.toggle_tag(Mine.Tags.kanji_with_studying_vocab_with_primary_on_reading, any(primary_on_readings) and has_studying_vocab_with_reading(primary_on_readings[0]))
        kanji.toggle_tag(Mine.Tags.kanji_has_studying_vocab_for_each_primary_reading, any(primary_readings) and not any(reading for reading in primary_readings if not has_studying_vocab_with_reading(reading)))
        kanji.toggle_tag(Mine.Tags.kanji_has_primary_reading_with_no_studying_vocab, any(primary_readings) and any(studying_reading_vocab) and any(reading for reading in primary_readings if not has_studying_vocab_with_reading(reading)))

        def vocab_matches_any_reading(_vocab:VocabNote) -> bool:
            return any(_primary_reading for _primary_reading in primary_readings if any(_vocab_reading for _vocab_reading in _vocab.get_readings() if _primary_reading in _vocab_reading))

        kanji.toggle_tag(Mine.Tags.kanji_has_studying_vocab_with_no_matching_primary_reading, any(_vocab for _vocab in studying_reading_vocab if not vocab_matches_any_reading(_vocab)))


        kanji.toggle_tag(Mine.Tags.kanji_is_radical, is_radical)
        kanji.toggle_tag(Mine.Tags.kanji_is_radical_purely, is_radical and not any(vocab_with_kanji_in_any_form))
        kanji.toggle_tag(Mine.Tags.kanji_is_radical_silent, is_radical and not any(primary_readings))

    def tag_has_single_kanji_vocab_with_reading_different_from_kanji_primary_reading(kanji: KanjiNote) -> None:
        vocabs = app.col().vocab.with_kanji_in_main_form(kanji)
        single_kanji_vocab = [v for v in vocabs if v.get_question() == kanji.get_question()]
        kanji.toggle_tag(Mine.Tags.kanji_with_single_kanji_vocab, any(single_kanji_vocab))
        if single_kanji_vocab:
            primary_readings: list[str] = primary_reading.findall(f"{kanji.get_reading_on_html()} {kanji.get_reading_kun_html()} {kanji.get_reading_nan()}")

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

def precache_studying_status() -> None:
    def cache_studying_status(note: JPNote) -> None:
        note.is_studying(CardTypes.reading)
        note.is_studying(CardTypes.listening)

    progress_display_runner.process_with_progress(app.col().kanji.all(), cache_studying_status, "Precaching studying status: Kanji")
    progress_display_runner.process_with_progress(app.col().vocab.all(), cache_studying_status, "Precaching studying status:  Vocabulary")
    progress_display_runner.process_with_progress(app.col().sentences.all(), cache_studying_status, "Precaching studying status: Sentences")

def adjust_kanji_primary_readings() -> None:
    primary_reading_pattern = re.compile(r'<primary>(.*?)</primary>')

    updated_kanji:set[KanjiNote] = set()

    def adjust_kanji_readings(kanji: KanjiNote) -> None:
        def make_on_reading_primary(primary_reading: str) -> None:
            new_reading = ex_str.replace_word(primary_reading, f'<primary>{primary_reading}</primary>', kanji.get_reading_on_html())
            print(f"""{kanji.get_question()}: {new_reading}""")
            #kanji.set_reading_on(new_reading)

        def make_kun_reading_primary(primary_reading: str) -> None:
            new_reading = ex_str.replace_word(primary_reading, f'<primary>{primary_reading}</primary>', kanji.get_reading_kun_html())
            #print(f"""{kanji.get_question()}: {new_reading}""")
            updated_kanji.add(kanji)
            kanji.set_reading_kun(new_reading)

        def has_vocab_with_reading(reading:str) -> bool:
            for vocab in (x for x in kanji.get_vocab_notes() if x.is_studying()):
                if reading in vocab._get_reading():
                    return True
            return False

        kun_primary_readings: set[str] = set(primary_reading_pattern.findall(kanji.get_reading_kun_html()))
        kun_readings_with_vocab = set(reading for reading in kanji.get_readings_kun() if has_vocab_with_reading(reading))

        missing_primary_readings = kun_readings_with_vocab - kun_primary_readings

        for missing_reading in missing_primary_readings:
            make_kun_reading_primary(missing_reading)
            kanji.set_field("_primary_readings_tts_audio", "")


    progress_display_runner.process_with_progress(app.col().kanji.all(), adjust_kanji_readings, "Adjusting kanji readings")
    print(f"""nid:{",".join(str(k.get_id()) for k in updated_kanji) }""")
