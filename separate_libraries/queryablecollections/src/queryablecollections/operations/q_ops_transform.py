from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections.type_aliases import Selector

concat = itertools.chain
select = map
flatten = itertools.chain.from_iterable


def select_many[TItem, TSubItem](self: Iterable[TItem], selector: Selector[TItem, Iterable[TSubItem]]) -> Iterable[TSubItem]:
    return flatten(select(selector, self))