from urllib import parse

from PyQt6.QtWidgets import QMenu
from aqt.utils import openLink

from hooks.right_click_menu_utils import add_lookup_action, add_text_vocab_lookup
from note.note_constants import NoteFields, NoteTypes
from ankiutils import app, query_builder
from sysutils import kana_utils
from sysutils.typed import non_optional

from hooks import shortcutfinger


def setup_anki_open_menu(open_in_anki_menu:QMenu, menu_string:str) -> None:
    def build_exact_menu(exact_menu:QMenu) -> None:
        add_lookup_action(exact_menu, shortcutfinger.home1("Open Exact matches | no sentences | reading cards"), query_builder.exact_matches_no_sentences_reading_cards(menu_string))
        add_lookup_action(exact_menu, shortcutfinger.home2("Open Exact matches with sentences"), query_builder.exact_matches(menu_string))


    def build_kanji_menu(kanji_menu:QMenu) -> None:
        def create_kanji_lookup() -> str:
            hiragana = kana_utils.to_hiragana(menu_string)
            if kana_utils.is_only_kana(hiragana):
                return query_builder.notes_lookup(list(app.col().kanji.with_reading(hiragana)))
            return query_builder.kanji_in_string(menu_string)

        add_lookup_action(kanji_menu, shortcutfinger.home1("Kanji"), create_kanji_lookup())
        add_lookup_action(kanji_menu, shortcutfinger.home2("Kanji by reading part"), query_builder.kanji_with_reading_part(menu_string))
        add_lookup_action(kanji_menu, shortcutfinger.home3("Kanji with radicals"), query_builder.kanji_with_radicals_in_string(menu_string))

    def build_vocab_menu(vocab_menu:QMenu) -> None:
        add_lookup_action(vocab_menu, shortcutfinger.home1("Vocab form -"), query_builder.single_vocab_by_form_exact(menu_string))
        add_lookup_action(vocab_menu, shortcutfinger.home2("Vocab form - read card only"), query_builder.single_vocab_by_form_exact_read_card_only(menu_string))
        add_lookup_action(vocab_menu, shortcutfinger.home3("Vocab form, reading or answer"), query_builder.single_vocab_by_question_reading_or_answer_exact(menu_string))
        add_lookup_action(vocab_menu, shortcutfinger.home4("Vocab Wildcard"), query_builder.single_vocab_wildcard(menu_string))
        add_text_vocab_lookup(vocab_menu, shortcutfinger.up1("Text words"), menu_string)

    def build_sentence_menu(sentence_menu:QMenu) -> None:
        add_lookup_action(sentence_menu, shortcutfinger.home1("Sentence - Parse Vocabulary"), query_builder.sentence_search(menu_string))
        add_lookup_action(sentence_menu, shortcutfinger.home2("Sentence - Exact String"), query_builder.sentence_search(menu_string, exact=True))

    build_exact_menu(non_optional(open_in_anki_menu.addMenu(shortcutfinger.home1("Exact matches"))))
    build_kanji_menu(non_optional(open_in_anki_menu.addMenu(shortcutfinger.home2("Kanji"))))
    build_vocab_menu(non_optional(open_in_anki_menu.addMenu(shortcutfinger.home3("Vocab"))))
    build_sentence_menu(non_optional(open_in_anki_menu.addMenu(shortcutfinger.home4("Sentence"))))

