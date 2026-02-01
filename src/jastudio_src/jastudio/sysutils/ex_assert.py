from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def that(condition: bool, message: str | Callable[[], str] = "assertion failed") -> None:
    if not condition:
        if callable(message): message = message()
        raise AssertionError(message)

def equal(value: object, expected: object, message: str = "assertion failed") -> None:
    that(value == expected, message)

def not_none(value: object, message: str = "") -> None:  # noqa: ANN401
    if not value: raise AssertionError(message)
