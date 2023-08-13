from typing import Callable

import aqt
from PyQt6.QtWidgets import QMenu
from aqt.browser import Browser
from aqt.editor import Editor, EditorMode
from aqt.webview import AnkiWebView

from batches import local_note_updater
from note.wanikanjinote import WaniKanjiNote
from sysutils.utils import UIUtils

from wanikani.wani_constants import Wani


def add_ui_action(menu: QMenu, name: str, callback: Callable[[], None]) -> None:
    menu.addAction(name, lambda: run_ui_action(callback))


def build_radical_search_string(selected: str) -> str:
    start = f"{Wani.RadicalFields.Radical_Name}:{selected} OR"
    clauses = " OR ".join([f"{Wani.RadicalFields.Radical}:{char}" for char in selected])
    return f"note:{Wani.NoteType.Radical} ( {start} {clauses} )"


def add_kanji_primary_vocab(note: WaniKanjiNote, selection: str, _view: AnkiWebView):
    primary_vocabs = [voc for voc in [note.get_primary_vocab(), note.tag_readings_in_string(selection, lambda read: f"<read>{read}</read>")] if voc]
    note.set_primary_vocab(", ".join(primary_vocabs))
    local_note_updater.update_kanji(note)


def set_kanji_primary_vocab(note: WaniKanjiNote, selection: str, view: AnkiWebView):
    note.set_primary_vocab("")
    add_kanji_primary_vocab(note, selection, view)


def run_ui_action(callback: Callable[[], None]) -> None:
    callback()
    UIUtils.refresh()


def add_sentence_lookup(menu, name: str, search):
    add_lookup_action(menu, name, f"(deck:*sentence* deck:*listen*) (Jlab-Kanji:*{search}* OR Expression:*{search}* OR Reading:*{search}*)")


def register_show_previewer(editor: Editor):
    if editor.editorMode == EditorMode.EDIT_CURRENT:
        UIUtils.show_current_review_in_preview()
        editor.parentWindow.activateWindow()


def add_lookup_action(menu: QMenu, name: str, search: str):
    menu.addAction(name, lambda: anki_lookup(search))


def anki_lookup(text):
    browser: Browser = aqt.dialogs.open('Browser', aqt.mw)
    browser.form.searchEdit.lineEdit().setText(text)
    browser.onSearchActivated()
    UIUtils.activate_preview()
