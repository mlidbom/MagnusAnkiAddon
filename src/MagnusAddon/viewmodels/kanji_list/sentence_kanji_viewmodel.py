from note.kanjinote import KanjiNote
from sysutils import kana_utils
from sysutils.stringutils import StringUtils


class KanjiViewModel:
    def __init__(self, kanji: KanjiNote):
        self._kanji = kanji

    def question(self) -> str: return self._kanji.get_question()
    def answer(self) -> str: return self._kanji.get_active_answer()
    def readings(self) -> str:
        return f"{self._kanji.get_reading_kun()}, {kana_utils.to_katakana(self._kanji.get_reading_on())}"

    def mnemonic(self) -> str:
        return self._kanji.get_mnemonics_override() if self._kanji.get_mnemonics_override() not in {"-", ""} else ""

    def __str__(self) -> str:
        return f"{self.question()}      {StringUtils.pad_to_length(self.answer(), 60)}: {self.readings()}"
