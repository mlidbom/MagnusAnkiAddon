from typing import Callable

from anki.cards import Card
from aqt import qconnect
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu

from ankiutils import app
from ankiutils.app import main_window, ui_utils
from batches import local_note_updater
from configuration.configuration import show_japanese_options
from configuration.configuration_value import ConfigurationValueBool
from note.jpnote import JPNote
from sysutils.typed import checked_cast, non_optional
from wanikani import note_importer, wani_note_updater
from wanikani.wani_downloader import WaniDownloader

def refresh() -> None:
    note = JPNote.note_from_card(non_optional(main_window().reviewer.card))

    if isinstance(note, JPNote):
        note.update_generated_data()

def add_checkbox_config(menu: QMenu, config_value:ConfigurationValueBool) -> None:
    checkbox_action = QAction(config_value.title, main_window())
    checkbox_action.setCheckable(True)
    checkbox_action.setChecked(config_value.get_value())
    qconnect(checkbox_action.triggered, config_value.set_value)
    menu.addAction(checkbox_action)


def add_menu_ui_action(sub_menu: QMenu, heading: str, callback: Callable[[],None], shortcut: str = "") -> None:
    action = QAction(heading, main_window())
    if shortcut: action.setShortcut(shortcut)

    def ui_callback() -> None:
        ui_utils().run_ui_action(callback)

    qconnect(action.triggered, ui_callback)
    sub_menu.addAction(action)

def build_main_menu() -> None:
    my_menu = non_optional(main_window().form.menuTools.addMenu("Magnu&s"))

    config_menu = non_optional(my_menu.addMenu("Config"))
    add_checkbox_config(config_menu, app.config.yomitan_integration_copy_answer_to_clipboard)
    config_menu.addAction("Options", show_japanese_options)

    build_local_menu(my_menu)
    build_wani_menu(my_menu)

    add_menu_ui_action(my_menu, "Refresh UI", refresh, "F5")
    my_menu.addAction("&Reset", app.reset)

def build_local_menu(menu: QMenu) -> None:
    sub_menu = non_optional(menu.addMenu("Local Action&s"))
    add_menu_ui_action(sub_menu, "Update &All", local_note_updater.update_all)
    add_menu_ui_action(sub_menu, "Update &Vocab", local_note_updater.update_vocab)
    add_menu_ui_action(sub_menu, "Update &Kanji", local_note_updater.update_kanji)
    add_menu_ui_action(sub_menu, "Update &Sentences", local_note_updater.update_sentences)
    add_menu_ui_action(sub_menu, "Reparse words from sentences", local_note_updater.reparse_sentence_words)
    add_menu_ui_action(sub_menu, "Create Sentences from Context Sentences With Audio", local_note_updater.generate_sentences_for_context_sentences_with_audio)
    add_menu_ui_action(sub_menu, "Convert &Immersion Kit sentences", local_note_updater.convert_immersion_kit_sentences)
    add_menu_ui_action(sub_menu, "Tag kanji metadata", local_note_updater.tag_kanji_metadata)

    danger_zone = QMenu("Danger Zone. No warnings given before executing!", main_window())
    sub_menu.addMenu(danger_zone)
    #add_menu_ui_action(danger_zone, "Adjust kanji primary readings", local_note_updater.adjust_kanji_primary_readings)

def build_wani_menu(menu: QMenu) -> None:
    sub_menu = non_optional(menu.addMenu("&Wanikani Actions"))
    add_menu_ui_action(sub_menu, "Update Radicals", wani_note_updater.update_radical)
    add_menu_ui_action(sub_menu, "Update Kanji", wani_note_updater.update_kanji)
    add_menu_ui_action(sub_menu, "Update Vocabulary", wani_note_updater.update_vocab)
    add_menu_ui_action(sub_menu, "Import Missing Radicals", note_importer.import_missing_radicals)
    add_menu_ui_action(sub_menu, "Import Missing Kanji", note_importer.import_missing_kanji)
    add_menu_ui_action(sub_menu, "Import Missing Vocabulary", note_importer.import_missing_vocab)
    add_menu_ui_action(sub_menu, "Import Missing context sentences", note_importer.import_missing_context_sentences)

    add_menu_ui_action(sub_menu, "Download Missing Vocabulary audio", WaniDownloader.fetch_missing_vocab_audio)
    add_menu_ui_action(sub_menu, "Delete Missing Radicals", wani_note_updater.delete_missing_radicals)
    add_menu_ui_action(sub_menu, "Delete Missing Kanji", wani_note_updater.delete_missing_kanji)
    add_menu_ui_action(sub_menu, "Delete Missing Vocabulary", wani_note_updater.delete_missing_vocab)


def init() -> None:
    build_main_menu()
