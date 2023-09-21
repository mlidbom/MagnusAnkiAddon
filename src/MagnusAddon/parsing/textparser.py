from parsing.jamdict_extensions.dict_lookup import DictLookup
from parsing.janome_extensions.parsed_word import ParsedWord
from parsing.janome_extensions.tokenizer_ext import TokenizerExt

_tokenizer = TokenizerExt()


def _word_is_in_dictionary(word: str) -> bool:
    result = DictLookup.lookup_word_shallow(word)
    return result.found_words()

_max_lookahead = 12
def identify_words(sentence: str) -> list[ParsedWord]:
    def add_word_if_it_is_in_dictionary(word: str) -> None:
        if _word_is_in_dictionary(word) and word not in found_words:
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

