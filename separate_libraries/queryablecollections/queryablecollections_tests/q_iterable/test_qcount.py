from __future__ import annotations

from common_helpers import value_test


def test_length_returns_length_of_sequence() -> None:
    value_test([0], lambda x: x.qcount(), 1)
    value_test([0, 3], lambda x: x.qcount(), 2)
    value_test([0, 3, 5], lambda x: x.qcount(), 3)