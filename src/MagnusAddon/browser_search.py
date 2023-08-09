# coding: utf-8
import aqt
from anki.cards import *
from aqt.browser import Browser

from aqt import *
from aqt.browser.previewer import Previewer
from aqt.webview import AnkiWebView, AnkiWebViewKind

from magnus import my_clipboard
from magnus.wani_constants import Wani as wani
from magnus.wani_utils import NoteUtils
from magnus.wanikani_note import WaniKanjiNote
from .magnus.wani_constants import *


def lookup(text):
    browser: Browser = aqt.dialogs.open('Browser', aqt.mw)
    browser.form.searchEdit.lineEdit().setText(text)
    browser.onSearchActivated()

    mw.app.processEvents()
    if browser._previewer is None:
        browser.onTogglePreview()

    else:
        browser._previewer.activateWindow()


def add_lookup_action(menu:QMenu, name: str, search:str):
    action = menu.addAction(name)
    action.triggered.connect(lambda: lookup(search))


def build_radical_search_string(selected: str) -> str:
    start = f"{Wani.RadicalFields.Radical_Name}:{selected} OR"
    clauses = " OR ".join([f"{Wani.RadicalFields.Radical}:{char}" for char in selected])
    return f"note:{Wani.NoteType.Radical} ( {start} {clauses} )"

def register_lookup_actions(view: AnkiWebView, root_menu: QMenu):
    def get_kanji_note() -> WaniKanjiNote:
        def get_note() -> Note:
            if view.kind == AnkiWebViewKind.MAIN:
                return mw.reviewer.card.note()
            if view.kind == AnkiWebViewKind.PREVIEWER:
                return [window for window in mw.app.topLevelWidgets() if isinstance(window, Previewer)][0].card().note()

        note = get_note()
        if NoteUtils.get_note_type(note) == Wani.NoteType.Kanji:
            return WaniKanjiNote(note)

        return None

    selected = view.page().selectedText().strip()
    if not selected:
        selected = my_clipboard.get_text()

    kanji_note = get_kanji_note()

    if not selected and not kanji_note:
        return

    menu = root_menu.addMenu("Anki Search")

    if kanji_note:
        kanji = kanji_note.get_kanji()
        add_lookup_action(menu, "Kanji Vocabs", f"deck:*Vocab* deck:*Read* (Vocab:*{kanji}*)")

    if selected:
        add_lookup_action(menu, "Kanji",
                          f"note:{wani.NoteType.Kanji} ( {' OR '.join([f'{wani.KanjiFields.Kanji}:{char}' for char in selected])} )")

        add_lookup_action(menu, "Vocab Wildcard" , f"deck:*Vocab* deck:*Read* (Vocab:*{selected}* OR Reading:*{selected}* OR Vocab_Meaning:*{selected}*)")
        add_lookup_action(menu, "Vocab Exact", f"deck:*Vocab* deck:*Read* (Vocab:{selected} OR Reading:{selected} OR Vocab_Meaning:{selected} )")
        add_lookup_action(menu, "Radical", build_radical_search_string(selected))
        add_lookup_action(menu, "Sentence", f"tag:{Mine.Tags.Sentence} {selected}")
        add_lookup_action(menu, "Listen", f"deck:{Mine.DeckFilters.Listen} {selected}")
        add_lookup_action(menu, "Listen Sentence", f"(deck:*sentence* deck:*listen*) (Jlab-Kanji:*{selected}* OR Expression:*{selected}*)")
        add_lookup_action(menu, "Listen Sentence Reading", f"(deck:*sentence* deck:*listen*) (Jlab-Hiragana:*{selected}* OR Reading:*{selected}*)")

gui_hooks.webview_will_show_context_menu.append(register_lookup_actions)
gui_hooks.editor_will_show_context_menu.append(register_lookup_actions)