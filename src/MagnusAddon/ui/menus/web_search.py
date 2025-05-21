from __future__ import annotations

from typing import TYPE_CHECKING
from urllib import parse

from aqt.utils import openLink
from sysutils.typed import non_optional
from ui.menus.menu_utils import shortcutfinger

if TYPE_CHECKING:
    from collections.abc import Callable

    from PyQt6.QtWidgets import QMenu


def build_web_search_menu(search_web_menu:QMenu, search_string:Callable[[],str]) -> None:
    def add_web_lookup(menu: QMenu, name: str, url: str) -> None:
        menu.addAction(name, lambda: openLink(url % parse.quote(search_string(), encoding="utf8")))

    def set_up_kanji_menu(kanji_lookup_menu:QMenu) -> None:
        add_web_lookup(kanji_lookup_menu, shortcutfinger.home1("Kanji explosion"), "https://www.kurumi.com/jp/kjbh/?k=%s")
        add_web_lookup(kanji_lookup_menu, shortcutfinger.home2("Kanshudo"), "https://www.kanshudo.com/search?q=%s")
        add_web_lookup(kanji_lookup_menu, shortcutfinger.home3("Kanji map"), "https://thekanjimap.com/%s")

    def set_up_sentences_menu(sentences_lookup_menu:QMenu) -> None:
        add_web_lookup(sentences_lookup_menu, shortcutfinger.home1("Sentences: Immersion Kit"), "https://www.immersionkit.com/dictionary?exact=true&sort=sentence_length%%3Aasc&keyword=%s")
        add_web_lookup(sentences_lookup_menu, shortcutfinger.home2("Sentences: Tatoeba"), "https://tatoeba.org/en/sentences/search?from=jpn&to=eng&query=%s")

    def set_up_misc_menu(misc_lookup_menu:QMenu) -> None:
        def set_up_translate_menu(translate_menu: QMenu) -> None:
            add_web_lookup(translate_menu, shortcutfinger.home1("Translate: Deepl"), "https://www.deepl.com/en/translator#ja/en/%s")
            add_web_lookup(translate_menu, shortcutfinger.home2("Translate: Kanshudo"), "https://www.kanshudo.com/sentence_translate?q=%s")

        def set_up_images_menu(images_menu: QMenu) -> None:
            add_web_lookup(images_menu, shortcutfinger.home1("Images: Google"), "https://www.google.com/search?udm=2&tbs=sur:cl&q=%s")
            add_web_lookup(images_menu, shortcutfinger.home2("Images: Bing"), "https://www.bing.com/images/search?qft=+filterui:licenseType-Any&q=%s")

        def set_up_conjugate_menu(conjugate_menu: QMenu) -> None:
            add_web_lookup(conjugate_menu, shortcutfinger.home1("Conjugate: Japanese verb conjugator"), "https://www.japaneseverbconjugator.com/VerbDetails.asp?Go=Conjugate&txtVerb=%s")
            add_web_lookup(conjugate_menu, shortcutfinger.home2("Conjugate: Verbix"), "https://www.verbix.com/webverbix/japanese/%s")

        def set_up_grammar_menu(grammar_lookup_menu: QMenu) -> None:
            add_web_lookup(grammar_lookup_menu, shortcutfinger.home1("Grammar: Google"), "https://www.google.com/search?q=japanese+grammar+%s")
            add_web_lookup(grammar_lookup_menu, shortcutfinger.home2("Grammar: Japanese with anime"), "https://www.google.com/search?q=site:www.japanesewithanime.com+%s")
            add_web_lookup(grammar_lookup_menu, shortcutfinger.home3("Grammar: Wiktionary"), "https://en.wiktionary.org/wiki/%s")

        set_up_conjugate_menu(non_optional(misc_lookup_menu.addMenu(shortcutfinger.home1("Conjugate"))))
        set_up_translate_menu(non_optional(misc_lookup_menu.addMenu(shortcutfinger.home2("Translate"))))
        set_up_grammar_menu(non_optional(misc_lookup_menu.addMenu(shortcutfinger.home3("Grammar"))))
        set_up_images_menu(non_optional(misc_lookup_menu.addMenu(shortcutfinger.home4("Images"))))

    def set_up_lookup_menu(lookup_menu:QMenu) -> None:
        add_web_lookup(lookup_menu, shortcutfinger.home1("English: Merriam Webster"), "https://www.merriam-webster.com/dictionary/%s")
        add_web_lookup(lookup_menu, shortcutfinger.home2("Wiktionary"), "https://en.wiktionary.org/wiki/%s")
        add_web_lookup(lookup_menu, shortcutfinger.home3("Lookup: Takoboto"), "https://takoboto.jp/?q=%s")
        add_web_lookup(lookup_menu, shortcutfinger.home4("Lookup: Jisho"), "https://jisho.org/search/%s")
        add_web_lookup(lookup_menu, shortcutfinger.up1("Lookup: Wanikani"), "https://www.wanikani.com/search?query=%s")
        add_web_lookup(lookup_menu, shortcutfinger.down1("Lookup: Word Kanshudo"), "https://www.kanshudo.com/searchw?q=%s")

    set_up_kanji_menu(non_optional(search_web_menu.addMenu(shortcutfinger.home1("Kanji"))))
    set_up_sentences_menu(non_optional(search_web_menu.addMenu(shortcutfinger.home2("Sentences"))))
    set_up_misc_menu(non_optional(search_web_menu.addMenu(shortcutfinger.home3("Misc"))))
    set_up_lookup_menu(non_optional(search_web_menu.addMenu(shortcutfinger.home4("Lookup"))))
