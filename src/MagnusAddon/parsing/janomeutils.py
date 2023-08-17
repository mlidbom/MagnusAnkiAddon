from janome.tokenizer import Tokenizer, Token

from sysutils import kana_utils
from sysutils.collections import listutil
from sysutils.utils import StringUtils
from parsing.janomeutils_part_of_speech_translation import _part_of_speech_translation

class ParsedWord:
    def __init__(self, word: str, parts_of_speech: str) -> None:
        self.word = word
        self.parts_of_speech = parts_of_speech

    def is_kana_only(self) -> bool: return kana_utils.is_only_kana(self.word)

_tokenizer = Tokenizer()

def translate_parts_of_speech(token: Token) -> str:
    translated_pos = [_part_of_speech_translation[pos] for pos in token.part_of_speech.split(',')]
    return ','.join(translated_pos)

def get_word_parts_of_speech(word: str) -> str:
    tokens = list(_tokenizer.tokenize(word))


    return translate_parts_of_speech(tokens[0])

def extract_dictionary_forms(text: str) -> list[ParsedWord]:
    expression = StringUtils.strip_markup(text)
    tokens = [token for token in _tokenizer.tokenize(expression) if token.part_of_speech.split(',')[0] not in ['記号']]  # Exclude punctuation
    tokens = listutil.remove_duplicates_with_lambda(tokens, lambda token: token.base_form)

    dictionary_forms = list[ParsedWord]()
    for index, token in enumerate(tokens):
        dictionary_form = token.base_form

        parts_of_speech = translate_parts_of_speech(token)
        dictionary_forms.append(ParsedWord(dictionary_form, parts_of_speech))

    return dictionary_forms
