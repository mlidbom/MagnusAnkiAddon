from anki.cards import Card, CardId
from aqt import mw, gui_hooks
from aqt.browser import Browser  # type: ignore
from aqt.qt import QKeySequence, QShortcut
from typing import List
import json
import os

from PyQt6.QtWidgets import QWidget

from ankiutils import app, query_builder, search_executor, ui_utils
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import typed


def init() -> None:
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

    def null_op() -> None: pass

    QShortcut(QKeySequence("0"), mw).activated.connect(remove_mnemonic)

    for char in "u":#reset some pesky shortcuts constantly being accidentally triggered
        QShortcut(QKeySequence(char), mw).activated.connect(null_op)