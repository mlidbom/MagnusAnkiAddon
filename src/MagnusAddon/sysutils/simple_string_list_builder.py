from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots

if TYPE_CHECKING:
    from collections.abc import Callable


class SimpleStringListBuilder(Slots):
    def __init__(self) -> None:
        self.value: list[str] = []

    def append(self, text: str) -> SimpleStringListBuilder:
        return self.append_if(True, text)

    def append_if(self, condition: bool, text: str) -> SimpleStringListBuilder:
        if condition: self.value.append(text)
        return self

    def append_if_lambda(self, condition: bool, text: Callable[[], str]) -> SimpleStringListBuilder:
        if condition: self.value.append(text())
        return self

    def as_set(self) -> set[str]: return set(self.value)

    def concat(self, values: list[str]) -> SimpleStringListBuilder:
        self.value.extend(values)
        return self