from __future__ import annotations

from autoslot import Slots
from sysutils import ex_sequence, kana_utils


class DifficultyCalculator(Slots):
    def __init__(self, starting_seconds:float, hiragana_seconds:float, katakata_seconds:float, kanji_seconds:float) -> None:
        self.starting_seconds = starting_seconds
        self.hiragana_seconds = hiragana_seconds
        self.katakata_seconds = katakata_seconds
        self.kanji_seconds = kanji_seconds

    def allowed_seconds(self, string:str) -> float:
        hiragana_seconds = ex_sequence.count(string, kana_utils.character_is_hiragana) * self.hiragana_seconds
        katakana_seconds = ex_sequence.count(string, kana_utils.character_is_katakana) * self.katakata_seconds
        kanji_seconds = ex_sequence.count(string, kana_utils.character_is_kanji) * self.kanji_seconds

        return self.starting_seconds + hiragana_seconds + katakana_seconds + kanji_seconds