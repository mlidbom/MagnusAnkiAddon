from note.jp_collection import JPLegacyCollection
from note.sentencenote import SentenceNote
from viewmodels.kanji_list.kanji_list_viewmodel import KanjiListViewModel
from viewmodels.kanji_list.sentence_kanji_viewmodel import KanjiViewModel


def create(sentence: SentenceNote) -> KanjiListViewModel:
    kanji = sentence.extract_kanji()
    kanji_notes = JPLegacyCollection.fetch_kanji_notes(kanji)
    kanji_viewmodels = [KanjiViewModel(note) for note in kanji_notes]
    return KanjiListViewModel(sentence, kanji_viewmodels)