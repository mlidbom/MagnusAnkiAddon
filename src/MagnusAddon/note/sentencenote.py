from __future__ import annotations

from ankiutils import app
from note.jpnote import JPNote
from parsing.janome_extensions.parsed_word import ParsedWord
from sysutils import timeutil, kana_utils
from parsing import textparser
from sysutils.stringutils import StringUtils
from note.note_constants import SentenceNoteFields, NoteTypes
from anki.notes import Note


class SentenceNote(JPNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def _on_edited(self) -> None: self.update_generated_data()

    def _get_source_answer(self) -> str: return super().get_field(SentenceNoteFields.source_answer)
    def _get_user_answer(self) -> str: return super().get_field(SentenceNoteFields.user_answer)
    def get_active_answer(self) -> str: return self._get_user_answer() or self._get_source_answer()
    def _set_user_answer(self, question: str) -> None: return super().set_field(SentenceNoteFields.user_answer, question)

    def _get_source_question(self) -> str: return StringUtils.strip_html_markup(super().get_field(SentenceNoteFields.source_question))
    def _set_source_question(self, question: str) -> None: return super().set_field(SentenceNoteFields.source_question, question)


    def _get_user_question(self) -> str: return StringUtils.strip_html_markup(super().get_field(SentenceNoteFields.user_question))
    def get_active_question(self) -> str: return self._get_user_question() or self._get_source_question()

    def get_user_extra_vocab(self) -> list[str]: return StringUtils.extract_comma_separated_values(super().get_field(SentenceNoteFields.user_extra_vocab))
    def _set_user_extra_vocab(self, extra: list[str]) -> None: return super().set_field(SentenceNoteFields.user_extra_vocab, ",".join(extra))

    def get_user_excluded_vocab(self) -> set[str]: return set(StringUtils.extract_comma_separated_values(super().get_field(SentenceNoteFields.user_excluded_vocab)))

    def add_extra_vocab(self, vocab:str) -> None:
        self._set_user_extra_vocab(self.get_user_extra_vocab() + [vocab.strip()])


    def exclude_vocab(self, vocab:str) -> None:
        excluded = self.get_user_excluded_vocab()
        excluded.add(vocab.strip())
        self._set_user_excluded_vocab(excluded)

    def _set_user_excluded_vocab(self, excluded: set[str]) -> None:
        super().set_field(SentenceNoteFields.user_excluded_vocab, ",".join(excluded))

    def set_break_down(self, value: str) -> None: super().set_field(SentenceNoteFields.break_down, value)


    def parse_words_from_expression(self) -> list[ParsedWord]: return textparser.identify_words(self.get_active_question())
    def get_parsed_words(self) -> list[str]: return super().get_field(SentenceNoteFields.ParsedWords).split(",")
    def _set_parsed_words(self, value: list[str]) -> None:
        value.append(str(timeutil.one_second_from_now()))
        super().set_field(SentenceNoteFields.ParsedWords, ",".join(value))

    def _parsed_words_timestamp(self) -> int:
        words = self.get_parsed_words()
        return int(words[-1]) if words and words[-1].isdigit() else 0

    def _needs_words_reparsed(self) -> bool: return self._note.mod > self._parsed_words_timestamp()

    def update_generated_data(self) -> None:
        self._update_parsed_words()
        super().set_field(SentenceNoteFields.active_answer, self.get_active_answer())
        super().set_field(SentenceNoteFields.active_question, self.get_active_question())

    def _update_parsed_words(self) -> None:
        if self._needs_words_reparsed():
            self._set_parsed_words([word.word for word in self.parse_words_from_expression()])

    def extract_kanji(self) -> list[str]:
        clean = StringUtils.strip_html_and_bracket_markup(self._get_source_question())
        return [char for char in clean if not kana_utils.is_kana(char)]

    @classmethod
    def create(cls, question: str, answer: str) -> SentenceNote:
        inner_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Sentence))
        note = SentenceNote(inner_note)
        note._set_source_question(question)
        note._set_user_answer(answer)
        note.update_generated_data()
        app.anki_collection().addNote(inner_note)
        return note

