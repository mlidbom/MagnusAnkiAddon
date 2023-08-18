from parsing.janome_extensions.parsed_word import ParsedWord
from parsing.janome_extensions.token_ext import TokenExt
from parsing.janome_extensions.tokenizer_ext import TokenizerExt
from sysutils.collections import listutil
from sysutils.utils import StringUtils
from parsing.janome_extensions.janomeutils_part_of_speech_translation import part_of_speech_translation

_tokenizer = TokenizerExt()

def translate_parts_of_speech(token: TokenExt) -> str:
    translated_pos = [part_of_speech_translation[pos] for pos in token.part_of_speech.split(',')]
    return ','.join(translated_pos)

def get_word_parts_of_speech(word: str) -> str:
    tokens = _tokenizer.tokenize(word)
    return translate_parts_of_speech(tokens[0])

def extract_dictionary_forms(text: str) -> list[ParsedWord]:
    expression = StringUtils.strip_markup(text)
    tokens = _tokenizer.tokenize(expression)
    tokens = listutil.remove_duplicates_with_lambda(tokens, lambda token: token.base_form)

    dictionary_forms = list[ParsedWord]()
    for index, token in enumerate(tokens):
        dictionary_form = token.base_form

        parts_of_speech = translate_parts_of_speech(token)
        dictionary_forms.append(ParsedWord(dictionary_form, parts_of_speech))

    return dictionary_forms
