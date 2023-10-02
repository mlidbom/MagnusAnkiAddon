from __future__ import annotations

from typing import Any, TypeVar


def str_(value: Any) -> str: return checked_cast(str, value)
def int_(value: Any) -> int: return checked_cast(int, value)

CastT = TypeVar('CastT')
def checked_cast(cls: type[CastT], var: object) -> CastT:
    """
    Runtime-check an object for a specific type and return it cast as such
    """
    if not isinstance(var, cls):
        msg = f"{var}: expected {cls.__name__}, not {var.__class__.__name__}"
        raise TypeError(msg)
    return var