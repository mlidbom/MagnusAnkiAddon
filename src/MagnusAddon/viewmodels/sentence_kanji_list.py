from ankiutils import anki_shim
from note.jp_collection import JPCollection
from note.kanjinote import KanjiNote
from note.sentencenote import SentenceNote


class SentenceKanjiViewModel:
    def __init__(self, kanji: KanjiNote):
        self.kanji = kanji

class SentenceKanjiListViewModel:
    def __init__(self, sentence: str, kanji_list: list[SentenceKanjiViewModel]):
        self.sentence = sentence


def create(sentence: SentenceNote) -> SentenceKanjiListViewModel:
    kanji = sentence.extract_kanji()
    kanji_notes = JPCollection.fetch_kanji_notes()


    return SentenceKanjiListViewModel()