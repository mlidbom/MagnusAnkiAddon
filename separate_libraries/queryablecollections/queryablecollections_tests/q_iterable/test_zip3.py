from __future__ import annotations

from queryablecollections.collections.q_list import QList
from queryablecollections.q_iterable import query


def test_zip3_with_equal_length_sequences_returns_each_combination() -> None:
    assert (
            query([1, 2, 3])
            .zip3([10, 20, 30],
                  [100, 200, 300],
                  [1000, 2000, 3000],
                  lambda a, b, c, d: (a, b, c, d))
            .to_list()
            == [(1, 10, 100, 1000), (2, 20, 200, 2000), (3, 30, 300, 3000)]
    )

def test_zip3_with_single_element_sequences_returns_that_element() -> None:
    assert query([1]).zip3([10], [100], [1000], lambda a, b, c, d: (a, b, c, d)).to_list() == [(1, 10, 100, 1000)]

def test_zip3_with_shorter_first_sequence_returns_number_of_elements_in_first_sequence() -> None:
    assert (
            query([1, 2])
            .zip3([10, 20, 30, 40],
                  [100, 200, 300, 400],
                  [1000, 2000, 3000, 4000],
                  lambda a, b, c, d: (a, b, c, d))
            .to_list()
            == [(1, 10, 100, 1000), (2, 20, 200, 2000)]
    )

def test_zip3_with_second_sequence_shorter_returns_number_of_elements_in_second_sequence() -> None:
    assert (
            query([1, 2, 3, 4])
            .zip3([10, 20],
                  [100, 200, 300, 400],
                  [1000, 2000, 3000, 4000],
                  lambda a, b, c, d: (a, b, c, d))
            .to_list()
            == [(1, 10, 100, 1000), (2, 20, 200, 2000)]
    )

def test_zip3_with_third_sequence_shorter_returns_number_of_elements_in_third_sequence() -> None:
    assert (
            query([1, 2, 3, 4])
            .zip3([10, 20, 30, 40],
                  [100, 200],
                  [1000, 2000, 3000, 4000],
                  lambda a, b, c, d: (a, b, c, d))
            .to_list()
            == [(1, 10, 100, 1000), (2, 20, 200, 2000)]
    )

def test_zip3_with_fourth_sequence_shorter_returns_number_of_elements_in_fourth_sequence() -> None:
    assert (
            query([1, 2, 3, 4])
            .zip3([10, 20, 30, 40],
                  [100, 200, 300, 400],
                  [1000, 2000],
                  lambda a, b, c, d: (a, b, c, d))
            .to_list()
            == [(1, 10, 100, 1000), (2, 20, 200, 2000)]
    )

def test_zip3_with_empty_first_sequence_returns_no_elements() -> None:
    assert (
            query(list[int]([]))
            .zip3([1, 2, 3],
                  [10, 20, 30]
                  , [100, 200, 300],
                  lambda a, b, c, d: (a, b, c, d))
            .to_list()
            == []
    )

def test_zip3_with_empty_second_sequence_returns_no_elements() -> None:
    assert (
            query([1, 2, 3])
            .zip3(list[int](),
                  [10, 20, 30],
                  [100, 200, 300],
                  lambda a, b, c, d: (a, b, c, d))
            .to_list()
            == []
    )

def test_zip3_with_empty_third_sequence_returns_no_elements() -> None:
    assert (
            query([1, 2, 3])
            .zip3([10, 20, 30],
                  list[int](),
                  [100, 200, 300],
                  lambda a, b, c, d: (a, b, c, d))
            .to_list()
            == []
    )

def test_zip3_with_empty_fourth_sequence_returns_no_elements() -> None:
    assert (
            query([1, 2, 3])
            .zip3([10, 20, 30],
                  [100, 200, 300],
                  list[int](),
                  lambda a, b, c, d: (a, b, c, d))
            .to_list()
            == []
    )

def test_zip3_with_all_empty_sequences_returns_no_elements() -> None:
    assert (
            QList[int]()
            .zip3(QList[int](),
                  QList[int](),
                  QList[int](),
                  lambda a, b, c, d: (a, b, c, d))
            .to_list()
            == []
    )
