from __future__ import annotations
from typing import TYPE_CHECKING

from sysutils.ex_str import newline

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.extracted_word import ExtractedWord
    from note.vocabnote import VocabNote

from note.jpnote import JPNote
from sysutils import timeutil, kana_utils
from sysutils import ex_str
from note.note_constants import SentenceNoteFields, NoteTypes
from anki.notes import Note

class SentenceNote(JPNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_question(self) -> str: return self._get_user_question() or self._get_source_question()
    def get_answer(self) -> str: return self._get_user_answer() or self._get_source_answer()

    def _get_source_answer(self) -> str: return self.get_field(SentenceNoteFields.source_answer)
    def _get_user_answer(self) -> str: return self.get_field(SentenceNoteFields.user_answer)

    def _set_user_answer(self, question: str) -> None: return self.set_field(SentenceNoteFields.user_answer, question)

    def _get_source_question(self) -> str: return ex_str.strip_html_markup(self.get_field(SentenceNoteFields.source_question))
    def _set_source_question(self, question: str) -> None: return self.set_field(SentenceNoteFields.source_question, question)

    def _get_user_question(self) -> str: return ex_str.strip_html_markup(self.get_field(SentenceNoteFields.user_question))

    def get_user_extra_vocab(self) -> list[str]: return ex_str.extract_newline_separated_values(self.get_field(SentenceNoteFields.user_extra_vocab))
    def _set_user_extra_vocab(self, extra: list[str]) -> None: return self.set_field(SentenceNoteFields.user_extra_vocab, newline.join(extra))

    def get_user_excluded_vocab(self) -> set[str]: return set(ex_str.extract_newline_separated_values(self.get_field(SentenceNoteFields.user_excluded_vocab)))
    def _set_user_excluded_vocab(self, excluded: set[str]) -> None: self.set_field(SentenceNoteFields.user_excluded_vocab, newline.join(excluded))

    def add_extra_vocab(self, vocab: str) -> None:
        self._set_user_extra_vocab(self.get_user_extra_vocab() + [vocab.strip()])

    def remove_extra_vocab(self, vocab: str) -> None:
        self._set_user_extra_vocab([v for v in self.get_user_extra_vocab() if not v == vocab] )

    def exclude_vocab(self, vocab: str) -> None:
        excluded = self.get_user_excluded_vocab()
        excluded.add(vocab.strip())
        self._set_user_excluded_vocab(excluded)

    def parse_words_from_expression(self) -> list[ExtractedWord]:
        from language_services.janome_ex.word_extraction import word_extractor
        return word_extractor.extract_words(self.get_question())

    def ud_extract_word_forms(self) -> list[str]:
        from language_services.universal_dependencies import ud_tokenizers
        from language_services.universal_dependencies.shared.tree_building import ud_tree_builder
        from language_services.universal_dependencies.shared.tree_building.ud_tree_node import UDTreeNode

        tree = ud_tree_builder.build_tree(ud_tokenizers.default, self.get_question())
        word_forms: set[str] = set()

        def get_node_forms(node: UDTreeNode) -> None:
            word_forms.add(node.form)
            if node.lemma_should_be_shown_in_breakdown():
                word_forms.add(node.lemma)

        tree.visit(get_node_forms)

        return list(word_forms)

    def ud_extract_vocab(self) -> list[VocabNote]:
        from ankiutils import app
        return app.col().vocab.with_forms(self.ud_extract_word_forms())

    def _get_parsed_words(self) -> list[str]: return self.get_field(SentenceNoteFields.ParsedWords).split(",")
    def get_words(self) -> set[str]: return (self.get_parsed_words() | set(self.get_user_extra_vocab())) - self.get_user_excluded_vocab()
    def get_parsed_words(self) -> set[str]: return set(self._get_parsed_words())
    def _set_parsed_words(self, value: list[str]) -> None:
        value.append(str(timeutil.one_second_from_now()))
        self.set_field(SentenceNoteFields.ParsedWords, ",".join(value))

    def _parsed_words_timestamp(self) -> int:
        words = self._get_parsed_words()
        return int(words[-1]) if words and words[-1].isdigit() else 0

    def _needs_words_reparsed(self) -> bool: return self._note.mod > self._parsed_words_timestamp()

    def update_generated_data(self) -> None:
        super().update_generated_data()
        self._update_parsed_words()
        self.set_field(SentenceNoteFields.active_answer, self.get_answer())
        self.set_field(SentenceNoteFields.active_question, self.get_question())

    def _update_parsed_words(self) -> None:
        if self._needs_words_reparsed():
            self._set_parsed_words([word.word for word in self.parse_words_from_expression()])

    def extract_kanji(self) -> list[str]:
        clean = ex_str.strip_html_and_bracket_markup(self._get_source_question())
        return [char for char in clean if kana_utils.is_kanji(char)]

    @classmethod
    def create(cls, question: str, answer: str) -> SentenceNote:
        from ankiutils import app
        inner_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Sentence))
        note = SentenceNote(inner_note)
        note._set_source_question(question)
        note._set_user_answer(answer)
        note.update_generated_data()
        app.anki_collection().addNote(inner_note)
        return note
