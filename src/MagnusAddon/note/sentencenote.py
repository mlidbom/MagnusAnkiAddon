from anki.notes import Note

from note.mynote import MyNote
from sysutils import timeutil, janomeutils
from sysutils.janomeutils import ParsedWord
from wanikani.wani_constants import SentenceNoteFields


class SentenceNote(MyNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_expression(self) -> str: return super().get_field(SentenceNoteFields.Expression)
    def set_expression(self, value: str) -> None: super().set_field(SentenceNoteFields.Expression, value)

    def get_expression__(self) -> str: return super().get_field(SentenceNoteFields.Expression__)
    def set_expression__(self, value: str) -> None: super().set_field(SentenceNoteFields.Expression__, value)

    def get_active_expression(self) -> str:
        return self.get_expression__() or self.get_expression()

    def parse_words_from_expression(self) -> list[ParsedWord]: return janomeutils.extract_dictionary_forms(self.get_active_expression())
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
