from urllib import parse

from PyQt6.QtWidgets import QMenu
from aqt.utils import openLink

from hooks.right_click_menu_utils import add_sentence_lookup, add_lookup_action, add_text_vocab_lookup
from note.note_constants import NoteFields, NoteTypes
from ankiutils import search_utils as su
from sysutils.typed import checked_cast


def setup_search_menu(root_menu: QMenu, sel_clip: str) -> None:
    if sel_clip:
        search_menu = checked_cast(QMenu, root_menu.addMenu("&Search"))
        setup_anki_search_menu(search_menu, sel_clip)
        setup_web_search_menu(search_menu, sel_clip)


def setup_anki_search_menu(search_menu: QMenu, sel_clip: str) -> None:
    search_anki_menu = checked_cast(QMenu, search_menu.addMenu("&Anki"))
    add_lookup_action(search_anki_menu, "&Kanji", su.kanji_in_string(sel_clip))
    add_lookup_action(search_anki_menu, "&Vocab", su.single_vocab_by_question_reading_or_answer_exact(sel_clip))
    add_lookup_action(search_anki_menu, "Vocab &Wildcard", su.single_vocab_wildcard(sel_clip))
    add_lookup_action(search_anki_menu, "&Radical", build_radical_search_string(sel_clip))
    add_sentence_lookup(search_anki_menu, "&Sentence", sel_clip)
    add_text_vocab_lookup(search_anki_menu, "Text &words", sel_clip)

def setup_web_search_menu(search_menu: QMenu, sel_clip: str) -> None:
    search_web_menu = checked_cast(QMenu, search_menu.addMenu("&Web"))
    add_web_lookup(search_web_menu, "&Takoboto", u"https://takoboto.jp/?q=%s", sel_clip)
    add_web_lookup(search_web_menu, "&Japanese with anime", "https://www.google.com/search?q=site:www.japanesewithanime.com+%s", sel_clip)

    add_web_lookup(search_web_menu, "&Google images", "https://www.google.com/images?q=%s", sel_clip)

    add_web_lookup(search_web_menu, "&Merriam Webster", u"https://www.merriam-webster.com/dictionary/%s", sel_clip)
    add_web_lookup(search_web_menu, "&Immersion Kit", u"https://www.immersionkit.com/dictionary?exact=true&sort=shortness&keyword=%s", sel_clip)
    add_web_lookup(search_web_menu, "Japanese verb &conjugator", u"https://www.japaneseverbconjugator.com/VerbDetails.asp?Go=Conjugate&txtVerb=%s", sel_clip)
    add_web_lookup(search_web_menu, "&Kanshudo Word Search", u"https://www.kanshudo.com/searchw?q=%s", sel_clip)
    add_web_lookup(search_web_menu, "&Kanshudo Sentence Translate", u"https://www.kanshudo.com/sentence_translate?q=%s", sel_clip)

    add_web_lookup(search_web_menu, "&Deepl", u"https://www.deepl.com/en/translator#ja/en/%s", sel_clip),
    add_web_lookup(search_web_menu, "&Jisho", u"https://jisho.org/search/%s", sel_clip)
    add_web_lookup(search_web_menu, "&Wanikani", u"https://www.wanikani.com/search?query=%s", sel_clip)
    add_web_lookup(search_web_menu, "&Verbix conjugate", u"https://www.verbix.com/webverbix/japanese/%s", sel_clip)


def add_web_lookup(menu: QMenu, name: str, url: str, search: str):
    search = parse.quote(search, encoding='utf8')
    menu.addAction(name, lambda: openLink(url % search))


def build_radical_search_string(selected: str) -> str:
    start = f"{NoteFields.Radical.answer}:{selected} OR"
    clauses = " OR ".join([f"{NoteFields.Radical.question}:{char}" for char in selected])
    return f"note:{NoteTypes.Radical} ( {start} {clauses} )"
