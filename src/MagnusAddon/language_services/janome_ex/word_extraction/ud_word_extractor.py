from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.universal_dependencies import ud_tokenizers



_tokenizer = ud_tokenizers.qkana

_noise_characters = {'.',',',':',';','/','|','。','、'}
_max_lookahead = 12

version = "ud_extractor_1"
# noinspection DuplicatedCode
def extract_words(sentence: str) -> list[str]:
    from ankiutils import app

    anki_vocab = app.col().vocab

    def add_word_if_it_is_in_dictionary(word: str) -> None:
        if anki_vocab.with_form(word) or DictLookup.lookup_word_shallow(word).found_words():
            add_word(word)

    # noinspection DuplicatedCode
    def add_word(word: str) -> None:
        if word not in found_words and word not in _noise_characters:
            found_words.add(word)
            found_words_list.append(word)

    def check_for_compound_words() -> None:
        surface_compound = token.form
        for lookahead_index in range(token_index + 1, min(token_index + _max_lookahead, len(tokens))):
            look_ahead_token = tokens[lookahead_index]
            base_compound = surface_compound + look_ahead_token.lemma
            surface_compound += look_ahead_token.form

            if base_compound != surface_compound:
                add_word_if_it_is_in_dictionary(base_compound)
            add_word_if_it_is_in_dictionary(surface_compound)

    tokens = _tokenizer.tokenize(sentence).tokens
    found_words = set[str]()
    found_words_list:list[str] = []

    for token_index, token in enumerate(tokens):
        add_word(token.lemma)
        add_word(token.form)
        check_for_compound_words()

    return found_words_list

