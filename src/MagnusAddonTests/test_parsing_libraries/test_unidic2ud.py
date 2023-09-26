import pytest
import unidic2ud
from unidic2ud import cabocha

_parsers = [("default", (unidic2ud.load())), # Often most intuitive results. Polarity negative feature. Good for something?
            ("kindai", (unidic2ud.load("kindai"))), # pretty similar to default, sometimes default does better, somtimes kindai. Maybe just maybe kindai does better over-all
            #("spoken", (unidic2ud.load("spoken"))), # A candidate, similar to kindai, but some differences that may be good for some sentences at least
            #("kinsei_edo", (unidic2ud.load("kinsei\\50c_kinsei-edo"))), # quite similar to kindai it seems to me.
            #("kinsei_kindai_bungo", (unidic2ud.load("kinsei\\60a_kindai-bungo"))), # quite similar to kindai it seems to me.
            ("gendai", (unidic2ud.load("gendai"))),
            #("novel", (unidic2ud.load("novel"))), # quite similar to kindai it seems to me.
            #("qkana", (unidic2ud.load("qkana"))), # quite similar to kindai it seems to me.
            #("kyogen", (unidic2ud.load("kyogen"))), #Probably No. recognizes ない as an i-adjective and mapped it to the correct kanji, unlike standard and kindai which just calls it 助動詞. Then in it's eagerness to find kanji it maps the particle ね to 音 and calls it a noun.... Ouch
            #("wakan", (unidic2ud.load("wakan"))), #No. wakan gives wack results
            #("wabun", (unidic2ud.load("wabun"))), #No. oddness abounds
            #("manyo", (unidic2ud.load("manyo"))) #No. seems to usually give some truly strange results
            ]

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
    ("何か意味があるんだと思う", [])
])
def test_unidic2ud(sentence: str, expected: list[str]) -> None:
    run_tests(sentence)


def run_tests(sentence) -> None:
    results = [(name, parser(sentence)) for name, parser in _parsers]

    print()
    for name, result in results:
        if hasattr(result, "to_tree") and callable(result.to_tree):
            print(name)
            print(sentence)
            print(result.to_tree())
        else:
            print(f"""{name} has no to_tree() method""")

    for name, result in results:
        print(name)
        print(sentence)
        print(result)

@pytest.mark.parametrize('sentence, expected', [
    ("そんなに気になるなら あの時俺も友達だって言えばよかったじゃん", []),
    ("普段どうやって日記読んでたんだ", []),
    ("何か意味があるんだと思う", [])
])
def test_unidic2ud_temp(sentence: str, expected: list[str]) -> None:
    run_tests(sentence)


# def test_something() -> None:
#     def find_first_index(the_list: list, criteria: callable) -> int:
#         return next((i for i, item in enumerate(the_list) if criteria(item)), -1)
#
#     lst = [1, 4, 7, 10, 13]
#     index = find_first_index(lst, lambda x: x > 500)
#
#     assert index == 2
