from janome.tokenizer import Tokenizer, Token

from sysutils import kana_utils
from sysutils.collections import listutil
from sysutils.utils import StringUtils

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

    # if len(tokens) != 1:
    #     raise ValueError(f"'{word}' is not a single word or it's not recognized.")

    return translate_parts_of_speech(tokens[0])

def extract_dictionary_forms(text: str) -> list[ParsedWord]:
    expression = StringUtils.strip_markup(text)
    tokens = [token for token in _tokenizer.tokenize(expression) if token.part_of_speech.split(',')[0] not in ['記号']]  # Exclude punctuation
    tokens = listutil.remove_duplicates_with_lambda(tokens, lambda token: token.base_form)
    tokens = [token for token in tokens if token.base_form not in _excluded_items]

    dictionary_forms = list[ParsedWord]()
    for index, token in enumerate(tokens):
        dictionary_form = token.base_form
#        if dictionary_form in _replaced_items:
#            dictionary_form = _replaced_items[dictionary_form]

        parts_of_speech = translate_parts_of_speech(token)
        dictionary_forms.append(ParsedWord(dictionary_form, parts_of_speech))

    return dictionary_forms


# _replaced_items: dict[str, str] = {
#     "する": "為る",
#     "こと": "事"
# }
_excluded_items = {"た", "ます", "たい"}

_part_of_speech_translation = {
    '*': '*',
    'その他': 'others',
    'アルファベット': 'alphabet',
    'サ変接続': 'suru-verb',
    'ナイ形容詞語幹': 'negative-adjective-stem',
    'フィラー': 'filler',
    '一般': 'general',
    '並立助詞': 'coordinating-conjunction',
    '人名': 'person-name',
    '代名詞': 'pronoun',
    '係助詞': 'binding',
    '副助詞': 'adverbial',
    '副助詞／並立助詞／終助詞': 'adverbial/coordinating-conjunction/ending',
    '副詞': 'adverb',
    '副詞化': 'adverbialization',
    '副詞可能': 'adverbial',
    '助動詞': 'auxiliary-verb',
    '助動詞語幹': 'auxiliary-verb-stem',
    '助数詞': 'counter',
    '助詞': 'particle',
    '助詞類接続': 'particle-connection',
    '動詞': 'verb',
    '動詞非自立的': 'auxiliary-verb',
    '句点': 'period',
    '名': 'first-name',
    '名詞': 'noun',
    '名詞接続': 'noun-connection',
    '固有名詞': 'proper-noun',
    '国': 'country',
    '地域': 'region',
    '姓': 'surname',
    '引用': 'quotation',
    '形容動詞語幹': 'adjectival-verb-stem',
    '形容詞': 'adjective',
    '形容詞接続': 'adjective-connection',
    '感動詞': 'exclamation',
    '括弧閉': 'closing-bracket',
    '括弧開': 'opening-bracket',
    '接尾': 'suffix',
    '接続助詞': 'conjunctive',
    '接続詞': 'conjunction',
    '接頭詞': 'prefix',
    '数': 'numeric',
    '数接続': 'numeric-connection',
    '格助詞': 'case-particle',
    '特殊': 'special',
    '空白': 'space',
    '終助詞': 'sentence-ending',
    '組織': 'organization',
    '縮約': 'contraction',
    '自立': 'independent',
    '記号': 'symbol',
    '読点': 'comma',
    '連体化': 'adnominalization',
    '連体詞': 'adnominal-adjective',
    '連語': 'compound',
    '間投': 'interjection',
    '非自立': 'dependent'
}
