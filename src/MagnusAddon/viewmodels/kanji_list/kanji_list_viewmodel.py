from viewmodels.kanji_list.sentence_kanji_viewmodel import KanjiViewModel


class KanjiListViewModel:
    def __init__(self, kanji_list: list[KanjiViewModel]):
        self.kanji_list = kanji_list

    def __str__(self) -> str: return "\n".join([str(kan) for kan in self.kanji_list])
