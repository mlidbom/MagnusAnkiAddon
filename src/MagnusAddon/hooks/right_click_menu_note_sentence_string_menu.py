from __future__ import annotations

from typing import TYPE_CHECKING

from hooks import shortcutfinger
from hooks.right_click_menu_utils import add_ui_action
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from sysutils import ex_lambda
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_form import CandidateForm
    from note.sentences.sentencenote import SentenceNote
    from note.sentences.word_exclusion_set import WordExclusionSet
    from PyQt6.QtWidgets import QMenu

def build_string_menu(string_menu: QMenu, sentence: SentenceNote, menu_string: str) -> None:
    def build_highlighted_vocab_menu_add(highlighted_vocab_menu: QMenu) -> None:
        for index, _vocab in enumerate(sentence.configuration.highlighted_words()):
            add_ui_action(highlighted_vocab_menu, shortcutfinger.numpad(index, f"{_vocab}"), ex_lambda.bind2(sentence.configuration.position_highlighted_word, menu_string, index))

        add_ui_action(highlighted_vocab_menu, shortcutfinger.home1("[Last]"), lambda: sentence.configuration.position_highlighted_word(menu_string))

    def add_add_word_exclusion_action(add_menu: QMenu, exclusion_type_title: str, exclusion_set: WordExclusionSet) -> None:
        menu_string_as_word_exclusion = WordExclusion.global_(menu_string)
        valid_top_level_words = sentence.get_valid_parsed_non_child_words()
        top_level_words_excluded_by_menu_string: list[CandidateForm] = [w for w in valid_top_level_words if menu_string_as_word_exclusion.excludes_form_at_index(w.form, w.start_index)]
        if any(top_level_words_excluded_by_menu_string):
            if len(top_level_words_excluded_by_menu_string) == 1:
                add_ui_action(add_menu, exclusion_type_title, lambda: exclusion_set.add(top_level_words_excluded_by_menu_string[0].to_exclusion()))
            else:
                add_exclusion_menu: QMenu = non_optional(add_menu.addMenu(exclusion_type_title))

                for excluded_index, matched in enumerate(top_level_words_excluded_by_menu_string):
                    add_ui_action(add_exclusion_menu, shortcutfinger.numpad_no_numbers(excluded_index, f"{matched.start_index}: {matched.form}"), ex_lambda.bind1(exclusion_set.add, matched.to_exclusion()))
        else:
            add_ui_action(add_menu, exclusion_type_title, lambda: None).setEnabled(False)

    def add_remove_word_exclusion_action(word_exclusion_remove: QMenu, exclusion_type_title: str, exclusion_set: WordExclusionSet) -> None:
        menu_string_as_word_exclusion = WordExclusion.global_(menu_string)
        current_exclusions = exclusion_set.get()
        covered_existing_exclusions = [excl for excl in current_exclusions if menu_string_as_word_exclusion.excludes_all_words_excluded_by(excl)]
        if any(covered_existing_exclusions):
            if len(covered_existing_exclusions) == 1:
                add_ui_action(word_exclusion_remove, exclusion_type_title, lambda: exclusion_set.remove_string(menu_string))
            else:
                remove_at_index_menu: QMenu = non_optional(word_exclusion_remove.addMenu(exclusion_type_title))
                for excluded_index, matched_exclusion in enumerate(covered_existing_exclusions):
                    add_ui_action(remove_at_index_menu, shortcutfinger.numpad_no_numbers(excluded_index, f"{matched_exclusion.index}:{matched_exclusion.word}"), ex_lambda.bind1(exclusion_set.remove, matched_exclusion))
        else:
            add_ui_action(word_exclusion_remove, exclusion_type_title, lambda: None, False)

    def build_add_menu(add_menu: QMenu) -> None:
        add_add_word_exclusion_action(add_menu, shortcutfinger.home1("Hidden matches"), sentence.configuration.hidden_matches)
        build_highlighted_vocab_menu_add(non_optional(add_menu.addMenu(shortcutfinger.home2("Highlighted Vocab"))))
        add_add_word_exclusion_action(add_menu, shortcutfinger.home3("Incorrect matches"), sentence.configuration.incorrect_matches)

    def build_remove_menu(remove_menu: QMenu) -> None:
        add_remove_word_exclusion_action(remove_menu, shortcutfinger.home1("Hidden matches"), sentence.configuration.hidden_matches)
        add_ui_action(remove_menu, shortcutfinger.home2("Highlighted vocab"), lambda: sentence.configuration.remove_highlighted_word(menu_string)).setEnabled(menu_string in sentence.configuration.highlighted_words())
        add_remove_word_exclusion_action(remove_menu, shortcutfinger.home3("Incorrect matches"), sentence.configuration.incorrect_matches)

    build_add_menu(non_optional(string_menu.addMenu(shortcutfinger.home1("Add"))))
    build_remove_menu(non_optional(string_menu.addMenu(shortcutfinger.home2("Remove"))))
    add_ui_action(string_menu, shortcutfinger.home3("Split with word-break tag in question"), lambda: sentence.question.split_token_with_word_break_tag(menu_string), menu_string in sentence.get_question())
