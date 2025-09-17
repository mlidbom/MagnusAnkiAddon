from __future__ import annotations

from typing import TYPE_CHECKING, override

from ex_autoslot import ProfilableAutoSlots
from sysutils import ex_str, kana_utils

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabNoteKanji(ProfilableAutoSlots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.__vocab = vocab

    @property
    def _vocab(self) -> VocabNote: return self.__vocab()

    def extract_main_form_kanji(self) -> list[str]:
        clean = ex_str.strip_html_and_bracket_markup(self._vocab.get_question())
        return [char for char in clean if kana_utils.character_is_kanji(char)]

    def extract_all_kanji(self) -> set[str]:
        clean = ex_str.strip_html_and_bracket_markup(self._vocab.get_question() + self._vocab.forms.all_raw_string())
        return {char for char in clean if kana_utils.character_is_kanji(char)}

    @override
    def __repr__(self) -> str: return f"""main: {self.extract_main_form_kanji()}, all: {self.extract_all_kanji()}"""