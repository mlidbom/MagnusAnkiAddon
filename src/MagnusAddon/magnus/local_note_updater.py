from aqt.utils import showInfo

from .utils import StringUtils
from .wani_collection import WaniCollection
from .wanikani_note import *

def prepare_kanji_meaning(kanji: WaniKanjiNote) -> str:
    meaning = kanji.get_kanji_meaning()
    meaning = StringUtils.strip_markup(meaning)
    meaning = meaning.strip().replace(",", "/").replace(" ", "")
    return meaning

def update_kanji_names(all_vocabulary, all_kanji):
    kanji_dict = {kanji.get_kanji(): prepare_kanji_meaning(kanji) for kanji in all_kanji}
    for vocab_note in all_vocabulary:
        kanji_list = StringUtils.extract_characters(vocab_note.get_vocab())
        kanji_list = [item for item in kanji_list if item in kanji_dict]
        kanji_meanings = [kanji_dict[kanji] for kanji in kanji_list]
        kanji_names_string = " # ".join(kanji_meanings)
        vocab_note.set_kanji_name(kanji_names_string)

def update_vocab() -> None:
    all_vocabulary: list[WaniVocabNote] = WaniCollection.fetch_all_vocab_notes()
    all_kanji: list[WaniKanjiNote] = WaniCollection.fetch_all_kanji_notes()

    update_kanji_names(all_vocabulary, all_kanji)