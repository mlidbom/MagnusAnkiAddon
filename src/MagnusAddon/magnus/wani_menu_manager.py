import aqt.browser
from anki.cards import Card
from aqt.editor import Editor

from magnus import wani_note_updater, note_importer, wani_queue_manager, local_note_updater
from magnus.wani_downloader import WaniDownloader
from aqt import gui_hooks, mw
from aqt.qt import *
import win32clipboard
import re

from magnus.wanikani_note import WaniVocabNote

def add_menu_action(sub_menu, heading, callback):
    qaction = QAction(heading, mw)
    qconnect(qaction.triggered, callback)
    sub_menu.addAction(qaction)

def build_main_menu():
    my_menu = QMenu("Magnus", mw)
    mw.form.menuTools.addMenu(my_menu)

    local_menu = QMenu("Local", mw)
    my_menu.addMenu(local_menu)
    build_local_menu(local_menu)

    wani_menu = QMenu("Wanikani", mw)
    my_menu.addMenu(wani_menu)
    build_wani_menu(wani_menu)

def build_local_menu(sub_menu):
    add_menu_action(sub_menu, "Update Vocab Kanji Names", local_note_updater.update_vocab)

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

def setup_browser_context_menu(browser: aqt.browser.Browser, menu: QMenu):
    selected_cards = browser.selected_cards()

    if len(selected_cards) == 1:
        action = menu.addAction("Prioritize selected cards")
        action.triggered.connect(lambda: wani_queue_manager.prioritize_selected_cards(selected_cards))


def set_clipboard_text(text):
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
    except:
        pass  # Occationally this code randomly fails. Let's not have that result in a crash of the addon OK?

def copy_sort_field_to_windows_clipboard(card: Card):
    note = card.note()
    model = note.model()
    sort_field = model['sortf']
    sort_value = note.fields[sort_field]
    clean_string = re.sub('<.*?>', '', sort_value)
    clean_string = re.sub('\[.*?\]', '', clean_string)
    set_clipboard_text(clean_string)


build_main_menu()
gui_hooks.editor_did_init_buttons.append(setup_editor_buttons)
gui_hooks.browser_will_show_context_menu.append(setup_browser_context_menu)
gui_hooks.reviewer_did_show_answer.append(copy_sort_field_to_windows_clipboard)