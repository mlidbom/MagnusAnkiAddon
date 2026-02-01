from __future__ import annotations

from typing import TYPE_CHECKING

from jastudio.ankiutils import app, query_builder
from jastudio.sysutils import ex_str
from jastudio.sysutils.typed import non_optional
from jastudio.ui.menus.menu_utils import shortcutfinger
from jastudio.ui.menus.menu_utils.ex_qmenu import add_lookup_action, add_ui_action

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QMenu

    from jastudio.note.kanjinote import KanjiNote

def build_note_menu(note_menu: QMenu, kanji: KanjiNote) -> None:
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

def build_view_menu(_view_menu:QMenu, _kanji:KanjiNote) -> None:
    pass

def format_kanji_meaning(meaning: str) -> str:
    val = (ex_str.replace_html_and_bracket_markup_with(meaning, "|")
           .lower()
           .replace("||", "|")
           .replace("||", "|")
           .replace("||", "|")
           .replace(", ", "|")
           .replace(" ", "-")
           .replace("-|-", " | "))

    val = val.removesuffix("|")
    return val.removeprefix("|")
