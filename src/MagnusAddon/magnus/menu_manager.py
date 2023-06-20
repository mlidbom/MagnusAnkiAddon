import aqt

from magnus import note_updater, note_importer, wanikani
from aqt.utils import showInfo, qconnect
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


def setup_editor_buttons(buttons, the_editor: aqt.editor.Editor):
    unsuspend_button = the_editor.addButton("", "Unsuspend with dependencies",
                                            lambda local_editor: wanikani.unsuspend_with_dependencies(
                                                local_editor.note))
    buttons.append(unsuspend_button)

    update_button = the_editor.addButton("", "Update from wanikani",
                                         lambda local_editor: note_updater.update_from_wanikani(
                                             WaniVocabNote(local_editor.note)))
    buttons.append(update_button)


build_main_menu()
gui_hooks.editor_did_init_buttons.append(setup_editor_buttons)
