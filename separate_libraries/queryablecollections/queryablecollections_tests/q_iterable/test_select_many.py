from __future__ import annotations

from common_helpers import value_test


def test_select_many_flattens_nested_sequences() -> None:
    value_test([[1, 2], [3, 4]],
               lambda x: x.select_many(lambda y: y).to_list(),
               [1, 2, 3, 4], skip_sets=True)
