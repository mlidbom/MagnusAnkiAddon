from __future__ import annotations

from queryablecollections.collections.q_list import QList
from queryablecollections.q_iterable import query


def test_zip_with_equal_length_sequences_returns_each_combination() -> None:
    assert (query([1, 2, 3])
            .zip([10, 20, 30], lambda x, y: x + y)
            .to_list() == [11, 22, 33])

def test_zip_with_single_element_sequences_returns_that_element() -> None:
    assert query([42]).zip([100], lambda x, y: x - y).to_list() == [-58]

def test_zip_with_shorter_first_sequence_returns_the_number_of_elements_in_the_first_sequence() -> None:
    assert (query([1, 2])
            .zip([10, 20, 30, 40], lambda x, y: x * y)
            .to_list() == [10, 40])

def test_zip_with_second_sequence_shorter_returns_the_number_of_elements_in_the_second_sequence() -> None:
    assert (query([1, 2, 3, 4])
            .zip([10, 20], lambda x, y: x + y)
            .to_list() == [11, 22])

def test_zip_with_empty_first_sequence_returns_no_elements() -> None:
    assert (query(list[int]([]))
            .zip([1, 2, 3], lambda x, y: x + y)
            .to_list() == [])

def test_zip_with_empty_second_sequence_returns_no_elements() -> None:
    assert (query([1, 2, 3])
            .zip(list[int](), lambda x, y: x + y)
            .to_list() == [])

def test_zip_with_both_empty_sequences_returns_no_elements() -> None:
    assert (QList[int]()
            .zip(QList[int](), lambda x, y: x + y)
            .to_list() == [])
