from note.jp_collection import JPLegacyCollection
from note.kanjinote import KanjiNote
from note.sentencenote import SentenceNote
from sysutils import kana_utils


class SentenceKanjiViewModel:
    def __init__(self, kanji: KanjiNote):
        self.kanji = kanji

    def question(self) -> str: return self.kanji.get_question()
    def answer(self) -> str: return self.kanji.get_active_answer()
    def readings(self) -> str:
        return f"{self.kanji.get_reading_kun()}, {kana_utils.to_katakana(self.kanji.get_reading_on())}"

    def mnemonic(self) -> str:
        return self.kanji.get_mnemonics_override() if self.kanji.get_mnemonics_override() not in {"-", ""} else ""

class SentenceKanjiListViewModel:
    def __init__(self, sentence: SentenceNote, kanji_list: list[SentenceKanjiViewModel]):
        self.sentence = sentence
        self.kanji_list = kanji_list


def create(sentence: SentenceNote) -> SentenceKanjiListViewModel:
    kanji = sentence.extract_kanji()
    kanji_notes = JPLegacyCollection.fetch_kanji_notes(kanji)
    kanji_viewmodels = [SentenceKanjiViewModel(note) for note in kanji_notes]
    return SentenceKanjiListViewModel(sentence, kanji_viewmodels)