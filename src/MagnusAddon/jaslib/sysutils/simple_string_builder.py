from __future__ import annotations

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jaslib.sysutils.simple_string_list_builder import SimpleStringListBuilder


class SimpleStringBuilder(Slots):
    def __init__(self, auto_separator: str = "") -> None:
        self._builder: SimpleStringListBuilder = SimpleStringListBuilder()
        self.auto_separator: str = auto_separator

    def append(self, text: str) -> SimpleStringBuilder:
        return self.append_if(True, text)

    def append_if(self, condition: bool, text: str) -> SimpleStringBuilder:
        self._builder.append_if(condition, text)
        return self

    def build(self) -> str:
        return self.auto_separator.join(self._builder.value)
