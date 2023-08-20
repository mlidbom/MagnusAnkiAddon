import pytest
from sudachipy import Dictionary, SplitMode

@pytest.mark.parametrize('text', [
    "声出したら駄目だからね",
    #"彼の日本語のレベルは私と同じ位だ"
    # "これをください",
    # "ハート形",
    # "どうやってここを知った"
])
def test_sudachi(text:str) -> None:
    tokenizer = Dictionary(dict_type="full").create()

    a = [mo.get_word_info() for mo in tokenizer.tokenize(text, SplitMode.A)]
    b = [mo.get_word_info() for mo in tokenizer.tokenize(text, SplitMode.B)]
    c = [mo.get_word_info() for mo in tokenizer.tokenize(text, SplitMode.C)]
    something = 1