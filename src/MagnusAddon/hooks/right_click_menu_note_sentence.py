from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import query_builder
from hooks import shortcutfinger
from hooks.right_click_menu_utils import add_lookup_action, add_ui_action
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from note.note_constants import NoteFields, NoteTypes
from sysutils import ex_lambda
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_form import CandidateForm
    from note.sentences.sentencenote import SentenceNote
    from note.sentences.word_exclusion_set import WordExclusionSet
    from PyQt6.QtWidgets import QMenu

def build_note_menu(note_menu: QMenu, sentence: SentenceNote) -> None:
    note_lookup_menu: QMenu = non_optional(note_menu.addMenu(shortcutfinger.home1("Open")))

    add_lookup_action(note_lookup_menu, shortcutfinger.home1("Highlighted Vocab"), query_builder.vocabs_lookup_strings(sentence.configuration.highlighted_words()))
    add_lookup_action(note_lookup_menu, shortcutfinger.home2("Highlighted Vocab Read Card"), query_builder.vocabs_lookup_strings_read_card(sentence.configuration.highlighted_words()))
    add_lookup_action(note_lookup_menu, shortcutfinger.home3("Kanji"), f"""note:{NoteTypes.Kanji} ({" OR ".join([f"{NoteFields.Kanji.question}:{kan}" for kan in sentence.extract_kanji()])})""")
    add_lookup_action(note_lookup_menu, shortcutfinger.home4("Parsed words"), query_builder.notes_by_id([voc.get_id() for voc in sentence.get_parsed_words_notes()]))

    add_ui_action(note_menu, shortcutfinger.home5("Reset higlighted"), lambda: sentence.configuration.reset_highlighted_words())
    add_ui_action(note_menu, shortcutfinger.up1("Reset incorrect matches"), lambda: sentence.configuration.incorrect_matches.reset())
    add_ui_action(note_menu, shortcutfinger.up2("Reset hidden matches"), lambda: sentence.configuration.hidden_matches.reset())

def build_string_menu(string_menu: QMenu, sentence: SentenceNote, menu_string: str) -> None:
    build_highlighted_vocab_menu(non_optional(string_menu.addMenu(shortcutfinger.home1("Highlighted Vocab"))), sentence, menu_string)

    def build_word_exclusion_set_menu(word_exclusion_set_menu: QMenu, exclusion_set: WordExclusionSet) -> None:
        menu_string_as_word_exclusion = WordExclusion.global_(menu_string)
        valid_top_level_words = sentence.get_valid_parsed_non_child_words()
        top_level_words_excluded_by_menu_string: list[CandidateForm] = [w for w in valid_top_level_words if menu_string_as_word_exclusion.excludes_form_at_index(w.form, w.start_index)]
        if any(top_level_words_excluded_by_menu_string):
            if len(top_level_words_excluded_by_menu_string) == 1:
                add_ui_action(word_exclusion_set_menu, shortcutfinger.home1("Add"), lambda: exclusion_set.add_global(menu_string))
            else:
                add_exclusion_menu: QMenu = non_optional(word_exclusion_set_menu.addMenu(shortcutfinger.home1("Add")))

                for excluded_index, matched in enumerate(top_level_words_excluded_by_menu_string):
                    add_ui_action(add_exclusion_menu,shortcutfinger.numpad_no_numbers(excluded_index, f"{matched.start_index}: {matched.form}"),  ex_lambda.bind1(exclusion_set.add, matched.to_exclusion()))
        else:
            add_ui_action(word_exclusion_set_menu, shortcutfinger.home1("Add"), lambda: exclusion_set.add_global(menu_string))

        current_exclusions = exclusion_set.get()
        covered_existing_exclusions = [x for x in current_exclusions if menu_string_as_word_exclusion.covers(x)]
        if any(covered_existing_exclusions):
            if len(covered_existing_exclusions) == 1:
                add_ui_action(word_exclusion_set_menu, shortcutfinger.home2("Remove"), lambda: exclusion_set.remove_string(menu_string))
            else:
                remove_exclution_menu: QMenu = non_optional(word_exclusion_set_menu.addMenu(shortcutfinger.home2("Remove")))
                for excluded_index, matched_exclusion in enumerate(covered_existing_exclusions):
                    add_ui_action(remove_exclution_menu,shortcutfinger.numpad_no_numbers(excluded_index, f"{matched_exclusion.index}:{matched_exclusion.word}"), ex_lambda.bind1(exclusion_set.remove, matched_exclusion))

    build_word_exclusion_set_menu(non_optional(string_menu.addMenu(shortcutfinger.home2("Incorrect matches"))), sentence.configuration.incorrect_matches)
    build_word_exclusion_set_menu(non_optional(string_menu.addMenu(shortcutfinger.home3("Hidden matches"))), sentence.configuration.hidden_matches)

    build_highlighted_vocab_menu(non_optional(string_menu.addMenu(shortcutfinger.home4("Highlighted Vocab Separator"))), sentence, "-")

def build_highlighted_vocab_menu(highlighted_vocab_menu: QMenu, sentence: SentenceNote, _vocab_to_add: str) -> None:
    for index, _vocab in enumerate(sentence.configuration.highlighted_words()):
        add_ui_action(highlighted_vocab_menu,shortcutfinger.numpad(index, f"{_vocab}"), ex_lambda.bind2(sentence.configuration.position_highlighted_word, _vocab_to_add, index))

    add_ui_action(highlighted_vocab_menu, shortcutfinger.home1("[Last]"), lambda: sentence.configuration.position_highlighted_word(_vocab_to_add))

    if _vocab_to_add in sentence.configuration.highlighted_words():
        add_ui_action(highlighted_vocab_menu, shortcutfinger.home2("Remove"), lambda: sentence.configuration.remove_highlighted_word(_vocab_to_add))
