from __future__ import annotations

from test_common_helpers import value_test_including_unordered_collections


def test_concat_appends_second_sequence_to_first() -> None:
    value_test_including_unordered_collections([1, 2],
                                               lambda x: x.concat([3, 4]).to_list(),
                                               [1, 2, 3, 4])
