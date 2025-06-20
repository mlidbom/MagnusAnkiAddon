from __future__ import annotations

from typing import Callable

from ankiutils import app, ui_utils
from ankiutils.app import get_ui_utils, main_window
from aqt import qconnect
from batches import local_note_updater
from configuration.configuration import show_japanese_options
from configuration.readings_mapping_dialog import show_readings_mappings
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QInputDialog, QLineEdit, QMenu
from sysutils import object_instance_tracker
from sysutils.typed import non_optional
from ui.menus.menu_utils import ex_qmenu, shortcutfinger
from ui.menus.open_in_anki import build_open_in_anki_menu
from ui.menus.web_search import build_web_search_menu
from ui.open_note.open_note_dialog import NoteSearchDialog
from wanikani import note_importer
from wanikani.wani_downloader import WaniDownloader


def refresh() -> None:
    if not app.is_initialized():
        return

    note = ui_utils.try_get_review_note()
    if note:
        note.update_generated_data()

def add_menu_ui_action(sub_menu: QMenu, heading: str, callback: Callable[[], None], shortcut: str = "") -> None:
    action = QAction(heading, main_window())
    if shortcut: action.setShortcut(shortcut)

    def ui_callback() -> None:
        get_ui_utils().run_ui_action(callback)

    qconnect(action.triggered, ui_callback)
    sub_menu.addAction(action)

def build_main_menu() -> None:
    my_menu = non_optional(main_window().form.menubar.addMenu(shortcutfinger.home1("Japanese")))

    build_config_menu(non_optional(my_menu.addMenu(shortcutfinger.home1("Config"))))
    build_lookup_menu(non_optional(my_menu.addMenu(shortcutfinger.home2("Lookup"))))
    build_local_menu(non_optional(my_menu.addMenu(shortcutfinger.home3("Local Actions"))))
    build_debug_menu(non_optional(my_menu.addMenu(shortcutfinger.home4("Debug"))))

def build_lookup_menu(lookup_menu: QMenu) -> None:
    def get_text_input() -> str:
        text, ok = QInputDialog.getText(None, "input", "enter text", QLineEdit.EchoMode.Normal, "")
        return text if ok and text else ""

    lookup_menu.addAction(shortcutfinger.home1("Open note Ctrl+o"), lambda: NoteSearchDialog.toggle_dialog_visibility())
    build_open_in_anki_menu(non_optional(lookup_menu.addMenu(shortcutfinger.home2("Anki"))), get_text_input)
    build_web_search_menu(non_optional(lookup_menu.addMenu(shortcutfinger.home3("Web"))), get_text_input)

def build_debug_menu(debug_menu: QMenu) -> None:
    debug_menu.addAction(shortcutfinger.home1("Show instance report"), lambda: app.get_ui_utils().tool_tip(object_instance_tracker.single_line_report(), 10000))
    debug_menu.addAction(shortcutfinger.home2("Take Snapshot"), object_instance_tracker.take_snapshot)
    debug_menu.addAction(shortcutfinger.home3("Show current snapshot diff"), lambda: app.get_ui_utils().tool_tip(object_instance_tracker.current_snapshot().single_line_diff_report(), 10000))
    debug_menu.addAction(shortcutfinger.home4("Show diff against first snapshot"), lambda: app.get_ui_utils().tool_tip(object_instance_tracker.create_transient_snapshot_against_first_snapshot().single_line_diff_report(), 10000))
    debug_menu.addAction(shortcutfinger.home5("Show diff against current snapshot"), lambda: app.get_ui_utils().tool_tip(object_instance_tracker.create_transient_snapshot_against_last_snapshot().single_line_diff_report(), 10000))
    debug_menu.addAction(shortcutfinger.up1("Run GC and report"), local_note_updater.print_gc_status_and_collect)
    debug_menu.addAction(shortcutfinger.up2("Reset"), app.reset)
    add_menu_ui_action(debug_menu, shortcutfinger.down1("Refresh UI ('F5')"), refresh)

def build_config_menu(config_menu: QMenu) -> None:
    def build_feature_toggles_menu(_title: str) -> None:
        section_index = 0
        toggles_menu = non_optional(config_menu.addMenu(_title))
        for section_index, (section, toggles) in enumerate(app.config().feature_toggles):
            section_menu = non_optional(toggles_menu.addMenu(shortcutfinger.finger_by_priority_order(section_index, section)))
            ex_qmenu.build_checkbox_config_section_menu(section_menu, toggles)

        add_menu_ui_action(toggles_menu, shortcutfinger.finger_by_priority_order(section_index + 1, "Toggle all sentence auto yield compound last token flags (Ctrl+Shift+Alt+d)"), app.config().toggle_all_sentence_display_auto_yield_flags)

    build_feature_toggles_menu(shortcutfinger.home1("Feature Toggles"))
    non_optional(config_menu.addAction(shortcutfinger.home2("Readings mappings"), show_readings_mappings)).setShortcut("Ctrl+Shift+m")
    non_optional(config_menu.addAction(shortcutfinger.home3("Options"), show_japanese_options)).setShortcut("Ctrl+Shift+s")

def build_local_menu(local_menu: QMenu) -> None:
    def build_update_menu(update_menu: QMenu) -> None:
        add_menu_ui_action(update_menu, shortcutfinger.home1("Vocab"), local_note_updater.update_vocab)
        add_menu_ui_action(update_menu, shortcutfinger.home2("Kanji"), local_note_updater.update_kanji)
        add_menu_ui_action(update_menu, shortcutfinger.home3("Sentences"), local_note_updater.update_sentences)
        add_menu_ui_action(update_menu, shortcutfinger.home4("Tag note metadata"), local_note_updater.tag_note_metadata)
        add_menu_ui_action(update_menu, shortcutfinger.home5("All the above"), local_note_updater.update_all)
        add_menu_ui_action(update_menu, shortcutfinger.up1("Reparse sentences"), local_note_updater.reparse_all_sentences)
        add_menu_ui_action(update_menu, shortcutfinger.down1("All the above: Full rebuild"), local_note_updater.full_rebuild)

    def build_danger_zone_menu(danger_zone: QMenu) -> None:
        build_wani_menu(non_optional(danger_zone.addMenu("Wanikani Actions")))

    build_update_menu(non_optional(local_menu.addMenu(shortcutfinger.home1("Update"))))

    add_menu_ui_action(local_menu, shortcutfinger.home2("Convert &Immersion Kit sentences"), local_note_updater.convert_immersion_kit_sentences)
    add_menu_ui_action(local_menu, shortcutfinger.home3("Update everyting except reparsing sentences"), local_note_updater.update_all)
    build_danger_zone_menu(non_optional(local_menu.addMenu(shortcutfinger.home4("Danger Zone"))))

def build_wani_menu(sub_menu: QMenu) -> None:
    add_menu_ui_action(sub_menu, "Import Missing Kanji", note_importer.import_missing_kanji)
    add_menu_ui_action(sub_menu, "Import Missing Vocabulary", note_importer.import_missing_vocab)
    add_menu_ui_action(sub_menu, "Import Missing context sentences", note_importer.import_missing_context_sentences)
    add_menu_ui_action(sub_menu, "Download Missing Vocabulary audio", WaniDownloader.fetch_missing_vocab_audio)

def init() -> None:
    build_main_menu()
