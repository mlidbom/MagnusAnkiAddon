import re
from typing import Callable

from anki.notes import NoteId

from ankiutils import app, query_builder
from language_services.janome_ex.tokenizing import janome_ex
from note.kanjinote import KanjiNote
from note.note_constants import Mine
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
        studying_vocab = [voc for voc in app.col().vocab.with_kanji(kanji) if voc.is_studying()]
        if not studying_vocab:
            kanji.set_tag(Mine.Tags.kanji_with_no_studying_vocab)
        else:
            kanji.remove_tag(Mine.Tags.kanji_with_no_studying_vocab)

            primary_on_readings:list[str] = primary_reading.findall(kanji.get_reading_on())
            if not primary_on_readings:
                kanji.set_tag(Mine.Tags.kanji_with_no_primary_on_readings)
            else:
                first_primary_on_reading = primary_on_readings[0]
                vocab_with_first_primary_on_reading = [voc for voc in studying_vocab if any(reading for reading in voc.get_readings() if first_primary_on_reading in reading)]
                if not vocab_with_first_primary_on_reading:
                    kanji.set_tag(Mine.Tags.kanji_with_no_studying_vocab_with_primary_on_reading)

    def tag_has_single_kanji_vocab_with_reading_different_from_kanji_primary_reading(kanji: KanjiNote) -> None:
        vocabs = app.col().vocab.with_kanji(kanji)
        single_kanji_vocab = [v for v in vocabs if v.get_question() == kanji.get_question()]
        if single_kanji_vocab:
            kanji.set_tag(Mine.Tags.kanji_with_single_kanji_vocab)
            primary_on_readings: list[str] = primary_reading.findall(kanji.get_reading_on())
            primary_kun_readings: list[str] = primary_reading.findall(kanji.get_reading_kun())
            primary_readings:set[str] = set(primary_on_readings + primary_kun_readings)

            for vocab in single_kanji_vocab:
                for reading in vocab.get_readings():
                    if reading not in primary_readings:
                        kanji.set_tag(Mine.Tags.kanji_with_single_kanji_vocab_with_different_reading)
                        if vocab.is_studying():
                            kanji.set_tag(Mine.Tags.kanji_with_studying_single_kanji_vocab_with_different_reading)




    all_kanji = app.col().kanji.all()
    progress_display_runner.process_with_progress(all_kanji, tag_kanji, "Tagging kanji with studying metadata")
    progress_display_runner.process_with_progress(all_kanji, tag_has_single_kanji_vocab_with_reading_different_from_kanji_primary_reading, "Tagging kanji with single kanji vocab")


# def backup_kanji_readings() -> None:
#     for kanji in app.col().kanji.all():
#         kanji.set_field("_on_backup", kanji.get_field(NoteFields.Kanji.Reading_On))
#         kanji.set_field("_kun_backup", kanji.get_field(NoteFields.Kanji.Reading_Kun))

def adjust_kanji_primary_readings() -> None:
    primary_reading_pattern = re.compile(r'<primary>(.*?)</primary>')

    def find_and_fix_reading(type:str, primary_reading: str, current_readings:str, setter:Callable[[str], None]) -> None:
                new_text = re.sub(rf'\b{re.escape(primary_reading)}\b', f'<primary>{primary_reading}</primary>', current_readings)
                print(f"""{type}:replacing 
{current_readings} with 
{new_text}

""")
                setter(new_text)


    def adjust_kanji_readings(kanji: KanjiNote) -> None:
        vocabs = app.col().vocab.with_kanji(kanji)
        single_kanji_vocab = [v for v in vocabs if v.get_question() == kanji.get_question()]
        if single_kanji_vocab:
            primary_on_readings: list[str] = primary_reading_pattern.findall(kanji.get_reading_on())
            primary_kun_readings: list[str] = primary_reading_pattern.findall(kanji.get_reading_kun())
            primary_readings: set[str] = set(primary_on_readings + primary_kun_readings)

            for vocab in single_kanji_vocab:
                for reading in vocab.get_readings():
                    if reading not in primary_readings:
                        kanji.set_field("_primary_readings_tts_audio", "")
                        kanji.set_tag("fixed_primary_readings")
                        if reading in kanji.get_reading_on_list():
                            find_and_fix_reading("ON", reading, kanji.get_reading_on(), kanji.set_reading_on)
                        elif reading in kanji.get_reading_kun_list():
                            find_and_fix_reading("KUN", reading, kanji.get_reading_kun(), kanji.set_reading_kun)
                        elif reading in kanji.get_reading_nan_list():
                            find_and_fix_reading("NAN", reading, kanji.get_reading_nan(), kanji.set_reading_nan)
                        else:
                            print(f"{kanji.get_question()}:WTF:{reading} #####################################################################################")


    progress_display_runner.process_with_progress(app.col().kanji.all(), adjust_kanji_readings, "Adjusting kanji readings")

def remove_kun_readings_html() -> None:
    for kanji in app.col().kanji.all():
        kanji.set_reading_kun(ex_str.strip_html_markup(kanji.get_reading_kun()))