# from __future__ import annotations
#
# from typing import TYPE_CHECKING, override
#
# from autoslot import Slots
# from jaspythonutils.sysutils import ex_str
#
# from jaslib.language_services import kana_utils
#
# if TYPE_CHECKING:
#     from jaslib.note.kanjinote import KanjiNote
#
#
# class KanjiViewModel(Slots):
#     def __init__(self, kanji: KanjiNote) -> None:
#         self.kanji: KanjiNote = kanji
#
#     def question(self) -> str: return self.kanji.get_question()
#     def answer(self) -> str: return self.kanji.get_answer()
#     def readings(self) -> str:
#         readings = f"""{kana_utils.hiragana_to_katakana(self.kanji.get_reading_on_html())} <span class="readingsSeparator">|</span> {self.kanji.get_reading_kun_html()}"""
#         if self.kanji.get_reading_nan_html():
#             readings += f""" <span class="readingsSeparator">|</span> {self.kanji.get_reading_nan_html()}"""
#
#         return readings
#
#     def mnemonic(self) -> str:
#         return self.kanji.get_active_mnemonic()
#
#     @override
#     def __str__(self) -> str:
#         return f"{self.question()}      {ex_str.pad_to_length(self.answer(), 60)}: {self.readings()}"
