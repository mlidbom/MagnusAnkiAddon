import collections
from typing import Any, Callable, Generic, TypeVar

VT = TypeVar('VT')  # Value type

class DefaultDictCaseInsensitive(collections.defaultdict[str, VT], Generic[VT]):
    def __init__(self, default_factory: Callable[[], VT], **kwargs: Any):
        super().__init__(default_factory, **{key.lower(): value for key, value in kwargs.items()})

    def __getitem__(self, key: str) -> VT:
        return super().__getitem__(key.lower())

    def __setitem__(self, key: str, value: VT) -> None:
        super().__setitem__(key.lower(), value)

    def __contains__(self, key: Any) -> bool:
        return super().__contains__(key.lower())