from __future__ import annotations

from common_helpers import value_test


def test_concat_appends_second_sequence_to_first() -> None:
    value_test([1, 2],
               lambda x: x.concat([3, 4]).to_list(),
               [1, 2, 3, 4])
