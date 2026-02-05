from __future__ import annotations

from typing import TYPE_CHECKING

from jaslib.batches import local_note_updater
from jaspythonutils.sysutils.typed import checked_cast, non_optional
from PyQt6.QtCore import pyqtBoundSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QInputDialog, QLineEdit, QMenu

from jastudio.ankiutils import app, ui_utils
from jastudio.ankiutils.app import get_ui_utils, main_window
from jastudio.configuration.configuration import show_japanese_options
from jastudio.configuration.readings_mapping_dialog import show_readings_mappings
from jastudio.sysutils import object_instance_tracker
from jastudio.ui import avalonia_host
from jastudio.ui.menus.menu_utils import shortcutfinger
from jastudio.ui.menus.open_in_anki import build_open_in_anki_menu
from jastudio.ui.menus.web_search import build_web_search_menu
from jastudio.ui.open_note.open_note_dialog import NoteSearchDialog

if TYPE_CHECKING:
    from collections.abc import Callable

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

    checked_cast(pyqtBoundSignal, action.triggered).connect(ui_callback)  # pyright: ignore[reportUnknownMemberType]
    sub_menu.addAction(action)  # pyright: ignore[reportUnknownMemberType]

def build_main_menu() -> None:
    my_menu = non_optional(main_window().form.menubar.addMenu(shortcutfinger.home1("Japanese")))

    build_config_menu(non_optional(my_menu.addMenu(shortcutfinger.home1("Config"))))
    build_lookup_menu(non_optional(my_menu.addMenu(shortcutfinger.home2("Lookup"))))
    build_local_menu(non_optional(my_menu.addMenu(shortcutfinger.home3("Local Actions"))))
    build_debug_menu(non_optional(my_menu.addMenu(shortcutfinger.home4("Debug"))))
    # Avalonia UI test
    my_menu.addAction(shortcutfinger.down2("About JA Studio"), avalonia_host.show_about_dialog)  # pyright: ignore[reportUnknownMemberType]
    
    # Add "Japanese Avalonia" menu that shows Avalonia popup on hover
    _add_avalonia_main_menu(my_menu)

def build_lookup_menu(lookup_menu: QMenu) -> None:
    def get_text_input() -> str:
        text, ok = QInputDialog.getText(None, "input", "enter text", QLineEdit.EchoMode.Normal, "")
        return text if ok and text else ""

    lookup_menu.addAction(shortcutfinger.home1("Open note Ctrl+o"), lambda: NoteSearchDialog.toggle_dialog_visibility())  # pyright: ignore[reportUnknownMemberType]
    build_open_in_anki_menu(non_optional(lookup_menu.addMenu(shortcutfinger.home2("Anki"))), get_text_input)
    build_web_search_menu(non_optional(lookup_menu.addMenu(shortcutfinger.home3("Web"))), get_text_input)

def build_debug_menu(debug_menu: QMenu) -> None:
    debug_menu.addAction(shortcutfinger.home1("Show instance report"), lambda: app.get_ui_utils().tool_tip(object_instance_tracker.single_line_report(), 10000))  # pyright: ignore[reportUnknownMemberType]
    debug_menu.addAction(shortcutfinger.home2("Take Snapshot"), object_instance_tracker.take_snapshot)  # pyright: ignore[reportUnknownMemberType]
    debug_menu.addAction(shortcutfinger.home3("Show current snapshot diff"), lambda: app.get_ui_utils().tool_tip(object_instance_tracker.current_snapshot().single_line_diff_report(), 10000))  # pyright: ignore[reportUnknownMemberType]
    debug_menu.addAction(shortcutfinger.home4("Show diff against first snapshot"), lambda: app.get_ui_utils().tool_tip(object_instance_tracker.create_transient_snapshot_against_first_snapshot().single_line_diff_report(), 10000))  # pyright: ignore[reportUnknownMemberType]
    debug_menu.addAction(shortcutfinger.home5("Show diff against current snapshot"), lambda: app.get_ui_utils().tool_tip(object_instance_tracker.create_transient_snapshot_against_last_snapshot().single_line_diff_report(), 10000))  # pyright: ignore[reportUnknownMemberType]  # pyright: ignore[reportUnknownMemberType]

    import jastudio.batches.local_note_updater
    debug_menu.addAction(shortcutfinger.up1("Run GC and report"), jastudio.batches.local_note_updater.print_gc_status_and_collect)  # pyright: ignore[reportUnknownMemberType]
    debug_menu.addAction(shortcutfinger.up2("Reset"), app.reset)  # pyright: ignore[reportUnknownMemberType]
    add_menu_ui_action(debug_menu, shortcutfinger.down1("Refresh UI ('F5')"), refresh)

