# coding: utf-8
from aqt.browser import Browser

from aqt.browser.previewer import Previewer
from aqt.editor import *
from aqt.webview import AnkiWebView, AnkiWebViewKind

from batches import local_note_updater
from hooks import web_search
from sysutils import my_clipboard
from sysutils.utils import StringUtils, UIUtils
from wanikani.wani_constants import Wani as wani
from wanikani.utils.wani_utils import NoteUtils
from wanikani.wanikani_note import *
from wanikani.wani_constants import *


def lookup(text):
    browser: Browser = aqt.dialogs.open('Browser', aqt.mw)
    browser.form.searchEdit.lineEdit().setText(text)
    browser.onSearchActivated()
    UIUtils.activate_preview()


def add_lookup_action(menu: QMenu, name: str, search: str):
    action = menu.addAction(name)
    action.triggered.connect(lambda: lookup(search))


def add_ui_action(menu: QMenu, name: str, callback: Callable[[], None]) -> None:
    menu.addAction(name, lambda: run_ui_action(callback))


def build_radical_search_string(selected: str) -> str:
    start = f"{Wani.RadicalFields.Radical_Name}:{selected} OR"
    clauses = " OR ".join([f"{Wani.RadicalFields.Radical}:{char}" for char in selected])
    return f"note:{Wani.NoteType.Radical} ( {start} {clauses} )"


def add_kanji_primary_vocab(note: WaniKanjiNote, selection: str, view: AnkiWebView):
    def format_vocab() -> str:
        readings = f"{note.get_reading_kun()}, {note.get_reading_on()}"
        readings_list = [s.split(".")[0].strip() for s in (StringUtils.strip_markup(readings).split(","))]
        readings_list.sort(key=len, reverse=True)
        for reading in readings_list:
            if reading and reading in selection:
                return selection.replace(reading, f"<read>{reading}</read>", 1)
        return selection

    primary_vocabs = [voc for voc in [note.get_PrimaryVocab(), format_vocab()] if voc]
    note.set_PrimaryVocab(", ".join(primary_vocabs))
    local_note_updater.update_kanji(note)


def set_kanji_primary_vocab(note: WaniKanjiNote, selection: str, view: AnkiWebView):
    note.set_PrimaryVocab("")
    add_kanji_primary_vocab(note, selection, view)


def run_ui_action(callback: Callable[[], None]) -> None:
    callback()
    UIUtils.refresh()


