from __future__ import annotations

from typing import TYPE_CHECKING

from anki.notes import NoteId
from jaspythonutils.sysutils.typed import non_optional
from JAStudio.Core.Note import NoteFields, NoteTypes

from jastudio.ankiutils import app, query_builder
from jastudio.ui.menus.menu_utils import shortcutfinger
from jastudio.ui.menus.menu_utils.ex_qmenu import add_checkbox_config, add_lookup_action, add_ui_action

if TYPE_CHECKING:
    from JAStudio.Core.Note import SentenceNote
    from PyQt6.QtWidgets import QMenu

def build_note_menu(note_menu: QMenu, sentence: SentenceNote) -> None:
    def build_lookup_menu(note_lookup_menu: QMenu) -> None:
        add_lookup_action(note_lookup_menu, shortcutfinger.home1("Highlighted Vocab"), query_builder.vocabs_lookup_strings(list(sentence.configuration.highlighted_words())))
        add_lookup_action(note_lookup_menu, shortcutfinger.home2("Highlighted Vocab Read Card"), query_builder.vocabs_lookup_strings_read_card(list(sentence.configuration.highlighted_words())))
        add_lookup_action(note_lookup_menu, shortcutfinger.home3("Kanji"), f"""note:{NoteTypes.Kanji} ({" OR ".join([f"{NoteFields.Kanji.question}:{kan}" for kan in sentence.extract_kanji()])})""")
        add_lookup_action(note_lookup_menu, shortcutfinger.home4("Parsed words"), query_builder.notes_by_id([NoteId(voc.GetId()) for voc in sentence.get_parsed_words_notes()]))

    def build_remove_menu(remove_menu: QMenu) -> None:
        add_ui_action(remove_menu, shortcutfinger.home1("All highlighted"), lambda: sentence.configuration.reset_highlighted_words()).setEnabled(any(sentence.configuration.highlighted_words()))
        add_ui_action(remove_menu, shortcutfinger.home2("All incorrect matches"), lambda: sentence.configuration.incorrect_matches.reset()).setEnabled(any(sentence.configuration.incorrect_matches.get()))
        add_ui_action(remove_menu, shortcutfinger.home3("All hidden matches"), lambda: sentence.configuration.hidden_matches.reset()).setEnabled(any(sentence.configuration.hidden_matches.get()))
        add_ui_action(remove_menu, shortcutfinger.home4("Source comments"), lambda: sentence.source_comments.empty()).setEnabled(sentence.source_comments.has_value())

    def build_remove_user(remove_user_menu: QMenu) -> None:
        add_ui_action(remove_user_menu, shortcutfinger.home1("comments"), lambda: sentence.user.comments.empty()).setEnabled(sentence.user.comments.has_value())
        add_ui_action(remove_user_menu, shortcutfinger.home2("answer"), lambda: sentence.user.question.empty()).setEnabled(sentence.user.answer.has_value())
        add_ui_action(remove_user_menu, shortcutfinger.home3("question"), lambda: sentence.user.question.empty()).setEnabled(sentence.user.question.has_value())

    build_lookup_menu(non_optional(note_menu.addMenu(shortcutfinger.home1("Open"))))
    build_remove_menu(non_optional(note_menu.addMenu(shortcutfinger.home2("Remove"))))
    build_remove_user(non_optional(note_menu.addMenu(shortcutfinger.home3("Remove User"))))

def build_view_menu(view_menu: QMenu) -> None:  # pyright: ignore
    index = 0
    for index, toggle in enumerate(app.config().sentence_view_toggles):
        add_checkbox_config(view_menu, toggle, shortcutfinger.finger_by_priority_order(index, toggle.title))

    add_ui_action(view_menu,
                  shortcutfinger.finger_by_priority_order(index + 1, "Toggle all sentence auto yield compound last token flags (Ctrl+Shift+Alt+d)"),
                  app.config().toggle_all_sentence_display_auto_yield_flags)
