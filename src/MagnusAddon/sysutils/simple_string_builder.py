from __future__ import annotations

from sysutils.simple_string_list_builder import SimpleStringListBuilder


class SimpleStringBuilder:
    def __init__(self, auto_separator: str = "") -> None:
        self._builder = SimpleStringListBuilder()
        self.auto_separator = auto_separator

    def append(self, text: str) -> SimpleStringBuilder:
        return self.append_if(text, True)

    def append_if(self, text: str, condition: bool) -> SimpleStringBuilder:
        self._builder.append_if(text, condition)
        return self

    def build(self) -> str:
        return self.auto_separator.join(self._builder.value)
