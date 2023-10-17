from collections import defaultdict

from language_services.universal_dependencies import ud_tokenizers
from language_services.universal_dependencies.shared.tokenizing.deprel import UdRelationshipTag
from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken
from language_services.universal_dependencies.shared.tokenizing.xpos import UdJapanesePartOfSpeechTag
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.ud_tree_node_spec import UDTreeNodeSpec
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.ud_tree_spec import UDTreeSpec

N = UDTreeNodeSpec
R = UDTreeSpec

sentences = [
    "今じゃ町は夜でも明るいしもう会うこともないかもな",
    "食べてもいいけど",
    "いるのにキス",
    "聞かなかったことにしてあげる",
    "とりあえず　ご飯食べよう",
    "先生にいいように言って",
    "意外とかっこいいな",
    "私に日記を書くように言ったのも自分が楽をするためでした",
    "そう　相変わらず無表情ばっかの気がするけど",
    "ように言ったのも",
    "ごめん　自分から誘っといて ちゃんと調べておけばよかった",
    "探しているんですか",
    "ダメダメ私を助けて",
    "知らない",
    "いつまでも来ないと知らないからね",
    "ついに素晴らしい女性に逢えた。",
    "なかったかな",
    "離れていくよ",
    "夢を見た",
    "言われるまで気づかなかった",
    "行きたい所全部行こう",
    "当てられても",
    "逃げたり",
    "するためでした",
    "一度聞いたことがある",
    "友達だから余計に気になっちゃうんだよ",
    "自分のことを知ってもらえてない人に",
    "よかった",
    "良かった",
    "良くない",
    "良ければ",
    "良かったら",
    "よかったじゃん",
    "言えばよかった",
    "一度夢を見た",
    "そっちへ行ったぞ",
    "だったら",
    "だろう",
    "ううん藤宮さんは日記を捨てるような人じゃない",
    "としたら",
    "あいつが話の中に出てくるのが",
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
    "じゃ　神経衰弱をやろう",
    "この前の　放課後",
    "と…とりあえず　ご飯食べよう",
    "意外とかっこいいな"]

def test_generate_upos_xpos_mapping() -> None:
    print()

    all_tokens: list[UDToken] = []

    xpos_deprel_word_mappings: dict[UdJapanesePartOfSpeechTag, dict[UdRelationshipTag, set[str]]] = defaultdict(lambda: defaultdict(set))
    deprel_xpos_word_mappings: dict[UdRelationshipTag, dict[UdJapanesePartOfSpeechTag, set[str]]] = defaultdict(lambda: defaultdict(set))

    for sentence in sentences:
        for parser in [ud_tokenizers.default]:
            all_tokens += parser.tokenize(sentence).tokens

    for token in all_tokens:
        xpos_deprel_word_mappings[token.xpos][token.deprel].add(token.form)
        deprel_xpos_word_mappings[token.deprel][token.xpos].add(token.form)

    print("""
xpos to deprel mappings
    """)
    for _xpos in xpos_deprel_word_mappings:
        _deprel_words = xpos_deprel_word_mappings[_xpos]
        _deprels = [dep for dep in _deprel_words]

        def deprel_with_words(_deprel: UdRelationshipTag) -> str:
            return f"""{_deprel.description}{{{", ".join(d for d in _deprel_words[_deprel])}}}"""

        print(f"""{_xpos.description}: {", ".join((deprel_with_words(depr) for depr in _deprels))}""")

    print("""
    
    
deprel to xpos mappings
    """)
    for _deprel in deprel_xpos_word_mappings:
        _xpos_words = deprel_xpos_word_mappings[_deprel]
        _xposes = [dep for dep in _xpos_words]

        def xpos_with_words(_xpos: UdJapanesePartOfSpeechTag) -> str:
            return f"""{_xpos.description}{{{", ".join(d for d in _xpos_words[_xpos])}}}"""

        print(f"""{_deprel.description}: {", ".join((xpos_with_words(depr) for depr in _xposes))}""")