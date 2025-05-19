from __future__ import annotations


def that(condition: bool, message: str = "assertion failed") -> None:
    if not condition: raise AssertionError(message)

def equal(value: object, expected:object, message: str = "assertion failed") -> None:
    that(value == expected, message)