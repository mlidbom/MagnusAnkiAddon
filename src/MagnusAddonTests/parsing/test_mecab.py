from typing import List, Any, Tuple

import MeCab

class MecabToken:
    def __init__(self, token_string: str) -> None:
        token_and_info = token_string.split("\t")
        self.surface = token_and_info[0]
        self._info = token_and_info[1].split(",")
        self.parts_of_speech = self._info[:6]
        self.forms = self._info[6:12]

    def pos_string(self) -> str: return ",".join(self.parts_of_speech)
    def forms_string(self) -> str: return ",".join(self.forms)

    def kanji_form(self) -> str: return self.forms[1]

    def __repr__(self) -> str:
        return f"""{self.forms} # {self.pos_string()}"""

class MecabTokenizer:
    def __init__(self) -> None:
        self._tagger = tagger = MeCab.Tagger()

    def tokenize(self, text: str) -> list[MecabToken]:
        parsed: str = self._tagger.parse(text)
        nodes = [token for token in parsed.split("\n") if token != 'EOS' and token != '']
        return [MecabToken(token) for token in nodes]

    def use_kanji_representations(self, text: str) -> str:
        tokens = self.tokenize(text)
        kanji_only = [t.kanji_form() for t in tokens]
        result = "".join(kanji_only)
        return result

tokenizer = MecabTokenizer()
def test_mecab() -> None:
    input_text = "よかった"
    kanji_representation = tokenizer.use_kanji_representations(input_text)

    print(kanji_representation)