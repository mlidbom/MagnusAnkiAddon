from jamdict.jmdict import JMDEntry
from jamdict.util import LookupResult
from janome.tokenizer import Tokenizer, Token
from jamdict import Jamdict

from parsing.janomeutils import ParsedWord, is_noise_token

_tokenizer: Tokenizer = Tokenizer()

class DictEntry:
    def __init__(self, entry: JMDEntry) -> None:
        self.entry = entry

    def is_kana_only(self) -> bool:
        return any((sense for sense
                    in self.entry.senses
                    if 'word usually written using kana alone' in sense.misc))

    @classmethod
    def create(cls, result: LookupResult) -> list['DictEntry']:
        return [cls(entry) for entry in result.entries]

    def readings(self) -> list[str]: return [ent.text for ent in self.entry.kana_forms]


class DictLookup:
    from note.wanivocabnote import WaniVocabNote

    _jamdict = Jamdict(memory_mode=True)

    def __init__(self, result: LookupResult):
        self.result = result
        self.entries = DictEntry.create(result)

    def found_words_count(self) -> int: return len(self.entries)
    def found_words(self) -> bool: return len(self.entries) > 0

    def is_uk(self) -> bool: return any((ent for ent
                                         in self.entries
                                         if ent.is_kana_only()))

    @classmethod
    def lookup_word_shallow(cls, word: str) -> 'DictLookup':
        return DictLookup(cls._jamdict.lookup(word, lookup_chars=False, lookup_ne=False))

    @classmethod
    def lookup_vocab_word_shallow(cls, word: WaniVocabNote) -> DictEntry:

        lookup = cls.lookup_word_shallow(word.get_vocab())

        matching = [ent for ent in lookup.entries if word.get_reading() in ent.readings()]

        if not any(matching): raise Exception("No matching entries")
        if len(matching) > 1: raise Exception("Multiple matching entries")

        return DictEntry(matching[0].entry)

    @classmethod
    def lookup_word_shallow_strict(cls, word: str) -> 'DictLookup':
        return DictLookup(cls._jamdict.lookup(word, lookup_chars=False, lookup_ne=False, strict_lookup=True))

    @classmethod
    def lookup_word_deep(cls, word: str) -> 'DictLookup':
        return DictLookup(cls._jamdict.lookup(word))


def is_valid_word(word: str) -> bool:
    result = DictLookup.lookup_word_shallow(word)
    return result.found_words()

def identify_words(sentence: str) -> list[ParsedWord]:
    tokens: list[Token] = [token for token in _tokenizer.tokenize(sentence)]
    potential_words = list[ParsedWord]()

    for token_index in range(len(tokens)):
        word_combination:str = tokens[token_index].node.surface
        if is_valid_word(word_combination) and word_combination not in potential_words:
            potential_words.append(ParsedWord(word_combination, ""))
        for lookahead_index in range(token_index + 1, len(tokens)):
            word_combination += tokens[lookahead_index].node.surface
            if is_valid_word(word_combination) and word_combination not in potential_words:
                potential_words.append(ParsedWord(word_combination, ""))
            else:
                break

    return potential_words

def identify_words2(sentence: str) -> list[ParsedWord]:
    tokens: list[Token] = [token for token in _tokenizer.tokenize(sentence) if not is_noise_token(token)]
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

    tokens: list[Token] = [token for token in _tokenizer.tokenize(sentence) if not token.part_of_speech.startswith("記号")]
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



