from __future__ import annotations

from queryablecollections.collections.q_list import QList
from queryablecollections.q_iterable import query


def test_zip_tuple2_with_equal_length_sequences_returns_each_combination() -> None:
    assert (
            query([1, 2, 3])
            .zip_tuple2([10, 20, 30], [100, 200, 300])
            .to_list()
            == [(1, 10, 100), (2, 20, 200), (3, 30, 300)]
    )

def test_zip_tuple2_with_single_element_sequences_returns_that_element() -> None:
    assert query([1]).zip_tuple2([10], [100]).to_list() == [(1, 10, 100)]

def test_zip_tuple2_with_shorter_first_sequence_returns_number_of_elements_in_first_sequence() -> None:
    assert (
            query([1, 2])
            .zip_tuple2([10, 20, 30, 40], [100, 200, 300, 400])
            .to_list()
            == [(1, 10, 100), (2, 20, 200)]
    )

def test_zip_tuple2_with_second_sequence_shorter_returns_number_of_elements_in_second_sequence() -> None:
    assert (
            query([1, 2, 3, 4])
            .zip_tuple2([10, 20], [100, 200, 300, 400])
            .to_list()
            == [(1, 10, 100), (2, 20, 200)]
    )

def test_zip_tuple2_with_third_sequence_shorter_returns_number_of_elements_in_third_sequence() -> None:
    assert (
            query([1, 2, 3, 4])
            .zip_tuple2([10, 20, 30, 40], [100, 200])
            .to_list()
            == [(1, 10, 100), (2, 20, 200)]
    )

def test_zip_tuple2_with_empty_first_sequence_returns_no_elements() -> None:
    assert (
            query(list[int]([]))
            .zip_tuple2([1, 2, 3], [10, 20, 30])
            .to_list()
            == []
    )

def test_zip_tuple2_with_empty_second_sequence_returns_no_elements() -> None:
    assert (
            query([1, 2, 3])
            .zip_tuple2(list[int](), [10, 20, 30])
            .to_list()
            == []
    )

def test_zip_tuple2_with_empty_third_sequence_returns_no_elements() -> None:
    assert (
            query([1, 2, 3])
            .zip_tuple2([10, 20, 30], list[int]())
            .to_list()
            == []
    )

def test_zip_tuple2_with_all_empty_sequences_returns_no_elements() -> None:
    assert (
            QList[int]()
            .zip_tuple2(QList[int](), QList[int]())
            .to_list()
            == []
    )