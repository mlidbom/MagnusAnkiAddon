from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from ankiutils import app  # noqa  # pyright: ignore[reportUnusedImport]
from fixtures.collection_factory import inject_empty_collection
from language_services.jamdict_ex.dict_lookup import DictLookup
from note.vocabulary.vocabnote import VocabNote

if TYPE_CHECKING:
    from collections.abc import Iterator

    from language_services.jamdict_ex.dict_entry import DictEntry
    from language_services.jamdict_ex.dict_lookup_result import DictLookupResult

# noinspection PyUnusedFunction
@pytest.fixture(scope="module", autouse=True)
def setup_empty_collection() -> Iterator[None]:
    with inject_empty_collection():
        yield

@pytest.mark.parametrize("word, readings", [
        ("為る", ["する"]),
        ("為る", ["なる"])
])
def test_uk(word: str, readings: list[str]) -> None:
    dict_entry = get_dict_entry(word, readings)
    assert dict_entry.is_uk()
    assert dict_entry.found_words_count() == 1

@pytest.mark.parametrize("word, readings", [
        ("毎月", ["まいつき", "まいげつ"])
])
def test_multi_readings(word: str, readings: list[str]) -> None:
    dict_entry = get_dict_entry(word, readings)
    assert dict_entry.found_words_count() == 1

@pytest.mark.parametrize("word, readings", [
        ("元", ["もと"]),
        ("角", ["かく", "かど"]),
        ("これ", ["これ"]),
        ("正す", ["ただす"]),
        ("て", ["て"])
])
def test_multi_matches(word: str, readings: list[str]) -> None:
    dict_entry = get_dict_entry(word, readings)
    assert dict_entry.found_words_count() > 1

@pytest.mark.parametrize("word, readings", [
        ("に", ["に"]),
        ("しか", ["しか"]),
        ("ローマ字", ["ろーまじ"]),
        ("狩り", ["かり"]),
        ("おけばよかった", ["おけばよかった"])
])
def test_missing(word: str, readings: list[str]) -> None:
    dict_entry = get_dict_entry(word, readings)
    assert dict_entry.found_words_count() == 1

@pytest.mark.parametrize("word", [
        "しない",
])
def test_should_be_missing(word: str) -> None:
    result = DictLookup.lookup_word(word)
    assert len(result.entries) == 0

@pytest.mark.parametrize("word, readings", [
        ("田代島", ["たしろじま"])
])
def test_names(word: str, readings: list[str]) -> None:
    dict_entry = get_dict_entry(word, readings)
    assert dict_entry.found_words_count() == 1

@pytest.mark.parametrize("word, readings, forms", [
        ("怪我", ["けが"], {"怪我", "ケガ", "けが"}),
        ("部屋", ["へや"], {"部屋"})
])
def test_valid_forms(word: str, readings: list[str], forms: set[str]) -> None:
    dict_entry = get_dict_entry(word, readings)
    assert dict_entry.found_words_count() == 1
    assert dict_entry.valid_forms() == forms

@pytest.mark.parametrize("word, readings, answer", [
        ("張り切る", ["はりきる"], "to-be-in-high-spirits/to-be-full-of-vigor-(vigour)/to-be-enthusiastic/to-be-eager/to-stretch-to-breaking-point"),
        ("早まる", ["はやまる"], "to-be-brought-forward-(e.g.-by-three-hours)/to-be-moved-up/to-be-advanced | to-be-hasty/to-be-rash | to-quicken/to-speed-up/to-gather-speed"),
        ("部屋", ["へや"], "room/chamber | apartment/flat/pad | stable"),
        ("拭く", ["ふく"], "to-wipe/to-dry"),
        ("歩く", ["あるく"], "to-walk")
])
def test_generate_answer(word: str, readings: list[str], answer: str) -> None:
    lookup_result = get_dict_entry(word, readings)
    generated_answer = lookup_result.format_answer()
    assert generated_answer == answer

@pytest.mark.parametrize("word, readings, pos", [
        ("怪我", ["けが"], {"noun", "suru verb"}),
        ("部屋", ["へや"], {"noun"}),
        ("確実", ["かくじつ"], {"na-adjective", "noun"}),
        ("式", ["しき"], {"suffix", "noun"}),
        ("吸う", ["すう"], {"godan verb", "transitive"}),
        ("走る", ["はしる"], {"godan verb", "intransitive"}),
        ("帰る", ["かえる"], {"godan verb", "intransitive"}),
        ("使う", ["つかう"], {"godan verb", "transitive"}),
        ("書く", ["かく"], {"godan verb", "transitive"}),
        ("立つ", ["たつ"], {"godan verb", "intransitive"}),
        ("死ぬ", ["しぬ"], {"nu verb", "godan verb", "intransitive"}),
        ("飛ぶ", ["とぶ"], {"godan verb", "intransitive"}),
        ("読む", ["よむ"], {"godan verb", "transitive"}),
        ("小さな", ["ちいさな"], {"pre-noun-adjectival"})
])
def test_pos(word: str, readings: list[str], pos: set[str]) -> None:
    dict_entry = get_dict_entry(word, readings)
    assert dict_entry.found_words_count() == 1

    assert dict_entry.entries[0].parts_of_speech() == pos
    assert dict_entry.parts_of_speech() == pos

def get_single_dict_entry(word: str, readings: list[str]) -> DictEntry:
    dict_entry = get_dict_entry(word, readings)
    assert dict_entry.found_words_count() == 1
    return dict_entry.entries[0]

def get_dict_entry(word: str, readings: list[str]) -> DictLookupResult:
    vocab = VocabNote.factory.create(word, "", readings)
    return DictLookup.lookup_vocab_word_or_name(vocab)
