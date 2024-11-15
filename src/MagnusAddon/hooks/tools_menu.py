from typing import Callable

from aqt import qconnect
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu

from ankiutils import app
from ankiutils.app import main_window, ui_utils
from batches import local_note_updater
from configuration.configuration import show_japanese_options
from configuration.configuration_value import ConfigurationValueBool
from hooks import shortcutfinger
from note.jpnote import JPNote
from sysutils.typed import non_optional
from wanikani import note_importer
from wanikani.wani_downloader import WaniDownloader

def refresh() -> None:
    note = JPNote.note_from_card(non_optional(main_window().reviewer.card))

    if isinstance(note, JPNote):
        note.update_generated_data()


def add_menu_ui_action(sub_menu: QMenu, heading: str, callback: Callable[[],None], shortcut: str = "") -> None:
    action = QAction(heading, main_window())
    if shortcut: action.setShortcut(shortcut)

    def ui_callback() -> None:
        ui_utils().run_ui_action(callback)

    qconnect(action.triggered, ui_callback)
    sub_menu.addAction(action)

def build_main_menu() -> None:
    my_menu = non_optional(main_window().form.menuTools.addMenu("Magnu&s"))

    build_config_menu(my_menu, shortcutfinger.home1("Config"))
    build_local_menu(my_menu, shortcutfinger.home2("Local Actions"))
    build_debug_menu(my_menu, shortcutfinger.home3("Debug"))
    build_wani_menu(my_menu, shortcutfinger.home4("Wanikani Actions"))

def build_debug_menu(my_menu: QMenu, title:str) -> None:
    debug_menu = non_optional(my_menu.addMenu(title))
    add_menu_ui_action(debug_menu, "Refresh UI", refresh, "F5")
    my_menu.addAction("&Reset", app.reset)

def build_config_menu(my_menu: QMenu, title:str) -> None:
    config_menu = non_optional(my_menu.addMenu(title))

    def add_checkbox_config(menu: QMenu, config_value: ConfigurationValueBool, _title:str) -> None:
        checkbox_action = QAction(_title, main_window())
        checkbox_action.setCheckable(True)
        checkbox_action.setChecked(config_value.get_value())
        qconnect(checkbox_action.triggered, config_value.set_value)
        menu.addAction(checkbox_action)

    def build_feature_toggles_menu(_title: str) -> None:
        toggles_menu = non_optional(config_menu.addMenu(_title))
        for index, toggle in enumerate(app.config().feature_toggles):
            add_checkbox_config(toggles_menu, toggle, shortcutfinger.numpad_no_numbers(index, toggle.title))

    build_feature_toggles_menu(shortcutfinger.home1("Feature Toggles"))

    config_menu.addAction("Options", show_japanese_options)


def build_local_menu(menu: QMenu, title:str) -> None:
    sub_menu = non_optional(menu.addMenu(title))
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

def build_wani_menu(menu: QMenu, title:str) -> None:
    sub_menu = non_optional(menu.addMenu(title))
    add_menu_ui_action(sub_menu, "Import Missing Radicals", note_importer.import_missing_radicals)
    add_menu_ui_action(sub_menu, "Import Missing Kanji", note_importer.import_missing_kanji)
    add_menu_ui_action(sub_menu, "Import Missing Vocabulary", note_importer.import_missing_vocab)
    add_menu_ui_action(sub_menu, "Import Missing context sentences", note_importer.import_missing_context_sentences)
    add_menu_ui_action(sub_menu, "Download Missing Vocabulary audio", WaniDownloader.fetch_missing_vocab_audio)


def init() -> None:
    build_main_menu()
