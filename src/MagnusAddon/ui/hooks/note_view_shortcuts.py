from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app, ui_utils
from aqt import gui_hooks
from note.kanjinote import KanjiNote
from note.sentences.sentencenote import SentenceNote
from note.vocabulary.vocabnote import VocabNote
from PyQt6.QtCore import pyqtBoundSignal
from PyQt6.QtGui import QKeySequence, QShortcut
from sysutils import typed
from sysutils.typed import try_cast

if TYPE_CHECKING:
    from collections.abc import Callable

    from aqt.main import MainWindowState
    from configuration.configuration_value import ConfigurationValueBool
    from PyQt6.QtWidgets import QWidget

def init() -> None:
    def try_get_review_note_of_type[T](note_type: type[T]) -> T | None:
        return try_cast(note_type, ui_utils.try_get_review_note())

    def refresh_shallow() -> None: app.get_ui_utils().refresh(refresh_browser=False)

    def remove_mnemonic() -> None:
        kanji = try_get_review_note_of_type(KanjiNote)
        if kanji:
            kanji.set_user_mnemonic("")
            refresh_shallow()

        vocab = try_get_review_note_of_type(VocabNote)
        if vocab:
            vocab.user.mnemonic.empty()
            refresh_shallow()

    def generate_compound_parts() -> None:
        vocab = try_get_review_note_of_type(VocabNote)
        if vocab:
            vocab.compound_parts.auto_generate()
            refresh_shallow()

    def reset_incorrect_matches() -> None:
        sentence = try_get_review_note_of_type(SentenceNote)
        if sentence:
            sentence.configuration.incorrect_matches.reset()
            refresh_shallow()

    def reset_source_comments() -> None:
        sentence = try_get_review_note_of_type(SentenceNote)
        if sentence:
            sentence.source_comments.empty()
            refresh_shallow()

    # noinspection DuplicatedCode
    def toggle_show_compound_parts_in_sentence_breakdown() -> None:
        app.config().show_compound_parts_in_sentence_breakdown.set_value(not app.config().show_compound_parts_in_sentence_breakdown.get_value())
        if app.config().show_compound_parts_in_sentence_breakdown.get_value():
            app.config().show_sentence_breakdown_in_edit_mode.set_value(False)
        refresh_shallow()

    def toggle_expando_flag(flag: ConfigurationValueBool, exit_edit_mode: bool = True) -> None:
        flag.set_value(not flag.get_value())

        if exit_edit_mode:
            app.config().show_compound_parts_in_sentence_breakdown.set_value(False)

        refresh_shallow()

    def toggle_hide_transparent_compounds__in_sentence_breakdown() -> None:
        toggle_expando_flag(app.config().hide_compositionally_transparent_compounds)

    def toggle_hide_all_compounds_in_sentence_breakdown() -> None:
        toggle_expando_flag(app.config().hide_all_compounds)

    def toggle_show_kanji_in_sentence_breakdown() -> None:
        toggle_expando_flag(app.config().show_kanji_in_sentence_breakdown)

    def toggle_show_kanji_mnemonics_in_sentence_breakdown() -> None:
        toggle_expando_flag(app.config().show_kanji_mnemonics_in_sentence_breakdown)

    def toggle_show_sentence_breakdown_in_edit_mode() -> None:
        toggle_expando_flag(app.config().show_sentence_breakdown_in_edit_mode, exit_edit_mode=False)

    def toggle_yield_last_token_in_suru_verb_compounds_to_overlapping_compound() -> None:
        toggle_expando_flag(app.config().automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound)

    def toggle_yield_last_token_in_passive_verb_compounds_to_overlapping_compound() -> None:
        toggle_expando_flag(app.config().automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound)

    def toggle_yield_last_token_in_causative_verb_compounds_to_overlapping_compound() -> None:
        toggle_expando_flag(app.config().automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound)

    def toggle_all_yield_last_token_flags() -> None:
        app.config().toggle_all_sentence_display_auto_yield_flags()
        app.config().show_compound_parts_in_sentence_breakdown.set_value(False)
        refresh_shallow()

    def set_shortcut(widget: QWidget, shortcut: str, callback: Callable[[], None]) -> None:
        typed.checked_cast(pyqtBoundSignal, QShortcut(QKeySequence(shortcut), widget).activated).connect(callback)  # pyright: ignore[reportUnknownMemberType]

    def inject_shortcuts_in_widget(widget: QWidget) -> None:
        for key, callback in stortcuts.items():
            set_shortcut(widget, key, callback)

    def inject_shortcuts_in_reviewer(_state: MainWindowState, state_shortcuts: list[tuple[str, Callable[[], None]]]) -> None:
        def remove_shortcut(string: str) -> None:
            for shortcut in state_shortcuts:
                if shortcut[0] == string:
                    state_shortcuts.remove(shortcut)
                    return

        for char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "o", "e", "u"]:
            remove_shortcut(char)

        for key, callback in stortcuts.items():
            state_shortcuts.append((key, callback))

    stortcuts: dict[str, Callable[[], None]] = {"a": toggle_show_kanji_in_sentence_breakdown,
                                                "o": toggle_show_compound_parts_in_sentence_breakdown,
                                                "e": toggle_all_yield_last_token_flags,
                                                "u": toggle_hide_all_compounds_in_sentence_breakdown,
                                                "i": toggle_hide_transparent_compounds__in_sentence_breakdown,
                                                "k": toggle_show_sentence_breakdown_in_edit_mode,
                                                "q": toggle_show_kanji_mnemonics_in_sentence_breakdown,
                                                "0": remove_mnemonic,
                                                "7": reset_source_comments,
                                                "8": reset_incorrect_matches,
                                                "9": generate_compound_parts,
                                                "Ctrl+Shift+Alt+s": toggle_yield_last_token_in_suru_verb_compounds_to_overlapping_compound,
                                                "Ctrl+Shift+Alt+h": toggle_yield_last_token_in_passive_verb_compounds_to_overlapping_compound,
                                                "Ctrl+Shift+Alt+t": toggle_yield_last_token_in_causative_verb_compounds_to_overlapping_compound,
                                                "Ctrl+Shift+Alt+d": toggle_all_yield_last_token_flags}

    gui_hooks.previewer_did_init.append(inject_shortcuts_in_widget)  # pyright: ignore[reportUnknownMemberType]
    gui_hooks.state_shortcuts_will_change.append(inject_shortcuts_in_reviewer)  # pyright: ignore[reportUnknownMemberType]
