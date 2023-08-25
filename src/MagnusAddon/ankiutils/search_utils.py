from typing import Callable

import aqt
from aqt.browser import Browser

from note.mynote import MyNote
from note.sentencenote import SentenceNote
from note.wanikanjinote import WaniKanjiNote
from note.waniradicalnote import WaniRadicalNote
from note.wanivocabnote import WaniVocabNote
from parsing import textparser
from parsing.janome_extensions.parsed_word import ParsedWord
from sysutils.ui_utils import UIUtils
from wanikani.wani_constants import Wani, Mine

class SearchTags:
    Note = "note"
    Tag = "tag"
    Deck = "deck"
    Card = "card"

def vocab_uk_by_reading(reading: str) -> str: return f"""(tag:_uk AND Reading:{reading})"""

deck_listen = f"{SearchTags.Deck}:{Mine.DeckFilters.Listen}"
kanji_filter = f"{SearchTags.Note}:{Wani.NoteType.Kanji}"
vocab_read = f"({SearchTags.Note}:{Wani.NoteType.Vocab} {SearchTags.Deck}:*Read*)"

def single_vocab_wildcard(vocab:str) -> str: return f"{vocab_read} (Q:*{vocab}* OR Reading:*{vocab}* OR A:*{vocab}*)"

def vocab_dependencies_lookup_query(vocab: WaniVocabNote) -> str:
    def single_vocab_clause(voc: ParsedWord) -> str:
        return f'(tag:_uk AND Reading:{voc.word})' if voc.is_kana_only() else f'Q:{voc.word}'

    def create_vocab_clause(text:str) -> str:
        dictionary_forms = [voc for voc in textparser.identify_words(text) if voc.word != vocab.get_question()]
        return f"({vocab_read} ({' OR '.join([single_vocab_clause(voc) for voc in dictionary_forms])})) OR " if dictionary_forms else ""

    def create_vocab_vocab_clause() -> str:
        return create_vocab_clause(vocab.get_question())

    def create_kanji_clause() -> str:
        return f"note:{Wani.NoteType.Kanji} ( {' OR '.join([f'{Wani.KanjiFields.question}:{char}' for char in vocab.get_question()])} )"

    return f'''{create_vocab_vocab_clause()} ({create_kanji_clause()})'''

def do_lookup_and_show_previewer(text: str) -> None:
    do_lookup(text)
    UIUtils.activate_preview()


def do_lookup(text) -> None:
    browser: Browser = aqt.dialogs.open('Browser', aqt.mw)
    browser.form.searchEdit.lineEdit().setText(text)
    browser.onSearchActivated()


def lookup_promise(search: Callable[[], str]) -> Callable[[],None]: return lambda: do_lookup_and_show_previewer(search())

def sentence_vocab_lookup(sentence:SentenceNote) -> str: return text_vocab_lookup(sentence.get_active_question())

def vocab_with_kanji(note:WaniKanjiNote) -> str: return f"{vocab_read} Q:*{note.get_question()}*"

def text_vocab_lookup(text:str) -> str:
    def voc_clause(voc: ParsedWord) -> str:
        return f'(tag:_uk AND Reading:{voc.word})' if voc.is_kana_only() else f'Q:{voc.word}'

    dictionary_forms = textparser.identify_words(text)
    return f"{vocab_read} ({' OR '.join([voc_clause(voc) for voc in dictionary_forms])})"


def lookup_dependencies(note: MyNote):
    # noinspection PyTypeChecker
    type_map: dict[type, Callable[[], str]] = {
        WaniVocabNote: lambda: vocab_dependencies_lookup_query(note),
        WaniKanjiNote: lambda: vocab_with_kanji(note),
        SentenceNote: lambda: sentence_vocab_lookup(note),
        WaniRadicalNote: lambda: "",
        MyNote: lambda: ""
    }

    search = type_map[type(note)]()
    if search:
        UIUtils.deactivate_preview()
        do_lookup(search)
        UIUtils.activate_reviewer()