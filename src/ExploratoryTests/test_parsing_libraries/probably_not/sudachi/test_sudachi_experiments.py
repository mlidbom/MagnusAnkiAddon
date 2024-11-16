import pytest
from sudachipy import Dictionary, SplitMode

@pytest.mark.parametrize('text', [
    "な…何をそんなに一生懸命探しているんですか",
    #"いつまでも来ないと知らないからね",
    #"彼の日本語のレベルは私と同じ位だ"
    # "これをください",
    # "ハート形",
    # "どうやってここを知った"
])
def test_sudachi(text:str) -> None:
    tokenizer = Dictionary(dict_type="full").create()

    split_mode_a_tokens = [mo for mo in (tokenizer.tokenize(text, SplitMode.A))]
    split_mode_b_tokens = [mo for mo in tokenizer.tokenize(text, SplitMode.B)]
    split_mode_c_tokens = [mo for mo in tokenizer.tokenize(text, SplitMode.C)]

    a_info = [mo.get_word_info() for mo in split_mode_a_tokens]
    b_info = [mo.get_word_info() for mo in split_mode_b_tokens]
    c_info = [mo.get_word_info() for mo in split_mode_c_tokens]

    for word in a_info:
        print(word.surface)