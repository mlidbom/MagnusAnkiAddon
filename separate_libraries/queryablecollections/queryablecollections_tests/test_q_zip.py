from __future__ import annotations

from typing import Any

from queryablecollections.collections.q_list import QList
from queryablecollections.q_iterable import query


class TestZip:
    def test_zip_with_equal_length_sequences_returns_each_combination(self) -> None:
        assert (query([1, 2, 3])
                .zip([10, 20, 30], lambda x, y: x + y)
                .to_list() == [11, 22, 33])

    def test_zip_with_single_element_sequences_returns_that_element(self) -> None:
        assert query([42]).zip([100], lambda x, y: x - y).to_list() == [-58]

    def test_zip_with_shorter_first_sequence_returns_the_number_of_elements_in_the_first_sequence(self) -> None:
        assert (query([1, 2])
                .zip([10, 20, 30, 40], lambda x, y: x * y)
                .to_list() == [10, 40])

    def test_zip_with_second_sequence_shorter_returns_the_number_of_elements_in_the_second_sequence(self) -> None:
        assert (query([1, 2, 3, 4])
                .zip([10, 20], lambda x, y: x + y)
                .to_list() == [11, 22])

    def test_zip_with_empty_first_sequence_returns_no_elements(self) -> None:
        assert (query(list[int]([]))
                .zip([1, 2, 3], lambda x, y: x + y)
                .to_list() == [])

    def test_zip_with_empty_second_sequence_returns_no_elements(self) -> None:
        assert (query([1, 2, 3])
                .zip(list[int](), lambda x, y: x + y).to_list() == [])

    def test_zip_with_both_empty_sequences_returns_no_elements(self) -> None:
        assert (QList[int]()
                .zip(QList[int](), lambda x, y: x + y)
                .to_list() == [])

    def test_zip_is_lazy(self) -> None:
        call_count = 0

        def counting_selector(x: int, y: int) -> Any:
            nonlocal call_count
            call_count += 1
            return x + y

        zipped = query([1, 2, 3]).zip([10, 20, 30], counting_selector)

        assert call_count == 0

        result = zipped.to_list()
        assert call_count == 3
        assert result == [11, 22, 33]
