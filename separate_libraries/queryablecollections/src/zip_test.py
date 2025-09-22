from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


class QIter[T]:
    def zip[T2, TOut](self, second: QIter[T2], select: Callable[[T, T2], TOut]) -> QIter[TOut]:...
    def zip2[T2, T3, TOut](self, second: QIter[T2], third: QIter[T3], select: Callable[[T, T2, T3], TOut]) -> QIter[TOut]: ...
    def zip3[T2, T3, T4, TOut](self, second: QIter[T2], third: QIter[T3], fourth: QIter[T4], select: Callable[[T, T2, T3, T4], TOut]) -> QIter[TOut]: ...