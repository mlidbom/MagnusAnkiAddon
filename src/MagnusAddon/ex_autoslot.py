from __future__ import annotations

from abc import ABCMeta

from manually_copied_in_libraries.autoslot import SlotsPlusDict, SlotsPlusDictMeta


# todo prorably add some code here to only use PlusDict when profiling and save us that overhead when not profiling, like ProfilableAutoSlots = SlotsPlusDict if os.environ.get('LINE_PROFILE') else Slots
class ProfilableAutoSlots(SlotsPlusDict):
    pass

class SlotsPlusDictABC(ABCMeta, SlotsPlusDictMeta):
    pass

class ProfilableAutoSlotsABC(metaclass=SlotsPlusDictABC):
    pass