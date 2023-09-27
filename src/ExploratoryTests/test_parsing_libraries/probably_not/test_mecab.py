#Fast but output nothing but text and has no dependency information I can find and does not seem too intelligent in parsing compared to competitors.

import MeCab
import pytest

#pytestmark = pytest.mark.skip(reason="Running exploratory code constantly is just distracting.")

class MecabToken:
    def __init__(self, token_string: str) -> None:
        token_and_info = token_string.split("\t")
        self.surface = token_and_info[0]
        self._info = token_and_info[1].split(",")
        self.parts_of_speech = self._info[:6]
        self.forms = self._info[6:12]

    def pos_string(self) -> str: return ",".join(self.parts_of_speech)
    def forms_string(self) -> str: return ",".join(self.forms)

    def kanji_form(self) -> str:
        preferred_kanji_form = self.forms[1].split("-")[0]
        return preferred_kanji_form

    def __repr__(self) -> str:
        return f"""{self.forms} # {self.pos_string()}"""

class MecabTokenizer:
    def __init__(self) -> None:
        self._tagger = MeCab.Tagger()

    def tokenize(self, text: str) -> list[MecabToken]:
        parsed: str = self._tagger.parse(text)
        nodes = [token for token in parsed.split("\n") if token != 'EOS' and token != '']
        return [MecabToken(token) for token in nodes]

    def use_kanji_representations(self, text: str) -> str:
        tokens = self.tokenize(text)
        kanji_only = [t.kanji_form() for t in tokens]
        result = "".join(kanji_only)
        return result

tokenizer:MecabTokenizer

@pytest.fixture(scope='module', autouse=True)
def setup() -> None:
    global tokenizer
    tokenizer = MecabTokenizer()

@pytest.mark.parametrize('sentence, expected', [
    ("探しているんですか", ['探す', 'て', '居る', 'の', 'です', 'か']), #good: 居る
    ("としたら", ['と', '為る', 'た']), #good: 為る
    ("離れていくよ", ['離れる', 'て', '行く', 'よ']), #good: 行く
    ("いつまでも来ないと知らないからね", ['何時', 'まで', 'も', '来る', 'ない', 'と', '知る', 'ない', 'から', 'ね']), #good: 何時
    ("ダメダメ私を殺して", ['駄目', '駄目', '私', 'を', '殺す', 'て']), #good: 駄目
    ("夢を見た", ['夢', 'を', '見る', 'た']),
    ("言われるまで気づかなかった", ['言う', 'れる', 'まで', '気付く', 'ない', 'た']), #good: 気付く
    ("行きたい所全部行こう", ['行く', 'たい', '所', '全部', '行く']),
    ("当てられても", ['当てる', 'られる', 'て', 'も']),
    ("逃げたり", ['逃げる', 'たり']),
    ("いるのにキス", ['居る', 'の', 'に', 'キス']), #good: 居る
    ("するためでした", ['為る', '為', 'です', 'た']),#good 為る, 為 times two :)
    ("探しているんですか", ['探す', 'て', '居る', 'の', 'です', 'か']), #good: 居る
    ("一度聞いたことがある", ['一', '度', '聞く', 'た', '事', 'が', '有る']), #good: 有る
    ("よかった", ['良い', 'た']), #good: 良い
    ("良ければ", ['良い', 'ば']), #good: ば
    ("良かったら", ['良い', 'た']), #good
    ("良くない", ['良い', '無い']), #good: 無い
    ("よかったじゃん", ['良い', 'た', 'じゃん']),#good
    ("言えばよかった", ['言う', 'ば', '良い', 'た']) #good: 良い
])
def test_mecab(sentence:str, expected:list[str]) -> None:
    tokens = tokenizer.tokenize(sentence)
    kanji_forms = [a.kanji_form() for a in tokens]

    assert kanji_forms == expected

@pytest.mark.parametrize('sentence, expected', [
    ("知らない", ['知る', 'ない']), # todo nai...
    ("いつまでも来ないと知らないからね", ['何時', 'まで', 'も', '来る', 'ない', 'と', '知る', 'ない', 'から', 'ね']), #todo nai...
    ("なかったかな", ['ない', 'た', 'か', 'な']),  # todo nai...
    ("ついに素晴らしい女性に逢えた。", ['遂に', '素晴らしい', '女性', 'に', '会う', 'た', '。']), #todo it switches kanji's here....
    ("ううん藤宮さんは日記を捨てるような人じゃない", ['ううん', 'フジミヤ', 'さん', 'は', '日記', 'を', '捨てる', '様', 'だ', '人', 'だ', '無い']), #todo it switches kanji for katakana here
    ("食べてもいいけど", ['食べる', 'て', 'も', '良い', 'けれど']),#good: 良い　todo: けど -> けれど
    ("ように言ったのも", ['様', 'だ', '言う', 'た', 'の', 'も']), #good: 様 todo: だ
])
def test_tmp(sentence:str, expected:list[str]) -> None:
    tokens = tokenizer.tokenize(sentence)
    kanji_forms = [a.kanji_form() for a in tokens]

    assert kanji_forms == expected

@pytest.mark.parametrize('sentence, expected', [
    ("ついに素晴らしい女性に逢えた", ['遂に', '素晴らしい', '女性', 'に', '会う', 'た']), #good: 遂に todo it switches kanji's here....
])
def test_tmp_2(sentence:str, expected:list[str]) -> None:
    tokens = tokenizer.tokenize(sentence)
    kanji_forms = [a.kanji_form() for a in tokens]

    assert kanji_forms == expected