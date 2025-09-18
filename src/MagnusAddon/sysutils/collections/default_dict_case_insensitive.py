from __future__ import annotations

import collections
from typing import TYPE_CHECKING, override

from ex_autoslot import ProfilableAutoSlots
from sysutils import typed

if TYPE_CHECKING:
    from sysutils.standard_type_aliases import Func
    pass

class DefaultDictCaseInsensitive[VT](collections.defaultdict[str, VT], ProfilableAutoSlots):
    def __init__(self, default_factory: Func[VT], **kwargs: object) -> None:
        super().__init__(default_factory, **{key.lower(): value for key, value in kwargs.items()})

    @override
    def __getitem__(self, key: str) -> VT:
        return super().__getitem__(key.lower())

    @override
    def __setitem__(self, key: str, value: VT) -> None:
        super().__setitem__(key.lower(), value)

    @override
    def __contains__(self, key: object) -> bool:
        return super().__contains__(typed.str_(key).lower())