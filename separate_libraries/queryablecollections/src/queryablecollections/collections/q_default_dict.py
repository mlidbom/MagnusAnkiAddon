from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, override

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C
from queryablecollections.collections.q_key_value_pair import KeyValuePair
from queryablecollections.q_iterable import QIterable

if TYPE_CHECKING:
    from queryablecollections._private_implementation_details.type_aliases import Func


class QDefaultDict[TKey, TItem](defaultdict[TKey, TItem], QIterable[TKey]):
    __slots__: tuple[str, ...] = ()
    def __init__(self, factory: Func[TItem]) -> None:
        super().__init__(factory)

    def qitems(self) -> QIterable[KeyValuePair[TKey, TItem]]: return C.lazy_iterable(lambda: self.items()).select(KeyValuePair)

    @override
    def _optimized_length(self) -> int: return len(self)
