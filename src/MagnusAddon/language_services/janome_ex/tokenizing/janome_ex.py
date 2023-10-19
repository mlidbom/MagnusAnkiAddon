from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer

_tokenizer = JNTokenizer()


def get_word_parts_of_speech(word: str) -> str:
    tokenized = _tokenizer.tokenize(word)
    return tokenized.tokens[0].parts_of_speech.translate() if tokenized.tokens else ""

