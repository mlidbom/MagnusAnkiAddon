from __future__ import annotations

from typing_extensions import Any


def not_none(value:Any, message:str = "") -> None:  # noqa: ANN401
    if not value: raise AssertionError(message)