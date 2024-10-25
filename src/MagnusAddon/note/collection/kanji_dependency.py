from __future__ import annotations

from note.kanjinote import KanjiNote
from note.radicalnote import RadicalNote
from sysutils import kana_utils

class KanjiDependency:
    def __init__(self, name: str, character: str, icon_substitute_for_character: str, mnemonic: str, readings: list[str]):
        self.name = name
        self.character = character
        self.icon_substitute_for_character = icon_substitute_for_character
        self.mnemonic = mnemonic
        self.readings = readings

    @staticmethod
    def from_radical(radical: RadicalNote) -> KanjiDependency:
        return KanjiDependency(name=radical.get_answer(),
                               character=radical.get_question(),
                               icon_substitute_for_character=radical.get_radical_icon(),
                               mnemonic=radical.get_active_mnemonic(),
                               readings=[])

    @staticmethod
    def from_kanji(kanji: KanjiNote) -> KanjiDependency:
        return KanjiDependency(name=kanji.get_answer(),
                               character=kanji.get_question(),
                               icon_substitute_for_character="",
                               mnemonic=kanji.get_active_mnemonic(),
                               readings=[kana_utils.to_katakana(reading) for reading in kanji.get_reading_on_list_html()] + kanji.get_reading_kun_list_html())
