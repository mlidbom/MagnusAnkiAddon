from _weakref import ReferenceType
from typing import TypeVar, Generic, Optional
import weakref

from sysutils.typed import non_optional

T = TypeVar('T')

class WeakRef(Generic[T]):
    def __init__(self, obj: T):
        self._ref: ReferenceType[T] = weakref.ref(obj)

    @property
    def instance(self) -> T: return non_optional(self._ref())
    def __call__(self) -> Optional[T]: return non_optional(self._ref())

    def __repr__(self) -> str: return f"WeakRef: {self.instance.__repr__()}"
