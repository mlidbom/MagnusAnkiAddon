# coding: utf-8
import aqt
from anki.hooks import addHook

from .my_anki import *
from .wani_constants import *


def lookup(text):
    browser = aqt.dialogs.open('Browser', aqt.mw)
    browser.form.searchEdit.lineEdit().setText(text)
    browser.onSearchActivated()


def add_vocab_lookup_action(view, menu):
    selected = view.page().selectedText()
    if not selected:
        return

    suffix = (selected[:20] + '..') if len(selected) > 20 else selected
    label = f'Anki -> Wanikani Vocab'
    action = menu.addAction(label)
    action.triggered.connect(lambda: lookup(
        "{}:{} {}:*{}*".format(SearchTags.NoteType, Wani.NoteType.Vocab, Wani.VocabFields.Vocab, selected)))


def add_kanji_lookup_action(view, menu):
    selected = view.page().selectedText()
    if not selected:
        return

    suffix = (selected[:20] + '..') if len(selected) > 20 else selected
    label = f'Anki -> Wanikani Kanji'
    action = menu.addAction(label)
    action.triggered.connect(lambda: lookup(
        "{}:{} {}:{}".format(SearchTags.NoteType, Wani.NoteType.Kanji, Wani.KanjiFields.Kanji, selected)))


def add_radical_lookup_action(view, menu):
    selected = view.page().selectedText()
    if not selected:
        return

    suffix = (selected[:20] + '..') if len(selected) > 20 else selected
    label = f'Anki -> Wanikani Radical'
    action = menu.addAction(label)
    action.triggered.connect(lambda: lookup(
        "{}:{} {}:{}".format(SearchTags.NoteType, Wani.NoteType.Radical, Wani.RadicalFields.Radical, selected)))


def add_sentence_lookup_action(view, menu):
    selected = view.page().selectedText()
    if not selected:
        return

    suffix = (selected[:20] + '..') if len(selected) > 20 else selected
    label = f'Anki -> Sentence'
    action = menu.addAction(label)
    action.triggered.connect(lambda: lookup(
        "{}:{} {}".format(SearchTags.Tag, Mine.Tags.Sentence, selected)))


def add_listen_lookup_action(view, menu):
    selected = view.page().selectedText()
    if not selected:
        return

    suffix = (selected[:20] + '..') if len(selected) > 20 else selected
    label = f'Anki -> Listen'
    action = menu.addAction(label)
    action.triggered.connect(lambda: lookup(
        "{}:{} {}".format(SearchTags.Deck, Mine.DeckFilters.Listen, selected)))


def add_listen_sentence_lookup_action(view, menu):
    selected = view.page().selectedText()
    if not selected:
        return

    suffix = (selected[:20] + '..') if len(selected) > 20 else selected
    label = f'Anki -> Listen Sentence'
    action = menu.addAction(label)
    action.triggered.connect(lambda: lookup(
        "{}:{} {}:{} {}".format(SearchTags.Deck, Mine.DeckFilters.Listen, SearchTags.Deck, Mine.DeckFilters.Sentence,
                                selected)))


addHook("AnkiWebView.contextMenuEvent", add_vocab_lookup_action)
addHook("EditorWebView.contextMenuEvent", add_vocab_lookup_action)

addHook("AnkiWebView.contextMenuEvent", add_kanji_lookup_action)
addHook("EditorWebView.contextMenuEvent", add_kanji_lookup_action)

addHook("AnkiWebView.contextMenuEvent", add_radical_lookup_action)
addHook("EditorWebView.contextMenuEvent", add_radical_lookup_action)

addHook("AnkiWebView.contextMenuEvent", add_sentence_lookup_action)
addHook("EditorWebView.contextMenuEvent", add_sentence_lookup_action)

addHook("AnkiWebView.contextMenuEvent", add_listen_lookup_action)
addHook("EditorWebView.contextMenuEvent", add_listen_lookup_action)

addHook("AnkiWebView.contextMenuEvent", add_listen_sentence_lookup_action)
addHook("EditorWebView.contextMenuEvent", add_listen_sentence_lookup_action)
