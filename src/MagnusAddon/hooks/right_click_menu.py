# coding: utf-8
from typing import Callable

import aqt
from PyQt6.QtWidgets import QMenu
from anki.cards import Card
from aqt import mw, gui_hooks
from aqt.browser import Browser

from aqt.browser.previewer import Previewer
from aqt.editor import Editor, EditorMode
from aqt.webview import AnkiWebView, AnkiWebViewKind

from batches import local_note_updater
from sysutils.utils import UIUtils
from Note.MyNote import MyNote
from Note.WaniKanjiNote import WaniKanjiNote
from Note.WaniRadicalNote import WaniRadicalNote
from Note.WaniVocabNote import WaniVocabNote
from wanikani.utils.wani_utils import NoteUtils
from sysutils import my_clipboard, kana_utils
from urllib import parse
from aqt.utils import openLink

from wanikani.wani_constants import Wani, Mine, MyNoteFields


def add_web_lookup(menu: QMenu, name: str, url: str, search: str):
    search = parse.quote(search, encoding='utf8')
    menu.addAction(name, lambda: openLink(url % search))

def anki_lookup(text):
    browser: Browser = aqt.dialogs.open('Browser', aqt.mw)
    browser.form.searchEdit.lineEdit().setText(text)
    browser.onSearchActivated()
    UIUtils.activate_preview()


def add_lookup_action(menu: QMenu, name: str, search: str):
    menu.addAction(name, lambda: anki_lookup(search))


def add_ui_action(menu: QMenu, name: str, callback: Callable[[], None]) -> None:
    menu.addAction(name, lambda: run_ui_action(callback))


def build_radical_search_string(selected: str) -> str:
    start = f"{Wani.RadicalFields.Radical_Name}:{selected} OR"
    clauses = " OR ".join([f"{Wani.RadicalFields.Radical}:{char}" for char in selected])
    return f"note:{Wani.NoteType.Radical} ( {start} {clauses} )"


def add_kanji_primary_vocab(note: WaniKanjiNote, selection: str, _view: AnkiWebView):
    primary_vocabs = [voc for voc in [note.get_primary_vocab(), WaniKanjiNote.format_vocabulary(note, selection)] if voc]
    note.set_primary_vocab(", ".join(primary_vocabs))
    local_note_updater.update_kanji(note)


def set_kanji_primary_vocab(note: WaniKanjiNote, selection: str, view: AnkiWebView):
    note.set_primary_vocab("")
    add_kanji_primary_vocab(note, selection, view)


def run_ui_action(callback: Callable[[], None]) -> None:
    callback()
    UIUtils.refresh()


