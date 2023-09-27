#loading a single instance takes several seconds.
import pytest

import spacy
from spacy import Language
from spacy.tokens import Doc

from src.ExploratoryTests.test_parsing_libraries.test_unidic2ud import get_lines_from_output, align_tab_separated_values

#pytestmark = pytest.mark.skip(reason="Running exploratory code constantly is just distracting.")

nlp:Language

@pytest.fixture(scope='module', autouse=True)
def setup() -> None:
    global nlp
    nlp = spacy.load('ja_ginza')

@pytest.mark.parametrize('sentence, expected', [
    ("そんなに気になるなら あの時俺も友達だって言えばよかったじゃん", []),
    ("普段どうやって日記読んでたんだ", []),
    ("何か意味があるんだと思う", []),
    ("いつまでも来ないと知らないからね", []),
    ("何か意味があるんだと思う", []),
    ("離れていくよ", []),
    ("ああだからあの時忘れんなって言ったのに", []),
    ("ダメダメ私を助けて", []),
    ("ついに素晴らしい女性に逢えた。", []),
    ("ううん藤宮さんは日記を捨てるような人じゃない", []),
    ("探しているんですか", []),
    ("行きたい所全部行こう", []),
    ("一度聞いたことがある", []),
    ("よかったじゃん", []),
    ("言えばよかった", []),
    ("言われるまで気づかなかった", []),
    ("夢を見た", []),
    ("知らない", []),
])
def test_just_display_various_sentences(sentence: str, expected: list[str]) -> None:
    doc = nlp(sentence)

    print()

    formatted = format_output(doc)
    print(formatted)


def doc_to_standard(doc: Doc) -> str:
    string = ""
    for sent in doc.sents:
        string += f"""# text =", {sent.text}"""
        for i, token in enumerate(sent):
            string += f"\n{i + 1}\t{token.text}\t{token.lemma_}\t{token.pos_}\t{token.tag_}\t_\t{token.head.i + 1}\t{token.dep_}\t_\t{token.morph}"

    return string

def format_output(doc:Doc) -> str:
    output = doc_to_standard(doc)
    line_rows = get_lines_from_output(output)
    return align_tab_separated_values(line_rows)