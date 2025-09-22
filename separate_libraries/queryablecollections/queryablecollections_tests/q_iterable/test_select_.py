from __future__ import annotations

from common_helpers import select_test


def test_select() -> None:
    select_test((1, 2, 3),
                lambda x: x * 2,
                [2, 4, 6])
