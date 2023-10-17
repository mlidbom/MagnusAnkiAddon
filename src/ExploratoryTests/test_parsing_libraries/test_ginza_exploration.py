import pytest
import spacy
from spacy.tokens import Token

from language_services.universal_dependencies import ud_tokenizers
from sysutils import ex_sequence, ex_str

ginza = spacy.load("ja_ginza")

@pytest.mark.parametrize("sentence", [
    "気になる人は　その",
    "なんというか 事情を分ってくれる人は少しでも多い方がいいと思うんだ",
    "悪くなさそうね良かった",
    "朝、近所をぶらぶらした",
    "そんなに気になるなら あの時俺も友達だって言えばよかったじゃん",
    "普段どうやって日記読んでたんだ",
    "何か意味があるんだと思う",
    "いつまでも来ないと知らないからね",
    "離れていくよ",
    "ああだからあの時忘れんなって言ったのに",
    "ダメダメ私を助けて",
    "ついに素晴らしい女性に逢えた。",
    "ううん藤宮さんは日記を捨てるような人じゃない",
    "探しているんですか",
    "行きたい所全部行こう",
    "当てられても",
    "一度聞いたことがある",
    "よかったじゃん",
    "言えばよかった",
    "言われるまで気づかなかった",
    "夢を見た",
    "知らない",
    "何よあの態度偉そうに",
    "これから本題に入るんだけど",
    "食べられるもの",
    "俺以外に友達がいなくてよかったとか　絶対思っちゃダメなのに",
    "日代さんが 先生に知らせてくれたらしい",
    "やっぱりあの噂ホントだったんだ",
    "だったら記憶喪失の振りすることも簡単だよな",
    "だったら記憶喪失の振りすることも簡単だよな",
    "食べてもいいけど",
    "ケータイ持ってるやつは自宅に連絡しておけ",
    "なぜかというと",
    "あり得るか",
    "二千九百円",
    "今ここで死ぬあなたには関係のない話でしょう",
    "じゃ　神経衰弱をやろう",
    "この前の　放課後"
    "と…とりあえず　ご飯食べよう"
    "意外とかっこいいな",
    "これから一分後に"
])
def test_display_interesting_sentences_we_should_add_real_tests_for(sentence: str) -> None:
    print()
    print(sentence)


    ud_tokens = ud_tokenizers.ginza.tokenize(sentence)
    print(ud_tokens.str_(exclude_lemma_and_norm=True))

    doc = ginza(sentence)

    sents = [sent for sent in doc.sents]
    sent_tokens: list[list[Token]] = [[token for token in sent] for sent in sents]
    tokens:list[Token] = ex_sequence.flatten(sent_tokens)

    print(f"""sents:""")
    for sent in sents:

        print(f"""{ex_str.pad_to_length("noun_chunks:", 10)}{[nc for nc in sent.noun_chunks]}""")

    print()
    for token in tokens:
        print(f"""{ex_str.pad_to_length("text:", 10)}{token.text}""")

        subtree_tokens = [t for t in token.subtree]
        print(f"""{ex_str.pad_to_length("subtree:", 10)}{":".join([t.text for t in subtree_tokens])}""")
        print(f"""{ex_str.pad_to_length("children:", 10)}{":".join([t.text for t in token.children])}""")
        print(f"""{ex_str.pad_to_length("ancestors:", 10)}{":".join([t.text for t in token.ancestors])}""")


        print(f"""{ex_str.pad_to_length("left_edge:", 10)}{token.left_edge.text}""")
        print(f"""{ex_str.pad_to_length("lefts:", 10)}{":".join([t.text for t in token.lefts])}""")
        print(f"""{ex_str.pad_to_length("n_lefts:", 10)}{token.n_lefts}""")


        print(f"""{ex_str.pad_to_length("right_edge:", 10)}{token.right_edge.text}""")
        print(f"""{ex_str.pad_to_length("rights:", 10)}{":".join([t.text for t in token.rights])}""")
        print(f"""{ex_str.pad_to_length("n_rights:", 10)}{token.n_rights}""")

        print(f"""{ex_str.pad_to_length("morph:", 10)}{token.morph}""")
        print(f"""{ex_str.pad_to_length("conjuncts:", 10)}{":".join([t.text for t in token.conjuncts])}""")


        print()



#     lexemes: list[Lexeme] = [l for l in doc.vocab]
#
#     print("""
#
# lexemes:""")
#     for lexeme in lexemes:
#         print(lexeme.norm_)
#
#     noun_chunks = [chunk.text for chunk in doc.noun_chunks]
#
#
#     print("""
# noun chunks:""")
#     print(noun_chunks)
#
#     print("""
#
# Morphs:""")
#     for token in doc:
#         for morph in token.morph:
#             print(morph)
#
#     print("""
#
# orth_:""")
#     for sent in doc.sents:
#         for token in sent:
#             print(token.orth_)