# coding: utf-8
import aqt
from anki.cards import *
from aqt.browser import Browser

from aqt import *
from aqt.browser.previewer import Previewer
from aqt.reviewer import RefreshNeeded
from aqt.webview import AnkiWebView, AnkiWebViewKind

from magnus import my_clipboard
from magnus.utils import StringUtils, UIUtils
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


def set_kanji_primary_vocab(note: WaniKanjiNote, selection:str, view: AnkiWebView):
    def try_format_vocab(readings:str):
        markup_stripped = StringUtils.strip_markup(readings)
        split_to_list = markup_stripped.split(",")
        stripped_okurigana = [s.split(".")[0].strip() for s in split_to_list]
        for reading in stripped_okurigana:
            if reading and reading in selection:
                note.set_PrimaryVocab(selection.replace(reading, f"<read>{reading}</read>"))
                return True
        return False

    if not try_format_vocab(note.get_reading_kun()) and not try_format_vocab(note.get_reading_on()):
        note.set_PrimaryVocab(selection)

    #lookup(f"note:{wani.NoteType.Kanji} {wani.KanjiFields.Kanji}:{note.get_kanji()}")
    UIUtils.refresh(view)

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

    selection = view.page().selectedText().strip()
    selection_or_clipboard = selection
    if not selection_or_clipboard:
        selection_or_clipboard = my_clipboard.get_text().strip()

    note = get_note()
    if not selection_or_clipboard and not note:
        return

    menu = root_menu.addMenu("Anki Search")

    if isinstance(note, WaniKanjiNote):
        add_lookup_action(menu, "Kanji Vocabs", f"deck:*Vocab* deck:*Read* (Vocab:*{note.get_kanji()}*)")
        radicals = [rad.strip() for rad in note.get_radicals_names().split(",")]
        radicals_clause = " OR ".join([f"{Wani.RadicalFields.Radical_Name}:{rad}" for rad in radicals])
        add_lookup_action(menu, "Kanji Radicals", f"note:{Wani.NoteType.Radical} ({radicals_clause})")

        if selection:
            kanji_menu = root_menu.addMenu("Kanji Actions")
            kanji_menu.addAction("Set primary vocab").triggered.connect(lambda: set_kanji_primary_vocab(note, selection, view) )

    if isinstance(note, WaniVocabNote):
        add_lookup_action(menu, "Vocab Kanji",
                          f"note:{wani.NoteType.Kanji} ( {' OR '.join([f'{wani.KanjiFields.Kanji}:{char}' for char in note.get_kanji()])} )")

    if isinstance(note, WaniRadicalNote):
        radicals_names = f""

        add_lookup_action(menu, "Radical Kanji",
                          f"note:{wani.NoteType.Kanji} {Wani.KanjiFields.Radicals_Names}:re:\\b{note.get_radical_name()}\\b")

    if selection_or_clipboard:
        add_lookup_action(menu, "Kanji",
                          f"note:{wani.NoteType.Kanji} ( {' OR '.join([f'{wani.KanjiFields.Kanji}:{char}' for char in selection_or_clipboard])} )")

        add_lookup_action(menu, "Vocab Wildcard" , f"deck:*Vocab* deck:*Read* (Vocab:*{selection_or_clipboard}* OR Reading:*{selection_or_clipboard}* OR Vocab_Meaning:*{selection_or_clipboard}*)")
        add_lookup_action(menu, "Vocab Exact", f"deck:*Vocab* deck:*Read* (Vocab:{selection_or_clipboard} OR Reading:{selection_or_clipboard} OR Vocab_Meaning:{selection_or_clipboard} )")
        add_lookup_action(menu, "Radical", build_radical_search_string(selection_or_clipboard))
        add_lookup_action(menu, "Sentence", f"tag:{Mine.Tags.Sentence} {selection_or_clipboard}")
        add_lookup_action(menu, "Listen", f"deck:{Mine.DeckFilters.Listen} {selection_or_clipboard}")
        add_lookup_action(menu, "Listen Sentence", f"(deck:*sentence* deck:*listen*) (Jlab-Kanji:*{selection_or_clipboard}* OR Expression:*{selection_or_clipboard}*)")
        add_lookup_action(menu, "Listen Sentence Reading", f"(deck:*sentence* deck:*listen*) (Jlab-Hiragana:*{selection_or_clipboard}* OR Reading:*{selection_or_clipboard}*)")

gui_hooks.webview_will_show_context_menu.append(register_lookup_actions)
gui_hooks.editor_will_show_context_menu.append(register_lookup_actions)