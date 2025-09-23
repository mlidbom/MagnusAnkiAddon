from __future__ import annotations

from test_common_helpers import value_test_including_unordered_collections


def test_select_many_flattens_nested_sequences() -> None:
    value_test_including_unordered_collections([[1, 2], [3, 4]],
                                               lambda x: x.select_many(lambda y: y).to_list(),
                                               [1, 2, 3, 4], skip_sets=True)
