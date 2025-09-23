
from __future__ import annotations

from test_common_helpers import lists_value_test


def test_select_index_transforms_elements_with_their_indices() -> None:
    lists_value_test(["a", "b", "c"],
               lambda x: x.select_index(lambda item, index: f"{index}:{item}").to_list(),
               ["0:a", "1:b", "2:c"])


def test_select_index_with_empty_collection_returns_empty() -> None:
    lists_value_test(list[str](),
               lambda x: x.select_index(lambda item, index: f"{index}:{item}").to_list(),
               list[str]())


def test_select_index_with_single_element() -> None:
    lists_value_test(["hello"],
               lambda x: x.select_index(lambda item, index: f"{index}:{item}").to_list(),
               ["0:hello"])


def test_select_index_with_numbers() -> None:
    lists_value_test([10, 20, 30],
               lambda x: x.select_index(lambda item, index: item + index).to_list(),
               [10, 21, 32])


def test_select_index_only_uses_index() -> None:
    lists_value_test(["ignore", "these", "values"],
               lambda x: x.select_index(lambda item, index: index * 2).to_list(),
               [0, 2, 4])


def test_select_index_only_uses_item() -> None:
    lists_value_test(["a", "b", "c"],
               lambda x: x.select_index(lambda item, index: item.upper()).to_list(),
               ["A", "B", "C"])


def test_select_index_creates_tuples() -> None:
    lists_value_test([10, 20, 30],
               lambda x: x.select_index(lambda item, index: (index, item)).to_list(),
               [(0, 10), (1, 20), (2, 30)])


def test_select_index_with_mixed_types() -> None:
    lists_value_test([1, "hello", 3.14],
               lambda x: x.select_index(lambda item, index: f"[{index}] {item}").to_list(),
               ["[0] 1", "[1] hello", "[2] 3.14"])


def test_select_index_can_be_chained() -> None:
    lists_value_test([1, 2, 3],
               lambda x: x.select_index(lambda item, index: item + index).where(lambda x: x > 2).to_list(),
               [3, 5])


def test_select_index_with_boolean_logic() -> None:
    lists_value_test([10, 15, 20, 25],
               lambda x: x.select_index(lambda item, index: index % 2 == 0 and item > 15).to_list(),
               [False, False, True, False])