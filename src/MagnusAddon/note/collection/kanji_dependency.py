from __future__ import annotations

from note.kanjinote import KanjiNote
from note.radicalnote import RadicalNote

class KanjiDependency:
    def __init__(self, name: str, character: str, icon_substitute_for_character: str, mnemonic: str):
        self.name = name
        self.character = character
        self.icon_substitute_for_character = icon_substitute_for_character
        self.mnemonic = mnemonic

    @staticmethod
    def from_radical(radical: RadicalNote) -> KanjiDependency:
        return KanjiDependency(name=radical.get_answer(),
                               character=radical.get_question(),
                               icon_substitute_for_character=radical.get_radical_icon(),
                               mnemonic=radical.get_active_mnemonic())

    @staticmethod
    def from_kanji(kanji: KanjiNote) -> KanjiDependency:
        return KanjiDependency(name=kanji.get_answer(),
                               character=kanji.get_question(),
                               icon_substitute_for_character="",
                               mnemonic=kanji.get_active_mnemonic())
