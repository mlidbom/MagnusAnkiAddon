
from __future__ import annotations

from test_common_helpers import lists_value_test


def test_combines_items_with_their_index() -> None:
    lists_value_test([10, 20, 30],
               lambda x: x.select_index(lambda item, index: (index, item)).to_list(),
               [(0, 10), (1, 20), (2, 30)])

def test_with_empty_collection_returns_empty() -> None:
    lists_value_test(list[str](),
               lambda x: x.select_index(lambda item, index: f"{index}:{item}").to_list(),
               list[str]())


def test_with_single_element() -> None:
    lists_value_test(["hello"],
               lambda x: x.select_index(lambda item, index: f"{index}:{item}").to_list(),
               ["0:hello"])