def setup_web_search_menu(search_web_menu:QMenu, menu_string:str) -> None:
    def add_web_lookup(menu: QMenu, name: str, url: str, search: str) -> None:
        search = parse.quote(search, encoding='utf8')
        menu.addAction(name, lambda: openLink(url % search))

    def set_up_kanji_menu(kanji_lookup_menu:QMenu) -> None:
        add_web_lookup(kanji_lookup_menu, shortcutfinger.home1("Kanji explosion"), u"https://www.kurumi.com/jp/kjbh/?k=%s", menu_string)
        add_web_lookup(kanji_lookup_menu, shortcutfinger.home2("Kanshudo"), u"https://www.kanshudo.com/search?q=%s", menu_string)
        add_web_lookup(kanji_lookup_menu, shortcutfinger.home3("Kanji map"), u"https://thekanjimap.com/%s", menu_string)

    def set_up_sentences_menu(sentences_lookup_menu:QMenu) -> None:
        add_web_lookup(sentences_lookup_menu, shortcutfinger.home1("Sentences: Immersion Kit"), u"https://www.immersionkit.com/dictionary?exact=true&sort=sentence_length%%3Aasc&keyword=%s", menu_string)
        add_web_lookup(sentences_lookup_menu, shortcutfinger.home2("Sentences: Tatoeba"), u"https://tatoeba.org/en/sentences/search?from=jpn&to=eng&query=%s", menu_string)

    def set_up_misc_menu(misc_lookup_menu:QMenu) -> None:
        set_up_conjugate_menu(non_optional(misc_lookup_menu.addMenu(shortcutfinger.home1("Conjugate"))))
        set_up_translate_menu(non_optional(misc_lookup_menu.addMenu(shortcutfinger.home2("Translate"))))
        set_up_grammar_menu(non_optional(misc_lookup_menu.addMenu(shortcutfinger.home3("Grammar"))))
        set_up_images_menu(non_optional(misc_lookup_menu.addMenu(shortcutfinger.home4("Images"))))

    def set_up_grammar_menu(grammar_lookup_menu:QMenu) -> None:
        add_web_lookup(grammar_lookup_menu, shortcutfinger.home1("Grammar: Google"), "https://www.google.com/search?q=japanese+grammar+%s", menu_string)
        add_web_lookup(grammar_lookup_menu, shortcutfinger.home2("Grammar: Japanese with anime"), "https://www.google.com/search?q=site:www.japanesewithanime.com+%s", menu_string)
        add_web_lookup(grammar_lookup_menu, shortcutfinger.home3("Grammar: Wiktionary"), "https://en.wiktionary.org/wiki/%s", menu_string)

    def set_up_lookup_menu(lookup_menu:QMenu) -> None:
        add_web_lookup(lookup_menu, shortcutfinger.home1("English: Merriam Webster"), u"https://www.merriam-webster.com/dictionary/%s", menu_string)
        add_web_lookup(lookup_menu, shortcutfinger.home2("Lookup: Takoboto"), u"https://takoboto.jp/?q=%s", menu_string)
        add_web_lookup(lookup_menu, shortcutfinger.home3("Lookup: Word Kanshudo"), u"https://www.kanshudo.com/searchw?q=%s", menu_string)
        add_web_lookup(lookup_menu, shortcutfinger.home4("Lookup: Jisho"), u"https://jisho.org/search/%s", menu_string)
        add_web_lookup(lookup_menu, shortcutfinger.down1("Lookup: Wanikani"), u"https://www.wanikani.com/search?query=%s", menu_string)

    def set_up_images_menu(images_menu:QMenu) -> None:
        add_web_lookup(images_menu, shortcutfinger.home1("Images: Google"), "https://www.google.com/search?udm=2&tbs=sur:cl&q=%s", menu_string)
        add_web_lookup(images_menu, shortcutfinger.home2("Images: Bing"), "https://www.bing.com/images/search?qft=+filterui:licenseType-Any&q=%s", menu_string)

    def set_up_conjugate_menu(conjugate_menu:QMenu) -> None:
        add_web_lookup(conjugate_menu, shortcutfinger.home1("Conjugate: Japanese verb conjugator"), u"https://www.japaneseverbconjugator.com/VerbDetails.asp?Go=Conjugate&txtVerb=%s", menu_string)
        add_web_lookup(conjugate_menu, shortcutfinger.home2("Conjugate: Verbix"), u"https://www.verbix.com/webverbix/japanese/%s", menu_string)

    def set_up_translate_menu(translate_menu:QMenu) -> None:
        add_web_lookup(translate_menu, shortcutfinger.home1("Translate: Deepl"), u"https://www.deepl.com/en/translator#ja/en/%s", menu_string)
        add_web_lookup(translate_menu, shortcutfinger.home2("Translate: Kanshudo"), u"https://www.kanshudo.com/sentence_translate?q=%s", menu_string)

    set_up_kanji_menu(non_optional(search_web_menu.addMenu(shortcutfinger.home1("Kanji"))))
    set_up_sentences_menu(non_optional(search_web_menu.addMenu(shortcutfinger.home2("Sentences"))))
    set_up_misc_menu(non_optional(search_web_menu.addMenu(shortcutfinger.home3("Misc"))))
    set_up_lookup_menu(non_optional(search_web_menu.addMenu(shortcutfinger.home4("Lookup"))))
