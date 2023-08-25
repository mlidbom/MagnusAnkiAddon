from typing import Callable

import aqt
from aqt.browser import Browser

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
        dictionary_forms = textparser.identify_words(text)
        return f"{vocab_read} ({' OR '.join([single_vocab_clause(voc) for voc in dictionary_forms])})"

    def create_vocab_vocab_clause() -> str:
        return create_vocab_clause(vocab.get_question())

    def create_kanji_clause() -> str:
        return f"note:{Wani.NoteType.Kanji} ( {' OR '.join([f'{Wani.KanjiFields.question}:{char}' for char in vocab.get_question()])} )"

    return f'''({create_vocab_vocab_clause()}) OR ({create_kanji_clause()})'''

def do_lookup(text: str) -> None:
    browser: Browser = aqt.dialogs.open('Browser', aqt.mw)
    browser.form.searchEdit.lineEdit().setText(text)
    browser.onSearchActivated()
    UIUtils.activate_preview()

def lookup_promise(search: Callable[[], str]) -> Callable[[],None]: return lambda: do_lookup(search())
