from ankiutils import app
from viewmodels.kanji_list.kanji_list_viewmodel import KanjiListViewModel
from viewmodels.kanji_list.sentence_kanji_viewmodel import KanjiViewModel


def create(kanji: list[str]) -> KanjiListViewModel:
    kanji_notes = app.col().fetch_kanji_notes(kanji)
    kanji_viewmodels = [KanjiViewModel(note) for note in kanji_notes]
    return KanjiListViewModel(kanji_viewmodels)