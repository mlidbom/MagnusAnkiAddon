from __future__ import annotations

from typing import Any, Optional

from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.janome_ex.word_extraction.extracted_word import ExtractedWord
from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer
from note.note_constants import Mine
from note.vocabnote import VocabNote

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
            try:
                return WordExclusion(parts[1].strip(), int(parts[0].strip()))
            except ValueError:
                pass
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
        self.length = len(word.surface)
        self.shadowed_by:Optional[HierarchicalWord] = None
        self.shadowed:list[HierarchicalWord] = []
        self.start_index = self.word.start_index
        self.end_index = self.word.lookahead_index
        self.start_character_index = self.word.character_index
        self.end_character_index = self.start_character_index + self.length - 1
        self.may_have_children = self.start_index < self.end_index

    def add_shadowed(self, child:HierarchicalWord) -> None:
        self.shadowed.append(child)
        child.shadowed_by = self

    def is_shadowing(self, other: HierarchicalWord) -> bool:
        if self == other or self.shadowed_by:
            return False

        if self.start_character_index < other.start_character_index <= self.end_character_index:
            return True

        if self.start_character_index == other.start_character_index:
            if self.length > other.length:
                return True

            if self.word.word_length() > other.word.word_length() and other.word.word in self.word.word:
                return True

        return False

    def __repr__(self) -> str:
        return f"HierarchicalWord('{self.start_index}:{self.end_index} | {self.start_character_index}:{self.end_character_index}, {self.word.surface}:{self.word.word}: parent:{self.shadowed_by.word.word if self.shadowed_by else ''}')"

    def to_exclusion(self) -> WordExclusion:
        return WordExclusion(self.word.word, self.start_index)

def extract_words_hierarchical(sentence: str, excluded_words:list[WordExclusion]) -> list[HierarchicalWord]:
    hierarchical_all = extract_words_hierarchical_all(sentence, excluded_words)
    only_non_children = [w for w in hierarchical_all if not w.shadowed_by]
    return only_non_children

def extract_words_hierarchical_all(sentence: str, excluded_words:list[WordExclusion]) -> list[HierarchicalWord]:
    def sort_key(word:ExtractedWord) -> tuple[int, int, int]: return word.character_index, -word.surface_length(), -word.word_length()
    def is_excluded(word:HierarchicalWord) -> bool: return any(exclusion for exclusion in excluded_words if exclusion.excludes(word))

    starting_point = [HierarchicalWord(word) for word in sorted(extract_words(sentence, allow_duplicates=True), key=sort_key)]

    without_exclusions = [word for word in starting_point if not is_excluded(word)]

    for word in without_exclusions:
        shadowed = [w for w in without_exclusions if word.is_shadowing(w)]
        for child in shadowed:
            word.add_shadowed(child)

    return without_exclusions

# noinspection DuplicatedCode
def extract_words(sentence: str, allow_duplicates:bool = False) -> list[ExtractedWord]:
    from ankiutils import app

    def _is_word(word: str) -> bool:
        return app.col().vocab.is_word(word) or DictLookup.is_word(word)

    def add_word_if_it_is_in_dictionary(word: str, surface:str, lookahead_index: int) -> None:
        if _is_word(word):
            add_word(word, surface, lookahead_index)

    def is_excluded_form(vocab_form:str, candidate_form:str) -> bool:
        return (any(voc for voc in (app.col().vocab.with_form(vocab_form)) if candidate_form in voc.get_excluded_forms()) or
                any(voc for voc in (app.col().vocab.with_form(candidate_form)) if candidate_form in voc.get_excluded_forms()))

    # noinspection DuplicatedCode
    def add_word(word: str, surface:str, lookahead_index: int) -> None:
        if (allow_duplicates or word not in found_words) and word not in _noise_characters:
            found_words.add(word)
            found_words_list.append(ExtractedWord(word, surface, token_index, lookahead_index, character_index))

    def is_next_token_inflecting_word(index:int) -> bool:
        def lookup_vocabs_prefer_exact_match(form: str) -> list[VocabNote]:
            matches: list[VocabNote] = app.col().vocab.with_form(form)
            exact_match = [voc for voc in matches if voc.get_question_without_noise_characters() == form]
            return exact_match if exact_match else matches

        if index >= len(tokens) - 1:
            return False

        next_token = tokens[index + 1]
        vocab:list[VocabNote] = lookup_vocabs_prefer_exact_match(next_token.base_form)

        if any([voc for voc in vocab if voc.has_tag(Mine.Tags.inflecting_word)]):
            return True

        return False

    def is_inflected_word(index: int) -> bool:
        _token = tokens[index]
        if _token.is_inflected_verb():
            return True

        if _token.is_inflectable_word():
            if index < len(tokens) - 1:
                if is_next_token_inflecting_word(index):
                    return True

        return False

    # noinspection DuplicatedCode
    def check_for_compound_words() -> None:
        surface_compound = token.surface
        for lookahead_index in range(token_index + 1, min(token_index + _max_lookahead, len(tokens))):
            look_ahead_token = tokens[lookahead_index]
            base_compound = surface_compound + look_ahead_token.base_form
            surface_compound += look_ahead_token.surface

            if base_compound != surface_compound and not is_excluded_form(surface_compound, base_compound):
                add_word_if_it_is_in_dictionary(base_compound, surface_compound, lookahead_index)
            if not is_excluded_form(token.base_form, surface_compound):
                add_word_if_it_is_in_dictionary(surface_compound, surface_compound, lookahead_index)

    tokens = _tokenizer.tokenize(sentence).tokens
    found_words = set[str]()
    found_words_list:list[ExtractedWord] = []

    character_index = 0
    for token_index, token in enumerate(tokens):
        if not is_excluded_form(token.surface, token.base_form):
            add_word(token.base_form, token.surface, 0)

        if (token.surface != token.base_form
                and not is_inflected_word(token_index)
                and not is_excluded_form(token.base_form, token.surface)): #If the surface is the stem of an inflected verb, don't use it. It's not a word in its own right in this sentence.
            add_word(token.surface, token.surface, 0)
        check_for_compound_words()

        character_index += len(token.surface)

    return found_words_list
