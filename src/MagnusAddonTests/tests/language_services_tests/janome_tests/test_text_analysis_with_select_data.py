from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from fixtures.collection_factory import inject_anki_collection_with_select_data
from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
from note.sentences.sentence_configuration import SentenceConfiguration

if TYPE_CHECKING:
    from collections.abc import Iterator

# noinspection PyUnusedFunction
@pytest.fixture(scope="module")
def setup_collection_with_select_data() -> Iterator[None]:
    with inject_anki_collection_with_select_data(special_vocab=True):
        yield

@pytest.mark.parametrize("sentence, expected_output", [
    ("走る",
     ["走る"]),
    ("走って",
     ["走る", "て"]),
    ("これをください。",
     ["これ", "を", "くださる", "ください"]),
    ("ハート形",
     ["ハート形", "ハート", "形"]),
    ("私が行きましょう。",
     ["私", "が", "行く", "行き", "ましょう", "ます", "ましょ", "う"]),
    ("１人でいる時間がこれほどまでに長く感じるとは",
     ["１人で", "１人", "１", "人", "で", "いる", "時間", "が", "これほど", "これ", "ほど", "までに", "まで", "に", "長い", "感じる", "とは", "と", "は"]
     ),
    ("どうやってここを知った。",
     ["どうやって", "どう", "やる", "て", "ここ", "を", "知る", "た"]),
    ("彼の日本語のレベルは私と同じ位だ。",
     ["彼の", "彼", "の", "日本語", "の", "レベル", "は", "私", "と", "同じ位", "同じ", "位", "だ"]),
    ("それなのに 周りは化け物が出ることで有名だと聞き",
     ["それなのに", "周り", "は", "化け物", "が", "出る", "こと", "で", "有名", "だ", "と", "聞く", "聞き"]),
    ("清めの一波", ["清める", "清め", "の"]),
    ("さっさと傷を清めてこい",
     ["傷", "を", "清める", "て", "くる", "こい"]),
    ("すげえ", ["すげえ", "すげ", "え"]),
    ("「コーヒーはいかがですか？」「いえ、結構です。お構いなく。」", ["コーヒー", "は", "いかが", "ですか", "です", "か", "いえ", "結構", "です", "お構いなく"]),
    ("解放する", ["解放する", "解放", "する"]),
    ("落書きしたろ", ["落書き", "する", "た"]),
    ("なのかな", ["なの", "な", "の", "かな", "か", "な"]),
    ("前だったのか", ["前", "だった", "だ", "たの", "た", "のか", "の", "か"]),
    ("未練たらしい", ["未練たらしい", "未練", "たらしい"]),
    ("作るに決まってるだろ", ["作る", "に決まってる", "に決まる", "に", "決まる", "てる", "だ", "だろ"]),
    ("良いものを食べる", ["良い", "もの", "を", "食べる"]),
    ("のに", ["のに"]),
    ("もう逃がしません", ["もう", "逃がす", "ません", "ます", "ん"])
])
def test_identify_words(setup_collection_with_select_data: object, sentence: str, expected_output: list[str]) -> None:
    analysis = TextAnalysis(sentence, SentenceConfiguration.empty())
    root_words = [w.form for w in analysis.valid_word_variants]
    assert root_words == expected_output

@pytest.mark.parametrize("sentence, expected_output", [
    ("言わず", ["言う", "ず"]),
    ("声出したら駄目だからね", ["声", "出す", "たら", "駄目", "だから", "だ", "から", "ね"]),
    ("無理して思い出す", ["無理", "して", "する", "て", "思い出す"]),
    ("私が頼んだの", ["もう", "逃がす", "ません", "ます", "ん"]),
])
def test_excluded_surfaces(setup_collection_with_select_data: object, sentence: str, expected_output: list[str]) -> None:
    analysis = TextAnalysis(sentence, SentenceConfiguration.empty())
    root_words = [w.form for w in analysis.valid_word_variants]
    assert root_words == expected_output

@pytest.mark.parametrize("sentence, expected_output", [
    ("うわ こわっ", ["うわ", "こい", "わっ"]),
])
def test_strictly_suffix(setup_collection_with_select_data: object, sentence: str, expected_output: list[str]) -> None:
    analysis = TextAnalysis(sentence, SentenceConfiguration.empty())
    root_words = [w.form for w in analysis.valid_word_variants]
    assert root_words == expected_output

@pytest.mark.parametrize("sentence, expected_output", [
    ("うるせえ", ["うるせえ", "せえ", "せる", "せ", "え"]),
    #todo: losing the 貸せ here does not feel right. It's because we have stopped including words not in the dictionary in the parsing results, but as this shows, that means we lose imperative and potential godan verbs. That's not OK.
    ("お金貸せって", ["お金", "って"])
])
def test_requires_a_stem(setup_collection_with_select_data: object, sentence: str, expected_output: list[str]) -> None:
    analysis = TextAnalysis(sentence, SentenceConfiguration.empty())
    root_words = [w.form for w in analysis.valid_word_variants]
    assert root_words == expected_output

def test_ignores_noise_characters(setup_collection_with_select_data: object) -> None:
    sentence = ". , : ; / | 。 、ー ? !"
    expected = {"ー"}

    analysis = TextAnalysis(sentence, SentenceConfiguration.empty())
    words = {w.form for w in analysis.valid_word_variants}
    assert words == expected