def build_config_menu(config_menu: QMenu) -> None:
    non_optional(config_menu.addAction(shortcutfinger.home1("Options"), show_japanese_options)).setShortcut("Ctrl+Shift+s")  # pyright: ignore[reportUnknownMemberType]
    non_optional(config_menu.addAction(shortcutfinger.home2("Readings mappings"), show_readings_mappings)).setShortcut("Ctrl+Shift+m")  # pyright: ignore[reportUnknownMemberType]

def build_local_menu(local_menu: QMenu) -> None:
    def build_update_menu(update_menu: QMenu) -> None:
        add_menu_ui_action(update_menu, shortcutfinger.home1("Vocab"), local_note_updater.update_vocab)
        add_menu_ui_action(update_menu, shortcutfinger.home2("Kanji"), local_note_updater.update_kanji)
        add_menu_ui_action(update_menu, shortcutfinger.home3("Sentences"), local_note_updater.update_sentences)
        add_menu_ui_action(update_menu, shortcutfinger.home4("Tag note metadata"), local_note_updater.tag_note_metadata)
        add_menu_ui_action(update_menu, shortcutfinger.home5("All the above"), local_note_updater.update_all)
        add_menu_ui_action(update_menu, shortcutfinger.up1("Reparse sentences"), local_note_updater.reparse_all_sentences)
        add_menu_ui_action(update_menu, shortcutfinger.down1("All the above: Full rebuild"), local_note_updater.full_rebuild)

    build_update_menu(non_optional(local_menu.addMenu(shortcutfinger.home1("Update"))))

    import jastudio.batches.local_note_updater
    add_menu_ui_action(local_menu, shortcutfinger.home2("Convert &Immersion Kit sentences"), jastudio.batches.local_note_updater.convert_immersion_kit_sentences)
    add_menu_ui_action(local_menu, shortcutfinger.home3("Update everyting except reparsing sentences"), local_note_updater.update_all)
    add_menu_ui_action(local_menu, shortcutfinger.home4("Create vocab notes for parsed words with no vocab notes"), local_note_updater.create_missing_vocab_with_dictionary_entries)
    add_menu_ui_action(local_menu, shortcutfinger.home5("Regenerate vocab source answers from jamdict"), local_note_updater.regenerate_jamdict_vocab_answers)

def _add_avalonia_main_menu(menu: QMenu) -> None:
    """Add Japanese Avalonia menu entry that shows Avalonia popup on hover."""
    avalonia_action = menu.addAction("🎯 Japanese Avalonia (Hover)")  # pyright: ignore[reportUnknownMemberType]
    
    shown = [False]
    
    def on_hover() -> None:
        if shown[0]:
            return
        shown[0] = True
        
        try:
            from PyQt6.QtWidgets import QApplication
            
            # Get menu position and convert to physical pixels
            action_rect = menu.actionGeometry(avalonia_action)
            action_global_pos = menu.mapToGlobal(action_rect.topLeft())
            
            screen = QApplication.screenAt(action_global_pos)
            dpi_scale = screen.devicePixelRatio() if screen else 1.0
            
            physical_x = int(action_global_pos.x() * dpi_scale)
            physical_y = int(action_global_pos.y() * dpi_scale)
            
            # Use the real Japanese main menu with refresh callback
            avalonia_host.show_japanese_main_menu(refresh, physical_x, physical_y)
        except Exception as e:
            from jaslib import mylog
            mylog.error(f"Failed to show Avalonia main menu: {e}")
    
    avalonia_action.hovered.connect(on_hover)  # pyright: ignore[reportUnknownMemberType, reportOptionalMemberAccess]

def init() -> None:
    build_main_menu()
