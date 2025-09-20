from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections.q_errors import EmptyIterableError

if TYPE_CHECKING:
    from queryablecollections._private_implementation_details.type_aliases import Predicate, Selector
    from queryablecollections.q_iterable import QIterable

def each_element[TItem](self: QIterable[TItem], predicate: Predicate[TItem], message: str | Selector[TItem, str] | None = None) -> QIterable[TItem]:
    for item in self:
        actual_message = message if isinstance(message, str) else message(item) if message is not None else ""
        if not predicate(item): raise AssertionError(actual_message)
    return self

def collection[TItem](self: QIterable[TItem], predicate: Predicate[QIterable[TItem]], message: str | None = None) -> QIterable[TItem]:
    if not predicate(self): raise AssertionError(message)
    return self

def not_empty[TItem](self: QIterable[TItem]) -> QIterable[TItem]:
    if self.none(): raise EmptyIterableError()
    return self
