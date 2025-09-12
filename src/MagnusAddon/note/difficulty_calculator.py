from __future__ import annotations

from autoslot import Slots
from sysutils import ex_sequence, kana_utils


class DifficultyCalculator(Slots):
    def __init__(self, starting_seconds:float, hiragana_seconds:float, katakata_seconds:float, kanji_seconds:float) -> None:
        self.starting_seconds: float  = starting_seconds
        self.hiragana_seconds: float  = hiragana_seconds
        self.katakata_seconds: float  = katakata_seconds
        self.kanji_seconds: float = kanji_seconds

    @staticmethod
    def is_other_character(char:str) -> bool:
        return not kana_utils.character_is_kana(char) and not kana_utils.character_is_kanji(char)

    def allowed_seconds(self, string:str) -> float:
        hiragana_seconds = ex_sequence.count(string, kana_utils.character_is_hiragana) * self.hiragana_seconds
        katakana_seconds = ex_sequence.count(string, kana_utils.character_is_katakana) * self.katakata_seconds
        kanji_seconds = ex_sequence.count(string, kana_utils.character_is_kanji) * self.kanji_seconds

        other_character_seconds = ex_sequence.count(string, self.is_other_character) * self.hiragana_seconds

        return self.starting_seconds + hiragana_seconds + katakana_seconds + kanji_seconds + other_character_seconds