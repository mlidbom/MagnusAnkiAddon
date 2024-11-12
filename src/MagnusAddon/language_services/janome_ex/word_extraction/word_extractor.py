from __future__ import annotations

from typing import Any, Optional

from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.janome_ex.word_extraction.extracted_word import ExtractedWord
from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer

_tokenizer = JNTokenizer()


_noise_characters = {'.',',',':',';','/','|','。','、'}
_max_lookahead = 12

version = "janome_extractor_1"


class WordExclusion:
    _separator = "####"
    _no_index = -1
    def __init__(self, word:str, index:int = _no_index) -> None:
        self.word = word
        self.index = index

    def excludes(self, word:HierarchicalWord) -> bool:
        return word.word.word == self.word and (self.index == WordExclusion._no_index or self.index == word.word.start_index)

    @classmethod
    def from_string(cls, exclusion:str) -> WordExclusion:
        if cls._separator in exclusion:
            parts = exclusion.split(cls._separator)
            return WordExclusion(parts[1].strip(), int(parts[0].strip()))
        return WordExclusion(exclusion.strip())

    def as_string(self) -> str:
        return self.word if self.index == WordExclusion._no_index else f"""{self.index}{self._separator}{self.word}"""

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, WordExclusion):
            return self.word == other.word and self.index == other.index
        return False

    def __hash__(self) -> int:
        return hash((self.word, self.index))

    def covers(self, other:WordExclusion) -> bool:
        return self.word == other.word and (self.index == WordExclusion._no_index or self.index == other.index)

class HierarchicalWord:
    def __init__(self, word: ExtractedWord):
        self.word = word
        self.parent:Optional[HierarchicalWord] = None
        self.children:list[HierarchicalWord] = []
        self.start_index = self.word.start_index
        self.end_index = self.word.lookahead_index
        self.may_have_children = self.start_index < self.end_index

    def add_child(self, child:HierarchicalWord) -> None:
        self.children.append(child)
        child.parent = self

    def is_parent_of(self, other: HierarchicalWord ) -> bool:
        return self.may_have_children and other != self and self.start_index <= other.start_index <= self.end_index and other.end_index < self.end_index

    def __repr__(self) -> str:
        return f"HierarchicalWord('{self.start_index}:{self.end_index}, {self.word.word}: parent:{self.parent.word.word if self.parent else ''}')"

    def to_exclusion(self) -> WordExclusion:
        return WordExclusion(self.word.word, self.start_index)

def extract_words_hierarchical(sentence: str, excluded_words:list[WordExclusion]) -> list[HierarchicalWord]:
    only_non_children = [w for w in extract_words_hierarchical_all(sentence, excluded_words) if not w.parent]
    return only_non_children

def extract_words_hierarchical_all(sentence: str, excluded_words:list[WordExclusion]) -> list[HierarchicalWord]:
    def sort_key(word:ExtractedWord) -> tuple[int, int]: return word.start_index, -word.length()
    def is_excluded(word:HierarchicalWord) -> bool: return any(exclusion for exclusion in excluded_words if exclusion.excludes(word))

    starting_point = [HierarchicalWord(word) for word in sorted(extract_words(sentence, allow_duplicates=True), key=sort_key)]

    without_exclusions = [word for word in starting_point if not is_excluded(word)]

    for word in without_exclusions:
        children = [w for w in without_exclusions if word.is_parent_of(w)]
        for child in children:
            word.add_child(child)

    return without_exclusions

# noinspection DuplicatedCode
def extract_words(sentence: str, allow_duplicates:bool = False) -> list[ExtractedWord]:
    from ankiutils import app

    def _is_word(word: str) -> bool:
        return any(app.col().vocab.with_form(word)) or DictLookup.is_word(word)

    def add_word_if_it_is_in_dictionary(word: str, lookahead_index: int) -> None:
        if _is_word(word):
            add_word(word, lookahead_index)

    # noinspection DuplicatedCode
    def add_word(word: str, lookahead_index: int) -> None:
        if (allow_duplicates or word not in found_words) and word not in _noise_characters:
            found_words.add(word)
            found_words_list.append(ExtractedWord(word, token_index, lookahead_index))

    # noinspection DuplicatedCode
    def check_for_compound_words() -> None:
        surface_compound = token.surface
        for lookahead_index in range(token_index + 1, min(token_index + _max_lookahead, len(tokens))):
            look_ahead_token = tokens[lookahead_index]
            base_compound = surface_compound + look_ahead_token.base_form
            surface_compound += look_ahead_token.surface

            if base_compound != surface_compound:
                add_word_if_it_is_in_dictionary(base_compound, lookahead_index)
            add_word_if_it_is_in_dictionary(surface_compound, lookahead_index)

    tokens = _tokenizer.tokenize(sentence).tokens
    found_words = set[str]()
    found_words_list:list[ExtractedWord] = []

    for token_index, token in enumerate(tokens):
        add_word(token.base_form, 0)

        if token.surface != token.base_form and not (token.parts_of_speech.is_verb() and token.inflected_form == "連用タ接続"): #if the surface is the stem of an inflected verb, don't use it, it's not a word in its own right in this sentence.
            add_word(token.surface, 0)
        check_for_compound_words()

    return found_words_list

