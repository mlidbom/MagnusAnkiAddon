from __future__ import annotations

from ankiutils import app
from jaslib.viewmodels.kanji_list.kanji_list_viewmodel import KanjiListViewModel
from jaslib.viewmodels.kanji_list.sentence_kanji_viewmodel import KanjiViewModel


def create(kanji: list[str]) -> KanjiListViewModel:
    kanji_notes = app.col().kanji.with_any_kanji_in(kanji)
    kanji_viewmodels = [KanjiViewModel(note) for note in kanji_notes]
    return KanjiListViewModel(kanji_viewmodels)