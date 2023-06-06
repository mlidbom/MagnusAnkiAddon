# coding: utf-8

import aqt
from anki.hooks import addHook


def lookup(text):
    browser = aqt.dialogs.open('Browser', aqt.mw)
    browser.form.searchEdit.lineEdit().setText(text)
    browser.onSearchActivated()


def add_vocab_lookup_action(view, menu):
    selected = view.page().selectedText()
    if not selected:
        return

    suffix = (selected[:20] + '..') if len(selected) > 20 else selected
    label = f'Search for Wanikani Vocab "{suffix}" in Anki &Browser'
    action = menu.addAction(label)
    action.triggered.connect(lambda: lookup("note:vocab_model Vocab:*" + selected + "*"))


def add_kanji_lookup_action(view, menu):
    selected = view.page().selectedText()
    if not selected:
        return

    suffix = (selected[:20] + '..') if len(selected) > 20 else selected
    label = f'Search for Wanikani Kanji "{suffix}" in Anki &Browser'
    action = menu.addAction(label)
    action.triggered.connect(lambda: lookup("note:kanji_model kanji:" + selected))

def add_radical_lookup_action(view, menu):
    selected = view.page().selectedText()
    if not selected:
        return

    suffix = (selected[:20] + '..') if len(selected) > 20 else selected
    label = f'Search for Wanikani Radical "{suffix}" in Anki &Browser'
    action = menu.addAction(label)
    action.triggered.connect(lambda: lookup("note:radical_model radical:" + selected))


addHook("AnkiWebView.contextMenuEvent", add_vocab_lookup_action)
addHook("EditorWebView.contextMenuEvent", add_vocab_lookup_action)
addHook("AnkiWebView.contextMenuEvent", add_kanji_lookup_action)
addHook("EditorWebView.contextMenuEvent", add_kanji_lookup_action)
addHook("AnkiWebView.contextMenuEvent", add_radical_lookup_action)
addHook("EditorWebView.contextMenuEvent", add_radical_lookup_action)
