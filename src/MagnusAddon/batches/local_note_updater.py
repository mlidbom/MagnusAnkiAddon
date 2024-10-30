import re

from anki.cards import CardId
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

def organize_sentences_by_difficulty() -> None:
    read_sentence_folder_common = "-JP::Read::​​Sent::level-"

    read_deckid_1 = typed.int_(app.anki_collection().decks.id_for_name(f"{read_sentence_folder_common}1"))
    read_deckid_2 = typed.int_(app.anki_collection().decks.id_for_name(f"{read_sentence_folder_common}2"))
    read_deckid_3 = typed.int_(app.anki_collection().decks.id_for_name(f"{read_sentence_folder_common}3"))
    read_deckid_4 = typed.int_(app.anki_collection().decks.id_for_name(f"{read_sentence_folder_common}4"))
    read_deckid_5 = typed.int_(app.anki_collection().decks.id_for_name(f"{read_sentence_folder_common}5"))
    read_deckid_6 = typed.int_(app.anki_collection().decks.id_for_name(f"{read_sentence_folder_common}6-"))

    read_deck_id_by_level = [0, read_deckid_1, read_deckid_2, read_deckid_3, read_deckid_4, read_deckid_5, read_deckid_6, read_deckid_6, read_deckid_6, read_deckid_6]
    read_card_ids_by_level:list[list[CardId]] = [[], [], [], [], [], [], [], [], [], []]

    multiplier = 1.5
    level_1 = 10
    level_2 = level_1 * multiplier
    level_3 = level_2 * multiplier
    level_4 = level_3 * multiplier
    level_5 = level_4 * multiplier
    level_6 = level_5 * multiplier
    level_7 = level_6 * multiplier
    level_8 = level_7 * multiplier

    levels = list(range(1,9))

    def tag_sentence_and_move_cards_to_correct_deck(sentence: SentenceNote) -> None:
        def find_difficulty() -> int:
            kanji_weight = 8
            kanji_count = ex_sequence.count(sentence.get_question(), kana_utils.is_kanji)
            kana_count = len(sentence.get_question()) - kanji_count
            return kana_count + (kanji_count * kanji_weight)

        def find_level() -> int:
            _difficulty = find_difficulty()
            if _difficulty <= level_1: return 1
            elif level_1 < _difficulty <= level_2: return 2
            elif level_2 < _difficulty <= level_3: return 3
            elif level_3 < _difficulty <= level_4: return 4
            elif level_4 < _difficulty <= level_5: return 5
            elif level_5 < _difficulty <= level_6: return 6
            elif level_6 < _difficulty <= level_7: return 7
            elif level_7 < _difficulty <= level_8: return 8
            elif level_8 < _difficulty : return 9
            else: raise Exception("This should never happen")

        sentence_level = find_level()

        for _level in levels:
            sentence.toggle_tag(f"{Mine.Tags.sentence_difficulty_folder}{_level}", sentence_level == _level)
            if _level == sentence_level:
                read_card_ids_by_level[_level].append(sentence.get_reading_card().id)

    def move_level_cards(level:int) -> None:
        app.anki_collection().set_deck(read_card_ids_by_level[level], read_deck_id_by_level[level])

    progress_display_runner.process_with_progress(app.col().sentences.all(), tag_sentence_and_move_cards_to_correct_deck, "Finding levels and tagging sentences")
    progress_display_runner.process_with_progress(levels, move_level_cards, "Moving cards")





