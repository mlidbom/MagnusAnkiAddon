from typing import Callable

from anki.cards import Card
from aqt import qconnect
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu

from ankiutils.app import main_window, ui_utils
from batches import local_note_updater
from hooks.note_content_building import jn_sentence_breakdown
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils.typed import checked_cast
from wanikani import note_importer, wani_note_updater
from wanikani.wani_downloader import WaniDownloader

def deep_refresh() -> None:
    note = JPNote.note_from_card(checked_cast(Card, main_window().reviewer.card))

    if isinstance(note, VocabNote) or isinstance(note, SentenceNote):
        local_note_updater.update_vocab()

    if isinstance(note, SentenceNote):
        jn_sentence_breakdown.build_breakdown_html(note)

    if isinstance(note, KanjiNote):
        local_note_updater.update_kanji()

def add_menu_ui_action(sub_menu: QMenu, heading: str, callback: Callable[[],None], shortcut: str = "") -> None:
    action = QAction(heading, main_window())
    if shortcut: action.setShortcut(shortcut)

    def ui_callback() -> None:
        ui_utils().run_ui_action(callback)

    qconnect(action.triggered, ui_callback)
    sub_menu.addAction(action)

def build_main_menu() -> None:
    my_menu = QMenu("Magnu&s", main_window())
    tools_menu = main_window().form.menuTools
    add_menu_ui_action(tools_menu, "Refresh UI", lambda: ui_utils().refresh(), "F5")
    add_menu_ui_action(tools_menu, "Deep update UI", deep_refresh, "Ctrl+F5")

    tools_menu.addMenu(my_menu)

    local_menu = QMenu("Local Action&s", main_window())
    my_menu.addMenu(local_menu)
    build_local_menu(local_menu)

    wani_menu = QMenu("&Wanikani Actions", main_window())
    my_menu.addMenu(wani_menu)
    build_wani_menu(wani_menu)

def build_local_menu(sub_menu: QMenu) -> None:
    add_menu_ui_action(sub_menu, "Update &All", local_note_updater.update_all)
    add_menu_ui_action(sub_menu, "Update &Vocab", local_note_updater.update_vocab)
    add_menu_ui_action(sub_menu, "Update &Kanji", local_note_updater.update_kanji)
    add_menu_ui_action(sub_menu, "Update &Sentences", local_note_updater.update_sentences)

def build_wani_menu(sub_menu: QMenu) -> None:
    add_menu_ui_action(sub_menu, "Update Radicals", wani_note_updater.update_radical)
    add_menu_ui_action(sub_menu, "Update Kanji", wani_note_updater.update_kanji)
    add_menu_ui_action(sub_menu, "Update Vocabulary", wani_note_updater.update_vocab)
    add_menu_ui_action(sub_menu, "Import Missing Radicals", note_importer.import_missing_radicals)
    add_menu_ui_action(sub_menu, "Import Missing Kanji", note_importer.import_missing_kanji)
    add_menu_ui_action(sub_menu, "Import Missing Vocabulary", note_importer.import_missing_vocab)
    add_menu_ui_action(sub_menu, "Download Missing Vocabulary audio", WaniDownloader.fetch_missing_vocab_audio)
    add_menu_ui_action(sub_menu, "Delete Missing Radicals", wani_note_updater.delete_missing_radicals)
    add_menu_ui_action(sub_menu, "Delete Missing Kanji", wani_note_updater.delete_missing_kanji)
    add_menu_ui_action(sub_menu, "Delete Missing Vocabulary", wani_note_updater.delete_missing_vocab)


def init() -> None:
    build_main_menu()
