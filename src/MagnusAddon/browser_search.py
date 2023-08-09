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

#Works sometimes, unsure of the pattern.
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
    def get_kanji_vocabs() -> list[str]:
        def get_note() -> Note:
            if view.kind == AnkiWebViewKind.MAIN:
                return mw.reviewer.card.note()
            if view.kind == AnkiWebViewKind.PREVIEWER:
                return [window for window in mw.app.topLevelWidgets() if isinstance(window, Previewer)][0].card().note()

        note = get_note()
        if NoteUtils.get_note_type(note) == Wani.NoteType.Kanji:
            return WaniKanjiNote(note).get_vocabs_raw()

        return None

    selected = view.page().selectedText().strip()
    if not selected:
        selected = my_clipboard.get_text()

    kanji_vocabs = get_kanji_vocabs()

    if not selected and not kanji_vocabs:
        return

    menu = root_menu.addMenu("Anki Search")

    if kanji_vocabs:
        add_lookup_action(menu, "Kanji Vocabs",
                          f"note:{Wani.NoteType.Vocab} ( {' OR '.join([f'{Wani.VocabFields.Vocab}:{vocab}' for vocab in kanji_vocabs])} )")

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