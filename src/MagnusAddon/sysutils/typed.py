from __future__ import annotations

from typing import Any, TypeVar, cast, get_origin

from beartype.door import is_bearable


def str_(value: Any) -> str: return checked_cast(str, value)  # noqa: ANN401
def int_(value: Any) -> int: return checked_cast(int, value)  # noqa: ANN401
def float_(value: Any) -> float: return checked_cast(float, value)  # noqa: ANN401
def bool_(value: Any) -> bool: return checked_cast(bool, value)  # noqa: ANN401

CastT = TypeVar("CastT")

def checked_cast(cls: type[CastT], instance: object) -> CastT:
    """ Runtime-check an object for simple built in types and return it cast as such """
    if not isinstance(instance, cls):
        raise TypeError(f"{repr(instance)}: expected {cls.__name__}, not {instance.__class__.__name__}")
    return instance

def checked_cast_generics(cls: type[CastT], instance: object) -> CastT:
    """ Runtime-check an object for a specific generic type and return it cast as such """
    if not is_bearable(instance, cls):
        msg = f"{repr(instance)}: expected {cls.__name__}, not {instance.__class__.__name__}"
        raise TypeError(msg)

    return cast(CastT, instance)

def _is_compatible_with_isinstance(cls: type[CastT]) -> bool:
    return cls.__module__ == "builtins" and get_origin(cls) is None

def checked_cast_dynamic(cls: type[CastT], instance: object) -> CastT:
    """ Runtime-check an object for a specific type and return it cast as such """
    return checked_cast(cls, instance) if _is_compatible_with_isinstance(cls) else checked_cast_generics(cls, instance)

def non_optional(instance:CastT | None) -> CastT:
    if instance is None: raise AssertionError()
    return instance

def try_cast(cls: type[CastT], instance: object) -> CastT | None:
    return instance if isinstance(instance, cls) else None
