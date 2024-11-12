from __future__ import annotations

from typing import Optional

from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.janome_ex.word_extraction.extracted_word import ExtractedWord
from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer

_tokenizer = JNTokenizer()


_noise_characters = {'.',',',':',';','/','|','。','、'}
_max_lookahead = 12

version = "janome_extractor_1"


class HierarchicalWord:
    def __init__(self, word: ExtractedWord):
        self.word = word
        self.parent:Optional[HierarchicalWord] = None
        self.children:list[HierarchicalWord] = []
        self.start = self.word.start_index
        self.end = self.word.lookahead_index
        self.length = self.end - self.start + 1

    def add_child(self, child:HierarchicalWord) -> None:
        self.children.append(child)
        child.parent = self

    def is_parent_of(self, other: HierarchicalWord ) -> bool:
        return other != self and self.start <= other.start <= self.end and other.end <= self.end

    def __repr__(self) -> str:
        return f"HierarchicalWord('{self.start}:{self.end}, {self.word.word}: parent:{self.parent.word.word if self.parent else ''}')"

def extract_words_hierarchical(sentence: str, excluded_words:set[str]) -> list[HierarchicalWord]:

    def sort_key(word:ExtractedWord) -> tuple[int, int]: return word.start_index, -word.length()

    starting_point = [HierarchicalWord(word) for word in sorted(extract_words(sentence), key=sort_key) if word.word not in excluded_words]

    for word in starting_point:
        children = [w for w in starting_point if word.is_parent_of(w)]
        for child in children:
            word.add_child(child)


    only_non_children = [w for w in starting_point if not w.parent]

    return only_non_children




# noinspection DuplicatedCode
def extract_words(sentence: str) -> list[ExtractedWord]:
    from ankiutils import app

    def _is_word(word: str) -> bool:
        return any(app.col().vocab.with_form(word)) or DictLookup.is_word(word)

    def add_word_if_it_is_in_dictionary(word: str, lookahead_index: int) -> None:
        if _is_word(word):
            add_word(word, lookahead_index)

    # noinspection DuplicatedCode
    def add_word(word: str, lookahead_index: int) -> None:
        if word not in found_words and word not in _noise_characters:
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

        if not (token.parts_of_speech.is_verb() and token.inflected_form == "連用タ接続"): #if the surface is the stem of an inflected verb, don't use it, it's not a word in its own right in this sentence.
            add_word(token.surface, 0)
        check_for_compound_words()

    return found_words_list

