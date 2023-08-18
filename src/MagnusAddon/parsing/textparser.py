from typing import Sequence

from jamdict.jmdict import JMDEntry
from jamdict import Jamdict

from parsing.janome_extensions.tokenizer_ext import TokenizerExt
from parsing.janomeutils import ParsedWord
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
    def lookup_vocab_word_or_name(cls, word: WaniVocabNote) -> 'DictLookup':
        return cls.lookup_word_or_name(word.get_vocab(), word.get_readings())

    @classmethod
    def lookup_word_or_name(cls, word: str, readings: list[str]) -> 'DictLookup':
        result = cls.try_lookup_word_or_name(word, readings)
        if not result.found_words():
            raise KeyError("No matching entries")
        return result

    @classmethod
    def try_lookup_word_or_name(cls, word: str, readings: list[str]) -> 'DictLookup':
        def kanji_form_matches() -> list[DictEntry]:
            return [ent for ent in lookup
                    if any(ent.has_matching_kana_form(reading) for reading in readings)
                    and ent.kanji_forms()
                    and ent.has_matching_kanji_form(word)]

        def any_kana_only_matches() -> list[DictEntry]:
            return [ent for ent in lookup
                    if any(ent.has_matching_kana_form(reading) for reading in readings)
                    and ent.is_kana_only()]

        lookup = cls._lookup_word_shallow(word)
        if not lookup:
            lookup = cls._lookup_name(word)

        matching = any_kana_only_matches() if kana_utils.is_only_kana(word) else kanji_form_matches()

        return DictLookup(matching)

    @classmethod
    def lookup_word_shallow(cls, word: str) -> 'DictLookup':
        return DictLookup(cls._lookup_word_shallow(word))

    @classmethod
    def _lookup_word_shallow(cls, word: str) -> 'list[DictEntry]':
        return DictEntry.create(cls._jamdict.lookup(word, lookup_chars=False, lookup_ne=False).entries)

    @classmethod
    def _lookup_name(cls, word: str) -> list[DictEntry]:
        return DictEntry.create(cls._jamdict.lookup(word, lookup_chars=False).names)


def is_valid_word(word: str) -> bool:
    result = DictLookup.lookup_word_shallow(word)
    return result.found_words()

def identify_words(sentence: str) -> list[ParsedWord]:
    tokens = [token for token in _tokenizer.tokenize(sentence)]
    potential_words = list[ParsedWord]()

    for token_index in range(len(tokens)):
        word_combination:str = tokens[token_index].surface
        if is_valid_word(word_combination) and word_combination not in potential_words:
            potential_words.append(ParsedWord(word_combination, ""))
        for lookahead_index in range(token_index + 1, len(tokens)):
            word_combination += tokens[lookahead_index].surface
            if is_valid_word(word_combination) and word_combination not in potential_words:
                potential_words.append(ParsedWord(word_combination, ""))
            else:
                break

    return potential_words

def identify_words2(sentence: str) -> list[ParsedWord]:
    tokens = [token for token in _tokenizer.tokenize(sentence) if not token.is_noise_token()]
    potential_words = list[str]()

    for token_index in range(len(tokens)):
        token = tokens[token_index]

        if not is_valid_word(token.base_form): continue # the is_noise_token method does not actually work as of yet so we do this.
        if token.base_form not in potential_words:
            potential_words.append(token.base_form)

        if not is_valid_word(token.surface): continue
        if token.surface not in potential_words:
            potential_words.append(token.surface)

        word_combination: str = token.surface
        for lookahead_index in range(token_index + 1, len(tokens)):
            surface_combination = word_combination + tokens[lookahead_index].surface
            if is_valid_word(surface_combination):
                if surface_combination not in potential_words:
                    potential_words.append(surface_combination)
                    word_combination = surface_combination
            else:
                base_form_combination = word_combination + tokens[lookahead_index].base_form
                if is_valid_word(base_form_combination):
                    if base_form_combination not in potential_words:
                        potential_words.append(base_form_combination)
                break

    return [ParsedWord(word, "") for word in potential_words]

def identify_first_word(sentence: str) -> str:

    tokens = _tokenizer.tokenize(sentence)
    word_combination = ""
    for token_index in range(len(tokens)):
        word_combination: str = tokens[token_index].base_form

        for lookahead_index in range(token_index + 1, len(tokens)):
            next_combination = word_combination + tokens[token_index + 1].base_form
            if not is_valid_word(next_combination):
                return word_combination
            word_combination = next_combination

        return word_combination


    return word_combination



