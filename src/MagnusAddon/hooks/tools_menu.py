from typing import Callable

from aqt import qconnect
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu

from ankiutils import app
from ankiutils.app import main_window, get_ui_utils
from batches import local_note_updater
from configuration.configuration import show_japanese_options
from configuration.configuration_value import ConfigurationValueBool
from configuration.readings_mapping_dialog import show_readings_mappings
from hooks import shortcutfinger
from hooks.right_click_menu_search import build_open_in_anki_menu, build_web_search_menu
from note.jpnote import JPNote
from sysutils.typed import non_optional
from wanikani import note_importer
from wanikani.wani_downloader import WaniDownloader
from PyQt6.QtWidgets import QInputDialog, QLineEdit

def refresh() -> None:
    note = JPNote.note_from_card(non_optional(main_window().reviewer.card))

    if isinstance(note, JPNote):
        note.update_generated_data()


def add_menu_ui_action(sub_menu: QMenu, heading: str, callback: Callable[[],None], shortcut: str = "") -> None:
    action = QAction(heading, main_window())
    if shortcut: action.setShortcut(shortcut)

    def ui_callback() -> None:
        get_ui_utils().run_ui_action(callback)

    qconnect(action.triggered, ui_callback)
    sub_menu.addAction(action)

def build_main_menu() -> None:
    my_menu = non_optional(main_window().form.menubar.addMenu(shortcutfinger.home1("Japanese")))

    build_lookup_menu(non_optional(my_menu.addMenu(shortcutfinger.home1("Lookup"))))
    build_config_menu(non_optional(my_menu.addMenu(shortcutfinger.home2("Config"))))
    build_local_menu(non_optional(my_menu.addMenu(shortcutfinger.home3("Local Actions"))))
    build_misc_menu(non_optional(my_menu.addMenu(shortcutfinger.home4("Debug"))))

def build_lookup_menu(lookup_menu: QMenu) -> None:
    def get_text_input() -> str:
        text, ok = QInputDialog.getText(None, "input", "enter text", QLineEdit.EchoMode.Normal, "")
        return text if ok and text else ""

    build_open_in_anki_menu(non_optional(lookup_menu.addMenu(shortcutfinger.up1("Anki"))), get_text_input)
    build_web_search_menu(non_optional(lookup_menu.addMenu(shortcutfinger.down1("Web"))), get_text_input)

def build_misc_menu(misc_menu: QMenu) -> None:
    build_debug_menu(non_optional(misc_menu.addMenu(shortcutfinger.home1("Debug"))))
    build_wani_menu(non_optional(misc_menu.addMenu(shortcutfinger.home2("Wanikani Actions"))))

def build_debug_menu(debug_menu: QMenu) -> None:
    add_menu_ui_action(debug_menu, shortcutfinger.home1("Refresh UI"), refresh, "F5")
    add_menu_ui_action(debug_menu, shortcutfinger.home3("Print_memory_usage"), local_note_updater.print_gc_status_and_collect)
    debug_menu.addAction(shortcutfinger.home4("Reset"), app.reset)

def build_config_menu(config_menu: QMenu) -> None:
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

    config_menu.addAction(shortcutfinger.home2("Options"), show_japanese_options)
    config_menu.addAction(shortcutfinger.home3("Readings mappings"), show_readings_mappings)


def build_local_menu(sub_menu: QMenu) -> None:
    def setup_update_menu(update_menu: QMenu) -> None:
        add_menu_ui_action(update_menu, "Update &All", local_note_updater.update_all)
        add_menu_ui_action(update_menu, "Update &Vocab", local_note_updater.update_vocab)
        add_menu_ui_action(update_menu, "Update &Kanji", local_note_updater.update_kanji)
        add_menu_ui_action(update_menu, "Update &Sentences", local_note_updater.update_sentences)
        add_menu_ui_action(update_menu, "Reparse words from sentences", local_note_updater.reparse_sentence_words)

    def setup_danger_zone_menu(danger_zone: QMenu) -> None:
        add_menu_ui_action(danger_zone, "Create Sentences from Context Sentences With Audio", local_note_updater.generate_sentences_for_context_sentences_with_audio)

    setup_update_menu(non_optional(sub_menu.addMenu(shortcutfinger.home1("Update"))))

    add_menu_ui_action(sub_menu, shortcutfinger.home2("Convert &Immersion Kit sentences"), local_note_updater.convert_immersion_kit_sentences)
    add_menu_ui_action(sub_menu, shortcutfinger.home3("Tag note metadata"), local_note_updater.tag_note_metadata)
    setup_danger_zone_menu(non_optional(sub_menu.addMenu(shortcutfinger.home4("Danger Zone"))))

def build_wani_menu(sub_menu: QMenu) -> None:
    add_menu_ui_action(sub_menu, "Import Missing Radicals", note_importer.import_missing_radicals)
    add_menu_ui_action(sub_menu, "Import Missing Kanji", note_importer.import_missing_kanji)
    add_menu_ui_action(sub_menu, "Import Missing Vocabulary", note_importer.import_missing_vocab)
    add_menu_ui_action(sub_menu, "Import Missing context sentences", note_importer.import_missing_context_sentences)
    add_menu_ui_action(sub_menu, "Download Missing Vocabulary audio", WaniDownloader.fetch_missing_vocab_audio)


def init() -> None:
    build_main_menu()
