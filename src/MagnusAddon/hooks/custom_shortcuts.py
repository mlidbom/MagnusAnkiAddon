from __future__ import annotations

from typing import Callable, TypeVar

import aqt
from ankiutils import app, ui_utils
from aqt import gui_hooks
from note.kanjinote import KanjiNote
from note.sentences.sentencenote import SentenceNote
from note.vocabulary.vocabnote import VocabNote
from sysutils.typed import try_cast

T: TypeVar = TypeVar("T")

def init() -> None:
    def try_get_review_note_of_type(note_type: type[T]) -> T | None:
        return try_cast(note_type, ui_utils.try_get_review_note())

    def remove_mnemonic() -> None:
        kanji = try_get_review_note_of_type(KanjiNote)
        if kanji:
            kanji.set_user_mnemonic("")
            app.get_ui_utils().refresh()

        vocab = try_get_review_note_of_type(VocabNote)
        if vocab:
            vocab.user.mnemonic.empty()
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

    def inject_shortcuts(_state: aqt.main.MainWindowState, shortcuts:list[tuple[str, Callable]]) -> None:
        def remove_shortcut(string: str) -> None:
            for shortcut in shortcuts:
                if shortcut[0] == string:
                    shortcuts.remove(shortcut)

        for char in ["0", "9", "8", "7", "u"]:
            remove_shortcut(char)

        shortcuts.append(("0", remove_mnemonic))
        shortcuts.append(("9", generate_compound_parts))
        shortcuts.append(("8", reset_incorrect_matches))
        shortcuts.append(("7", reset_source_comments))



    gui_hooks.state_shortcuts_will_change.append(inject_shortcuts)
