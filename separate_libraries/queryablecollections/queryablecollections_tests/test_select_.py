from __future__ import annotations

from test_iterable_common import select_test, value_test


def test_select() -> None: select_test((1, 2, 3), lambda x: x * 2, [2, 4, 6])

def test_select_many_flattens_nested_sequences() -> None: value_test([[1, 2], [3, 4]], lambda x: x.select_many(lambda y: y).to_list(), [1, 2, 3, 4], skip_sets=True)
