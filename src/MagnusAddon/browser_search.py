# coding: utf-8
import aqt
from PyQt6.QtWidgets import QMenu
from anki.hooks import addHook
from aqt.browser import Browser
from win32clipboard import CF_TEXT

from magnus import my_clipboard
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

def build_kanji_search_string(selected: str) -> str:
    clauses = " OR ".join([f"{Wani.KanjiFields.Kanji}:{char}" for char in selected])
    return f"note:{Wani.NoteType.Kanji} ( {clauses} )"

def build_radical_search_string(selected: str) -> str:
    start = f"{Wani.RadicalFields.Radical_Name}:{selected} OR"
    clauses = " OR ".join([f"{Wani.RadicalFields.Radical}:{char}" for char in selected])
    return f"note:{Wani.NoteType.Radical} ( {start} {clauses} )"

def register_lookup_actions(view, root_menu: QMenu):
    selected = view.page().selectedText().strip()
    if not selected:
        selected = my_clipboard.get_text()
        if not selected:
            return

    menu = root_menu.addMenu("Anki Search")

    add_lookup_action(menu, "Kanji", build_kanji_search_string(selected))
    add_lookup_action(menu, "Vocab Wildcard" , f"deck:*Vocab* deck:*Read* (Vocab:*{selected}* OR Reading:*{selected}* OR Vocab_Meaning:*{selected}*)")
    add_lookup_action(menu, "Vocab Exact", f"deck:*Vocab* deck:*Read* (Vocab:{selected} OR Reading:{selected} OR Vocab_Meaning:{selected} )")
    add_lookup_action(menu, "Radical", build_radical_search_string(selected))
    add_lookup_action(menu, "Sentence", f"tag:{Mine.Tags.Sentence} {selected}")
    add_lookup_action(menu, "Listen", f"deck:{Mine.DeckFilters.Listen} {selected}")
    add_lookup_action(menu, "Listen Sentence", f"(deck:*sentence* deck:*listen*) (Jlab-Kanji:*{selected}* OR Expression:*{selected}*)")
    add_lookup_action(menu, "Listen Sentence Reading", f"(deck:*sentence* deck:*listen*) (Jlab-Hiragana:*{selected}* OR Reading:*{selected}*)")


addHook("AnkiWebView.contextMenuEvent", register_lookup_actions)
addHook("EditorWebView.contextMenuEvent", register_lookup_actions)