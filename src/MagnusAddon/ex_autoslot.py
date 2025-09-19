from __future__ import annotations

from abc import ABCMeta

from ankiutils import app
from manually_copied_in_libraries.autoslot import Slots, SlotsMeta, SlotsPlusDict, SlotsPlusDictMeta


class SlotsABCMeta(ABCMeta, SlotsMeta):
    pass

class SlotsPlusDictABCMeta(ABCMeta, SlotsPlusDictMeta):  # pyright: ignore [reportRedeclaration]
    pass

# when running line profiling we have to have __dict__ in our classes, when not running line profiling we do not want that overhead
if app.is_running_line_profiling:
    class AutoSlots(SlotsPlusDict):  # pyright: ignore [reportRedeclaration]
        pass

    class AutoSlotsABC(metaclass=SlotsPlusDictABCMeta):  # pyright: ignore [reportRedeclaration]
        pass
else:
    class AutoSlots(Slots):
        pass

    class AutoSlotsABC(metaclass=SlotsABCMeta):
        pass