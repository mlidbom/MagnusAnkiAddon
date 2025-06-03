from __future__ import annotations


class SimpleStringListBuilder:
    def __init__(self) -> None:
        self.value:list[str] = []

    def append_if(self, text: str, condition: bool) -> SimpleStringListBuilder:
        if condition: self.value.append(text)
        return self

    def as_set(self) -> set[str]: return set(self.value)
