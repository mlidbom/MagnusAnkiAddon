from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from queryablecollections.q_iterable import query

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections.q_iterable import QIterable

class Query:
    @staticmethod
    def flatten[TChildItem](iterable: Iterable[Iterable[TChildItem]]) -> QIterable[TChildItem]:
        return query(itertools.chain.from_iterable(iterable))

    # endregion


# alises for those that want or need the ultimate in brevity
Q = Query