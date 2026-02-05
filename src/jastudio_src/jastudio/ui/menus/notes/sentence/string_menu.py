from __future__ import annotations

from typing import TYPE_CHECKING

from jaspythonutils.sysutils import ex_lambda
from jaspythonutils.sysutils.lazy import Lazy
from jaspythonutils.sysutils.typed import non_optional
from JAStudio.Core.LanguageServices.JanomeEx.WordExtraction import WordExclusion

from jastudio.ui.menus.menu_utils import shortcutfinger
from jastudio.ui.menus.menu_utils.ex_qmenu import add_ui_action

if TYPE_CHECKING:
    from JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches import Match
    from JAStudio.Core.Note import SentenceNote
    from JAStudio.Core.Note.Sentences import WordExclusionSet
    from PyQt6.QtWidgets import QMenu

def build_string_menu(string_menu: QMenu, sentence: SentenceNote, menu_string: str) -> None:
    def add_add_word_exclusion_action(add_menu: QMenu, exclusion_type_title: str, exclusion_set: WordExclusionSet) -> None:
        menu_string_as_word_exclusion = WordExclusion.global_(menu_string)
        analysis = sentence.create_analysis()
        display_matches = Lazy(lambda: analysis.display_matches) #these little tricks with the Lazy is to capture the analysis in a closure so that the weak references within the analysis don't get cleaned up before the action is invoked in the UI by the user.
        matches_excluded_by_menu_string: Lazy[list[Match]] = Lazy(lambda: [w for w in display_matches() if menu_string_as_word_exclusion.excludes_form_at_index(w.parsed_form, w.start_index)])
        if any(matches_excluded_by_menu_string()):
            if len(matches_excluded_by_menu_string()) == 1:
                add_ui_action(add_menu, exclusion_type_title, lambda: exclusion_set.add(matches_excluded_by_menu_string()[0].to_exclusion()))
            else:
                add_exclusion_menu: QMenu = non_optional(add_menu.addMenu(exclusion_type_title))

                for excluded_index, matched in enumerate(matches_excluded_by_menu_string()):
                    add_ui_action(add_exclusion_menu, shortcutfinger.finger_by_priority_order(excluded_index, f"{matched.start_index}: {matched.parsed_form}"), ex_lambda.bind1(exclusion_set.add, matched.to_exclusion()))
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
                    add_ui_action(remove_at_index_menu, shortcutfinger.finger_by_priority_order(excluded_index, f"{matched_exclusion.index}:{matched_exclusion.word}"), ex_lambda.bind1(exclusion_set.remove, matched_exclusion))
        else:
            add_ui_action(word_exclusion_remove, exclusion_type_title, lambda: None, False)

    def build_add_menu(add_menu: QMenu) -> None:
        add_ui_action(add_menu, shortcutfinger.home1("Highlighted Vocab"), lambda: sentence.configuration.add_highlighted_word(menu_string), menu_string not in sentence.configuration.highlighted_words())
        add_add_word_exclusion_action(add_menu, shortcutfinger.home2("Hidden matches"), sentence.configuration.hidden_matches)
        add_add_word_exclusion_action(add_menu, shortcutfinger.home3("Incorrect matches"), sentence.configuration.incorrect_matches)

    def build_remove_menu(remove_menu: QMenu) -> None:
        add_ui_action(remove_menu, shortcutfinger.home1("Highlighted vocab"), lambda: sentence.configuration.remove_highlighted_word(menu_string)).setEnabled(menu_string in sentence.configuration.highlighted_words())
        add_remove_word_exclusion_action(remove_menu, shortcutfinger.home2("Hidden matches"), sentence.configuration.hidden_matches)
        add_remove_word_exclusion_action(remove_menu, shortcutfinger.home3("Incorrect matches"), sentence.configuration.incorrect_matches)

    build_add_menu(non_optional(string_menu.addMenu(shortcutfinger.home1("Add"))))
    build_remove_menu(non_optional(string_menu.addMenu(shortcutfinger.home2("Remove"))))
    add_ui_action(string_menu, shortcutfinger.home3("Split with word-break tag in question"), lambda: sentence.question.split_token_with_word_break_tag(menu_string), menu_string in sentence.question.with_invisible_space())
