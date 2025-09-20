from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.type_aliases import Func

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections.collections.q_frozen_set import QFrozenSet
    from queryablecollections.collections.q_list import QList
    from queryablecollections.collections.q_sequence import QSequence
    from queryablecollections.collections.q_set import QSet
    from queryablecollections.q_cast import QCast
    from queryablecollections.q_iterable import QIterable
    from queryablecollections.q_ordered_iterable import QOrderedIterable

class ZeroImportOverheadCollectionConstructors:

    @staticmethod
    def qlist[TItem](iterable: Iterable[TItem]) -> QList[TItem]:
        from queryablecollections.collections.q_list import QList
        ZeroImportOverheadCollectionConstructors.qlist = QList  # replace this method with a direct call so that future calls have zero import overhead
        return ZeroImportOverheadCollectionConstructors.qlist(iterable)  # use the new version to prove from the very first call that it works

    @staticmethod
    def qsequence[TItem](iterable: Iterable[TItem]) -> QSequence[TItem]:
        from queryablecollections.collections.q_sequence import QImmutableSequence
        ZeroImportOverheadCollectionConstructors.qimmutablesequence = QImmutableSequence  # replace this method with a direct call so that future calls have zero import overhead
        return ZeroImportOverheadCollectionConstructors.qlist(iterable)  # use the new version to prove from the very first call that it works

    @staticmethod
    def qset[TItem](iterable: Iterable[TItem]) -> QSet[TItem]:
        from queryablecollections.collections.q_set import QSet
        ZeroImportOverheadCollectionConstructors.qset = QSet  # replace this method with a direct call so that future calls have zero import overhead
        return ZeroImportOverheadCollectionConstructors.qset(iterable)  # use the new version to prove from the very first call that it works

    @staticmethod
    def qfrozenset[TItem](iterable: Iterable[TItem]) -> QFrozenSet[TItem]:
        from queryablecollections.collections.q_frozen_set import QFrozenSet
        ZeroImportOverheadCollectionConstructors.qfrozenset = QFrozenSet  # replace this method with a direct call so that future calls have zero import overhead
        return ZeroImportOverheadCollectionConstructors.qfrozenset(iterable)  # use the new version to prove from the very first call that it works

    @staticmethod
    def qcast[TItem](qiterable: QIterable[TItem]) -> QCast[TItem]:
        from queryablecollections.q_cast import QCast
        ZeroImportOverheadCollectionConstructors.qcast = QCast  # replace this method with a direct call so that future calls have zero import overhead  # pyright: ignore [reportAttributeAccessIssue]
        return ZeroImportOverheadCollectionConstructors.qcast(qiterable)  # use the new version to prove from the very first call that it works

    @staticmethod
    def qiterable[TItem](qiterable: Iterable[TItem]) -> QIterable[TItem]:
        from queryablecollections.q_iterable import QiterableImplementation
        ZeroImportOverheadCollectionConstructors.qiterable = QiterableImplementation  # replace this method with a direct call so that future calls have zero import overhead  # pyright: ignore [reportAttributeAccessIssue]
        return ZeroImportOverheadCollectionConstructors.qiterable(qiterable)  # use the new version to prove from the very first call that it works

    @staticmethod
    def qlazyiterable[TItem](iterable_factory: Func[Iterable[TItem]]) -> QIterable[TItem]:
        from queryablecollections.q_iterable import QLazyiterable
        ZeroImportOverheadCollectionConstructors.qlazyiterable = QLazyiterable  # replace this method with a direct call so that future calls have zero import overhead  # pyright: ignore [reportAttributeAccessIssue]
        return ZeroImportOverheadCollectionConstructors.qlazyiterable(iterable_factory)  # use the new version to prove from the very first call that it works

    @staticmethod
    def qordered_iterable[TItem](qiterable: Iterable[TItem]) -> QOrderedIterable[TItem]:
        from queryablecollections.q_iterable import QOrderedIterable
        ZeroImportOverheadCollectionConstructors.qordered_iterable = QOrderedIterable  # replace this method with a direct call so that future calls have zero import overhead  # pyright: ignore [reportAttributeAccessIssue]
        return ZeroImportOverheadCollectionConstructors.qordered_iterable(qiterable)  # use the new version to prove from the very first call that it works
