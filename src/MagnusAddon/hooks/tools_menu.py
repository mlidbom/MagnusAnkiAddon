from typing import Callable

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu
from aqt import mw, qconnect

from batches import local_note_updater
from sysutils.ui_utils import UIUtils
from wanikani import note_importer
from wanikani import wani_note_updater
from wanikani.wani_downloader import WaniDownloader


def add_menu_action(sub_menu: QMenu, heading: str, callback: Callable, shortcut: str):
    action = QAction(heading, mw)
    if shortcut: action.setShortcut(shortcut)
    qconnect(action.triggered, callback)
    sub_menu.addAction(action)

def build_main_menu() -> None:
    my_menu = QMenu("Magnu&s", mw)
    tools_menu = mw.form.menuTools
    add_menu_action(tools_menu, "Refresh UI", lambda: UIUtils.refresh(), "Ctrl+F5")

    tools_menu.addMenu(my_menu)

    local_menu = QMenu("Local Action&s", mw)
    my_menu.addMenu(local_menu)
    build_local_menu(local_menu)

    wani_menu = QMenu("&Wanikani Actions", mw)
    my_menu.addMenu(wani_menu)
    build_wani_menu(wani_menu)

def build_local_menu(sub_menu: QMenu) -> None:
    add_menu_action(sub_menu, "Update &All", local_note_updater.update_all, "F5")
    add_menu_action(sub_menu, "Update &Vocab", local_note_updater.update_vocab, "F5")
    add_menu_action(sub_menu, "Update &Kanji", local_note_updater.update_kanji, "F5")
    add_menu_action(sub_menu, "Update &Sentences", local_note_updater.update_sentences, "F5")
    add_menu_action(sub_menu, "Set Vocab UK from dictionary", local_note_updater.set_vocab_uk_from_dictionary, "F5")


def build_wani_menu(sub_menu: QMenu) -> None:
    add_menu_action(sub_menu, "Update Radicals", wani_note_updater.update_radical, "F5")
    add_menu_action(sub_menu, "Update Kanji", wani_note_updater.update_kanji, "F5")
    add_menu_action(sub_menu, "Update Vocabulary", wani_note_updater.update_vocab, "F5")
    add_menu_action(sub_menu, "Import Missing Radicals", note_importer.import_missing_radicals, "F5")
    add_menu_action(sub_menu, "Import Missing Kanji", note_importer.import_missing_kanji, "F5")
    add_menu_action(sub_menu, "Import Missing Vocabulary", note_importer.import_missing_vocab, "F5")
    add_menu_action(sub_menu, "Download Missing Vocabulary audio", WaniDownloader.fetch_missing_vocab_audio, "F5")
    add_menu_action(sub_menu, "Delete Missing Radicals", wani_note_updater.delete_missing_radicals, "F5")
    add_menu_action(sub_menu, "Delete Missing Kanji", wani_note_updater.delete_missing_kanji, "F5")
    add_menu_action(sub_menu, "Delete Missing Vocabulary", wani_note_updater.delete_missing_vocab, "F5")


def init() -> None:
    build_main_menu()
