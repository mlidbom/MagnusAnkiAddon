from PyQt6.QtWidgets import QMenu

from ankiutils import query_builder
from hooks.right_click_menu_utils import add_lookup_action, add_ui_action
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from note.note_constants import NoteFields, NoteTypes
from note.sentencenote import SentenceNote
from sysutils.typed import non_optional
from hooks import shortcutfinger

def setup_note_menu(sentence: SentenceNote, note_menu: QMenu, string_menus: list[tuple[QMenu, str]]) -> None:
    note_lookup_menu: QMenu = non_optional(note_menu.addMenu(shortcutfinger.home1("Open")))

    add_lookup_action(note_lookup_menu, shortcutfinger.home1("Highlighted Vocab"), query_builder.vocabs_lookup_strings(sentence.get_user_highlighted_vocab()))
    add_lookup_action(note_lookup_menu, shortcutfinger.home2("Highlighted Vocab Read Card"), query_builder.vocabs_lookup_strings_read_card(sentence.get_user_highlighted_vocab()))
    add_lookup_action(note_lookup_menu, shortcutfinger.home3("Kanji"), f"""note:{NoteTypes.Kanji} ({" OR ".join([f"{NoteFields.Kanji.question}:{kan}" for kan in sentence.extract_kanji()])})""")
    add_lookup_action(note_lookup_menu, shortcutfinger.home4("Parsed words"), query_builder.notes_by_id([voc.get_id() for voc in sentence.get_parsed_words_notes()]))

    def position_vocab_menu(_menu:QMenu, _vocab_to_add: str, _title: str) -> None:
        highlighted_vocab_menu: QMenu = non_optional(_menu.addMenu(_title))
        for index, _vocab in enumerate(sentence.get_user_highlighted_vocab()):
            add_ui_action(highlighted_vocab_menu, shortcutfinger.numpad(index, f"{_vocab}"), lambda _index=index: sentence.position_extra_vocab(_vocab_to_add, _index))  # type: ignore

        add_ui_action(highlighted_vocab_menu, shortcutfinger.home1(f"[Last]"), lambda: sentence.position_extra_vocab(_vocab_to_add))

        if _vocab_to_add in sentence.get_user_highlighted_vocab():
            add_ui_action(highlighted_vocab_menu, shortcutfinger.home2("Remove"), lambda __vocab_to_add=_vocab_to_add: sentence.remove_extra_vocab(__vocab_to_add)) # type: ignore

    for string_menu, menu_string in string_menus:
        position_vocab_menu(string_menu, menu_string, shortcutfinger.home1("Highlighted Vocab"))

        potential_exclusion = WordExclusion.from_string(menu_string)
        current_words = sentence.get_valid_parsed_non_child_words()
        excluded = [w for w in current_words if potential_exclusion.excludes_form_at_index(w.form, w.start_index)]
        if any(excluded):
            if len(excluded) == 1:
                add_ui_action(string_menu, shortcutfinger.home2("Exclude vocab"), lambda _menu_string=menu_string: sentence.exclude_vocab(_menu_string)) # type: ignore
            else:
                exclude_menu: QMenu = non_optional(string_menu.addMenu(shortcutfinger.home2("Exclude vocab")))
                for excluded_index, matched in enumerate(excluded):
                    add_ui_action(exclude_menu, shortcutfinger.numpad_no_numbers(excluded_index, f"{matched.start_index}: {matched.word.word}"), lambda _matched=matched: sentence.exclude_vocab(_matched.to_exclusion().as_string())) # type: ignore
        else:
            add_ui_action(string_menu, shortcutfinger.home2("Exclude vocab"), lambda _menu_string=menu_string: sentence.exclude_vocab(_menu_string))  # type: ignore

        current_exclusions = sentence.get_user_word_exclusions()
        covered_existing_exclusions = [x for x in current_exclusions if potential_exclusion.covers(x)]
        if any(covered_existing_exclusions):
            if len(covered_existing_exclusions) == 1:
                add_ui_action(string_menu, shortcutfinger.home3("Remove exclusion"), lambda _menu_string=menu_string: sentence.remove_excluded_vocab(_menu_string)) # type: ignore
            else:
                remove_exclution_menu: QMenu = non_optional(string_menu.addMenu(shortcutfinger.home3("Remove exclusion")))
                for excluded_index, matched_exclusion in enumerate(covered_existing_exclusions):
                    add_ui_action(remove_exclution_menu, shortcutfinger.numpad_no_numbers(excluded_index, f"{matched_exclusion.index}:{matched_exclusion.word}"), lambda _matched_exclusion=matched_exclusion: sentence.remove_excluded_vocab(_matched_exclusion.as_string())) # type: ignore



    position_vocab_menu(note_menu, "-", shortcutfinger.home2("Highlighted Vocab Separator"))

    add_ui_action(note_menu, shortcutfinger.home5("Reset higlighted"), lambda: sentence.reset_highlighted())
    add_ui_action(note_menu, shortcutfinger.up1("Reset excluded"), lambda: sentence.reset_excluded())
