from __future__ import annotations

from typing import Any, Iterable

from queryablecollections.collections.q_list import QList
from queryablecollections.q_iterable import query


class TestZip2IterablesWithResultSelector:
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

class TestZip2IterablesWithoutResultSelector:
    def test_zip_with_equal_length_sequences_returns_tuple_pairs(self) -> None:
        assert (query([1, 2, 3])
                .zip([10, 20, 30])
                .to_list()) == [(1, 10),
                                (2, 20),
                                (3, 30)]

    def test_zip_with_single_element_sequences_returns_single_tuple(self) -> None:
        assert (query([42])
                .zip([100]).to_list()) == [(42, 100)]

    def test_zip_with_shorter_first_sequence_returns_the_number_of_elements_in_the_first_sequence(self) -> None:
        assert (query([1, 2])
                .zip([10, 20, 30, 40])
                .to_list() == [(1, 10), (2, 20)])

    def test_zip_with_second_sequence_shorter_returns_the_number_of_elements_in_the_second_sequence(self) -> None:
        assert (query([1, 2, 3, 4])
                .zip([10, 20])
                .to_list()) == [(1, 10),
                                (2, 20)]

    def test_zip_with_empty_first_sequence_returns_no_elements(self) -> None:
        assert (query(list[int]([]))
                .zip([1, 2, 3])
                .to_list()) == []

    def test_zip_with_empty_second_sequence_returns_no_elements(self) -> None:
        assert (query([1, 2, 3])
                .zip(list[int]())
                .to_list()) == []

    def test_zip_with_both_empty_sequences_returns_no_elements(self) -> None:
        assert (QList[int]()
                .zip(QList[int]())
                .to_list()) == []

    def test_zip_with_different_types_returns_mixed_type_tuples(self) -> None:
        assert (query(["a", "b", "c"])
                .zip([1, 2, 3])
                .to_list()) == [("a", 1), ("b", 2), ("c", 3)]

    def test_zip_is_lazy(self) -> None:
        consumed = False
        def consuming_iterable() -> Iterable[int]:
            nonlocal consumed
            consumed = True
            yield from [10, 20, 30]

        zipped = query([1, 2, 3]).zip(consuming_iterable())

        assert not consumed

        result = zipped.to_list()
        assert consumed
        assert result == [(1, 10), (2, 20), (3, 30)]

class TestZip3Iterables:
    def test_zip_with_equal_length_sequences_returns_tuple_triples(self) -> None:
        assert (query([1, 2, 3])
                .zip([10, 20, 30],
                     [100, 200, 300])
                .to_list()) == [(1, 10, 100),
                                (2, 20, 200),
                                (3, 30, 300)]

    def test_zip_with_single_element_sequences_returns_single_triple(self) -> None:
        assert (query([1])
                .zip([10], [100]).to_list()) == [(1, 10, 100)]

    def test_zip_with_shortest_first_sequence_returns_the_number_of_elements_in_the_first_sequence(self) -> None:
        assert (query([1, 2])
                .zip([10, 20, 30],
                     [100, 200, 300, 400])
                .to_list() == [(1, 10, 100), (2, 20, 200)])

    def test_zip_with_shortest_second_sequence_returns_the_number_of_elements_in_the_second_sequence(self) -> None:
        assert (query([1, 2, 3, 4])
                .zip([10, 20],
                     [100, 200, 300])
                .to_list() == [(1, 10, 100), (2, 20, 200)])

    def test_zip_with_shortest_third_sequence_returns_the_number_of_elements_in_the_third_sequence(self) -> None:
        assert (query([1, 2, 3, 4])
                .zip([10, 20, 30],
                     [100])
                .to_list() == [(1, 10, 100)])

    def test_zip_with_empty_first_sequence_returns_no_elements(self) -> None:
        assert (query(list[int]([]))
                .zip([1, 2, 3],
                     [10, 20, 30])
                .to_list() == [])

    def test_zip_with_empty_second_sequence_returns_no_elements(self) -> None:
        assert (query([1, 2, 3])
                .zip(list[int](),
                     [10, 20, 30])
                .to_list() == [])

    def test_zip_with_empty_third_sequence_returns_no_elements(self) -> None:
        assert (query([1, 2, 3])
                .zip([10, 20, 30],
                     list[int]())
                .to_list() == [])

    def test_zip_with_all_empty_sequences_returns_no_elements(self) -> None:
        assert (QList[int]()
                .zip(QList[int](),
                     QList[int]())
                .to_list() == [])

    def test_zip_with_different_types_returns_mixed_type_tuples(self) -> None:
        assert (query(["a", "b"])
                .zip([1, 2],
                     [10.5, 20.5])
                .to_list() == [("a", 1, 10.5), ("b", 2, 20.5)])

    def test_zip_is_lazy(self) -> None:
        second_consumed = False
        third_consumed = False

        def consuming_second() -> Iterable[int]:
            nonlocal second_consumed
            second_consumed = True
            yield from [10, 20, 30]

        def consuming_third() -> Iterable[int]:
            nonlocal third_consumed
            third_consumed = True
            yield from [100, 200, 300]

        zipped = query([1, 2, 3]).zip(consuming_second(), consuming_third())

        assert not second_consumed
        assert not third_consumed

        result = zipped.to_list()
        assert second_consumed
        assert third_consumed
        assert result == [(1, 10, 100), (2, 20, 200), (3, 30, 300)]
