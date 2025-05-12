from __future__ import annotations

from ankiutils import app, ui_utils
from aqt import mw, qconnect
from aqt.qt import QKeySequence, QShortcut
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.vocabnote import VocabNote


def init() -> None:
    def null_op() -> None: pass

    def remove_mnemonic() -> None:
        card_being_reviewed = ui_utils.try_get_card_being_reviewed()
        if card_being_reviewed:
            note = JPNote.note_from_card(card_being_reviewed)
            if isinstance(note, KanjiNote):
                note.set_user_mnemonic("")
                app.get_ui_utils().refresh()
            if isinstance(note, VocabNote):
                note.user_mnemonic.set("")
                app.get_ui_utils().refresh()

    def generate_compound_parts() -> None:
        card_being_reviewed = ui_utils.try_get_card_being_reviewed()
        if card_being_reviewed:
            note = JPNote.note_from_card(card_being_reviewed)
            if isinstance(note, VocabNote):
                note.auto_generate_compounds()
                app.get_ui_utils().refresh()

    qconnect(QShortcut(QKeySequence("0"), mw).activated, remove_mnemonic)
    qconnect(QShortcut(QKeySequence("9"), mw).activated, generate_compound_parts)

    for char in "u":  # reset some pesky shortcuts constantly being accidentally triggered
        qconnect(QShortcut(QKeySequence(char), mw).activated, null_op)
