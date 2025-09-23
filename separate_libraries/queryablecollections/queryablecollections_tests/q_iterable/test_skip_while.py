from __future__ import annotations

from queryablecollections.q_iterable import query


def test_skip_while_skips_elements_until_predicate_becomes_false() -> None:
    assert (query([1, 2, 3, 4, 5]).skip_while(
            lambda x: x < 3).to_list()
            == [3, 4, 5])

def test_skip_while_with_always_true_predicate_returns_no_elements() -> None:
    assert (query([1, 2, 3, 4, 5]).skip_while(
            lambda _: True).to_list()
            == [])

def test_skip_while_with_always_false_predicate_returns_all_elements() -> None:
    assert (query([1, 2, 3, 4, 5]).skip_while(
            lambda _: False).to_list()
            == [1, 2, 3, 4, 5])

def test_skip_while_with_first_element_failing_predicate_returns_all() -> None:
    assert (query([1, 2, 3]).skip_while(
            lambda x: x < 1).to_list()
            == [1, 2, 3])

def test_skip_while_from_empty_collection_returns_empty() -> None:
    assert (query(list[int]([])).skip_while(
            lambda _: True).to_list()
            == [])

def test_skip_while_with_single_element_matching_predicate_returns_no_elements() -> None:
    assert (query([1]).skip_while(
            lambda x: x == 1).to_list()
            == [])

def test_skip_while_with_single_element_not_matching_predicate_returns_the_element() -> None:
    assert (query([1]).skip_while(
            lambda x: x == 2).to_list()
            == [1])