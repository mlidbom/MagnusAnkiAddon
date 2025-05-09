from collections.abc import Callable

from PyQt6.QtWidgets import QMenu

from ankiutils import app, query_builder
from hooks.right_click_menu_utils import add_lookup_action, add_ui_action
from note.kanjinote import KanjiNote
from sysutils import ex_str, kana_utils
from sysutils.typed import non_optional
from hooks import shortcutfinger

def build_note_menu(kanji: KanjiNote, note_menu: QMenu) -> None:
    def build_lookup_menu(note_lookup_menu: QMenu) -> None:
        add_lookup_action(note_lookup_menu, shortcutfinger.home1("Primary Vocabs"), query_builder.vocabs_lookup_strings(kanji.get_primary_vocab()))
        add_lookup_action(note_lookup_menu, shortcutfinger.home2("Vocabs"), query_builder.vocab_with_kanji(kanji))
        add_lookup_action(note_lookup_menu, shortcutfinger.home3("Radicals"), query_builder.notes_lookup(kanji.get_radicals_notes()))
        add_lookup_action(note_lookup_menu, shortcutfinger.home4("Kanji"), query_builder.notes_lookup(app.col().kanji.with_radical(kanji.get_question())))
        add_lookup_action(note_lookup_menu, shortcutfinger.home5("Sentences"), query_builder.sentence_search(kanji.get_question(), exact=True))

    build_lookup_menu(non_optional(note_menu.addMenu(shortcutfinger.home1("Open"))))

    add_ui_action(note_menu, shortcutfinger.home5("Reset Primary Vocabs"), lambda: kanji.set_primary_vocab([]))

    if not kanji.get_user_answer():
        add_ui_action(note_menu, shortcutfinger.up1("Accept meaning"), lambda: kanji.set_user_answer(format_kanji_meaning(kanji.get_answer())))

    add_ui_action(note_menu, shortcutfinger.up2("Populate radicals from mnemonic tags"), lambda: kanji.populate_radicals_from_mnemonic_tags())
    add_ui_action(note_menu, shortcutfinger.up3("Bootstrap mnemonic from radicals"), lambda: kanji.bootstrap_mnemonic_from_radicals())
    add_ui_action(note_menu, shortcutfinger.up4("Reset mnemonic"), lambda: kanji.set_user_mnemonic(""))

def build_string_menu(string_menu: QMenu, kanji: KanjiNote, menu_string: str) -> None:
    def build_highlighted_vocab_menu(highlighted_vocab_menu: QMenu, _vocab_to_add: str) -> None:
        for index, _vocab in enumerate(kanji.get_primary_vocab()):
            add_ui_action(highlighted_vocab_menu, shortcutfinger.numpad(index, f"{_vocab}"), lambda _index=index: kanji.position_primary_vocab(_vocab_to_add, _index))  # type: ignore

        add_ui_action(highlighted_vocab_menu, shortcutfinger.home1(f"[Last]"), lambda: kanji.position_primary_vocab(_vocab_to_add))

        if _vocab_to_add in kanji.get_primary_vocab():
            add_ui_action(highlighted_vocab_menu, shortcutfinger.home2("Remove"), lambda __vocab_to_add=_vocab_to_add: kanji.remove_primary_vocab(__vocab_to_add))  # type: ignore

    def add_primary_readings_actions(menu: QMenu, title_factory: Callable[[str], str], string: str) -> None:
        if kana_utils.is_only_katakana(string):
            hiragana_string = kana_utils.to_hiragana(string)
            if hiragana_string in kanji.get_primary_readings_on():
                add_ui_action(menu, title_factory("Remove primary Onyomi Reading"), lambda: kanji.remove_primary_on_reading(hiragana_string))
            elif hiragana_string in kanji.get_readings_on():
                add_ui_action(menu, title_factory("Make primary Onyomi Reading"), lambda: kanji.add_primary_on_reading(hiragana_string))
        elif kana_utils.is_only_hiragana(string):
            if string in kanji.get_primary_readings_kun():
                add_ui_action(menu, title_factory("Remove primary Kunyomi reading"), lambda: kanji.remove_primary_kun_reading(string))
            elif string in kanji.get_readings_kun():
                add_ui_action(menu, title_factory("Make primary Kunyomi reading"), lambda: kanji.add_primary_kun_reading(string))

    def build_add_menu(add_menu:QMenu) -> None:
        add_ui_action(add_menu, shortcutfinger.home1("Similar meaning"), lambda _menu_string=menu_string: kanji.add_user_similar_meaning(_menu_string))  # type: ignore
        add_ui_action(add_menu, shortcutfinger.home2("Confused with"), lambda _menu_string=menu_string: kanji.add_related_confused_with(_menu_string))  # type: ignore

    build_highlighted_vocab_menu(non_optional(string_menu.addMenu(shortcutfinger.home1("Highlighted Vocab"))), menu_string)
    build_add_menu(non_optional(string_menu.addMenu(shortcutfinger.home2("Add"))))
    add_primary_readings_actions(string_menu, shortcutfinger.home3,menu_string)

def format_kanji_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning.lower().replace(", ", "/").replace(" ", "-"))
