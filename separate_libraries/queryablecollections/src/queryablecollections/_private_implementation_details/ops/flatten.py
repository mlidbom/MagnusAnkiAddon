from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

def flatten[T](self: Iterable[Iterable[T]]) -> Iterable[T]:
    return itertools.chain.from_iterable(self)
