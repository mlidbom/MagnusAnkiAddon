from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from fixtures.collection_factory import inject_collection_with_select_data
from note.sentences.sentencenote import SentenceNote

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis


# noinspection PyUnusedFunction
@pytest.fixture(scope="module")
def setup_collection_with_select_data() -> Iterator[None]:
    with inject_collection_with_select_data(special_vocab=True):
        yield

@pytest.mark.usefixtures("setup_collection_with_select_data")
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
     ["１人で", "１人", "１", "人", "でいる", "で", "いる", "時間", "が", "これほど", "これ", "ほど", "までに", "まで", "に", "長い", "感じる", "とは", "と", "は"]
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
    ("もう逃がしません", ["もう", "逃がす", "ません", "ます", "ん"]),
    ("死んどる", ["死ぬ", "んどる"])
])
def test_identify_words(sentence: str, expected_output: list[str]) -> None:
    sentence_note = SentenceNote.create_test_note(sentence, "")
    words = [w.parsed_form for w in sentence_note.parsing_result.get().parsed_words]
    assert words == expected_output

@pytest.mark.usefixtures("setup_collection_with_select_data")
@pytest.mark.parametrize("sentence, expected_output", [
    ("言わず", ["言う", "ず"]),
    ("声出したら駄目だからね", ["声", "出す", "たら", "駄目", "だから", "だ", "から", "ね"]),
    ("無理して思い出す", ["無理", "して", "する", "て", "思い出す"]),
    ("私が頼んだの", ["私", "が", "頼む", "んだ", "の"]),
])
def test_excluded_surfaces(sentence: str, expected_output: list[str]) -> None:
    sentence_note = SentenceNote.create_test_note(sentence, "")
    words = [w.parsed_form for w in sentence_note.parsing_result.get().parsed_words]
    assert words == expected_output

@pytest.mark.usefixtures("setup_collection_with_select_data")
@pytest.mark.parametrize("sentence, expected_output", [
    ("うわ こわっ", ["うわ", "こい", "わっ"]),
])
def test_strictly_suffix(sentence: str, expected_output: list[str]) -> None:
    sentence_note = SentenceNote.create_test_note(sentence, "")
    words = [w.parsed_form for w in sentence_note.parsing_result.get().parsed_words]
    assert words == expected_output

@pytest.mark.usefixtures("setup_collection_with_select_data")
@pytest.mark.parametrize("sentence, expected_output", [
    ("うるせえ", ["うるせえ", "せえ", "せる", "せ", "え"]),
    # todo: losing the 貸せ here does not feel right. It's because we have stopped including words not in the dictionary in the parsing results, but as this shows, that means we lose imperative and potential godan verbs. That's not OK.
    ("お金貸せって", ["お金", "って"])
])
def test_requires_a_stem(sentence: str, expected_output: list[str]) -> None:
    sentence_note = SentenceNote.create_test_note(sentence, "")
    root_words = [w.parsed_form for w in sentence_note.parsing_result.get().parsed_words]
    assert root_words == expected_output

@pytest.mark.usefixtures("setup_collection_with_select_data")
def test_ignores_noise_characters() -> None:
    sentence = ". , : ; / | 。 、ー ? !"
    expected = {"ー"}

    sentence_note = SentenceNote.create_test_note(sentence, "")
    words = {w.parsed_form for w in sentence_note.parsing_result.get().parsed_words}
    assert words == expected

@pytest.mark.usefixtures("setup_collection_with_select_data")
def test_that_vocab_is_not_indexed_even_if_form_is_highlighted_if_invalid_and_there_is_another_valid_vocab_with_the_form() -> None:
    sentence = SentenceNote.create_test_note("勝つんだ", "")
    sentence.configuration.highlighted_words().add("んだ")
    sentence.update_parsed_words(force=True)
    parsing_result = sentence.parsing_result.get()
    words = [w.parsed_form for w in parsing_result.parsed_words]
    assert words == ["勝つ", "んだ", "ん", "だ"]

@pytest.mark.usefixtures("setup_collection_with_select_data")
def test_no_memory_leak_weak_references_are_disposed() -> None:
    sentence_note = SentenceNote.create_test_note("作るに決まってるだろ, ", "")

    def assert_that_the_inner_weakref_has_been_destroyed[T1](fetch_member_from_analysis: Callable[[TextAnalysis], T1], access_weakref_that_should_have_been_deleted: Callable[[T1], object]) -> None:
        def create_analysis_and_return_value_of_first_func() -> T1:
            return fetch_member_from_analysis(sentence_note.create_analysis())
        first_value: T1 = create_analysis_and_return_value_of_first_func()

        with pytest.raises(ReferenceError):
            access_weakref_that_should_have_been_deleted(first_value)

    assert_that_the_inner_weakref_has_been_destroyed(lambda analysis: analysis.locations[0],
                                                     lambda location: location.analysis())
    assert_that_the_inner_weakref_has_been_destroyed(lambda analysis: analysis.locations[0].candidate_words[0],
                                                     lambda cand: cand.start_location)
    assert_that_the_inner_weakref_has_been_destroyed(lambda analysis: analysis.all_matches[0],
                                                     lambda match: match.word)
    assert_that_the_inner_weakref_has_been_destroyed(lambda analysis: analysis.all_matches[0]._display_requirements[0], # pyright: ignore[reportPrivateUsage]
                                                     lambda requirement: requirement.state_test.match)
    assert_that_the_inner_weakref_has_been_destroyed(lambda analysis: analysis.all_matches[0]._validity_requirements[0],  # pyright: ignore[reportPrivateUsage]
                                                     lambda requirement: requirement.state_test.match)
    assert_that_the_inner_weakref_has_been_destroyed(lambda analysis: analysis.all_matches[0]._validity_requirements[0].state_test.weakref,  # pyright: ignore[reportPrivateUsage]
                                                     lambda state_test_weak_ref: state_test_weak_ref())
