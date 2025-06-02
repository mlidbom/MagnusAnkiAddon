from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from sysutils.typed import non_optional
from ui.menus.menu_utils import shortcutfinger
from ui.menus.menu_utils.ex_qmenu import create_vocab_note_action
from ui.menus.notes.vocab.common import build_create_prefix_postfix_note_menu

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from PyQt6.QtWidgets import QMenu

def build_create_note_menu(note_create_menu: QMenu, vocab: VocabNote, selection: str, clipboard: str) -> None:
    def build_forms_menu(clone_to_form_menu: QMenu) -> None:
        forms_with_no_vocab = [form for form in vocab.forms.all_set() if not any(app.col().vocab.with_question(form))]

        def add_clone_to_form_action(title:str, form:str) -> None:
            create_vocab_note_action(clone_to_form_menu, title, lambda: vocab.cloner.clone_to_form(form))

        for index, form in enumerate(forms_with_no_vocab):
            add_clone_to_form_action(shortcutfinger.numpad(index, form), form)

    def build_noun_variations_menu(noun_menu: QMenu) -> None:
        create_vocab_note_action(noun_menu, shortcutfinger.home1("する-verb"), lambda: vocab.cloner.create_suru_verb())
        create_vocab_note_action(noun_menu, shortcutfinger.home2("します-verb"), lambda: vocab.cloner.create_shimasu_verb())
        create_vocab_note_action(noun_menu, shortcutfinger.home3("な-adjective"), lambda: vocab.cloner.create_na_adjective())
        create_vocab_note_action(noun_menu, shortcutfinger.home4("の-adjective"), lambda: vocab.cloner.create_no_adjective())
        create_vocab_note_action(noun_menu, shortcutfinger.up1("に-adverb"), lambda: vocab.cloner.create_ni_adverb())
        create_vocab_note_action(noun_menu, shortcutfinger.up2("と-adverb"), lambda: vocab.cloner.create_to_adverb())

    def build_verb_variations_menu(verb_menu: QMenu) -> None:
        create_vocab_note_action(verb_menu, shortcutfinger.home1("ます-form"), lambda: vocab.cloner.create_masu_form())
        create_vocab_note_action(verb_menu, shortcutfinger.home2("て-form"), lambda: vocab.cloner.create_te_form())
        create_vocab_note_action(verb_menu, shortcutfinger.home3("た-form"), lambda: vocab.cloner.create_ta_form())
        create_vocab_note_action(verb_menu, shortcutfinger.home4("ない-form"), lambda: vocab.cloner.create_nai_form())

    def build_misc_menu(misc_menu: QMenu) -> None:
        create_vocab_note_action(misc_menu, shortcutfinger.home1("く-form-of-い-adjective"), lambda: vocab.cloner.create_ku_form())
        create_vocab_note_action(misc_menu, shortcutfinger.home2("て-prefixed"), lambda: vocab.cloner.create_te_prefixed_word())
        create_vocab_note_action(misc_menu, shortcutfinger.home3("お-prefixed"), lambda: vocab.cloner.create_o_prefixed_word())
        create_vocab_note_action(misc_menu, shortcutfinger.home4("ん-suffixed"), lambda: vocab.cloner.create_n_suffixed_word())
        create_vocab_note_action(misc_menu, shortcutfinger.home5("か-suffixed"), lambda: vocab.cloner.create_ka_suffixed_word())

    build_forms_menu(non_optional(note_create_menu.addMenu(shortcutfinger.home1("Clone to form"))))
    build_noun_variations_menu(non_optional(note_create_menu.addMenu(shortcutfinger.home2("Noun variations"))))
    build_verb_variations_menu(non_optional(note_create_menu.addMenu(shortcutfinger.home3("Verb variations"))))
    build_misc_menu(non_optional(note_create_menu.addMenu(shortcutfinger.home4("Misc"))))

    if selection:
        build_create_prefix_postfix_note_menu(non_optional(note_create_menu.addMenu(shortcutfinger.up1("Selection"))), vocab, selection)

    if selection:
        pass

    if clipboard:
        build_create_prefix_postfix_note_menu(non_optional(note_create_menu.addMenu(shortcutfinger.up2("Clipboard"))), vocab, clipboard)