def register_lookup_actions(view: AnkiWebView, root_menu: QMenu):
    def get_card() -> MyNote:
        def get_card_inner() -> Card:
            if view.kind == AnkiWebViewKind.MAIN:
                return mw.reviewer.card
            if view.kind == AnkiWebViewKind.PREVIEWER:
                return [window for window in mw.app.topLevelWidgets() if isinstance(window, Previewer)][0].card()

        card = get_card_inner()
        if card:
            return NoteUtils.create_note(card)

    def add_sentence_lookup(menu, name: str, search):
        add_lookup_action(menu, name, f"(deck:*sentence* deck:*listen*) (Jlab-Kanji:*{search}* OR Expression:*{search}* OR Reading:*{search}*)")

    selection = view.page().selectedText().strip()
    sel_clip = selection
    if not sel_clip:
        sel_clip = my_clipboard.get_text().strip()

    note = get_card()
    if not sel_clip and not note:
        return

    note_menu = root_menu.addMenu("&Note")
    note_lookup_menu = note_menu.addMenu("&Lookup")
    note_add_menu = note_menu.addMenu("&Add")
    note_set_menu = note_menu.addMenu("&Set")

    if sel_clip:
        search_menu = root_menu.addMenu("&Search")

        search_anki_menu = search_menu.addMenu("&Anki")
        add_lookup_action(search_anki_menu, "&Kanji", f"note:{Wani.NoteType.Kanji} ( {' OR '.join([f'{Wani.KanjiFields.Kanji}:{char}' for char in sel_clip])} )")
        add_lookup_action(search_anki_menu, "&Vocab", f"deck:*Vocab* deck:*Read* (Vocab:{sel_clip} OR Reading:re:\\b{sel_clip}\\b OR Vocab_Meaning:re:\\b{sel_clip}\\b )")
        add_lookup_action(search_anki_menu, "Vocab &Wildcard", f"deck:*Vocab* deck:*Read* (Vocab:*{sel_clip}* OR Reading:*{sel_clip}* OR Vocab_Meaning:*{sel_clip}*)")
        add_lookup_action(search_anki_menu, "&Radical", build_radical_search_string(sel_clip))
        add_sentence_lookup(search_anki_menu, "&Sentence", sel_clip)
        add_lookup_action(search_anki_menu, "Listen", f"deck:{Mine.DeckFilters.Listen} {sel_clip}")

        search_web_menu = search_menu.addMenu("&Web")
        add_web_lookup(search_web_menu, "&Takoboto", u"https://takoboto.jp/?q=%s", sel_clip)
        add_web_lookup(search_web_menu, "&Merriam Webster", u"https://www.merriam-webster.com/dictionary/%s", sel_clip)
        add_web_lookup(search_web_menu, "&Immersion Kit", u"https://www.immersionkit.com/dictionary?exact=true&sort=shortness&keyword=%s", sel_clip)
        add_web_lookup(search_web_menu, "Japanese verb &conjugator", u"https://www.japaneseverbconjugator.com/VerbDetails.asp?Go=Conjugate&txtVerb=%s", sel_clip)
        add_web_lookup(search_web_menu, "&Kanshudo", u"https://www.kanshudo.com/searchw?q=%s", sel_clip)
        add_web_lookup(search_web_menu, "&Deepl", u"https://www.deepl.com/en/translator#ja/en/%s", sel_clip),
        add_web_lookup(search_web_menu, "&Jisho", u"https://jisho.org/search/%s", sel_clip)
        add_web_lookup(search_web_menu, "&Wanikani", u"https://www.wanikani.com/search?query=%s", sel_clip)
        add_web_lookup(search_web_menu, "&Verbix conjugate", u"https://www.verbix.com/webverbix/japanese/%s", sel_clip)

    if sel_clip:
        add_vocab_menu = note_add_menu.addMenu("&Vocab")
        add_ui_action(add_vocab_menu, "&1", lambda: note.set_field(MyNoteFields.Vocab1, sel_clip))
        add_ui_action(add_vocab_menu, "&2", lambda: note.set_field(MyNoteFields.Vocab2, sel_clip))
        add_ui_action(add_vocab_menu, "&3", lambda: note.set_field(MyNoteFields.Vocab3, sel_clip))
        add_ui_action(add_vocab_menu, "&4", lambda: note.set_field(MyNoteFields.Vocab4, sel_clip))
        add_ui_action(add_vocab_menu, "&5", lambda: note.set_field(MyNoteFields.Vocab5, sel_clip))

    if isinstance(note, WaniRadicalNote):
        add_lookup_action(note_lookup_menu, "&Kanji", f"note:{Wani.NoteType.Kanji} {Wani.KanjiFields.Radicals_Names}:re:\\b{note.get_radical_name()}\\b")

    if isinstance(note, WaniKanjiNote):
        kanji = note
        add_lookup_action(note_lookup_menu, "&Vocabs", f"deck:*Vocab* deck:*Read* (Vocab:*{note.get_kanji()}*)")
        radicals = [rad.strip() for rad in note.get_radicals_names().split(",")]
        radicals_clause = " OR ".join([f"{Wani.RadicalFields.Radical_Name}:{rad}" for rad in radicals])
        add_lookup_action(note_lookup_menu, "&Radicals", f"note:{Wani.NoteType.Radical} ({radicals_clause})")

        add_ui_action(note_menu, "&Hide mnemonic",lambda: kanji.override_meaning_mnemonic())
        add_ui_action(note_menu, "&Restore mnemonic", lambda: kanji.restore_meaning_mnemonic())
        add_ui_action(note_menu, "&Accept meaning", lambda: kanji.set_override_meaning(kanji.get_kanji_meaning().lower().replace(", ", "/").replace(" ", "-")))

        if selection:
            add_ui_action(note_add_menu, "&Primary vocab", lambda: add_kanji_primary_vocab(kanji, selection, view))
            add_ui_action(note_set_menu, "&Primary vocab", lambda: set_kanji_primary_vocab(kanji, selection, view))

    if isinstance(note, WaniVocabNote):
        vocab = note
        add_lookup_action(note_lookup_menu, "&Kanji", f"note:{Wani.NoteType.Kanji} ( {' OR '.join([f'{Wani.KanjiFields.Kanji}:{char}' for char in note.get_vocab()])} )")
        add_sentence_lookup(note_lookup_menu, "&Sentence", kana_utils.get_conjugation_base(vocab.get_vocab()))

        add_ui_action(note_menu, "&Hide mnemonic", lambda: vocab.override_meaning_mnemonic())
        add_ui_action(note_menu, "&Restore mnemonic", lambda: vocab.restore_meaning_mnemonic())
        add_ui_action(note_menu, "Accept &meaning", lambda: vocab.set_override_meaning(vocab.get_vocab_meaning().lower().replace(", ", "/").replace(" ", "-")))

        add_ui_action(note_set_menu, "&Meaning", lambda: vocab.set_override_meaning(sel_clip))
        add_ui_action(note_set_menu, "&Similar vocab", lambda: vocab.set_related_similar_vocab(sel_clip))
        add_ui_action(note_set_menu, "&Derived from", lambda: vocab.set_related_derived_from(sel_clip))
        add_ui_action(note_set_menu, "S&imilar meaning", lambda: vocab.set_related_similar_meaning(sel_clip))
        add_ui_action(note_set_menu, "&Homophone", lambda: vocab.set_related_homophones(sel_clip))
        add_ui_action(note_set_menu, "&Ergative twin", lambda: vocab.set_related_ergative_twin(sel_clip))

def register_show_previewer(editor: Editor):
    if editor.editorMode == EditorMode.EDIT_CURRENT:
        UIUtils.show_current_review_in_preview()
        editor.parentWindow.activateWindow()


def init():
    gui_hooks.webview_will_show_context_menu.append(register_lookup_actions)
    gui_hooks.editor_will_show_context_menu.append(register_lookup_actions)

    gui_hooks.editor_did_load_note.append(register_show_previewer)
