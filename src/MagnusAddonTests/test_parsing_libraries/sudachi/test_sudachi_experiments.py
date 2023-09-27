# import pytest
# from sudachipy import Dictionary, SplitMode
#
# @pytest.mark.parametrize('text', [
#     "な…何をそんなに一生懸命探しているんですか",
#     #"いつまでも来ないと知らないからね",
#     #"彼の日本語のレベルは私と同じ位だ"
#     # "これをください",
#     # "ハート形",
#     # "どうやってここを知った"
# ])
# def test_sudachi(text:str) -> None:
#     tokenizer = Dictionary(dict_type="full").create()
#
#     a = [mo for mo in (tokenizer.tokenize(text, SplitMode.A))]
#     b = [mo for mo in tokenizer.tokenize(text, SplitMode.B)]
#     c = [mo for mo in tokenizer.tokenize(text, SplitMode.C)]
#
#     a_info = [mo.get_word_info() for mo in a]
#     b_info = [mo.get_word_info() for mo in b]
#     c_info = [mo.get_word_info() for mo in c]
#     something = 1