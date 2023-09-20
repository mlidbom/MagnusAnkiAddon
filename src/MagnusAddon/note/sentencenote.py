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

    def _on_edited(self) -> None: self.update_generated_data()

    def _get_source_answer(self) -> str: return super().get_field(SentenceNoteFields.source_answer)
    def _get_user_answer(self) -> str: return super().get_field(SentenceNoteFields.user_answer)

    def _get_source_question(self) -> str: return super().get_field(SentenceNoteFields.source_question)

    def _get_user_question(self) -> str: return super().get_field(SentenceNoteFields.user_question)
    def get_active_question(self) -> str: return self._get_user_question() or self._get_source_question()

    def get_user_extra_vocab(self) -> list[str]: return StringUtils.extract_comma_separated_values(super().get_field(SentenceNoteFields.user_extra_vocab))
    def get_user_excluded_vocab(self) -> set[str]: return set(StringUtils.extract_comma_separated_values(super().get_field(SentenceNoteFields.user_excluded_vocab)))


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
        super().set_field(SentenceNoteFields.active_answer, self._get_user_answer() or self._get_source_answer())
        super().set_field(SentenceNoteFields.active_question, self._get_user_question() or self._get_source_question())

    def _update_parsed_words(self) -> None:
        if self._needs_words_reparsed():
            self._set_parsed_words([word.word for word in self.parse_words_from_expression()])

    def extract_kanji(self) -> list[str]:
        clean = StringUtils.strip_markup(self._get_source_question())
        return [char for char in clean if not kana_utils.is_kana(char)]
