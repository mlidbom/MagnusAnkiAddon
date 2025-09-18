from __future__ import annotations

from abc import ABCMeta

from ankiutils import app
from manually_copied_in_libraries.autoslot import Slots, SlotsMeta, SlotsPlusDict, SlotsPlusDictMeta

# when running line profiling we have to have __dict__ in our classes, when not running line profiling we do not want that overhead
if app.is_running_line_profiling:
    class AutoSlots(SlotsPlusDict):  # pyright: ignore [reportRedeclaration]
        pass

    class SlotsPlusDictABC(ABCMeta, SlotsPlusDictMeta):  # pyright: ignore [reportRedeclaration]
        pass

    class AutoSlotsABC(metaclass=SlotsPlusDictABC):  # pyright: ignore [reportRedeclaration]
        pass
else:
    class AutoSlots(Slots):
        pass

    class SlotsABC(ABCMeta, SlotsMeta):
        pass

    class AutoSlotsABC(metaclass=SlotsABC):
        pass