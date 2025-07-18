from __future__ import annotations


class SkipFalsyValuesDebugReprBuilder:
    def __init__(self) -> None:
        self.repr = ""

    def flag(self, name: str, value: bool) -> SkipFalsyValuesDebugReprBuilder:
        self.repr += f"{name} " if value else ""
        return self

    def include(self, value: object) -> SkipFalsyValuesDebugReprBuilder:
        self.repr += value.__repr__() + " | "
        return self

    def prop(self, name: str, value: object) -> SkipFalsyValuesDebugReprBuilder:
        self.repr += f"{name}: {value} " if value else ""
        return self
