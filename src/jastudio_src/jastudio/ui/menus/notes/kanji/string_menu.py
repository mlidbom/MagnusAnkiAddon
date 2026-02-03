from __future__ import annotations

from typing import TYPE_CHECKING

from jaspythonutils.sysutils import ex_lambda, kana_utils
from jaspythonutils.sysutils.typed import non_optional

from jastudio.ui.menus.menu_utils import shortcutfinger
from jastudio.ui.menus.menu_utils.ex_qmenu import add_ui_action

if TYPE_CHECKING:
    import collections.abc

    from jaslib.note.kanjinote import KanjiNote
    from PyQt6.QtWidgets import QMenu


def build(string_menu: QMenu, kanji: KanjiNote, menu_string: str) -> None:
    def build_highlighted_vocab_menu(highlighted_vocab_menu: QMenu, _vocab_to_add: str) -> None:
        for index, _vocab in enumerate(kanji.get_primary_vocab()):
            add_ui_action(highlighted_vocab_menu, shortcutfinger.numpad(index, f"{_vocab}"), ex_lambda.bind2(kanji.position_primary_vocab, menu_string, index))

        add_ui_action(highlighted_vocab_menu, shortcutfinger.home1("[Last]"), lambda: kanji.position_primary_vocab(_vocab_to_add))

        if _vocab_to_add in kanji.get_primary_vocab():
            add_ui_action(highlighted_vocab_menu, shortcutfinger.home2("Remove"), ex_lambda.bind1(kanji.remove_primary_vocab, _vocab_to_add))

    def add_primary_readings_actions(menu: QMenu, title_factory: collections.abc.Callable[[str], str], string: str) -> None:
        if kana_utils.is_only_katakana(string):
            hiragana_string = kana_utils.katakana_to_hiragana(string)
            if hiragana_string in kanji.get_primary_readings_on():
                add_ui_action(menu, title_factory("Remove primary Onyomi Reading"), lambda: kanji.remove_primary_on_reading(hiragana_string))
            elif hiragana_string in kanji.get_readings_on():
                add_ui_action(menu, title_factory("Make primary Onyomi Reading"), lambda: kanji.add_primary_on_reading(hiragana_string))
        elif kana_utils.is_only_hiragana(string):
            if string in kanji.get_primary_readings_kun():
                add_ui_action(menu, title_factory("Remove primary Kunyomi reading"), lambda: kanji.remove_primary_kun_reading(string))
            elif string in kanji.get_readings_kun():
                add_ui_action(menu, title_factory("Make primary Kunyomi reading"), lambda: kanji.add_primary_kun_reading(string))

    def build_add_menu(add_menu: QMenu) -> None:
        add_ui_action(add_menu, shortcutfinger.home1("Similar meaning"), lambda: kanji.add_user_similar_meaning(menu_string))
        add_ui_action(add_menu, shortcutfinger.home2("Confused with"), lambda: kanji.add_related_confused_with(menu_string))

    build_highlighted_vocab_menu(non_optional(string_menu.addMenu(shortcutfinger.home1("Highlighted Vocab"))), menu_string)
    build_add_menu(non_optional(string_menu.addMenu(shortcutfinger.home2("Add"))))
    add_primary_readings_actions(string_menu, shortcutfinger.home3, menu_string)
