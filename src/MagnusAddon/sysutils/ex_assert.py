from __future__ import annotations

from typing import Any


def that(condition: bool, message: str = "assertion failed") -> None:
    if not condition: raise AssertionError(message)

def equal(value: object, expected:object, message: str = "assertion failed") -> None:
    that(value == expected, message)

def not_none(value:Any, message:str = "") -> None:  # noqa: ANN401
    if not value: raise AssertionError(message)