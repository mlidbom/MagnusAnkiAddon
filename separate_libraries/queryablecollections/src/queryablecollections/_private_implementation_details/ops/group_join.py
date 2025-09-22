from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from queryablecollections._private_implementation_details.type_aliases import Selector

def group_join[TOuter, TInner, TKey, TResult](
        self: Iterable[TOuter],
        other: Iterable[TInner],
        self_key: Selector[TOuter, TKey],
        group_key: Selector[TInner, TKey],
        select: Callable[[TOuter, Iterable[TInner]], TResult]
) -> Iterable[TResult]:
    groups_by_key: dict[TKey, list[TInner]] = {}
    for other_item in other:
        key = group_key(other_item)
        if key not in groups_by_key:
            groups_by_key[key] = []
        groups_by_key[key].append(other_item)

    for self_item in self:
        self_key_value = self_key(self_item)
        yield select(self_item, groups_by_key.get(self_key_value, []))
