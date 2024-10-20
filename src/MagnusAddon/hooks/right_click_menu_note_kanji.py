from PyQt6.QtWidgets import QMenu

from ankiutils import app, query_builder
from hooks.right_click_menu_utils import add_lookup_action, add_ui_action
from note.kanjinote import KanjiNote
from sysutils import ex_str
from sysutils.typed import checked_cast
from hooks import shortcutfinger

def setup_note_menu(kanji: KanjiNote, note_menu: QMenu, string_menus: list[tuple[QMenu, str]]) -> None:
    note_lookup_menu = checked_cast(QMenu, note_menu.addMenu(shortcutfinger.home1("Open")))
    add_lookup_action(note_lookup_menu, shortcutfinger.home1("Primary Vocabs"), query_builder.vocabs_lookup_strings(kanji.get_primary_vocab()))
    add_lookup_action(note_lookup_menu, shortcutfinger.home2("Vocabs"), query_builder.vocab_with_kanji(kanji))
    add_lookup_action(note_lookup_menu, shortcutfinger.home3("Radicals"), query_builder.notes_by_note(app.col().kanji.dependencies_of(kanji)))
    add_lookup_action(note_lookup_menu, shortcutfinger.home4("Kanji"), query_builder.kanji_with_kanji_radical(kanji))
    add_lookup_action(note_lookup_menu, shortcutfinger.home5("Sentences"), query_builder.sentence_search(kanji.get_question(), exact=True))

    if not kanji.get_user_mnemonic():
        note_hide_menu = checked_cast(QMenu, note_menu.addMenu(shortcutfinger.home2("Hide/Remove")))
        add_ui_action(note_hide_menu, shortcutfinger.home1("Mnemonic"), lambda: kanji.override_meaning_mnemonic())
    if kanji.get_user_mnemonic() == "-":
        note_restore_menu: QMenu = checked_cast(QMenu, note_menu.addMenu(shortcutfinger.home3("Restore")))
        add_ui_action(note_restore_menu, shortcutfinger.home1("Mnemonic"), lambda: kanji.restore_meaning_mnemonic())
    if not kanji.get_user_answer():
        add_ui_action(note_menu, shortcutfinger.home4("Accept meaning"), lambda: kanji.set_user_answer(format_kanji_meaning(kanji.get_answer())))

    add_ui_action(note_menu, shortcutfinger.home5("Reset Primary Vocabs"), lambda: kanji.set_primary_vocab([]))

    def position_primary_vocab_menu(_menu: QMenu, _vocab_to_add: str, _title: str) -> None:
        highlighted_vocab_menu: QMenu = checked_cast(QMenu, _menu.addMenu(_title))
        for index, _vocab in enumerate(kanji.get_primary_vocab()):
            add_ui_action(highlighted_vocab_menu, shortcutfinger.numpad(index, f"{_vocab}"), lambda _index=index: kanji.position_primary_vocab(_vocab_to_add, _index))  # type: ignore

        add_ui_action(highlighted_vocab_menu, shortcutfinger.home1(f"[Last]"), lambda: kanji.position_primary_vocab(_vocab_to_add))

        if _vocab_to_add in kanji.get_primary_vocab():
            add_ui_action(highlighted_vocab_menu, shortcutfinger.home2("Remove"), lambda __vocab_to_add=_vocab_to_add: kanji.remove_primary_vocab(__vocab_to_add))  # type: ignore

    for string_menu, menu_string in string_menus:
        position_primary_vocab_menu(string_menu, menu_string, shortcutfinger.home1("Primary Vocab"))

        kanji_add_menu: QMenu = checked_cast(QMenu, string_menu.addMenu(shortcutfinger.home2("Add")))
        add_ui_action(kanji_add_menu, shortcutfinger.home1("Similar meaning"), lambda _menu_string=menu_string: kanji.add_user_similar_meaning(_menu_string)) # type: ignore

def format_vocab_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning
                                                .replace(" SOURCE", "")
                                                .replace(", ", "/")
                                                .replace(" ", "-")
                                                .lower())

def format_kanji_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning.lower().replace(", ", "/").replace(" ", "-"))
