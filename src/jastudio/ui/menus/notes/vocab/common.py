from __future__ import annotations

from typing import TYPE_CHECKING

from sysutils.typed import non_optional
from ui.menus.menu_utils import shortcutfinger
from ui.menus.menu_utils.ex_qmenu import create_vocab_note_action

if TYPE_CHECKING:
    from jastudio.note.vocabulary.vocabnote import VocabNote
    from PyQt6.QtWidgets import QMenu

def build_create_prefix_postfix_note_menu(prefix_postfix_note_menu: QMenu, vocab: VocabNote, addendum: str) -> None:
    def create_suffix_note_menu(suffix_note_menu: QMenu) -> None:
        create_vocab_note_action(suffix_note_menu, shortcutfinger.home1("dictionary-form"), lambda: vocab.cloner.create_suffix_version(addendum))
        create_vocab_note_action(suffix_note_menu, shortcutfinger.home2(f"い-stem {vocab.cloner.suffix_to_i_stem_preview(addendum)}"), lambda: vocab.cloner.suffix_to_i_stem(addendum))
        create_vocab_note_action(suffix_note_menu, shortcutfinger.home3(f"て-stem  {vocab.cloner.suffix_to_te_stem_preview(addendum)}"), lambda: vocab.cloner.suffix_to_te_stem(addendum))
        create_vocab_note_action(suffix_note_menu, shortcutfinger.home4(f"え-stem  {vocab.cloner.suffix_to_e_stem_preview(addendum)}"), lambda: vocab.cloner.suffix_to_e_stem(addendum))
        create_vocab_note_action(suffix_note_menu, shortcutfinger.home5(f"あ-stem  {vocab.cloner.suffix_to_a_stem_preview(addendum)}"), lambda: vocab.cloner.suffix_to_a_stem(addendum))
        create_vocab_note_action(suffix_note_menu, shortcutfinger.up1(f"chop-1  {vocab.cloner.suffix_to_chopped_preview(addendum, 1)}"), lambda: vocab.cloner.suffix_to_chopped(addendum, 1))
        create_vocab_note_action(suffix_note_menu, shortcutfinger.up1(f"chop-2  {vocab.cloner.suffix_to_chopped_preview(addendum, 2)}"), lambda: vocab.cloner.suffix_to_chopped(addendum, 2))
        create_vocab_note_action(suffix_note_menu, shortcutfinger.up1(f"chop-3  {vocab.cloner.suffix_to_chopped_preview(addendum, 3)}"), lambda: vocab.cloner.suffix_to_chopped(addendum, 3))
        create_vocab_note_action(suffix_note_menu, shortcutfinger.up1(f"chop-4  {vocab.cloner.suffix_to_chopped_preview(addendum, 4)}"), lambda: vocab.cloner.suffix_to_chopped(addendum, 4))

    def create_prefix_note_menu(prefix_note_menu: QMenu) -> None:
        create_vocab_note_action(prefix_note_menu, shortcutfinger.home1(f"Dictionary form: {addendum}{vocab.get_question()}"), lambda: vocab.cloner.prefix_to_dictionary_form(addendum))
        create_vocab_note_action(prefix_note_menu, shortcutfinger.home2(f"chop-1  {vocab.cloner.prefix_to_chopped_preview(addendum, 1)}"), lambda: vocab.cloner.prefix_to_chopped(addendum, 1))
        create_vocab_note_action(prefix_note_menu, shortcutfinger.home3(f"chop-2  {vocab.cloner.prefix_to_chopped_preview(addendum, 2)}"), lambda: vocab.cloner.prefix_to_chopped(addendum, 2))
        create_vocab_note_action(prefix_note_menu, shortcutfinger.home4(f"chop-3  {vocab.cloner.prefix_to_chopped_preview(addendum, 3)}"), lambda: vocab.cloner.prefix_to_chopped(addendum, 3))

    create_prefix_note_menu(non_optional(prefix_postfix_note_menu.addMenu(shortcutfinger.home1("Prefix-onto"))))
    create_suffix_note_menu(non_optional(prefix_postfix_note_menu.addMenu(shortcutfinger.home2("Suffix-onto"))))
