from anki.notes import Note

from note.mynote import MyNote
from parsing.janome_extensions.parsed_word import ParsedWord
from sysutils import timeutil, kana_utils
from parsing import textparser
from sysutils.utils import StringUtils
from wanikani.wani_constants import SentenceNoteFields


class SentenceNote(MyNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_q(self) -> str: return super().get_field(SentenceNoteFields.Q)
    def set_q(self, value: str) -> None: super().set_field(SentenceNoteFields.Q, value)

    def _get_q__(self) -> str: return super().get_field(SentenceNoteFields.Q__)
    def get_active_q(self) -> str:
        return self._get_q__() or self.get_q()

    def parse_words_from_expression(self) -> list[ParsedWord]: return textparser.identify_words(self.get_active_q())
    def _set_parsed_words(self, value: list[str]) -> None:
        value.append(str(timeutil.one_second_from_now()))
        super().set_field(SentenceNoteFields.ParsedWords, ",".join(value))

    def _parsed_words_timestamp(self) -> int:
        words = super().get_field(SentenceNoteFields.ParsedWords).split(",")
        return int(words[-1]) if words and words[-1].isdigit() else 0

    def _needs_words_reparsed(self) -> bool: return self._note.mod > self._parsed_words_timestamp()

    def update_parsed_words(self) -> None:
        if self._needs_words_reparsed():
            self._set_parsed_words([word.word for word in self.parse_words_from_expression()])

    def extract_kanji(self) -> list[str]:
        clean = StringUtils.strip_markup(self.get_q())
        return [char for char in clean if not kana_utils.is_kana(char)]
