from PyQt6.QtWidgets import QMenu

from ankiutils import query_builder
from hooks.right_click_menu_utils import add_lookup_action, add_ui_action
from note.note_constants import NoteFields, NoteTypes
from note.sentencenote import SentenceNote
from sysutils.typed import checked_cast
from hooks import shortcutfinger

def setup_note_menu(sentence: SentenceNote, note_menu: QMenu, string_menus: list[tuple[QMenu, str]]) -> None:
    note_lookup_menu: QMenu = checked_cast(QMenu, note_menu.addMenu(shortcutfinger.home1("Open")))

    add_lookup_action(note_lookup_menu, shortcutfinger.home1("Highlighted Vocab"), query_builder.vocabs_lookup_strings(sentence.get_user_highlighted_vocab()))
    add_lookup_action(note_lookup_menu, shortcutfinger.home2("Highlighted Vocab Read Card"), query_builder.vocabs_lookup_strings_read_card(sentence.get_user_highlighted_vocab()))
    add_lookup_action(note_lookup_menu, shortcutfinger.home3("Kanji"), f"""note:{NoteTypes.Kanji} ({" OR ".join([f"{NoteFields.Kanji.question}:{kan}" for kan in sentence.extract_kanji()])})""")
    add_lookup_action(note_lookup_menu, shortcutfinger.home4("Parsed words"), query_builder.notes_by_id([voc.get_id() for voc in sentence.ud_extract_vocab()]))

    def position_vocab_menu(_menu:QMenu, _vocab_to_add: str, _title: str) -> None:
        highlighted_vocab_menu: QMenu = checked_cast(QMenu, _menu.addMenu(_title))
        for index, _vocab in enumerate(sentence.get_user_highlighted_vocab()):
            add_ui_action(highlighted_vocab_menu, shortcutfinger.index(index, f"{_vocab}"), lambda _index=index: sentence.position_extra_vocab(_vocab_to_add, _index))  # type: ignore

        add_ui_action(highlighted_vocab_menu, shortcutfinger.home5(f"[Last]"), lambda: sentence.position_extra_vocab(_vocab_to_add))

        if _vocab_to_add in sentence.get_user_highlighted_vocab():
            add_ui_action(highlighted_vocab_menu, "R&emove", lambda __vocab_to_add=_vocab_to_add: sentence.remove_extra_vocab(__vocab_to_add)) # type: ignore

    for string_menu, menu_string in string_menus:
        position_vocab_menu(string_menu, menu_string, shortcutfinger.home1("Highlighted Vocab"))
        add_ui_action(string_menu, shortcutfinger.home2("Exclude vocab"), lambda _menu_string=menu_string: sentence.exclude_vocab(_menu_string)) # type: ignore

    position_vocab_menu(note_menu, "-", shortcutfinger.home2("Highlighted Vocab Separator"))
