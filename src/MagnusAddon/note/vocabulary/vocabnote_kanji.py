from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from sysutils import ex_str, kana_utils
from typed_linq_collections.collections.q_set import QSet
from typed_linq_collections.q_iterable import query

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef
    from typed_linq_collections.collections.q_list import QList

class VocabNoteKanji(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.__vocab = vocab

    @property
    def _vocab(self) -> VocabNote: return self.__vocab()

    def extract_main_form_kanji(self) -> QList[str]:
        clean = ex_str.strip_html_and_bracket_markup(self._vocab.get_question())
        return query(clean).where(kana_utils.character_is_kanji).to_list() #[char for char in clean if kana_utils.character_is_kanji(char)]

    def extract_all_kanji(self) -> QSet[str]:
        clean = ex_str.strip_html_and_bracket_markup(self._vocab.get_question() + self._vocab.forms.all_raw_string())
        return QSet(char for char in clean if kana_utils.character_is_kanji(char))

    @override
    def __repr__(self) -> str: return f"""main: {self.extract_main_form_kanji()}, all: {self.extract_all_kanji()}"""