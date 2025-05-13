from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ankiutils import app
from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer
from language_services.janome_ex.word_extraction.extracted_word import ExtractedWord
from language_services.janome_ex.word_extraction.hierarchicalword import HierarchicalWord
from note.note_constants import Mine
from sysutils import ex_sequence

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
    from note.vocabulary.vocabnote import VocabNote


_noise_characters = {'.',',',':',';','/','|','。','、'}
_max_lookahead = 12

class WordExtractor:
    def __init__(self, tokenizer: JNTokenizer) -> None:
        self.version = "janome_extractor_1"
        self._tokenizer = tokenizer

    def extract_words_hierarchical(self, sentence: str, excluded_words: list[WordExclusion]) -> list[HierarchicalWord]:
        hierarchical_all = self.extract_words_hierarchical_all(sentence, excluded_words)
        only_non_children = [w for w in hierarchical_all if not w.shadowed_by]
        return only_non_children

    def extract_words_hierarchical_all(self, sentence: str, excluded_words: list[WordExclusion]) -> list[HierarchicalWord]:
        def sort_key(word: ExtractedWord) -> tuple[int, int, int]: return word.character_index, -word.surface_length(), -word.word_length()
        def is_excluded(word: HierarchicalWord) -> bool: return any(exclusion for exclusion in excluded_words if exclusion.excludes(word))

        starting_point = [HierarchicalWord(word) for word in sorted(self.extract_words(sentence, allow_duplicates=True, exclusions=excluded_words), key=sort_key)]

        without_exclusions = [word for word in starting_point if not is_excluded(word)]

        for word in without_exclusions:
            shadowed = [w for w in without_exclusions if word.is_shadowing(w)]
            for child in shadowed:
                word.add_shadowed(child)

        return without_exclusions

    # noinspection PyDefaultArgument
    def extract_words(self, sentence: str, allow_duplicates: bool = False, exclusions: Optional[list[WordExclusion]] = None) -> list[ExtractedWord]:
        exclusions = exclusions if exclusions else []
        def _is_word(word: str) -> bool:
            return app.col().vocab.is_word(word) or DictLookup.is_word(word)

        def add_word_if_it_is_in_dictionary(word: str, surface: str) -> None:
            if _is_word(word):
                add_word(word, surface)

        def is_excluded_contextually(form_:str) -> bool:
            context = ""
            if token_index > 0:
                context += tokens[token_index - 1].surface
            context += token.surface
            if token_index < len(tokens) - 1:
                context += tokens[token_index + 1].surface

            context_exclusions = ex_sequence.flatten([list(voc.forms.excluded_set()) for voc in app.col().vocab.with_question(form_)])
            return any(exclusion for exclusion in context_exclusions if form_ in exclusion and exclusion in context)

        def get_excluded_forms(form_:str) -> set[str]:
            unexcluded_vocab_with_form = [voc for voc in (app.col().vocab.with_form(form_)) if not any(exclusion for exclusion in exclusions if exclusion.word == voc.get_question())]
            excluded_forms_list_for_form = [voc.forms.excluded_set() for voc in unexcluded_vocab_with_form]
            excluded_forms_set = set.union(*excluded_forms_list_for_form) if excluded_forms_list_for_form else set()
            return excluded_forms_set

        def is_excluded_form(vocab_form: str, candidate_form: str) -> bool:
            if is_excluded_contextually(candidate_form):
                return True

            return candidate_form in get_excluded_forms(candidate_form) or candidate_form in get_excluded_forms(vocab_form)

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

            return any([voc for voc in vocab if voc.has_tag(Mine.Tags.inflecting_word)])

        def is_inflected_word(index: int) -> bool:
            _token = tokens[index]

            if (_token.is_inflectable_word()  # noqa: SIM103
                    and index < len(tokens) - 1
                    and is_next_token_inflecting_word(index)):
                return True

            return False

        def check_for_compound_words() -> None:
            surface_compound = token.surface
            for lookahead_index in range(token_index + 1, min(token_index + _max_lookahead, len(tokens))):
                look_ahead_token = tokens[lookahead_index]
                base_compound = surface_compound + look_ahead_token.base_form
                surface_compound += look_ahead_token.surface

                if (base_compound != surface_compound
                        and passes_exact_match_requirement(base_compound, surface_compound)
                        and not is_excluded_form(surface_compound, base_compound)
                        and not is_excluded_form(look_ahead_token.surface, look_ahead_token.base_form)):
                    add_word_if_it_is_in_dictionary(base_compound, surface_compound)
                if not is_excluded_form(token.base_form, surface_compound):
                    add_word_if_it_is_in_dictionary(surface_compound, surface_compound)

        def passes_exact_match_requirement(base:str, surface:str) -> bool:
            if base == surface:
                return True

            exact_matches = ex_sequence.flatten([app.col().vocab.with_question(form) for form in [base,surface]])
            return not any(v for v in exact_matches if v.meta_data.flags.requires_exact_match())

        text = self._tokenizer.tokenize(sentence)
        tokens = text.tokens
        found_words = set[str]()
        found_words_list: list[ExtractedWord] = []

        character_index = 0
        for token_index, token in enumerate(tokens):
            if not is_excluded_form(token.surface, token.base_form) and passes_exact_match_requirement(token.base_form, token.surface):
                add_word(token.base_form, token.surface)

            if (token.surface != token.base_form
                    and not is_inflected_word(token_index)
                    and not is_excluded_form(token.base_form, token.surface)):  # If the surface is the stem of an inflected verb, don't use it. It's not a word in its own right in this sentence.
                add_word(token.surface, token.surface)
            check_for_compound_words()

            character_index += len(token.surface)

        return found_words_list


jn_extractor = WordExtractor(JNTokenizer())