from __future__ import annotations

from typing import TypeVar

TProp: TypeVar = TypeVar("TProp")

class PropertyTypeError(TypeError):
    def __init__(self, prop: str, prop_type: type[TProp]) -> None:
        message = f"Property '{prop}' is not of type '{prop_type.__name__}'"
        super().__init__(message)
