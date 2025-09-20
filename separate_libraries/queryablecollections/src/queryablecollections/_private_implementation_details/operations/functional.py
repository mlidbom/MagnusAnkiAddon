from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from queryablecollections._private_implementation_details.type_aliases import Action1, Selector
    from queryablecollections.q_iterable import QIterable

def for_each[TItem](self: QIterable[TItem], action: Action1[TItem]) -> QIterable[TItem]:
    for item in self: action(item)
    return self

def for_single[TItem](self: QIterable[TItem], action: Selector[TItem, Any]) -> QIterable[TItem]:  # pyright: ignore[reportExplicitAny]
    action(self.single())
    return self

def for_single_or_none[TItem](self: QIterable[TItem], action: Selector[TItem, Any]) -> QIterable[TItem]:  # pyright: ignore[reportExplicitAny]
    value = self.single_or_none()
    if value is not None: action(value)
    return self

def pipe_to[TItem, TReturn](self: QIterable[TItem], action: Selector[QIterable[TItem], TReturn]) -> TReturn:
    return action(self)
