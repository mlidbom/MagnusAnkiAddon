from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sysutils.standard_type_aliases import Predicate, Selector

def assert_each[TItem](self: Iterable[TItem], predicate: Predicate[TItem], message: str | Selector[TItem, str] | None = None) -> None:
    for item in self:
        actual_message = message if isinstance(message, str) else message(item) if message is not None else ""
        if not predicate(item): raise AssertionError(actual_message)