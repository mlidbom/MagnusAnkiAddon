from urllib import parse

from PyQt6.QtWidgets import QMenu
from aqt.utils import openLink

from hooks.right_click_menu_utils import add_sentence_lookup, add_lookup_action
from wanikani.wani_constants import Wani, Mine


def setup_search_menu(root_menu, sel_clip):
    if sel_clip:
        search_menu = root_menu.addMenu("&Search")
        setup_anki_search_menu(search_menu, sel_clip)
        setup_web_search_menu(search_menu, sel_clip)


def setup_anki_search_menu(search_menu, sel_clip):
    search_anki_menu = search_menu.addMenu("&Anki")
    add_lookup_action(search_anki_menu, "&Kanji", f"note:{Wani.NoteType.Kanji} ( {' OR '.join([f'{Wani.KanjiFields.Kanji}:{char}' for char in sel_clip])} )")
    add_lookup_action(search_anki_menu, "&Vocab", f"deck:*Vocab* deck:*Read* (Vocab:{sel_clip} OR Reading:re:\\b{sel_clip}\\b OR Vocab_Meaning:re:\\b{sel_clip}\\b )")
    add_lookup_action(search_anki_menu, "Vocab &Wildcard", f"deck:*Vocab* deck:*Read* (Vocab:*{sel_clip}* OR Reading:*{sel_clip}* OR Vocab_Meaning:*{sel_clip}*)")
    add_lookup_action(search_anki_menu, "&Radical", build_radical_search_string(sel_clip))
    add_sentence_lookup(search_anki_menu, "&Sentence", sel_clip)
    add_lookup_action(search_anki_menu, "Listen", f"deck:{Mine.DeckFilters.Listen} {sel_clip}")


def setup_web_search_menu(search_menu, sel_clip):
    search_web_menu = search_menu.addMenu("&Web")
    add_web_lookup(search_web_menu, "&Takoboto", u"https://takoboto.jp/?q=%s", sel_clip)
    add_web_lookup(search_web_menu, "&Merriam Webster", u"https://www.merriam-webster.com/dictionary/%s", sel_clip)
    add_web_lookup(search_web_menu, "&Immersion Kit", u"https://www.immersionkit.com/dictionary?exact=true&sort=shortness&keyword=%s", sel_clip)
    add_web_lookup(search_web_menu, "Japanese verb &conjugator", u"https://www.japaneseverbconjugator.com/VerbDetails.asp?Go=Conjugate&txtVerb=%s", sel_clip)
    add_web_lookup(search_web_menu, "&Kanshudo", u"https://www.kanshudo.com/searchw?q=%s", sel_clip)
    add_web_lookup(search_web_menu, "&Deepl", u"https://www.deepl.com/en/translator#ja/en/%s", sel_clip),
    add_web_lookup(search_web_menu, "&Jisho", u"https://jisho.org/search/%s", sel_clip)
    add_web_lookup(search_web_menu, "&Wanikani", u"https://www.wanikani.com/search?query=%s", sel_clip)
    add_web_lookup(search_web_menu, "&Verbix conjugate", u"https://www.verbix.com/webverbix/japanese/%s", sel_clip)


def add_web_lookup(menu: QMenu, name: str, url: str, search: str):
    search = parse.quote(search, encoding='utf8')
    menu.addAction(name, lambda: openLink(url % search))


def build_radical_search_string(selected: str) -> str:
    start = f"{Wani.RadicalFields.Radical_Name}:{selected} OR"
    clauses = " OR ".join([f"{Wani.RadicalFields.Radical}:{char}" for char in selected])
    return f"note:{Wani.NoteType.Radical} ( {start} {clauses} )"