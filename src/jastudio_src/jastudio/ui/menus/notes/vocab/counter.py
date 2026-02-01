from __future__ import annotations

from autoslot import Slots


class Counter(Slots):
    def __init__(self, start_number: int) -> None:
        self.count: int = start_number

    def increment(self) -> int:
        self.count += 1
        return self.count
