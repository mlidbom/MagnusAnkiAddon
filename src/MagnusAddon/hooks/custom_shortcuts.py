from __future__ import annotations

from typing import TypeVar

from ankiutils import app, ui_utils
from aqt import mw, qconnect
from aqt.qt import QKeySequence, QShortcut
from note.kanjinote import KanjiNote
from note.sentences.sentencenote import SentenceNote
from note.vocabulary.vocabnote import VocabNote
from sysutils.typed import try_cast

T: TypeVar = TypeVar("T")

def init() -> None:
    def null_op() -> None: pass

    def try_get_review_note_of_type(note_type: type[T]) -> T | None:
        return try_cast(note_type, ui_utils.try_get_review_note())

    def remove_mnemonic() -> None:
        kanji = try_get_review_note_of_type(KanjiNote)
        if kanji:
            kanji.set_user_mnemonic("")
            app.get_ui_utils().refresh()

        vocab = try_get_review_note_of_type(VocabNote)
        if vocab:
            vocab.user_mnemonic.empty()
            app.get_ui_utils().refresh()

    def generate_compound_parts() -> None:
        vocab = try_get_review_note_of_type(VocabNote)
        if vocab:
            vocab.compound_parts.auto_generate()
            app.get_ui_utils().refresh()

    def reset_incorrect_matches() -> None:
        sentence = try_get_review_note_of_type(SentenceNote)
        if sentence:
            sentence.configuration.incorrect_matches.reset()
            app.get_ui_utils().refresh()

    def reset_source_comments() -> None:
        sentence = try_get_review_note_of_type(SentenceNote)
        if sentence:
            sentence.source_comments.empty()
            app.get_ui_utils().refresh()

    qconnect(QShortcut(QKeySequence("0"), mw).activated, remove_mnemonic)
    qconnect(QShortcut(QKeySequence("9"), mw).activated, generate_compound_parts)
    qconnect(QShortcut(QKeySequence("8"), mw).activated, reset_incorrect_matches)
    qconnect(QShortcut(QKeySequence("7"), mw).activated, reset_source_comments)

    for char in "u":  # reset some pesky shortcuts constantly being accidentally triggered
        qconnect(QShortcut(QKeySequence(char), mw).activated, null_op)
