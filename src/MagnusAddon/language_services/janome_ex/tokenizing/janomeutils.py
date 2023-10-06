from language_services.janome_ex.tokenizing.tokenizer_ext import TokenizerExt

_tokenizer = TokenizerExt()


def get_word_parts_of_speech(word: str) -> str:
    return _tokenizer.tokenize(word).tokens[0].parts_of_speech.translate()