def register_lookup_actions(view: AnkiWebView, root_menu: QMenu):
    def get_note() -> MyNote:
        def get_note() -> Note:
            if view.kind == AnkiWebViewKind.MAIN:
                return mw.reviewer.card.note()
            if view.kind == AnkiWebViewKind.PREVIEWER:
                return [window for window in mw.app.topLevelWidgets() if isinstance(window, Previewer)][0].card().note()

        note = get_note()
        if note:
            return NoteUtils.create_note(note)

    selection = view.page().selectedText().strip()
    selection_or_clipboard = selection
    if not selection_or_clipboard:
        selection_or_clipboard = my_clipboard.get_text().strip()

    note = get_note()
    if not selection_or_clipboard and not note:
        return

    menu = root_menu.addMenu("&Anki Search")

    if selection_or_clipboard:
        add_lookup_action(menu, "&Kanji",
                          f"note:{wani.NoteType.Kanji} ( {' OR '.join([f'{wani.KanjiFields.Kanji}:{char}' for char in selection_or_clipboard])} )")

        add_lookup_action(menu, "Vocab &Wildcard", f"deck:*Vocab* deck:*Read* (Vocab:*{selection_or_clipboard}* OR Reading:*{selection_or_clipboard}* OR Vocab_Meaning:*{selection_or_clipboard}*)")
        add_lookup_action(menu, "&Vocab Exact", f"deck:*Vocab* deck:*Read* (Vocab:{selection_or_clipboard} OR Reading:{selection_or_clipboard} OR Vocab_Meaning:{selection_or_clipboard} )")
        add_lookup_action(menu, "&Radical", build_radical_search_string(selection_or_clipboard))
        add_lookup_action(menu, "&Sentence", f"tag:{Mine.Tags.Sentence} {selection_or_clipboard}")
        add_lookup_action(menu, "Listen", f"deck:{Mine.DeckFilters.Listen} {selection_or_clipboard}")
        add_lookup_action(menu, "&Listen Sentence",
                          f"(deck:*sentence* deck:*listen*) (Jlab-Kanji:*{selection_or_clipboard}* OR Expression:*{selection_or_clipboard}* OR Reading:*{selection_or_clipboard}*)")
        # add_lookup_action(menu, "Listen Sentence Reading", f"(deck:*sentence* deck:*listen*) (Jlab-Hiragana:*{selection_or_clipboard}* OR Reading:*{selection_or_clipboard}*)")

    if selection_or_clipboard:
        actions_menu = root_menu.addMenu("&Generic Actions")
        add_ui_action(actions_menu, "Add Vocab &1", lambda: note.set_field(MyNoteFields.Vocab1, selection_or_clipboard))
        add_ui_action(actions_menu, "Add Vocab &2", lambda: note.set_field(MyNoteFields.Vocab2, selection_or_clipboard))
        add_ui_action(actions_menu, "Add Vocab &3", lambda: note.set_field(MyNoteFields.Vocab3, selection_or_clipboard))
        add_ui_action(actions_menu, "Add Vocab &4", lambda: note.set_field(MyNoteFields.Vocab4, selection_or_clipboard))
        add_ui_action(actions_menu, "Add Vocab &5", lambda: note.set_field(MyNoteFields.Vocab5, selection_or_clipboard))

    if isinstance(note, WaniRadicalNote):
        radical_menu = root_menu.addMenu("&Radical Actions")
        add_lookup_action(radical_menu, "Radical &Kanji", f"note:{wani.NoteType.Kanji} {Wani.KanjiFields.Radicals_Names}:re:\\b{note.get_radical_name()}\\b")

    if isinstance(note, WaniKanjiNote):
        kanji = note
        kanji_menu = root_menu.addMenu("&Kanji Actions")
        add_lookup_action(kanji_menu, "Kanji &Vocabs", f"deck:*Vocab* deck:*Read* (Vocab:*{note.get_kanji()}*)")
        radicals = [rad.strip() for rad in note.get_radicals_names().split(",")]
        radicals_clause = " OR ".join([f"{Wani.RadicalFields.Radical_Name}:{rad}" for rad in radicals])
        add_lookup_action(kanji_menu, "Kanji &Radicals", f"note:{Wani.NoteType.Radical} ({radicals_clause})")

        kanji_menu.addAction("&Hide mnemonic", lambda: run_ui_action(lambda: kanji.override_meaning_mnemonic()))
        kanji_menu.addAction("&Restore mnemonic", lambda: run_ui_action(lambda: kanji.restore_meaning_mnemonic()))

        add_ui_action(kanji_menu, "&Accept meaning", lambda: kanji.set_Override_meaning(kanji.get_kanji_meaning().lower().replace(",", "/").replace(" ", "")))

        if selection:
            kanji_menu.addAction("&Add primary vocab").triggered.connect(lambda: add_kanji_primary_vocab(kanji, selection, view))
            kanji_menu.addAction("&Set primary vocab").triggered.connect(lambda: set_kanji_primary_vocab(kanji, selection, view))

    if isinstance(note, WaniVocabNote):
        vocab = note
        vocab_menu = root_menu.addMenu("&Vocab Actions")
        add_lookup_action(vocab_menu, "Vocab &Kanji", f"note:{wani.NoteType.Kanji} ( {' OR '.join([f'{wani.KanjiFields.Kanji}:{char}' for char in note.get_vocab()])} )")

        add_ui_action(vocab_menu, "&Hide mnemonic", lambda: vocab.override_meaning_mnemonic())
        add_ui_action(vocab_menu, "&Restore mnemonic", lambda: vocab.restore_meaning_mnemonic())
        add_ui_action(vocab_menu, "&Accept meaning", lambda: vocab.set_Override_meaning(vocab.get_vocab_meaning().lower().replace(",", "/").replace(" ", "")))
        add_ui_action(vocab_menu, "Set similar &vocab", lambda: vocab.set_related_similar_vocab(selection_or_clipboard))
        add_ui_action(vocab_menu, "Set &derived from", lambda: vocab.set_related_derived_from(selection_or_clipboard))
        add_ui_action(vocab_menu, "Set &similar meaning", lambda: vocab.set_related_similar_meaning(selection_or_clipboard))
        add_ui_action(vocab_menu, "Set homo&phone", lambda: vocab.set_related_homophones(selection_or_clipboard))
        add_ui_action(vocab_menu, "Set &ergative twin", lambda: vocab.set_related_ergative_twin(selection_or_clipboard))


def register_show_previewer(editor: Editor):
    if editor.editorMode == EditorMode.EDIT_CURRENT:
        UIUtils.show_current_review_in_preview()
        editor.parentWindow.activateWindow()


def init():
    gui_hooks.webview_will_show_context_menu.append(web_search.add_lookup_action)
    gui_hooks.editor_will_show_context_menu.append(web_search.add_lookup_action)

    gui_hooks.webview_will_show_context_menu.append(register_lookup_actions)
    gui_hooks.editor_will_show_context_menu.append(register_lookup_actions)

    gui_hooks.editor_did_load_note.append(register_show_previewer)