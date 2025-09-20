from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections._private_implementation_details.type_aliases import Func
    from queryablecollections.collections.q_frozen_set import QFrozenSet
    from queryablecollections.collections.q_list import QList
    from queryablecollections.collections.q_sequence import QSequence
    from queryablecollections.collections.q_set import QSet
    from queryablecollections.q_cast import QCast
    from queryablecollections.q_iterable import QIterable
    from queryablecollections.q_ordered_iterable import QOrderedIterable

class ZeroImportOverheadCollectionConstructors:

    @staticmethod
    def list[TItem](iterable: Iterable[TItem]) -> QList[TItem]:
        from queryablecollections.collections.q_list import QList
        ZeroImportOverheadCollectionConstructors.list = QList  # replace this method with a direct call so that future calls have zero import overhead
        return ZeroImportOverheadCollectionConstructors.list(iterable)  # use the new version to prove from the very first call that it works

    @staticmethod
    def sequence[TItem](iterable: Iterable[TItem]) -> QSequence[TItem]:
        from queryablecollections.collections.q_sequence import QImmutableSequence
        ZeroImportOverheadCollectionConstructors.qimmutablesequence = QImmutableSequence  # replace this method with a direct call so that future calls have zero import overhead
        return ZeroImportOverheadCollectionConstructors.list(iterable)  # use the new version to prove from the very first call that it works

    @staticmethod
    def set[TItem](iterable: Iterable[TItem]) -> QSet[TItem]:
        from queryablecollections.collections.q_set import QSet
        ZeroImportOverheadCollectionConstructors.set = QSet  # replace this method with a direct call so that future calls have zero import overhead
        return ZeroImportOverheadCollectionConstructors.set(iterable)  # use the new version to prove from the very first call that it works

    @staticmethod
    def frozen_set[TItem](iterable: Iterable[TItem]) -> QFrozenSet[TItem]:
        from queryablecollections.collections.q_frozen_set import QFrozenSet
        ZeroImportOverheadCollectionConstructors.frozen_set = QFrozenSet  # replace this method with a direct call so that future calls have zero import overhead
        return ZeroImportOverheadCollectionConstructors.frozen_set(iterable)  # use the new version to prove from the very first call that it works

    @staticmethod
    def cast[TItem](qiterable: QIterable[TItem]) -> QCast[TItem]:
        from queryablecollections.q_cast import QCast
        ZeroImportOverheadCollectionConstructors.cast = QCast  # replace this method with a direct call so that future calls have zero import overhead  # pyright: ignore [reportAttributeAccessIssue]
        return ZeroImportOverheadCollectionConstructors.cast(qiterable)  # use the new version to prove from the very first call that it works

    @staticmethod
    def iterable[TItem](qiterable: Iterable[TItem]) -> QIterable[TItem]:
        from queryablecollections._private_implementation_details.q_iterable_implementation import QiterableImplementation
        ZeroImportOverheadCollectionConstructors.iterable = QiterableImplementation  # replace this method with a direct call so that future calls have zero import overhead  # pyright: ignore [reportAttributeAccessIssue]
        return ZeroImportOverheadCollectionConstructors.iterable(qiterable)  # use the new version to prove from the very first call that it works

    @staticmethod
    def empty_iterable[TItem]() -> QIterable[TItem]:  # pyright: ignore [reportInvalidTypeVarUse]
        empty_iterable = ZeroImportOverheadCollectionConstructors.iterable(())
        def get_empty() -> QIterable[TItem]: return empty_iterable  # pyright: ignore [reportReturnType]
        ZeroImportOverheadCollectionConstructors.empty_iterable = get_empty  # replace this method itself with  # pyright: ignore [reportAttributeAccessIssue]
        return ZeroImportOverheadCollectionConstructors.empty_iterable()

    @staticmethod
    def lazy_iterable[TItem](iterable_factory: Func[Iterable[TItem]]) -> QIterable[TItem]:
        from queryablecollections._private_implementation_details.q_lazy_iterable import QLazyiterable
        ZeroImportOverheadCollectionConstructors.lazy_iterable = QLazyiterable  # replace this method with a direct call so that future calls have zero import overhead  # pyright: ignore [reportAttributeAccessIssue]
        return ZeroImportOverheadCollectionConstructors.lazy_iterable(iterable_factory)  # use the new version to prove from the very first call that it works

    @staticmethod
    def ordered_iterable[TItem](qiterable: Iterable[TItem]) -> QOrderedIterable[TItem]:
        from queryablecollections.q_iterable import QOrderedIterable
        ZeroImportOverheadCollectionConstructors.ordered_iterable = QOrderedIterable  # replace this method with a direct call so that future calls have zero import overhead  # pyright: ignore [reportAttributeAccessIssue]
        return ZeroImportOverheadCollectionConstructors.ordered_iterable(qiterable)  # use the new version to prove from the very first call that it works
