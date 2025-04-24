from __future__ import annotations
from beartype.door import is_bearable
from typing import Any, Optional, TypeVar, get_origin

def str_(value: Any) -> str: return checked_cast(str, value)
def int_(value: Any) -> int: return checked_cast(int, value)
def float_(value: Any) -> float: return checked_cast(float, value)
def bool_(value: Any) -> bool: return checked_cast(bool, value)

CastT = TypeVar('CastT')

def checked_cast(cls: type[CastT], instance: object) -> CastT:
    """ Runtime-check an object for simple built in types and return it cast as such """
    if not isinstance(instance, cls):
        raise TypeError(f"{repr(instance)}: expected {cls.__name__}, not {instance.__class__.__name__}")
    return instance

def checked_cast_generics(cls: type[CastT], instance: object) -> CastT:
    """ Runtime-check an object for a specific type and return it cast as such """
    if not is_bearable(instance, cls):
        msg = f"{repr(instance)}: expected {cls.__name__}, not {instance.__class__.__name__}"
        raise TypeError(msg)

    return instance

def _is_compatible_with_isinstance(cls: type[CastT]) -> bool:
    return cls.__module__ == 'builtins' and get_origin(cls) is None

def checked_cast_dynamic(cls: type[CastT], instance: object) -> CastT:
    """ Runtime-check an object for a specific type and return it cast as such """
    return checked_cast(cls, instance) if _is_compatible_with_isinstance(cls) else checked_cast_generics(cls, instance)

def non_optional(instance:Optional[CastT]) -> CastT:
    if instance is None: raise AssertionError()
    return instance
