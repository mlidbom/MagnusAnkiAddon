# coding: utf-8
import aqt
from PyQt6.QtWidgets import QMenu
from anki.hooks import addHook
from aqt.browser import Browser

from .magnus.wani_constants import *


def lookup(text):
    browser: Browser = aqt.dialogs.open('Browser', aqt.mw)
    browser.form.searchEdit.lineEdit().setText(text)
    browser.onSearchActivated()

#Works sometimes, unsure of the pattern.
    if browser._previewer is None:
        browser.onTogglePreview()
    else:
        browser._previewer.activateWindow()


def add_lookup_action(menu:QMenu, name: str, search:str):
    action = menu.addAction(name)
    action.triggered.connect(lambda: lookup(search))

def register_lookup_actions(view, root_menu: QMenu):
    selected = view.page().selectedText().strip()
    if not selected:
        return

    menu = root_menu.addMenu("Anki Search")

    add_lookup_action(menu, "Kanji", f"note:{Wani.NoteType.Kanji} {Wani.KanjiFields.Kanji}:{selected}")
    add_lookup_action(menu, "Vocab Wildcard" , f"deck:*Vocab* deck:*Read* (Vocab:*{selected}* OR Reading:*{selected}*)")
    add_lookup_action(menu, "Vocab Exact", f"deck:*Vocab* deck:*Read* (Vocab:{selected} OR Reading:{selected})")
    add_lookup_action(menu, "Radical", f"note:{Wani.NoteType.Radical} ({Wani.RadicalFields.Radical}:{selected} OR {Wani.RadicalFields.Radical_Name}:{selected})")
    add_lookup_action(menu, "Sentence", f"tag:{Mine.Tags.Sentence} {selected}")
    add_lookup_action(menu, "Listen", f"deck:{Mine.DeckFilters.Listen} {selected}")
    add_lookup_action(menu, "Listen Sentence", f"(deck:*sentence* deck:*listen*) (Jlab-Kanji:*{selected}* OR Expression:*{selected}*)")
    add_lookup_action(menu, "Listen Sentence Reading", f"(deck:*sentence* deck:*listen*) (Jlab-Hiragana:*{selected}* OR Reading:*{selected}*)")


addHook("AnkiWebView.contextMenuEvent", register_lookup_actions)
addHook("EditorWebView.contextMenuEvent", register_lookup_actions)