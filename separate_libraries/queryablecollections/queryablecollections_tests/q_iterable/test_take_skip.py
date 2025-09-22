from __future__ import annotations

from queryablecollections.q_iterable import query


class TestTakeOperations:
    def test_take_returns_the_specified_number_of_elements_from_the_start(self) -> None:
        assert query([1, 2, 3, 4, 5]).take(3).to_list() == [1, 2, 3]

    def test_take_zero_returns_empty_iterable(self) -> None:
        assert query([1, 2, 3, 4, 5]).take(0).to_list() == []

    def test_take_negative_returns_empty_iterable(self) -> None:
        assert query([1, 2, 3, 4, 5]).take(-5).to_list() == []

    def test_take_more_than_available_returns_the_full_iterable(self) -> None:
        assert query([1, 2, 3]).take(10).to_list() == [1, 2, 3]

    def test_take_from_empty_returns_empty_iterable(self) -> None:
        assert query([]).take(5).to_list() == []

class TestSkipOperations:
    def test_skip_skips_the_specified_number_of_elements(self) -> None:
        assert query([1, 2, 3, 4, 5]).skip(2).to_list() == [3, 4, 5]

    def test_skip_zero_returns_all_elements(self) -> None:
        assert query([1, 2, 3, 4, 5]).skip(0).to_list() == [1, 2, 3, 4, 5]

    def test_skip_negative_count_returns_all_elements(self) -> None:
        assert query([1, 2, 3, 4, 5]).skip(-3).to_list() == [1, 2, 3, 4, 5]

    def test_skip_more_than_available_returns_no_elements(self) -> None:
        assert query([1, 2, 3]).skip(10).to_list() == []

    def test_skip_from_empty_returns_no_elements(self) -> None:
        assert query([]).skip(5).to_list() == []

class TestTakeLastOperations:
    def test_take_last_returns_the_last_x_elements(self) -> None:
        assert query([1, 2, 3, 4, 5]).take_last(3).to_list() == [3, 4, 5]

    def test_take_last_zero_returns_no_elements(self) -> None:
        assert query([1, 2, 3, 4, 5]).take_last(0).to_list() == []

    def test_take_last_negative_count_returns_no_elements(self) -> None:
        assert query([1, 2, 3, 4, 5]).take_last(-5).to_list() == []

    def test_take_last_more_than_available_returns_all_elements(self) -> None:
        assert query([1, 2, 3]).take_last(10).to_list() == [1, 2, 3]

    def test_take_last_from_empty_returns_no_elements(self) -> None:
        assert query([]).take_last(5).to_list() == []

    def test_take_last_single_element_returns_the_single_element(self) -> None:
        assert query([42]).take_last(1).to_list() == [42]

class TestSkipLastOperations:
    def test_skip_last_skips_the_last_x_elements(self) -> None:
        assert query([1, 2, 3, 4, 5]).skip_last(2).to_list() == [1, 2, 3]

    def test_skip_last_zero_returns_all_elements(self) -> None:
        assert query([1, 2, 3, 4, 5]).skip_last(0).to_list() == [1, 2, 3, 4, 5]

    def test_skip_last_negative_returns_all_elements(self) -> None:
        assert query([1, 2, 3, 4, 5]).skip_last(-3).to_list() == [1, 2, 3, 4, 5]

    def test_skip_last_more_than_available_returns_no_elements(self) -> None:
        assert query([1, 2, 3]).skip_last(10).to_list() == []

    def test_skip_last_from_empty_returns_no_elements(self) -> None:
        assert query([]).skip_last(5).to_list() == []

    def test_skip_last_single_element_returns_no_elements(self) -> None:
        assert query([42]).skip_last(1).to_list() == []

class TestLazyness:
    def test_take_is_lazy(self) -> None:
        call_count = 0
        def expensive_operation(_: int) -> int:
            nonlocal call_count
            call_count += 1
            return 0
        query([1, 2]).select(expensive_operation).take(3)
        assert call_count == 0

    def test_take_last_is_lazy(self) -> None:
        call_count = 0
        def expensive_operation(_: int) -> int:
            nonlocal call_count
            call_count += 1
            return 0
        query([1, 2, 3, 4]).select(expensive_operation).take_last(2)
        assert call_count == 0

    def test_skip_is_lazy(self) -> None:
        call_count = 0
        def expensive_operation(_: int) -> int:
            nonlocal call_count
            call_count += 1
            return 0
        query([1, 2, 3, 4]).select(expensive_operation).skip(2)
        assert call_count == 0

    def test_skip_last_is_lazy(self) -> None:
        call_count = 0
        def expensive_operation(_: int) -> int:
            nonlocal call_count
            call_count += 1
            return 0
        query([1, 2, 3, 4]).select(expensive_operation).skip_last(2)
        assert call_count == 0
