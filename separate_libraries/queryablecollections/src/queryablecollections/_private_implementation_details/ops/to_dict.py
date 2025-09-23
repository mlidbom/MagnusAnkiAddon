from __future__ import annotations

from typing import TYPE_CHECKING

# noinspection PyPep8Naming
from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from queryablecollections._private_implementation_details.type_aliases import Selector
    from queryablecollections.collections.q_dict import QDict
    from queryablecollections.q_iterable import QIterable


def to_dict[T, TKey, TValue](self: QIterable[T], key_selector: Selector[T, TKey], value_selector: Selector[T, TValue]) -> QDict[TKey, TValue]:
    return C.dict((key_selector(item), value_selector(item)) for item in self)
