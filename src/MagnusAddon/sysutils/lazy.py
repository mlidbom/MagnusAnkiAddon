from typing import Callable, Generic, TypeVar, Optional

T = TypeVar('T')

class Lazy(Generic[T]):
    def __init__(self, factory: Callable[[], T]):
        self.factory = factory
        self._instance: Optional[T] = None

    def instance(self) -> T:
        if self._instance is None:
            self._instance = self.factory()
        return self._instance
