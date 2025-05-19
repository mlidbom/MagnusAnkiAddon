from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from hooks import shortcutfinger
from hooks.right_click_menu_note_vocab_common import build_create_prefix_postfix_note_menu
from hooks.right_click_menu_utils import add_ui_action
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from note.sentences.sentencenote import SentenceNote
    from note.vocabulary.vocabnote import VocabNote
    from PyQt6.QtWidgets import QMenu

def build_string_menu(string_menu: QMenu, vocab: VocabNote, menu_string: str) -> None:
    def build_sentences_menu(sentence_menu: QMenu) -> None:
        def remove_highlight_from_sentences() -> None:
            for sent in sentences: sent.configuration.remove_highlighted_word(vocab.get_question())

        def mark_as_incorrect_match_in_sentences() -> None:
            for sent in sentences: sent.configuration.incorrect_matches.add_global(vocab.get_question())

        has_sentences = len(sentences) > 0

        add_ui_action(sentence_menu, shortcutfinger.home1("Add Highlight"),
                      lambda: sentences[0].configuration.position_highlighted_word(vocab.get_question()),
                      has_sentences and vocab.get_question() not in sentences[0].configuration.highlighted_words())
        add_ui_action(sentence_menu, shortcutfinger.home2("Remove highlight"),
                      lambda: remove_highlight_from_sentences(),
                      has_sentences and vocab.get_question() in sentences[0].configuration.highlighted_words())
        add_ui_action(sentence_menu, shortcutfinger.home3("Remove-sentence: Mark as incorrect match in sentence"),
                      lambda: mark_as_incorrect_match_in_sentences(),
                      has_sentences)

    def build_add_menu(vocab_add_menu: QMenu) -> None:
        def build_add_rule_menu(add_rule_menu: QMenu) -> None:
            add_ui_action(add_rule_menu, shortcutfinger.home1("Surface is not"), lambda: vocab.matching_rules.rules.surface_is_not.add(menu_string), menu_string not in vocab.matching_rules.rules.surface_is_not.get())
            add_ui_action(add_rule_menu, shortcutfinger.home2("Prefer over base"), lambda: vocab.matching_rules.rules.prefer_over_base.add(menu_string), menu_string not in vocab.matching_rules.rules.prefer_over_base.get())
            add_ui_action(add_rule_menu, shortcutfinger.home3("Prefix is not"), lambda: vocab.matching_rules.rules.prefix_is_not.add(menu_string), menu_string not in vocab.matching_rules.rules.prefix_is_not.get())
            add_ui_action(add_rule_menu, shortcutfinger.home4("Required prefix"), lambda: vocab.matching_rules.rules.required_prefix.add(menu_string), menu_string not in vocab.matching_rules.rules.required_prefix.get())

        add_ui_action(vocab_add_menu, shortcutfinger.home1("Similar meaning"), lambda: vocab.related_notes.synonyms.add(menu_string))
        add_ui_action(vocab_add_menu, shortcutfinger.home2("Confused with"), lambda: vocab.related_notes.confused_with.add(menu_string))
        build_add_rule_menu(non_optional(vocab_add_menu.addMenu(shortcutfinger.home3("Rule"))))

    def build_remove_menu(vocab_remove_menu: QMenu) -> None:
        def build_remove_rule_menu(remove_rule_menu: QMenu) -> None:
            add_ui_action(remove_rule_menu, shortcutfinger.home1("Surface is not"), lambda: vocab.matching_rules.rules.surface_is_not.remove(menu_string), menu_string in vocab.matching_rules.rules.surface_is_not.get())
            add_ui_action(remove_rule_menu, shortcutfinger.home2("Prefer over base"), lambda: vocab.matching_rules.rules.prefer_over_base.remove(menu_string), menu_string in vocab.matching_rules.rules.prefer_over_base.get())
            add_ui_action(remove_rule_menu, shortcutfinger.home3("Prefix is not"), lambda: vocab.matching_rules.rules.prefix_is_not.remove(menu_string), menu_string in vocab.matching_rules.rules.prefix_is_not.get())
            add_ui_action(remove_rule_menu, shortcutfinger.home4("Required prefix"), lambda: vocab.matching_rules.rules.required_prefix.remove(menu_string), menu_string in vocab.matching_rules.rules.required_prefix.get())

        add_ui_action(vocab_remove_menu, shortcutfinger.home1("Similar meaning"), lambda: vocab.related_notes.synonyms.remove(menu_string), menu_string in vocab.related_notes.synonyms.strings())
        add_ui_action(vocab_remove_menu, shortcutfinger.home2("Confused with"), lambda: vocab.related_notes.confused_with.remove(menu_string), menu_string in vocab.related_notes.confused_with.get())
        add_ui_action(vocab_remove_menu, shortcutfinger.home3("Derived from"), lambda: vocab.related_notes.derived_from.clear(), menu_string == vocab.related_notes.derived_from.get())
        add_ui_action(vocab_remove_menu, shortcutfinger.home4("Ergative twin"), lambda: vocab.related_notes.ergative_twin.remove(), menu_string == vocab.related_notes.ergative_twin.get())
        build_remove_rule_menu(non_optional(vocab_remove_menu.addMenu(shortcutfinger.home5("Rule"))))

    def build_set_menu(note_set_menu: QMenu) -> None:
        add_ui_action(note_set_menu, shortcutfinger.home1("Derived from"), lambda: vocab.related_notes.derived_from.set(menu_string))
        add_ui_action(note_set_menu, shortcutfinger.home2("Ergative twin"), lambda: vocab.related_notes.ergative_twin.set(menu_string))

    sentences = app.col().sentences.with_question(menu_string)

    build_add_menu(non_optional(string_menu.addMenu(shortcutfinger.home1("Add"))))
    build_set_menu(non_optional(string_menu.addMenu(shortcutfinger.home2("Set"))))
    build_remove_menu(non_optional(string_menu.addMenu(shortcutfinger.home3("Remove"))))
    build_sentences_menu(non_optional(string_menu.addMenu(shortcutfinger.home4("Sentence"))))
    build_create_prefix_postfix_note_menu(non_optional(string_menu.addMenu(shortcutfinger.up1(f"Create combined {menu_string}"))), vocab, menu_string)
