from __future__ import annotations

from manually_copied_in_libraries.autoslot import Slots

_frequency_maximum = {f"nf{num:02}" for num in range(1, 10)}
_frequency_high = {f"nf{num}" for num in range(11, 20)}
_frequency_medium = {f"nf{num}" for num in range(21, 40)}
_frequency_low = {f"nf{num}" for num in range(41, 60)}

_tags_maximum = {"ichi1"}
_tags_high = {"news1", "spec1"}
_tags_medium = {"news2", "spec2"}

class PrioritySpec(Slots):
    def __init__(self, tags: set[str]) -> None:
        self.tags: set[str] = tags

        if self.tags & _tags_maximum:
            self.priority_string: str = "priority_maximum"
            self.priority: int = 1
        elif self.tags & _tags_high:
            self.priority_string = "priority_high"
            self.priority = 11
        elif self.tags & _tags_medium:
            self.priority_string = "priority_medium"
            self.priority = 21
        elif self.tags & _frequency_maximum:
            self.priority_string = "priority_maximum"
            self.priority = int(list(self.tags & _frequency_maximum)[0][-1])  # the actual number from the nf tag
        elif self.tags & _frequency_high:
            self.priority_string = "priority_high"
            self.priority = int(list(self.tags & _frequency_high)[0][-2:])  # the actual number from the nf tag
        elif self.tags & _frequency_medium:
            self.priority_string = "priority_medium"
            self.priority = int(list(self.tags & _frequency_high)[0][-2:])  # the actual number from the nf tag
        elif self.tags & _frequency_low:
            self.priority_string = "priority_low"
            self.priority = int(list(self.tags & _frequency_high)[0][-2:])  # the actual number from the nf tag
        else:
            self.priority_string = "priority_low"
            self.priority = 50
