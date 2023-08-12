import re

import aqt.browser
from anki.cards import Card
from aqt import gui_hooks, mw
from aqt.editor import Editor
from aqt.qt import *

from batches import local_note_updater
from sysutils import my_clipboard
from sysutils.utils import UIUtils
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

def setup_browser_context_menu(browser: aqt.browser.Browser, menu: QMenu):
    selected_cards = browser.selected_cards()

    if len(selected_cards) == 1:
        action = menu.addAction("Prioritize selected cards")
        action.triggered.connect(lambda: wani_queue_manager.prioritize_selected_cards(selected_cards))


def copy_previewer_sort_field_to_windows_clipboard(html:str, card: Card, type_of_display:str) -> str:
    if type_of_display == 'previewAnswer':
        if not UIUtils.is_edit_current_active():
            copy_card_sort_field_to_clipboard(card)
    return html

class CopyCardData:
    note_id = 0

def copy_card_sort_field_to_clipboard(card):
    note = card.note()
    if note.id == CopyCardData.note_id:
        return
    else:
        CopyCardData.note_id = note.id
    model = note.model()
    sort_field = model['sortf']
    sort_value = note.fields[sort_field]
    clean_string = re.sub('<.*?>', '', sort_value)
    clean_string = re.sub('\[.*?\]', '', clean_string) # noqa
    my_clipboard.set_text(clean_string)


def setup():
    build_main_menu()
    gui_hooks.editor_did_init_buttons.append(setup_editor_buttons)
    gui_hooks.browser_will_show_context_menu.append(setup_browser_context_menu)
    gui_hooks.reviewer_did_show_answer.append(copy_card_sort_field_to_clipboard)
    gui_hooks.card_will_show.append(copy_previewer_sort_field_to_windows_clipboard)
