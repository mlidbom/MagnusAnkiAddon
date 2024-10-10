from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.janome_ex.word_extraction.extracted_word import ExtractedWord
from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer

_tokenizer = JNTokenizer()


def _word_is_in_dictionary(word: str) -> bool:
    result = DictLookup.lookup_word_shallow(word)
    return result.found_words()

_noise_characters = {'.',',',':',';','/','|','。','、'}
_max_lookahead = 12

version = 1
def extract_words(sentence: str) -> list[ExtractedWord]:
    from ankiutils import app
    anki_vocab = app.col().vocab

    def add_word_if_it_is_in_dictionary(word: str) -> None:
        if anki_vocab.with_form(word) or _word_is_in_dictionary(word):
            add_word(word)

    def add_word(word: str) -> None:
        if word not in found_words and word not in _noise_characters:
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
    found_words_list:list[str] = []

    for token_index, token in enumerate(tokens):
        add_word(token.base_form)
        add_word(token.surface)
        check_for_compound_words()

    return [ExtractedWord(word) for word in found_words_list]

