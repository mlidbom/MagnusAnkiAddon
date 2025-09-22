from __future__ import annotations

from common_helpers import value_test
from queryablecollections.collections.q_list import QList


def test_not_none_returns_only_elements_that_are_not_none() -> None: value_test([1, None], lambda x: x.where_not_none().to_list(), [1])
def test_not_none_returns_empty_list_if_all_elements_are_none() -> None: value_test(QList[str | None]([None, None]), lambda x: x.where_not_none().to_list(), list[str]())
