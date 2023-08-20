from parsing.janome_extensions.tokenizer_ext import TokenizerExt

_tokenizer = TokenizerExt()


def get_word_parts_of_speech(word: str) -> str:
    return _tokenizer.tokenize(word)[0].parts_of_speech.translate()

