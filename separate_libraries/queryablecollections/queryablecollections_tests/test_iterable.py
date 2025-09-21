from __future__ import annotations

from queryablecollections.q_iterable import query


def test_iterable_can_re_iterate() -> None:
    myquery = query([1, 2, 3]).select(lambda x: x)

    assert myquery.to_list() == [1, 2, 3]
    assert myquery.to_list() == [1, 2, 3]





