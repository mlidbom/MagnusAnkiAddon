import pytest
import unidic2ud
from unidic2ud import cabocha

kindai = unidic2ud.load("kindai")
cabocha = cabocha.Parser()

default = unidic2ud.load()
@pytest.mark.parametrize('sentence, expected', [
    ("知らない", []),
    ("いつまでも来ないと知らないからね", []),
    ("ついに素晴らしい女性に逢えた。", []),
    ("ううん藤宮さんは日記を捨てるような人じゃない", []),
    ("なかったかな", []),
    ("探しているんですか", []),
    ("としたら", []),
    ("夢を見た", []),
    ("行きたい所全部行こう", []),
    ("当てられても", []),
    ("逃げたり", []),
    ("いるのにキス", []),
    ("するためでした", []),
    ("一度聞いたことがある", []),
    ("よかった", []),
    ("良ければ", []),
    ("良かったら", []),
    ("良くない", []),
    ("よかったじゃん", []),
    ("言えばよかった", []),
    ("ダメダメ私を殺して", []),
    ("離れていくよ", []),
    ("言われるまで気づかなかった", []),
])
def test_unidic2ud(sentence: str, expected: list[str]) -> None:
    run_tests(sentence)


def run_tests(sentence) -> None:
    kindai_result = kindai(sentence)
    default_result = default(sentence)
    cabocha_result = cabocha.parse(sentence)

    print("kindai")
    print(kindai_result)

    print("default")
    print(default_result)

    print("cabocha")
    print(cabocha_result)


    print("kindai")
    print(kindai_result.to_tree())

    print("default")
    print(default_result.to_tree())

    print("cabocha")
    print(cabocha_result.toString())

    #assert kindai_result == default_result

@pytest.mark.parametrize('sentence, expected', [
    ("aoeu","")
])
def test_unidic2ud_temp(sentence: str, expected: list[str]) -> None:
    run_tests(sentence)
