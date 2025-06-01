from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from ankiutils import app
from fixtures.collection_factory import inject_anki_collection_with_select_data, inject_empty_anki_collection_with_note_types
from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
from note.sentences.sentence_configuration import SentenceConfiguration
from note.sentences.sentencenote import SentenceNote
from note.vocabulary.vocabnote import VocabNote

if TYPE_CHECKING:
    from collections.abc import Iterator

# noinspection PyUnusedFunction
@pytest.fixture(scope="function")
def setup_collection_with_select_data() -> Iterator[None]:
    with inject_anki_collection_with_select_data(special_vocab=True):
        yield

@pytest.fixture(scope="function")
def setup_empty_collection() -> Iterator[None]:
    with inject_empty_anki_collection_with_note_types():
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
    ("清めの一波", ["清める", "清め", "の", "一波"]),
    ("さっさと傷を清めてこい",
     ["さっさと", "傷", "を", "清める", "て", "くる", "こい"]),
    ("すげえ", ["すげえ", "すげ", "え"]),
    ("「コーヒーはいかがですか？」「いえ、結構です。お構いなく。」", ["コーヒー", "は", "いかが", "ですか", "です", "か", "いえ", "結構", "です", "お構いなく"]),
    ("解放する", ["解放する", "解放", "する"]),
    ("落書きしたろ", ["落書き", "する", "た"])
])
def test_identify_words(setup_collection_with_select_data: object, sentence: str, expected_output: list[str]) -> None:
    analysis = TextAnalysis(sentence, SentenceConfiguration.empty())
    root_words = [w.form for w in analysis.all_words]
    assert root_words == expected_output

@pytest.mark.parametrize("sentence, expected_output", [
    ("言わず", ["言う", "ず"]),
    ("声出したら駄目だからね", ["声", "出す", "たら", "駄目", "だから", "だ", "から", "ね"]),
    ("無理して思い出す", ["無理", "して", "する", "て", "思い出す"]),
    ("私が頼んだの", ["私", "が", "頼む", "だ", "の"]),
])
def test_excluded_surfaces(setup_collection_with_select_data: object, sentence: str, expected_output: list[str]) -> None:
    analysis = TextAnalysis(sentence, SentenceConfiguration.empty())
    root_words = [w.form for w in analysis.all_words]
    assert root_words == expected_output

@pytest.mark.parametrize("sentence, expected_output", [
    ("うわ こわっ", ["うわ", "こい", "わっ"]),
])
def test_strictly_suffix(setup_collection_with_select_data: object, sentence: str, expected_output: list[str]) -> None:
    analysis = TextAnalysis(sentence, SentenceConfiguration.empty())
    root_words = [w.form for w in analysis.all_words]
    assert root_words == expected_output

@pytest.mark.parametrize("sentence, expected_output", [
    ("うるせえ", ["うるせえ", "うる", "せえ", "せる", "せ", "え"]),
    ("金貸せって", ["金貸", "せる", "て"])
])
def test_requires_a_stem(setup_collection_with_select_data: object, sentence: str, expected_output: list[str]) -> None:
    analysis = TextAnalysis(sentence, SentenceConfiguration.empty())
    root_words = [w.form for w in analysis.all_words]
    assert root_words == expected_output

@pytest.mark.parametrize("sentence, expected_output", [
    ("金<wbr>貸せって", ["金", "貸す", "える", "って"])
])
def test_invisible_space_breakup(setup_collection_with_select_data: object, sentence: str, expected_output: list[str]) -> None:
    sentence_note = SentenceNote.create(sentence)
    analysis = TextAnalysis(sentence_note.get_question(), SentenceConfiguration.empty())
    root_words = [w.form for w in analysis.all_words]
    assert root_words == expected_output

@pytest.mark.parametrize("sentence, expected_output", [
    ("しろ", ["しろ"]),
    ("後で下に下りてらっしゃいね", ["後で", "下に", "下", "に", "下りる", "て", "らっしゃい", "ね"]),
])
def test_prefer_surfaces_over_bases(setup_collection_with_select_data: object, sentence: str, expected_output: list[str]) -> None:
    analysis = TextAnalysis(sentence, SentenceConfiguration.empty())
    root_words = [w.form for w in analysis.all_words]
    assert root_words == expected_output

@pytest.mark.parametrize("sentence, custom_words, expected_output", [
    ("彼の日本語のレベルは私と同じ位だ。",
     ["彼の日本語", "日本語のレベル"],
     ["彼", "彼の", "彼の日本語", "の", "日本語", "日本語のレベル", "レベル", "は", "私", "と", "同じ", "同じ位", "位", "だ"]
     )
])
def test_custom_vocab_words(setup_collection_with_select_data: object, sentence: str, custom_words: list[str], expected_output: list[str]) -> None:
    insert_custom_words(custom_words)

    analysis = TextAnalysis(sentence, SentenceConfiguration.empty())
    root_words = sorted({w.form for w in analysis.all_words})
    assert root_words == sorted(expected_output)

def test_ignores_noise_characters(setup_collection_with_select_data: object) -> None:
    sentence = ". , : ; / | 。 、ー ? !"
    expected = {"ー"}

    analysis = TextAnalysis(sentence, SentenceConfiguration.empty())
    words = {w.form for w in analysis.all_words}
    assert words == expected

def insert_custom_words(custom_words: list[str]) -> None:
    for custom_word in custom_words:
        VocabNote.factory.create(custom_word, "", [""])
    app.col().flush_cache_updates()
