from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu
from aqt import gui_hooks, mw, qconnect
from aqt.editor import Editor

from batches import local_note_updater
from wanikani import note_importer
from wanikani import wani_note_updater, wani_queue_manager
from wanikani.wani_downloader import WaniDownloader
from note.wanivocabnote import WaniVocabNote


def add_menu_action(sub_menu, heading, callback):
    action = QAction(heading, mw)
    qconnect(action.triggered, callback)
    sub_menu.addAction(action)

def build_main_menu():
    my_menu = QMenu("Magnu&s", mw)
    mw.form.menuTools.addMenu(my_menu)

    local_menu = QMenu("Local Action&s", mw)
    my_menu.addMenu(local_menu)
    build_local_menu(local_menu)

    wani_menu = QMenu("&Wanikani Actions", mw)
    my_menu.addMenu(wani_menu)
    build_wani_menu(wani_menu)

def build_local_menu(sub_menu):
    add_menu_action(sub_menu, "Update &All", local_note_updater.update_all)

def build_wani_menu(sub_menu):
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


def setup_editor_buttons(buttons, the_editor: Editor):
    buttons.append(the_editor.addButton("", "Unsuspend with dependencies",
                                            lambda local_editor: wani_queue_manager.unsuspend_with_dependencies(
                                                local_editor.note)))

    buttons.append(the_editor.addButton("", "prioritize with dependencies",
                                            lambda local_editor: wani_queue_manager.prioritize_with_dependencies(
                                                local_editor.note)))

    buttons.append(the_editor.addButton("", "answer again with zero interval with dependencies",
                                            lambda local_editor: wani_queue_manager.answer_again_with_zero_interval_for_new_note_cards_with_dependencies(
                                                local_editor.note)))

    buttons.append(the_editor.addButton("", "Update from wanikani",
                                        lambda local_editor: wani_note_updater.update_from_wanikani(
                                             local_editor.note)))

    buttons.append(the_editor.addButton("", "Fetch audio from wanikani",
                                        lambda local_editor: WaniDownloader.fetch_audio_from_wanikani(
                                            WaniVocabNote(local_editor.note))))


def setup():
    build_main_menu()
    gui_hooks.editor_did_init_buttons.append(setup_editor_buttons)
