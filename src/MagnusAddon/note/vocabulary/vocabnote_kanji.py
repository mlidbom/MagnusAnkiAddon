from __future__ import annotations

from typing import TYPE_CHECKING

from sysutils import ex_str, kana_utils

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote

class VocabNoteKanji:
    def __init__(self, vocab: VocabNote) -> None:
        self._vocab = vocab

    def extract_main_form_kanji(self) -> list[str]:
        clean = ex_str.strip_html_and_bracket_markup(self._vocab.get_question())
        return [char for char in clean if kana_utils.character_is_kanji(char)]

    def extract_all_kanji(self) -> set[str]:
        clean = ex_str.strip_html_and_bracket_markup(self._vocab.get_question() + self._vocab.forms.all_raw_string())
        return set(char for char in clean if kana_utils.character_is_kanji(char))