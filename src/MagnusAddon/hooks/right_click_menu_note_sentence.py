from PyQt6.QtWidgets import QMenu

from ankiutils import query_builder
from hooks.right_click_menu_utils import add_lookup_action, add_ui_action
from note.note_constants import NoteFields, NoteTypes
from note.sentencenote import SentenceNote
from sysutils.typed import checked_cast

def setup_note_menu(note: SentenceNote, note_menu: QMenu, string_menus: list[tuple[QMenu, str]]) -> None:
    note_lookup_menu: QMenu = checked_cast(QMenu, note_menu.addMenu("&Open"))

    sentence_note = checked_cast(SentenceNote, note)
    add_lookup_action(note_lookup_menu, "Highlighted V&ocab", query_builder.vocabs_lookup_strings(note.get_user_highlighted_vocab()))
    add_lookup_action(note_lookup_menu, "Highlighted Vocab Read C&ard", query_builder.vocabs_lookup_strings_read_card(note.get_user_highlighted_vocab()))
    add_lookup_action(note_lookup_menu, "&Kanji", f"""note:{NoteTypes.Kanji} ({" OR ".join([f"{NoteFields.Kanji.question}:{kan}" for kan in note.extract_kanji()])})""")
    add_lookup_action(note_lookup_menu, "&Parsed words", query_builder.notes_by_id([voc.get_id() for voc in note.ud_extract_vocab()]))

    def position_vocab_menu(_menu:QMenu, _vocab_to_add: str, _title: str) -> None:
        highlighted_vocab_menu: QMenu = checked_cast(QMenu, _menu.addMenu(_title))
        for index, _vocab in enumerate(sentence_note.get_user_highlighted_vocab()):
            add_ui_action(highlighted_vocab_menu, f"&{index + 1}. {_vocab}", lambda _index=index: sentence_note.position_extra_vocab(_vocab_to_add, _index))  # type: ignore

        add_ui_action(highlighted_vocab_menu, f"[L&ast]", lambda: sentence_note.position_extra_vocab(_vocab_to_add))

        if _vocab_to_add in sentence_note.get_user_highlighted_vocab():
            add_ui_action(highlighted_vocab_menu, "R&emove", lambda __vocab_to_add=_vocab_to_add: sentence_note.remove_extra_vocab(__vocab_to_add)) # type: ignore

    for string_menu, menu_string in string_menus:
        position_vocab_menu(string_menu, menu_string, "H&ighlighted Vocab")
        add_ui_action(string_menu, "E&xclude vocab", lambda _menu_string=menu_string: sentence_note.exclude_vocab(_menu_string)) # type: ignore

    position_vocab_menu(note_menu, "-", "H&ighlighted Vocab Separator")
