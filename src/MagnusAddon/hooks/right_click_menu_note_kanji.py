from PyQt6.QtWidgets import QMenu

from ankiutils import app, query_builder
from hooks.right_click_menu_utils import add_lookup_action, add_ui_action
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from sysutils import ex_str
from sysutils.typed import checked_cast

def setup_note_menu(note: JPNote, note_menu: QMenu, string_menus: list[tuple[QMenu, str]]) -> None:
    note_lookup_menu: QMenu
    note_hide_menu: QMenu

    if isinstance(note, KanjiNote):
        note_lookup_menu = checked_cast(QMenu, note_menu.addMenu("&Open"))

        kanji = note
        add_lookup_action(note_lookup_menu, "Primary Vocabs", query_builder.vocabs_lookup_strings(note.get_primary_vocab()))
        add_lookup_action(note_lookup_menu, "&Vocabs", query_builder.vocab_with_kanji(note))
        add_lookup_action(note_lookup_menu, "&Radicals", query_builder.notes_by_note(app.col().kanji.dependencies_of(kanji)))
        add_lookup_action(note_lookup_menu, "&Kanji", query_builder.kanji_with_kanji_radical(note))
        add_lookup_action(note_lookup_menu, "&Sentences", query_builder.sentence_search(kanji.get_question(), exact=True))

        if not kanji.get_user_mnemonic():
            note_hide_menu = checked_cast(QMenu, note_menu.addMenu("&Hide/Remove"))
            add_ui_action(note_hide_menu, "&Mnemonic", lambda: kanji.override_meaning_mnemonic())
        if kanji.get_user_mnemonic() == "-":
            note_restore_menu: QMenu = checked_cast(QMenu, note_menu.addMenu("&Restore"))
            add_ui_action(note_restore_menu, "&Mnemonic", lambda: kanji.restore_meaning_mnemonic())
        if not kanji.get_user_answer():
            add_ui_action(note_menu, "Accept &meaning", lambda: kanji.set_user_answer(format_kanji_meaning(kanji.get_answer())))

        add_ui_action(note_menu, "Reset Primary Vocabs", lambda: kanji.set_primary_vocab([]))

        for string_menu, menu_string in string_menus:
            primary_vocab_menu: QMenu = checked_cast(QMenu, string_menu.addMenu("Pr&imary Vocab"))
            if menu_string in kanji.get_primary_vocab():
                add_ui_action(primary_vocab_menu, "R&emove", lambda _menu_string=menu_string: kanji.remove_primary_vocab(_menu_string)) # type: ignore
            else:
                add_ui_action(primary_vocab_menu, "&Add", lambda _menu_string=menu_string: kanji.add_primary_vocab(_menu_string)) # type: ignore

            kanji_add_menu: QMenu = checked_cast(QMenu, string_menu.addMenu("&Add"))
            add_ui_action(kanji_add_menu, "&Similar meaning", lambda _menu_string=menu_string: kanji.add_user_similar_meaning(_menu_string)) # type: ignore

def format_vocab_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning
                                                .replace(" SOURCE", "")
                                                .replace(", ", "/")
                                                .replace(" ", "-")
                                                .lower())

def format_kanji_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning.lower().replace(", ", "/").replace(" ", "-"))
