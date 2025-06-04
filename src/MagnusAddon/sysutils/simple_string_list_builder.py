from __future__ import annotations


class SimpleStringListBuilder:
    def __init__(self) -> None:
        self.value: list[str] = []

    def append(self, text: str) -> SimpleStringListBuilder:
        return self.append_if(True, text)

    def append_if(self, condition: bool, text: str) -> SimpleStringListBuilder:
        if condition: self.value.append(text)
        return self

    def as_set(self) -> set[str]: return set(self.value)

    def concat(self, values: list[str]) -> SimpleStringListBuilder:
        self.value.extend(values)
        return self

    def concat_set(self, values: set[str]) -> SimpleStringListBuilder:
        return self.concat(list(values))
