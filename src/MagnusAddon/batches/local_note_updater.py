import re

from anki.notes import NoteId

from ankiutils import app, query_builder
from language_services.janome_ex.tokenizing import janome_ex
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.note_constants import CardTypes, Mine
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote

from sysutils import ex_sequence, ex_str, kana_utils, progress_display_runner, typed

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

        primary_readings: list[str] = primary_reading.findall(f"{kanji.get_reading_on_html()} {kanji.get_reading_kun_html()} {kanji.get_reading_nan()}")
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
    def reparse_sentence(sentence: SentenceNote) ->None:
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
            for vocab in (x for x in kanji.get_vocab_notes() if x.is_studying()) :
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

def tag_sentence_metadata() -> None:
    def tag_sentence(sentence: SentenceNote) -> None:
        def find_difficulty() -> int:
            kanji_weight = 8
            kanji_count = ex_sequence.count(sentence.get_question(), kana_utils.is_kanji)
            kana_count = len(sentence.get_question()) - kanji_count
            return kana_count + (kanji_count * kanji_weight)

        multiplier = 1.5
        level_1 = 10
        level_2 = level_1 * multiplier
        level_3 = level_2 * multiplier
        level_4 = level_3 * multiplier
        level_5 = level_4 * multiplier
        level_6 = level_5 * multiplier
        level_7 = level_6 * multiplier
        level_8 = level_7 * multiplier

        difficulty = find_difficulty()

        sentence.toggle_tag(Mine.Tags.sentence_difficulty_1, difficulty <= level_1)
        sentence.toggle_tag(Mine.Tags.sentence_difficulty_2, level_1 < difficulty <= level_2)
        sentence.toggle_tag(Mine.Tags.sentence_difficulty_3, level_2 < difficulty <= level_3)
        sentence.toggle_tag(Mine.Tags.sentence_difficulty_4, level_3 < difficulty <= level_4)
        sentence.toggle_tag(Mine.Tags.sentence_difficulty_5, level_4 < difficulty <= level_5)
        sentence.toggle_tag(Mine.Tags.sentence_difficulty_6, level_5 < difficulty <= level_6)
        sentence.toggle_tag(Mine.Tags.sentence_difficulty_7, level_6 < difficulty <= level_7)
        sentence.toggle_tag(Mine.Tags.sentence_difficulty_8, level_7 < difficulty <= level_8)
        sentence.toggle_tag(Mine.Tags.sentence_difficulty_9, level_8 < difficulty)

        
    progress_display_runner.process_with_progress(app.col().sentences.all(), tag_sentence, "Tagging sentences")

def place_sentence_cards_in_difficulty_deck() -> None:
    read_sentence_folder_common = "-JP::Read::​​Sent::level-"

    read_deckid_1 = typed.int_(app.anki_collection().decks.id_for_name(f"{read_sentence_folder_common}1"))
    read_deckid_2 = typed.int_(app.anki_collection().decks.id_for_name(f"{read_sentence_folder_common}2"))
    read_deckid_3 = typed.int_(app.anki_collection().decks.id_for_name(f"{read_sentence_folder_common}3"))
    read_deckid_4 = typed.int_(app.anki_collection().decks.id_for_name(f"{read_sentence_folder_common}4"))
    read_deckid_5 = typed.int_(app.anki_collection().decks.id_for_name(f"{read_sentence_folder_common}5"))
    read_deckid_6 = typed.int_(app.anki_collection().decks.id_for_name(f"{read_sentence_folder_common}6-"))

    read_level_1_cards = [sent.get_reading_card().id for sent in app.col().sentences.all() if sent.has_tag(Mine.Tags.sentence_difficulty_1)]
    read_level_2_cards = [sent.get_reading_card().id for sent in app.col().sentences.all() if sent.has_tag(Mine.Tags.sentence_difficulty_2)]
    read_level_3_cards = [sent.get_reading_card().id for sent in app.col().sentences.all() if sent.has_tag(Mine.Tags.sentence_difficulty_3)]
    read_level_4_cards = [sent.get_reading_card().id for sent in app.col().sentences.all() if sent.has_tag(Mine.Tags.sentence_difficulty_4)]
    read_level_5_cards = [sent.get_reading_card().id for sent in app.col().sentences.all() if sent.has_tag(Mine.Tags.sentence_difficulty_5)]
    read_level_6_cards = [sent.get_reading_card().id for sent in app.col().sentences.all() if sent.has_tag(Mine.Tags.sentence_difficulty_6) or sent.has_tag(Mine.Tags.sentence_difficulty_7) or sent.has_tag(Mine.Tags.sentence_difficulty_8) or sent.has_tag(Mine.Tags.sentence_difficulty_9)]

    app.anki_collection().set_deck(read_level_1_cards, read_deckid_1)
    app.anki_collection().set_deck(read_level_2_cards, read_deckid_2)
    app.anki_collection().set_deck(read_level_3_cards, read_deckid_3)
    app.anki_collection().set_deck(read_level_4_cards, read_deckid_4)
    app.anki_collection().set_deck(read_level_5_cards, read_deckid_5)
    app.anki_collection().set_deck(read_level_6_cards, read_deckid_6)





