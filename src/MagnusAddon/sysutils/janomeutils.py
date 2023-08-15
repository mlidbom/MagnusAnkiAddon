from janome.tokenizer import Tokenizer

from sysutils import stringlist
from sysutils.utils import StringUtils
__tokenizer = Tokenizer()



_excluded_items = {"た"}
def extract_dictionary_forms(text: str) -> list[str]:
    expression = StringUtils.strip_markup(text)
    tokens = [token for token in __tokenizer.tokenize(expression)]
    dictionary_forms = [token.base_form for token in tokens if token.part_of_speech.split(',')[0] not in ['記号', '助詞']]  # Exclude punctuation and particles
    dictionary_forms = stringlist.remove_duplicates(dictionary_forms)
    dictionary_forms = [form for form in dictionary_forms if form not in _excluded_items]
    return dictionary_forms
