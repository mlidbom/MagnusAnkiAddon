from __future__ import annotations

from abc import ABCMeta

from queryablecollections.included_libraries.autoslot import SlotsMeta


class SlotsABCMeta(ABCMeta, SlotsMeta):
    pass

class SlotsABC(metaclass=SlotsABCMeta):
    pass
