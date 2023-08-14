from anki.notes import Note

from note.mynote import MyNote
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

    def get_parsed_words(self) -> str: return super().get_field(SentenceNoteFields.ParsedWords)
    def set_parsed_words(self, value: str) -> None: super().set_field(SentenceNoteFields.ParsedWords, value)
