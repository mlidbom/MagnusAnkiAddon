from __future__ import annotations

import line_profiling_hacks
from manually_copied_in_libraries.autoslot import Slots, SlotsPlusDict

# when running line profiling we have to have __dict__ in our classes, when not running line profiling we do not want that overhead
if line_profiling_hacks.is_running_line_profiling:
    class AutoSlots(SlotsPlusDict):  # pyright: ignore [reportRedeclaration]
        pass
else:
    class AutoSlots(Slots):
        pass
