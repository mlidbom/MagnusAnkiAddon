from __future__ import annotations

from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer
from language_services.janome_ex.word_extraction.extracted_word import ExtractedWord
from language_services.janome_ex.word_extraction.hierarchicalword import HierarchicalWord
from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from note.note_constants import Mine
from note.vocabnote import VocabNote

_noise_characters = {'.',',',':',';','/','|','。','、'}
_max_lookahead = 12

class WordExtractor:
    def __init__(self, tokenizer: JNTokenizer) -> None:
        self.version = "janome_extractor_1"
        self._tokenizer = tokenizer

    def extract_words_hierarchical(self, sentence: str, excluded_words: list[WordExclusion]) -> list[HierarchicalWord]:
        analysis = TextAnalysis(sentence, excluded_words)

        hierarchical_all = self.extract_words_hierarchical_all(sentence, excluded_words)
        only_non_children = [w for w in hierarchical_all if not w.shadowed_by]
        return only_non_children

    def extract_words_hierarchical_all(self, sentence: str, excluded_words: list[WordExclusion]) -> list[HierarchicalWord]:
        def sort_key(word: ExtractedWord) -> tuple[int, int, int]: return word.character_index, -word.surface_length(), -word.word_length()
        def is_excluded(word: HierarchicalWord) -> bool: return any(exclusion for exclusion in excluded_words if exclusion.excludes(word))

        starting_point = [HierarchicalWord(word) for word in sorted(self.extract_words(sentence, allow_duplicates=True), key=sort_key)]

        without_exclusions = [word for word in starting_point if not is_excluded(word)]

        for word in without_exclusions:
            shadowed = [w for w in without_exclusions if word.is_shadowing(w)]
            for child in shadowed:
                word.add_shadowed(child)

        return without_exclusions

    # noinspection DuplicatedCode
    def extract_words(self, sentence: str, allow_duplicates: bool = False) -> list[ExtractedWord]:
        from ankiutils import app

        def _is_word(word: str) -> bool:
            return app.col().vocab.is_word(word) or DictLookup.is_word(word)

        def add_word_if_it_is_in_dictionary(word: str, surface: str) -> None:
            if _is_word(word):
                add_word(word, surface)

        def is_excluded_form(vocab_form: str, candidate_form: str) -> bool:
            return (any(voc for voc in (app.col().vocab.with_form(vocab_form)) if candidate_form in voc.get_excluded_forms()) or
                    any(voc for voc in (app.col().vocab.with_form(candidate_form)) if candidate_form in voc.get_excluded_forms()))

        def add_word(word: str, surface: str) -> None:
            if (allow_duplicates or word not in found_words) and word not in _noise_characters:
                found_words.add(word)
                found_words_list.append(ExtractedWord(word, surface, character_index))

        def is_next_token_inflecting_word(index: int) -> bool:
            def lookup_vocabs_prefer_exact_match(form: str) -> list[VocabNote]:
                matches: list[VocabNote] = app.col().vocab.with_form(form)
                exact_match = [voc for voc in matches if voc.get_question_without_noise_characters() == form]
                return exact_match if exact_match else matches

            if index >= len(tokens) - 1:
                return False

            next_token = tokens[index + 1]
            vocab: list[VocabNote] = lookup_vocabs_prefer_exact_match(next_token.base_form)

            if any([voc for voc in vocab if voc.has_tag(Mine.Tags.inflecting_word)]):
                return True

            return False

        def is_inflected_word(index: int) -> bool:
            _token = tokens[index]

            if _token.is_inflectable_word():
                if index < len(tokens) - 1:
                    if is_next_token_inflecting_word(index):
                        return True

            return False

        def check_for_compound_words() -> None:
            surface_compound = token.surface
            for lookahead_index in range(token_index + 1, min(token_index + _max_lookahead, len(tokens))):
                look_ahead_token = tokens[lookahead_index]
                base_compound = surface_compound + look_ahead_token.base_form
                surface_compound += look_ahead_token.surface

                if (base_compound != surface_compound
                        and not is_excluded_form(surface_compound, base_compound)
                        and not is_excluded_form(look_ahead_token.surface, look_ahead_token.base_form)):
                    add_word_if_it_is_in_dictionary(base_compound, surface_compound)
                if not is_excluded_form(token.base_form, surface_compound):
                    add_word_if_it_is_in_dictionary(surface_compound, surface_compound)

        text = self._tokenizer.tokenize(sentence)
        tokens = text.tokens
        found_words = set[str]()
        found_words_list: list[ExtractedWord] = []

        character_index = 0
        for token_index, token in enumerate(tokens):
            if not is_excluded_form(token.surface, token.base_form):
                add_word(token.base_form, token.surface)

            if (token.surface != token.base_form
                    and not is_inflected_word(token_index)
                    and not is_excluded_form(token.base_form, token.surface)):  # If the surface is the stem of an inflected verb, don't use it. It's not a word in its own right in this sentence.
                add_word(token.surface, token.surface)
            check_for_compound_words()

            character_index += len(token.surface)

        return found_words_list


jn_extractor = WordExtractor(JNTokenizer())