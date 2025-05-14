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
        def remove_highlight(_sentences: list[SentenceNote]) -> None:
            for _sentence in _sentences:
                _sentence.configuration.remove_highlighted_word(vocab.get_question())

        def exclude(_sentences: list[SentenceNote]) -> None:
            for _sentence in _sentences:
                _sentence.configuration.incorrect_matches.add_global(vocab.get_question())

        if not sentences: return

        sentence = sentences[0]

        if vocab.get_question() not in sentence.configuration.highlighted_words():
            add_ui_action(sentence_menu, shortcutfinger.home1("Add Highlight"), lambda _sentence=sentence: _sentence.configuration.position_highlighted_word(vocab.get_question()))
        else:
            # noinspection PyDefaultArgument
            add_ui_action(sentence_menu, shortcutfinger.home2("Remove highlight"), lambda _sentences=sentences: remove_highlight(_sentences))

        # noinspection PyDefaultArgument
        add_ui_action(sentence_menu, shortcutfinger.home3("Exclude this vocab"), lambda _sentences=sentences: exclude(_sentences))

    def build_add_menu(vocab_add_menu: QMenu) -> None:
        add_ui_action(vocab_add_menu, shortcutfinger.home1("Similar meaning"), lambda: vocab.related_notes.add_similar_meaning(menu_string))
        add_ui_action(vocab_add_menu, shortcutfinger.home2("Confused with"), lambda: vocab.related_notes.confused_with.add(menu_string))

    def build_remove_menu(vocab_remove_menu: QMenu) -> None:
        if menu_string in vocab.related_notes.similar_meanings():
            add_ui_action(vocab_remove_menu, shortcutfinger.home1("Similar meaning"), lambda: vocab.related_notes.remove_similar_meaning(menu_string))

        if menu_string in vocab.related_notes.confused_with.get():
            add_ui_action(vocab_remove_menu, shortcutfinger.home2("Confused with"), lambda: vocab.related_notes.remove_confused_with(menu_string))

    def build_set_menu(note_set_menu: QMenu) -> None:
        add_ui_action(note_set_menu, shortcutfinger.home1("Derived from"), lambda: vocab.related_notes.derived_from.set(menu_string))
        add_ui_action(note_set_menu, shortcutfinger.home2("Ergative twin"), lambda: vocab.related_notes.set_ergative_twin(menu_string))

    sentences = app.col().sentences.with_question(menu_string)

    build_sentences_menu(non_optional(string_menu.addMenu(shortcutfinger.home1("Sentence"))))
    build_add_menu(non_optional(string_menu.addMenu(shortcutfinger.home2("Add"))))
    build_set_menu(non_optional(string_menu.addMenu(shortcutfinger.home3("Set"))))
    build_remove_menu(non_optional(string_menu.addMenu(shortcutfinger.home4("Remove"))))
    build_create_prefix_postfix_note_menu(non_optional(string_menu.addMenu(shortcutfinger.up1(f"Create combined {menu_string}"))), vocab, menu_string)
