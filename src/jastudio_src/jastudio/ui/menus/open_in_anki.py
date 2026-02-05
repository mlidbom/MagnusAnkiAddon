from __future__ import annotations

from typing import TYPE_CHECKING

from jaspythonutils.sysutils.typed import non_optional
from JAStudio.Core import App

from jastudio.ankiutils import query_builder
from jastudio.ui.menus.menu_utils import shortcutfinger
from jastudio.ui.menus.menu_utils.ex_qmenu import add_lookup_action_lambda

if TYPE_CHECKING:
    from collections.abc import Callable

    from PyQt6.QtWidgets import QMenu


def build_open_in_anki_menu(open_in_anki_menu:QMenu, search_string:Callable[[],str]) -> None:
    def build_exact_menu(exact_menu:QMenu) -> None:
        add_lookup_action_lambda(exact_menu, shortcutfinger.home1("Open Exact matches | no sentences | reading cards"), lambda: query_builder.exact_matches_no_sentences_reading_cards(search_string()))
        add_lookup_action_lambda(exact_menu, shortcutfinger.home2("Open Exact matches with sentences"), lambda: query_builder.exact_matches(search_string()))


    def build_kanji_menu(kanji_menu:QMenu) -> None:
        add_lookup_action_lambda(kanji_menu, shortcutfinger.home1("All kanji in string"), lambda: query_builder.kanji_in_string(search_string()))
        add_lookup_action_lambda(kanji_menu, shortcutfinger.home2("By reading part"), lambda: query_builder.kanji_with_reading_part(search_string()))
        add_lookup_action_lambda(kanji_menu, shortcutfinger.home3("By reading exact"), lambda: query_builder.notes_lookup(list(App.Col().Kanji.WithReading(search_string()))))
        add_lookup_action_lambda(kanji_menu, shortcutfinger.home4("With radicals"), lambda: query_builder.kanji_with_radicals_in_string(search_string()))
        add_lookup_action_lambda(kanji_menu, shortcutfinger.up1("With meaning"), lambda: query_builder.kanji_with_meaning(search_string()))

    def build_vocab_menu(vocab_menu:QMenu) -> None:
        add_lookup_action_lambda(vocab_menu, shortcutfinger.home1("form -"), lambda: query_builder.single_vocab_by_form_exact(search_string()))
        add_lookup_action_lambda(vocab_menu, shortcutfinger.home2("form - read card only"), lambda: query_builder.single_vocab_by_form_exact_read_card_only(search_string()))
        add_lookup_action_lambda(vocab_menu, shortcutfinger.home3("form, reading or answer"), lambda: query_builder.single_vocab_by_question_reading_or_answer_exact(search_string()))
        add_lookup_action_lambda(vocab_menu, shortcutfinger.home4("Wildcard"), lambda: query_builder.single_vocab_wildcard(search_string()))
        add_lookup_action_lambda(vocab_menu, shortcutfinger.up1("Text words"), lambda: query_builder.text_vocab_lookup(search_string()))

    def build_sentence_menu(sentence_menu:QMenu) -> None:
        add_lookup_action_lambda(sentence_menu, shortcutfinger.home1("Parse Vocabulary"), lambda: query_builder.sentence_search(search_string()))
        add_lookup_action_lambda(sentence_menu, shortcutfinger.home2("Exact String"), lambda: query_builder.sentence_search(search_string(), exact=True))

    build_exact_menu(non_optional(open_in_anki_menu.addMenu(shortcutfinger.home1("Exact matches"))))
    build_kanji_menu(non_optional(open_in_anki_menu.addMenu(shortcutfinger.home2("Kanji"))))
    build_vocab_menu(non_optional(open_in_anki_menu.addMenu(shortcutfinger.home3("Vocab"))))
    build_sentence_menu(non_optional(open_in_anki_menu.addMenu(shortcutfinger.home4("Sentence"))))
