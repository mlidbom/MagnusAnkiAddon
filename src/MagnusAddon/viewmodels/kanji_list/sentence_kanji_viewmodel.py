from ankiutils import app
from note.kanjinote import KanjiNote
from sysutils import kana_utils
from sysutils import ex_str


class KanjiViewModel:
    def __init__(self, kanji: KanjiNote):
        self.kanji = kanji

    def question(self) -> str: return self.kanji.get_question()
    def answer(self) -> str: return self.kanji.get_answer()
    def readings(self) -> str:
        readings = f"""{kana_utils.to_katakana(self.kanji.get_reading_on_html())} <span class="readingsSeparator">|</span> {self.kanji.get_reading_kun_html()}"""
        if self.kanji.get_reading_nan_html():
            readings += f""" <span class="readingsSeparator">|</span> {self.kanji.get_reading_nan_html()}"""

        return readings

    def mnemonic(self) -> str:
        return self.kanji.get_active_mnemonic()

    def __str__(self) -> str:
        return f"{self.question()}      {ex_str.pad_to_length(self.answer(), 60)}: {self.readings()}"
