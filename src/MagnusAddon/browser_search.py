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
from magnus.wanikani_note import *
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
    def get_note() -> WaniNote:
        def get_note() -> Note:
            if view.kind == AnkiWebViewKind.MAIN:
                return mw.reviewer.card.note()
            if view.kind == AnkiWebViewKind.PREVIEWER:
                return [window for window in mw.app.topLevelWidgets() if isinstance(window, Previewer)][0].card().note()

        note = get_note()
        if note:
            return NoteUtils.create_note(note)

        return None

    selected = view.page().selectedText().strip()
    if not selected:
        selected = my_clipboard.get_text()

    note = get_note()
    if not selected and not note:
        return

    menu = root_menu.addMenu("Anki Search")

    if isinstance(note, WaniKanjiNote):
        add_lookup_action(menu, "Kanji Vocabs", f"deck:*Vocab* deck:*Read* (Vocab:*{note.get_kanji()}*)")
        radicals = [rad.strip() for rad in note.get_radicals_names().split(",")]
        radicals_clause = " OR ".join([f"{Wani.RadicalFields.Radical_Name}:{rad}" for rad in radicals])
        add_lookup_action(menu, "Kanji Radicals", f"note:{Wani.NoteType.Radical} ({radicals_clause})")

    if isinstance(note, WaniVocabNote):
        add_lookup_action(menu, "Vocab Kanji",
                          f"note:{wani.NoteType.Kanji} ( {' OR '.join([f'{wani.KanjiFields.Kanji}:{char}' for char in note.get_kanji()])} )")

    if isinstance(note, WaniRadicalNote):
        radicals_names = f""

        add_lookup_action(menu, "Radical Kanji",
                          f"note:{wani.NoteType.Kanji} {Wani.KanjiFields.Radicals_Names}:re:\\b{note.get_radical_name()}\\b")

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