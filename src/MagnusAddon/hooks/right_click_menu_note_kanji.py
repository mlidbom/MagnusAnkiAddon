from PyQt6.QtWidgets import QMenu

from ankiutils import query_builder
from hooks.right_click_menu_utils import add_lookup_action, add_ui_action
from note.kanjinote import KanjiNote
from sysutils import ex_str, kana_utils
from sysutils.typed import checked_cast
from hooks import shortcutfinger

def setup_note_menu(kanji: KanjiNote, note_menu: QMenu, string_menus: list[tuple[QMenu, str]]) -> None:
    note_lookup_menu = checked_cast(QMenu, note_menu.addMenu(shortcutfinger.home1("Open")))
    add_lookup_action(note_lookup_menu, shortcutfinger.home1("Primary Vocabs"), query_builder.vocabs_lookup_strings(kanji.get_primary_vocab()))
    add_lookup_action(note_lookup_menu, shortcutfinger.home2("Vocabs"), query_builder.vocab_with_kanji(kanji))
    add_lookup_action(note_lookup_menu, shortcutfinger.home3("Radicals"), query_builder.notes_by_note(kanji.get_radicals_notes()))
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

    def add_primary_readings_actions(menu: QMenu, string:str) -> None:
        if kana_utils.is_only_katakana(string):
            hiragana_string = kana_utils.to_hiragana(string)
            if hiragana_string in kanji.get_primary_readings_on():
                add_ui_action(menu, shortcutfinger.up1("Remove primary Onyomi Reading"), lambda: kanji.remove_primary_on_reading(hiragana_string))
            elif hiragana_string in kanji.get_readings_on():
                add_ui_action(menu, shortcutfinger.up1("Make primary Onyomi Reading"), lambda: kanji.add_primary_on_reading(hiragana_string))
        elif kana_utils.is_only_hiragana(string):
            if string in kanji.get_primary_readings_kun():
                add_ui_action(menu, shortcutfinger.up1("Remove primary Kunyomi reading"), lambda: kanji.remove_primary_kun_reading(string))
            elif string in kanji.get_readings_kun():
                add_ui_action(menu, shortcutfinger.up1("Make primary Kunyomi reading"), lambda: kanji.add_primary_kun_reading(string))

    for string_menu, menu_string in string_menus:
        position_primary_vocab_menu(string_menu, menu_string, shortcutfinger.home1("Primary Vocab"))

        kanji_add_menu: QMenu = checked_cast(QMenu, string_menu.addMenu(shortcutfinger.home2("Add")))
        add_ui_action(kanji_add_menu, shortcutfinger.home1("Similar meaning"), lambda _menu_string=menu_string: kanji.add_user_similar_meaning(_menu_string)) # type: ignore

        add_primary_readings_actions(string_menu, menu_string)


def format_vocab_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning
                                                .replace(" SOURCE", "")
                                                .replace(", ", "/")
                                                .replace(" ", "-")
                                                .lower())

def format_kanji_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning.lower().replace(", ", "/").replace(" ", "-"))
