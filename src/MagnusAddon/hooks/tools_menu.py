from typing import Callable

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu
from aqt import mw, qconnect

from batches import local_note_updater
from note.mynote import MyNote
from note.sentencenote import SentenceNote
from note.wanikanjinote import WaniKanjiNote
from note.wanivocabnote import WaniVocabNote
from note_content_building import sentence_content_builder
from sysutils.ui_utils import UIUtils
from wanikani import note_importer
from wanikani import wani_note_updater
from wanikani.wani_downloader import WaniDownloader

def deep_refresh() -> None:
    note = MyNote.note_from_card(mw.reviewer.card)

    if isinstance(note, WaniVocabNote) or isinstance(note, SentenceNote):
        local_note_updater.update_vocab()
        local_note_updater.set_vocab_uk_from_dictionary()

    if isinstance(note, SentenceNote):
        sentence_content_builder.build_breakdown_html(note)

    if isinstance(note, WaniKanjiNote):
        local_note_updater.update_kanji(note)

    UIUtils.refresh()

def add_menu_action(sub_menu: QMenu, heading: str, callback: Callable, shortcut: str = ""):
    action = QAction(heading, mw)
    if shortcut: action.setShortcut(shortcut)
    qconnect(action.triggered, callback)
    sub_menu.addAction(action)

def build_main_menu() -> None:
    my_menu = QMenu("Magnu&s", mw)
    tools_menu = mw.form.menuTools
    add_menu_action(tools_menu, "Refresh UI", lambda: UIUtils.refresh(), "F5")
    add_menu_action(tools_menu, "Deep update UI", deep_refresh, "Ctrl+F5")

    tools_menu.addMenu(my_menu)

    local_menu = QMenu("Local Action&s", mw)
    my_menu.addMenu(local_menu)
    build_local_menu(local_menu)

    wani_menu = QMenu("&Wanikani Actions", mw)
    my_menu.addMenu(wani_menu)
    build_wani_menu(wani_menu)

def build_local_menu(sub_menu: QMenu) -> None:
    add_menu_action(sub_menu, "Update &All", local_note_updater.update_all)
    add_menu_action(sub_menu, "Update &Vocab", local_note_updater.update_vocab)
    add_menu_action(sub_menu, "Update &Kanji", local_note_updater.update_kanji)
    add_menu_action(sub_menu, "Update &Sentences", local_note_updater.update_sentences)

    add_menu_action(sub_menu, "Update sentence &breakdown", local_note_updater.update_sentence_breakdown)
    add_menu_action(sub_menu, "Set Vocab UK from dictionary", local_note_updater.set_vocab_uk_from_dictionary)


def build_wani_menu(sub_menu: QMenu) -> None:
    add_menu_action(sub_menu, "Update Radicals", wani_note_updater.update_radical)
    add_menu_action(sub_menu, "Update Kanji", wani_note_updater.update_kanji)
    add_menu_action(sub_menu, "Update Vocabulary", wani_note_updater.update_vocab)
    add_menu_action(sub_menu, "Import Missing Radicals", note_importer.import_missing_radicals)
    add_menu_action(sub_menu, "Import Missing Kanji", note_importer.import_missing_kanji)
    add_menu_action(sub_menu, "Import Missing Vocabulary", note_importer.import_missing_vocab)
    add_menu_action(sub_menu, "Download Missing Vocabulary audio", WaniDownloader.fetch_missing_vocab_audio)
    add_menu_action(sub_menu, "Delete Missing Radicals", wani_note_updater.delete_missing_radicals)
    add_menu_action(sub_menu, "Delete Missing Kanji", wani_note_updater.delete_missing_kanji)
    add_menu_action(sub_menu, "Delete Missing Vocabulary", wani_note_updater.delete_missing_vocab)


def init() -> None:
    build_main_menu()
