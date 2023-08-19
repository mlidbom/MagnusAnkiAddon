from parsing.janome_extensions.parsed_word import ParsedWord
from parsing.janome_extensions.tokenizer_ext import TokenizerExt
from sysutils.collections import listutil
from sysutils.utils import StringUtils

_tokenizer = TokenizerExt()


def get_word_parts_of_speech(word: str) -> str:
    return _tokenizer.tokenize(word)[0].parts_of_speech.translate()

def extract_dictionary_forms(text: str) -> list[ParsedWord]:
    expression = StringUtils.strip_markup(text)
    tokens = _tokenizer.tokenize(expression)
    tokens = listutil.remove_duplicates_with_lambda(tokens, lambda tok: tok.base_form)

    dictionary_forms = list[ParsedWord]()
    for index, token in enumerate(tokens):
        dictionary_form = token.base_form

        parts_of_speech = token.parts_of_speech.translate()
        dictionary_forms.append(ParsedWord(dictionary_form, parts_of_speech))

    return dictionary_forms
