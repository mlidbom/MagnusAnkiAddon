from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from sysutils.collections.linq.l_iterable import query

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sysutils.collections.linq.l_iterable import LIterable

class LQuery:
    @staticmethod
    def flatten[TChildItem](iterable: Iterable[Iterable[TChildItem]]) -> LIterable[TChildItem]:
        return query(itertools.chain.from_iterable(iterable))

    # endregion


# alises for those that want or need the ultimate in brevity
LQ = LQuery
Q = LQuery