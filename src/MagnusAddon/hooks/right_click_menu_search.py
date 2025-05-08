from collections.abc import Callable
from urllib import parse

from PyQt6.QtWidgets import QMenu
from aqt.utils import openLink

from hooks.right_click_menu_utils import add_lookup_action_lambda
from ankiutils import app, query_builder
from sysutils.typed import non_optional

from hooks import shortcutfinger


def setup_anki_open_menu(open_in_anki_menu:QMenu, search_string:Callable[[],str]) -> None:
    def build_exact_menu(exact_menu:QMenu) -> None:
        add_lookup_action_lambda(exact_menu, shortcutfinger.home1("Open Exact matches | no sentences | reading cards"), lambda: query_builder.exact_matches_no_sentences_reading_cards(search_string()))
        add_lookup_action_lambda(exact_menu, shortcutfinger.home2("Open Exact matches with sentences"), lambda: query_builder.exact_matches(search_string()))


    def build_kanji_menu(kanji_menu:QMenu) -> None:
        add_lookup_action_lambda(kanji_menu, shortcutfinger.home1("All kanji in string"), lambda: query_builder.kanji_in_string(search_string()))
        add_lookup_action_lambda(kanji_menu, shortcutfinger.home2("By reading part"), lambda: query_builder.kanji_with_reading_part(search_string()))
        add_lookup_action_lambda(kanji_menu, shortcutfinger.home3("By reading exact"), lambda: query_builder.notes_lookup(list(app.col().kanji.with_reading(search_string()))))
        add_lookup_action_lambda(kanji_menu, shortcutfinger.home4("With radicals"), lambda: query_builder.kanji_with_radicals_in_string(search_string()))

    def build_vocab_menu(vocab_menu:QMenu) -> None:
        add_lookup_action_lambda(vocab_menu, shortcutfinger.home1("form -"), lambda: query_builder.single_vocab_by_form_exact(search_string()))
        add_lookup_action_lambda(vocab_menu, shortcutfinger.home2("form - read card only"), lambda: query_builder.single_vocab_by_form_exact_read_card_only(search_string()))
        add_lookup_action_lambda(vocab_menu, shortcutfinger.home3("form, reading or answer"), lambda: query_builder.single_vocab_by_question_reading_or_answer_exact(search_string()))
        add_lookup_action_lambda(vocab_menu, shortcutfinger.home4("Wildcard"), lambda: query_builder.single_vocab_wildcard(search_string()))
        add_lookup_action_lambda(vocab_menu, shortcutfinger.up1("Text words"), lambda: query_builder.text_vocab_lookup(search_string()))

    def build_sentence_menu(sentence_menu:QMenu) -> None:
        add_lookup_action_lambda(sentence_menu, shortcutfinger.home1("Parse Vocabulary"), lambda: query_builder.sentence_search(search_string()))
        add_lookup_action_lambda(sentence_menu, shortcutfinger.home2("Exact String"), lambda: query_builder.sentence_search(search_string(), exact=True))

    build_exact_menu(non_optional(open_in_anki_menu.addMenu(shortcutfinger.home1("Exact matches"))))
    build_kanji_menu(non_optional(open_in_anki_menu.addMenu(shortcutfinger.home2("Kanji"))))
    build_vocab_menu(non_optional(open_in_anki_menu.addMenu(shortcutfinger.home3("Vocab"))))
    build_sentence_menu(non_optional(open_in_anki_menu.addMenu(shortcutfinger.home4("Sentence"))))

