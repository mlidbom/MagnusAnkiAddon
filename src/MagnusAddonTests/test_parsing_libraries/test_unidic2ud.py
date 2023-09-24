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

    for name, result in [("kindai", kindai_result), ("default", default_result), ("cabocha", cabocha_result)]:
        print(name)
        print(result)
        if hasattr(result, "to_tree") and callable(result.to_tree):
            print(result.to_tree())

@pytest.mark.parametrize('sentence, expected', [
    ("そんなに気になるなら あの時俺も友達だって言えばよかったじゃん", [])
])
def test_unidic2ud_temp(sentence: str, expected: list[str]) -> None:
    run_tests(sentence)
