from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots

if TYPE_CHECKING:
    from collections.abc import Iterator

class BitFlagsSet(Slots):
    def __init__(self, bitfield: int = 0) -> None:
        self._bitfield: int = bitfield

    def has(self, flag: int) -> bool:
        return bool(self._bitfield & (1 << flag))

    def set_flag(self, flag: int) -> None:
        self._bitfield |= (1 << flag)

    def unset_flag(self, flag: int) -> None:
        self._bitfield &= ~(1 << flag)

    def all_flags(self) -> Iterator[int]:
        bitfield = self._bitfield
        bit_pos = 0
        while bitfield:
            if bitfield & 1:
                yield bit_pos
            bitfield >>= 1
            bit_pos += 1

    def count(self) -> int:
        return self._bitfield.bit_count()

    def is_empty(self) -> bool:
        return self._bitfield == 0

    @property
    def bitfield(self) -> int:
        return self._bitfield
