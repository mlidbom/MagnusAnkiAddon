from __future__ import annotations

from test_common_helpers import value_test


def test_returns_element_count_of_sequence() -> None:
    value_test([0], lambda x: x.qcount(), 1)
    value_test([0, 3], lambda x: x.qcount(), 2)
    value_test([0, 3, 5], lambda x: x.qcount(), 3)