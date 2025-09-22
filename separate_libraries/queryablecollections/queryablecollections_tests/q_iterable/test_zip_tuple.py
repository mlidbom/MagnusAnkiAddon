from __future__ import annotations

from queryablecollections.collections.q_list import QList
from queryablecollections.q_iterable import query


def test_zip_tuple_with_equal_length_sequences_returns_each_combination() -> None:
    assert (query([1, 2, 3])
            .zip_tuple([10, 20, 30])
            .to_list() == [(1, 10), (2, 20), (3, 30)])

def test_zip_tuple_with_single_element_sequences_returns_that_element() -> None:
    assert query([42]).zip_tuple([100]).to_list() == [(42, 100)]

def test_zip_tuple_with_shorter_first_sequence_returns_the_number_of_elements_in_the_first_sequence() -> None:
    assert (query([1, 2])
            .zip_tuple([10, 20, 30, 40])
            .to_list() == [(1, 10), (2, 20)])

def test_zip_tuple_with_second_sequence_shorter_returns_the_number_of_elements_in_the_second_sequence() -> None:
    assert (query([1, 2, 3, 4])
            .zip_tuple([10, 20])
            .to_list() == [(1, 10), (2, 20)])

def test_zip_tuple_with_empty_first_sequence_returns_no_elements() -> None:
    assert (query(list[int]([]))
            .zip_tuple([1, 2, 3])
            .to_list() == [])

def test_zip_tuple_with_empty_second_sequence_returns_no_elements() -> None:
    assert (query([1, 2, 3])
            .zip_tuple(list[int]())
            .to_list() == [])

def test_zip_tuple_with_both_empty_sequences_returns_no_elements() -> None:
    assert (QList[int]()
            .zip_tuple(QList[int]())
            .to_list() == [])