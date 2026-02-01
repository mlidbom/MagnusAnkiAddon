from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from jastudio.viewmodels.kanji_list.sentence_kanji_viewmodel import KanjiViewModel


class KanjiListViewModel(Slots):
    def __init__(self, kanji_list: list[KanjiViewModel]) -> None:
        self.kanji_list: list[KanjiViewModel] = kanji_list

    @override
    def __str__(self) -> str: return "\n".join([str(kan) for kan in self.kanji_list])
