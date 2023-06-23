import aqt.browser
from aqt.editor import Editor

from magnus import note_updater, note_importer, wani_queue_manager
from magnus.wani_downloader import WaniDownloader
from aqt import gui_hooks, mw
from aqt.qt import *

from magnus.wanikani_note import WaniVocabNote


def build_main_menu():
    sub_menu = QMenu("Wanikani", mw)
    mw.form.menuTools.addMenu(sub_menu)

    action = QAction("Update Radicals", mw)
    qconnect(action.triggered, note_updater.update_radical)
    sub_menu.addAction(action)

    action = QAction("Update Kanji", mw)
    qconnect(action.triggered, note_updater.update_kanji)
    sub_menu.addAction(action)

    action = QAction("Update Vocabulary", mw)
    qconnect(action.triggered, note_updater.update_vocab)
    sub_menu.addAction(action)

    action = QAction("Import Missing Radicals", mw)
    qconnect(action.triggered, note_importer.import_missing_radicals)
    sub_menu.addAction(action)

    action = QAction("Import Missing Kanji", mw)
    qconnect(action.triggered, note_importer.import_missing_kanji)
    sub_menu.addAction(action)

    action = QAction("Import Missing Vocabulary", mw)
    qconnect(action.triggered, note_importer.import_missing_vocab)
    sub_menu.addAction(action)

    action = QAction("Download Missing Vocabulary audio", mw)
    qconnect(action.triggered, WaniDownloader.fetch_missing_vocab_audio)
    sub_menu.addAction(action)

    action = QAction("Delete Missing Radicals", mw)
    qconnect(action.triggered, note_updater.delete_missing_radicals)
    sub_menu.addAction(action)

    action = QAction("Delete Missing Kanji", mw)
    qconnect(action.triggered, note_updater.delete_missing_kanji)
    sub_menu.addAction(action)

    action = QAction("Delete Missing Vocabulary", mw)
    qconnect(action.triggered, note_updater.delete_missing_vocab)
    sub_menu.addAction(action)


def setup_editor_buttons(buttons, the_editor: Editor):
    unsuspend_button = the_editor.addButton("", "Unsuspend with dependencies",
                                            lambda local_editor: wani_queue_manager.unsuspend_with_dependencies(
                                                local_editor.note))
    buttons.append(unsuspend_button)

    update_button = the_editor.addButton("", "Update from wanikani",
                                         lambda local_editor: note_updater.update_from_wanikani(
                                             local_editor.note))
    buttons.append(update_button)

    buttons.append(the_editor.addButton("", "Fetch audio from wanikani",
                                        lambda local_editor: WaniDownloader.fetch_audio_from_wanikani(
                                            WaniVocabNote(local_editor.note))))

def setup_browser_context_menu(browser: aqt.browser.Browser, menu: QMenu):
    selected_cards = browser.selected_cards()

    if len(selected_cards) == 1:
        action = menu.addAction("Prioritize with dependencies")
        action.triggered.connect(lambda: wani_queue_manager.prioritize_cards_with_dependencies(selected_cards))


build_main_menu()
gui_hooks.editor_did_init_buttons.append(setup_editor_buttons)
gui_hooks.browser_will_show_context_menu.append(setup_browser_context_menu)