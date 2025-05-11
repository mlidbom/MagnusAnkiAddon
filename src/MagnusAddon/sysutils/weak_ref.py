import weakref
from typing import TYPE_CHECKING, Generic, Optional, TypeVar

from sysutils.typed import non_optional

if TYPE_CHECKING:
    from _weakref import ReferenceType

T = TypeVar('T')

class WeakRef(Generic[T]):
    def __init__(self, obj: T) -> None:
        self._weakreference: ReferenceType[T] = weakref.ref(obj)

    @property
    def instance(self) -> T: return non_optional(self._weakreference())
    def __call__(self) -> Optional[T]: return non_optional(self._weakreference())

    def __repr__(self) -> str: return f"WeakRef: {self.instance.__repr__()}"
