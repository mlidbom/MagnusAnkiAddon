from urllib import parse

from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QMenu
from aqt.utils import openLink

from hooks.right_click_menu_utils import add_lookup_action, add_text_vocab_lookup
from note.note_constants import NoteFields, NoteTypes
from ankiutils import query_builder
from sysutils.typed import checked_cast

from hooks import shortcutfinger


def setup_anki_open_menu(string_menu:QMenu, menu_string:str) -> None:
    search_anki_menu = checked_cast(QMenu, string_menu.addMenu(shortcutfinger.home4("Open in Anki")))


    add_lookup_action(search_anki_menu, shortcutfinger.home1("Open Exact matches | no sentences | reading cards"), query_builder.exact_matches_no_sentences_reading_cards(menu_string))
    add_lookup_action(search_anki_menu, shortcutfinger.home2("Open Exact matches with sentences"), query_builder.exact_matches(menu_string))

    add_lookup_action(search_anki_menu, shortcutfinger.home3("Kanji"), query_builder.kanji_in_string(menu_string))
    add_lookup_action(search_anki_menu, shortcutfinger.home4("Radical"), build_radical_search_string(menu_string))

    add_lookup_action(search_anki_menu, shortcutfinger.up1("Vocab form -"), query_builder.single_vocab_by_form_exact(menu_string))
    add_lookup_action(search_anki_menu, shortcutfinger.up2("Vocab form - read card only"), query_builder.single_vocab_by_form_exact_read_card_only(menu_string))

    add_lookup_action(search_anki_menu, shortcutfinger.up3("Vocab form, reading or answer"), query_builder.single_vocab_by_question_reading_or_answer_exact(menu_string))
    add_lookup_action(search_anki_menu, shortcutfinger.up4("Vocab Wildcard"), query_builder.single_vocab_wildcard(menu_string))
    add_lookup_action(search_anki_menu, shortcutfinger.down1("Sentence - Parse Vocabulary"), query_builder.sentence_search(menu_string))
    add_lookup_action(search_anki_menu, shortcutfinger.down2("Sentence - Exact String"), query_builder.sentence_search(menu_string, exact=True))
    add_text_vocab_lookup(search_anki_menu, shortcutfinger.down3("Text words"), menu_string)

def setup_web_search_menu(string_menu:QMenu, menu_string:str) -> None:
    search_web_menu = checked_cast(QMenu, string_menu.addMenu(shortcutfinger.down1("Search Web")))

    add_web_lookup(search_web_menu, shortcutfinger.home1("English: Merriam Webster"), u"https://www.merriam-webster.com/dictionary/%s", menu_string)

    add_web_lookup(search_web_menu, shortcutfinger.home2("Sentences: Immersion Kit"), u"https://www.immersionkit.com/dictionary?exact=true&sort=shortness&keyword=%s", menu_string)
    add_web_lookup(search_web_menu, shortcutfinger.home3("Sentences: Tatoeba"), u"https://tatoeba.org/en/sentences/search?from=jpn&to=eng&query=%s", menu_string)

    kanji_lookup_menu = checked_cast(QMenu, search_web_menu.addMenu(shortcutfinger.home4("Kanji")))
    add_web_lookup(kanji_lookup_menu, shortcutfinger.home1("Kanji explosion"), u"https://www.kurumi.com/jp/kjbh/?k=%s", menu_string)
    add_web_lookup(kanji_lookup_menu, shortcutfinger.home2("Kanshudo"), u"https://www.kanshudo.com/search?q=%s", menu_string)
    add_web_lookup(kanji_lookup_menu, shortcutfinger.home3("Kanji map"), u"https://thekanjimap.com/%s", menu_string)

    add_web_lookup(search_web_menu, shortcutfinger.home5("Grammar: Google"), "https://www.google.com/search?q=japanese+grammar+%s", menu_string)
    add_web_lookup(search_web_menu, shortcutfinger.up1("Grammar: Japanese with anime"), "https://www.google.com/search?q=site:www.japanesewithanime.com+%s", menu_string)
    add_web_lookup(search_web_menu, shortcutfinger.up2("Grammar: Wiktionary"), "https://en.wiktionary.org/wiki/%s", menu_string)


    add_web_lookup(search_web_menu, shortcutfinger.up3("Images: Google"), "https://www.google.com/search?udm=2&tbs=sur:cl&q=%s", menu_string)
    add_web_lookup(search_web_menu, shortcutfinger.up4("Images: Bing"), "https://www.bing.com/images/search?qft=+filterui:licenseType-Any&q=%s", menu_string)

    add_web_lookup(search_web_menu, shortcutfinger.up5("Lookup: Takoboto"), u"https://takoboto.jp/?q=%s", menu_string)
    add_web_lookup(search_web_menu, shortcutfinger.down1("Lookup: Word Kanshudo"), u"https://www.kanshudo.com/searchw?q=%s", menu_string)

    add_web_lookup(search_web_menu, shortcutfinger.down2("Lookup: Jisho"), u"https://jisho.org/search/%s", menu_string)
    add_web_lookup(search_web_menu, shortcutfinger.down3("Lookup: Wanikani"), u"https://www.wanikani.com/search?query=%s", menu_string)

    add_web_lookup(search_web_menu, shortcutfinger.down5("Conjugate: Japanese verb conjugator"), u"https://www.japaneseverbconjugator.com/VerbDetails.asp?Go=Conjugate&txtVerb=%s", menu_string)
    add_web_lookup(search_web_menu, shortcutfinger.home6("Conjugate: Verbix"), u"https://www.verbix.com/webverbix/japanese/%s", menu_string)

    add_web_lookup(search_web_menu, shortcutfinger.up6("Translate: Deepl"), u"https://www.deepl.com/en/translator#ja/en/%s", menu_string)
    add_web_lookup(search_web_menu, shortcutfinger.down6("Translate: Kanshudo"), u"https://www.kanshudo.com/sentence_translate?q=%s", menu_string)

def add_web_lookup(menu: QMenu, name: str, url: str, search: str) -> None:
    search = parse.quote(search, encoding='utf8')

    menu.addAction(name, lambda: openLink(url % search))


def build_radical_search_string(selected: str) -> str:
    start = f"{NoteFields.Radical.answer}:{selected} OR"
    clauses = " OR ".join([f"{NoteFields.Radical.question}:{char}" for char in selected])
    return f"note:{NoteTypes.Radical} ( {start} {clauses} )"
