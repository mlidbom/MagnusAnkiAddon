from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from queryablecollections._private_implementation_details.type_aliases import Action1
    from queryablecollections.q_iterable import QIterable


def for_each[TItem](self: QIterable[TItem], action: Action1[TItem]) -> QIterable[TItem]:
    for item in self: action(item)
    return self
