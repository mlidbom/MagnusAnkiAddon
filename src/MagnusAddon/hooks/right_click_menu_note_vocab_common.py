from __future__ import annotations

from typing import TYPE_CHECKING

from hooks import shortcutfinger
from hooks.right_click_menu_utils import create_vocab_note_action
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from PyQt6.QtWidgets import QMenu


def build_create_prefix_postfix_note_menu(prefix_postfix_note_menu: QMenu, vocab: VocabNote, addendum: str) -> None:
    def create_suffix_note_menu(suffix_note_menu: QMenu) -> None:
        create_vocab_note_action(suffix_note_menu, shortcutfinger.home1("dictionary-form"), lambda: vocab.cloner.create_suffix_version(addendum))
        create_vocab_note_action(suffix_note_menu, shortcutfinger.home2("い-stem"), lambda: vocab.cloner.suffix_to_i_stem(addendum))
        create_vocab_note_action(suffix_note_menu, shortcutfinger.home3("て-stem"), lambda: vocab.cloner.suffix_to_te_stem(addendum))
        create_vocab_note_action(suffix_note_menu, shortcutfinger.home4("え-stem"), lambda: vocab.cloner.suffix_to_e_stem(addendum))
        create_vocab_note_action(suffix_note_menu, shortcutfinger.up1("あ-stem"), lambda: vocab.cloner.suffix_to_a_stem(addendum))

    create_vocab_note_action(prefix_postfix_note_menu, shortcutfinger.home1(f"prefix-{addendum}{vocab.get_question()}"), lambda: vocab.cloner.create_prefix_version(addendum))

    create_suffix_note_menu(non_optional(prefix_postfix_note_menu.addMenu(shortcutfinger.home2("Suffix-onto"))))