def setup_web_search_menu(search_web_menu:QMenu, search_string:Callable[[],str]) -> None:
    def add_web_lookup(menu: QMenu, name: str, url: str) -> None:
        menu.addAction(name, lambda: openLink(url % parse.quote(search_string(), encoding='utf8')))

    def set_up_kanji_menu(kanji_lookup_menu:QMenu) -> None:
        add_web_lookup(kanji_lookup_menu, shortcutfinger.home1("Kanji explosion"), u"https://www.kurumi.com/jp/kjbh/?k=%s")
        add_web_lookup(kanji_lookup_menu, shortcutfinger.home2("Kanshudo"), u"https://www.kanshudo.com/search?q=%s")
        add_web_lookup(kanji_lookup_menu, shortcutfinger.home3("Kanji map"), u"https://thekanjimap.com/%s")

    def set_up_sentences_menu(sentences_lookup_menu:QMenu) -> None:
        add_web_lookup(sentences_lookup_menu, shortcutfinger.home1("Sentences: Immersion Kit"), u"https://www.immersionkit.com/dictionary?exact=true&sort=sentence_length%%3Aasc&keyword=%s")
        add_web_lookup(sentences_lookup_menu, shortcutfinger.home2("Sentences: Tatoeba"), u"https://tatoeba.org/en/sentences/search?from=jpn&to=eng&query=%s")

    def set_up_misc_menu(misc_lookup_menu:QMenu) -> None:
        def set_up_translate_menu(translate_menu: QMenu) -> None:
            add_web_lookup(translate_menu, shortcutfinger.home1("Translate: Deepl"), u"https://www.deepl.com/en/translator#ja/en/%s")
            add_web_lookup(translate_menu, shortcutfinger.home2("Translate: Kanshudo"), u"https://www.kanshudo.com/sentence_translate?q=%s")

        def set_up_images_menu(images_menu: QMenu) -> None:
            add_web_lookup(images_menu, shortcutfinger.home1("Images: Google"), "https://www.google.com/search?udm=2&tbs=sur:cl&q=%s")
            add_web_lookup(images_menu, shortcutfinger.home2("Images: Bing"), "https://www.bing.com/images/search?qft=+filterui:licenseType-Any&q=%s")

        def set_up_conjugate_menu(conjugate_menu: QMenu) -> None:
            add_web_lookup(conjugate_menu, shortcutfinger.home1("Conjugate: Japanese verb conjugator"), u"https://www.japaneseverbconjugator.com/VerbDetails.asp?Go=Conjugate&txtVerb=%s")
            add_web_lookup(conjugate_menu, shortcutfinger.home2("Conjugate: Verbix"), u"https://www.verbix.com/webverbix/japanese/%s")

        def set_up_grammar_menu(grammar_lookup_menu: QMenu) -> None:
            add_web_lookup(grammar_lookup_menu, shortcutfinger.home1("Grammar: Google"), "https://www.google.com/search?q=japanese+grammar+%s")
            add_web_lookup(grammar_lookup_menu, shortcutfinger.home2("Grammar: Japanese with anime"), "https://www.google.com/search?q=site:www.japanesewithanime.com+%s")
            add_web_lookup(grammar_lookup_menu, shortcutfinger.home3("Grammar: Wiktionary"), "https://en.wiktionary.org/wiki/%s")

        set_up_conjugate_menu(non_optional(misc_lookup_menu.addMenu(shortcutfinger.home1("Conjugate"))))
        set_up_translate_menu(non_optional(misc_lookup_menu.addMenu(shortcutfinger.home2("Translate"))))
        set_up_grammar_menu(non_optional(misc_lookup_menu.addMenu(shortcutfinger.home3("Grammar"))))
        set_up_images_menu(non_optional(misc_lookup_menu.addMenu(shortcutfinger.home4("Images"))))

    def set_up_lookup_menu(lookup_menu:QMenu) -> None:
        add_web_lookup(lookup_menu, shortcutfinger.home1("English: Merriam Webster"), u"https://www.merriam-webster.com/dictionary/%s")
        add_web_lookup(lookup_menu, shortcutfinger.home2("Lookup: Takoboto"), u"https://takoboto.jp/?q=%s")
        add_web_lookup(lookup_menu, shortcutfinger.home3("Lookup: Word Kanshudo"), u"https://www.kanshudo.com/searchw?q=%s")
        add_web_lookup(lookup_menu, shortcutfinger.home4("Lookup: Jisho"), u"https://jisho.org/search/%s")
        add_web_lookup(lookup_menu, shortcutfinger.down1("Lookup: Wanikani"), u"https://www.wanikani.com/search?query=%s")

    set_up_kanji_menu(non_optional(search_web_menu.addMenu(shortcutfinger.home1("Kanji"))))
    set_up_sentences_menu(non_optional(search_web_menu.addMenu(shortcutfinger.home2("Sentences"))))
    set_up_misc_menu(non_optional(search_web_menu.addMenu(shortcutfinger.home3("Misc"))))
    set_up_lookup_menu(non_optional(search_web_menu.addMenu(shortcutfinger.home4("Lookup"))))
