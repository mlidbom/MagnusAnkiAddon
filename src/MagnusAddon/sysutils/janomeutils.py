from janome.tokenizer import Tokenizer

from sysutils import stringlist
from sysutils.utils import StringUtils
__tokenizer = Tokenizer()


def extract_dictionary_forms(text: str) -> list[str]:
    expression = StringUtils.strip_markup(text)
    tokens = [token for token in __tokenizer.tokenize(expression)]
    dictionary_forms = [token.base_form for token in tokens if token.part_of_speech.split(',')[0] != '記号']  # Exclude punctuation
    dictionary_forms = stringlist.remove_duplicates(dictionary_forms)
    return dictionary_forms
