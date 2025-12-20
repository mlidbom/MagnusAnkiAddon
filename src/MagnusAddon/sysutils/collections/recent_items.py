from __future__ import annotations

from collections import deque

from manually_copied_in_libraries.autoslot import Slots


class RecentItems[T](Slots):
    def __init__(self, max_size: int) -> None:
        self.items: deque[T] = deque(maxlen=max_size)
        self.max_size: int = max_size

    def is_recent(self, item: T) -> bool:
        seen = item in self.items
        if not seen: self.items.append(item)
        return seen
