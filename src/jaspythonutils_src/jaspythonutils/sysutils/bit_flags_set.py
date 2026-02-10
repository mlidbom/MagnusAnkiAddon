# from __future__ import annotations
#
# from typing import TYPE_CHECKING, override
#
# from typed_linq_collections.q_iterable import QIterable
#
# if TYPE_CHECKING:
#     from collections.abc import Iterator
#
# class BitFlagsSet(QIterable[int]):
#     __slots__: tuple[str, ...] = ("_bitfield",)
#
#     def __init__(self, bitfield: int = 0) -> None:
#         self._bitfield: int = bitfield
#
#     @override
#     def contains(self, value: int) -> bool:
#         return (self._bitfield & (1 << value)) != 0
#
#     def contains_bit(self, value: int) -> bool:
#         return (self._bitfield & value) != 0
#
#     def set_flag(self, flag: int) -> None:
#         self._bitfield |= (1 << flag)
#
#     def unset_flag(self, flag: int) -> None:
#         self._bitfield &= ~(1 << flag)
#
#     @override
#     def __iter__(self) -> Iterator[int]:
#         bitfield = self._bitfield
#         flag = 0
#         while bitfield:
#             if bitfield & 1:
#                 yield flag
#             bitfield >>= 1
#             flag += 1
#
#     @override
#     def __hash__(self) -> int:
#         return self._bitfield
#
#     @override
#     def __eq__(self, other: object) -> bool:
#         if isinstance(other, BitFlagsSet):
#             return self._bitfield == other._bitfield
#         return False
