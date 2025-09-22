from __future__ import annotations

from queryablecollections.q_iterable import query


def test_take_while_returns_elements_until_predicate_becomes_false() -> None:
    assert query([1, 2, 3, 4, 5]).take_while(lambda x: x < 4).to_list() == [1, 2, 3]

def test_take_while_with_always_true_predicate_returns_all_elements() -> None:
    assert query([1, 2, 3, 4, 5]).take_while(lambda x: x > 0).to_list() == [1, 2, 3, 4, 5]

def test_take_while_with_always_false_predicate_returns_no_elements() -> None:
    assert query([1, 2, 3, 4, 5]).take_while(lambda x: x < 0).to_list() == []

def test_take_while_with_first_element_failing_predicate_returns_empty() -> None:
    assert query([5, 1, 2, 3]).take_while(lambda x: x < 3).to_list() == []

def test_take_while_from_empty_collection_returns_empty() -> None:
    assert query(list[int]([])).take_while(lambda x: True).to_list() == []

def test_take_while_with_single_element_matching_predicate_returns_the_element() -> None:
    assert query([42]).take_while(lambda x: x > 0).to_list() == [42]

def test_take_while_with_single_element_not_matching_predicate_returns_no_elements() -> None:
    assert query([42]).take_while(lambda x: x < 0).to_list() == []

def test_take_while_is_lazy() -> None:
    call_count = 0

    def expensive_operation(_: int) -> int:
        nonlocal call_count
        call_count += 1
        return 0

    query([1, 2, 3, 4]).select(expensive_operation).take_while(lambda x: x < 6)
    assert call_count == 0

def test_take_while_stops_processing_at_the_first_element_that_fails_the_predidate() -> None:
    processed_values: list[int] = []

    def track_processing(x: int) -> int:
        processed_values.append(x)
        return x

    result = query([1, 2, 3, 4, 5]).select(track_processing).take_while(lambda x: x < 4).to_list()

    assert result == [1, 2, 3]
    assert processed_values == [1, 2, 3, 4]
