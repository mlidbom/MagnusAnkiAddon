from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from queryablecollections._private_implementation_details.type_aliases import Selector
    from queryablecollections.q_iterable import QIterable

def pipe[TItem, TReturn](self: QIterable[TItem],
                         action: Selector[QIterable[TItem], TReturn]) -> TReturn:
    return action(self)
