from typing import Sequence

from jamdict.jmdict import JMDEntry
from jamdict import Jamdict
from functools import lru_cache

from parsing.janome_extensions.parsed_word import ParsedWord
from parsing.janome_extensions.tokenizer_ext import TokenizerExt
from sysutils import kana_utils

_tokenizer = TokenizerExt()

class DictEntry:
    def __init__(self, entry: JMDEntry) -> None:
        self.entry = entry

    def is_kana_only(self) -> bool:
        return not self.entry.kanji_forms or any((sense for sense
                                                  in self.entry.senses
                                                  if 'word usually written using kana alone' in sense.misc))

    @classmethod
    def create(cls, entries: Sequence[JMDEntry]) -> list['DictEntry']:
        return [cls(entry) for entry in entries]

    def has_matching_kana_form(self, search: str) -> bool:
        search = kana_utils.to_hiragana(search)
        return any(search == kana_utils.to_hiragana(form) for form in self.kana_forms())

    def is_default_kana_form(self, search: str) -> bool:
        search = kana_utils.to_hiragana(search)
        return search == kana_utils.to_hiragana(self.kana_forms()[0])

    def has_matching_kanji_form(self, search: str) -> bool:
        search = kana_utils.to_hiragana(search)
        return any(search == kana_utils.to_hiragana(form) for form in self.kanji_forms())

    def is_default_kanji_form(self, search: str) -> bool:
        search = kana_utils.to_hiragana(search)
        return search == kana_utils.to_hiragana(self.kanji_forms()[0])

    def kana_forms(self) -> list[str]: return [ent.text for ent in self.entry.kana_forms]
    def kanji_forms(self) -> list[str]: return [ent.text for ent in self.entry.kanji_forms]


class DictLookup:
    from note.wanivocabnote import WaniVocabNote

    _jamdict = Jamdict(memory_mode=True)

    def __init__(self, entries: list[DictEntry]):
        self.entries = entries

    def found_words_count(self) -> int: return len(self.entries)
    def found_words(self) -> bool: return len(self.entries) > 0

    def is_uk(self) -> bool: return any((ent for ent
                                         in self.entries
                                         if ent.is_kana_only()))

    @classmethod
    def try_lookup_vocab_word_or_name(cls, word: WaniVocabNote) -> 'DictLookup':
        return cls.try_lookup_word_or_name(word.get_vocab(), word.get_readings())

    @classmethod
    def lookup_word_or_name(cls, word: str, readings: list[str]) -> 'DictLookup':
        result = cls.try_lookup_word_or_name(word, readings)
        if not result.found_words():
            raise KeyError("No matching entries")
        return result

    @classmethod
    def try_lookup_word_or_name(cls, word: str, readings: list[str]) -> 'DictLookup':
        return cls._try_lookup_word_or_name(word, tuple(readings))

    @classmethod
    @lru_cache(maxsize=None)
    def _try_lookup_word_or_name(cls, word: str, readings: tuple[str]) -> 'DictLookup':
        def kanji_form_matches() -> list[DictEntry]:
            return [ent for ent in lookup
                    if any(ent.has_matching_kana_form(reading) for reading in readings)
                    and ent.kanji_forms()
                    and ent.has_matching_kanji_form(word)]

        def any_kana_only_matches() -> list[DictEntry]:
            return [ent for ent in lookup
                    if any(ent.has_matching_kana_form(reading) for reading in readings)
                    and ent.is_kana_only()]

        lookup = cls._lookup_word(word)
        if not lookup:
            lookup = cls._lookup_name(word)

        matching = any_kana_only_matches() if kana_utils.is_only_kana(word) else kanji_form_matches()

        return DictLookup(matching)

    @classmethod
    def lookup_word_shallow(cls, word: str) -> 'DictLookup':
        return DictLookup(cls._lookup_word(word))

    @classmethod
    @lru_cache(maxsize=None)  # _lookup_word_shallow.cache_clear(), _lookup_word_shallow.cache_info()
    def _lookup_word(cls, word: str) -> 'list[DictEntry]':
        return DictEntry.create(cls._jamdict.lookup(word, lookup_chars=False, lookup_ne=False).entries)

    @classmethod
    @lru_cache(maxsize=None)  # _lookup_word_shallow.cache_clear(), _lookup_word_shallow.cache_info()
    def _lookup_name(cls, word: str) -> list[DictEntry]:
        return DictEntry.create(cls._jamdict.lookup(word, lookup_chars=False).names)


def word_is_in_dictionary(word: str) -> bool:
    result = DictLookup.lookup_word_shallow(word)
    return result.found_words()

_max_lookahead = 4
def identify_words(sentence: str) -> list[ParsedWord]:
    def add_word_if_it_is_in_dictionary(word: str) -> None:
        if word_is_in_dictionary(word) and word not in found_words:
            found_words.add(word)
            found_words_list.append(word)

    def check_for_compound_words() -> None:
        surface_compound = token.surface
        for lookahead_index in range(token_index + 1, min(token_index + _max_lookahead, len(tokens))):
            look_ahead_token = tokens[lookahead_index]
            base_compound = surface_compound + look_ahead_token.base_form
            surface_compound += look_ahead_token.surface

            if base_compound != surface_compound:
                add_word_if_it_is_in_dictionary(base_compound)
            add_word_if_it_is_in_dictionary(surface_compound)

    tokens = _tokenizer.tokenize(sentence).tokens
    found_words = set[str]()
    found_words_list = []

    for token_index, token in enumerate(tokens):
        add_word_if_it_is_in_dictionary(token.base_form)
        add_word_if_it_is_in_dictionary(token.surface)
        check_for_compound_words()

    return [ParsedWord(word) for word in found_words_list]


