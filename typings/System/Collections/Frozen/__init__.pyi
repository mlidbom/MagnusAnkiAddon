import typing, clr, abc
from System.Collections.Generic import IReadOnlySet_1, ISet_1, IEqualityComparer_1, IEnumerable_1, IEnumerator_1
from System.Collections import ICollection
from System.Collections.Immutable import ImmutableArray_1
from System import Span_1, Array_1

class FrozenSet_GenericClasses(abc.ABCMeta):
    Generic_FrozenSet_GenericClasses_FrozenSet_1_T = typing.TypeVar('Generic_FrozenSet_GenericClasses_FrozenSet_1_T')
    def __getitem__(self, types : typing.Type[Generic_FrozenSet_GenericClasses_FrozenSet_1_T]) -> typing.Type[FrozenSet_1[Generic_FrozenSet_GenericClasses_FrozenSet_1_T]]: ...

FrozenSet : FrozenSet_GenericClasses

FrozenSet_1_T = typing.TypeVar('FrozenSet_1_T')
class FrozenSet_1(typing.Generic[FrozenSet_1_T], IReadOnlySet_1[FrozenSet_1_T], ISet_1[FrozenSet_1_T], ICollection, abc.ABC):
    @property
    def Comparer(self) -> IEqualityComparer_1[FrozenSet_1_T]: ...
    @property
    def Count(self) -> int: ...
    @classmethod
    @property
    def Empty(cls) -> FrozenSet_1[FrozenSet_1_T]: ...
    @property
    def Items(self) -> ImmutableArray_1[FrozenSet_1_T]: ...
    def Contains(self, item: FrozenSet_1_T) -> bool: ...
    def GetEnumerator(self) -> FrozenSet_1.Enumerator_1[FrozenSet_1_T]: ...
    def IsProperSubsetOf(self, other: IEnumerable_1[FrozenSet_1_T]) -> bool: ...
    def IsProperSupersetOf(self, other: IEnumerable_1[FrozenSet_1_T]) -> bool: ...
    def IsSubsetOf(self, other: IEnumerable_1[FrozenSet_1_T]) -> bool: ...
    def IsSupersetOf(self, other: IEnumerable_1[FrozenSet_1_T]) -> bool: ...
    def Overlaps(self, other: IEnumerable_1[FrozenSet_1_T]) -> bool: ...
    def SetEquals(self, other: IEnumerable_1[FrozenSet_1_T]) -> bool: ...
    def TryGetValue(self, equalValue: FrozenSet_1_T, actualValue: clr.Reference[FrozenSet_1_T]) -> bool: ...
    # Skipped CopyTo due to it being static, abstract and generic.

    CopyTo : CopyTo_MethodGroup[FrozenSet_1_T]
    CopyTo_MethodGroup_FrozenSet_1_T = typing.TypeVar('CopyTo_MethodGroup_FrozenSet_1_T')
    class CopyTo_MethodGroup(typing.Generic[CopyTo_MethodGroup_FrozenSet_1_T]):
        CopyTo_MethodGroup_FrozenSet_1_T = FrozenSet_1.CopyTo_MethodGroup_FrozenSet_1_T
        @typing.overload
        def __call__(self, destination: Span_1[CopyTo_MethodGroup_FrozenSet_1_T]) -> None:...
        @typing.overload
        def __call__(self, destination: Array_1[CopyTo_MethodGroup_FrozenSet_1_T], destinationIndex: int) -> None:...

    # Skipped GetAlternateLookup due to it being static, abstract and generic.

    GetAlternateLookup : GetAlternateLookup_MethodGroup[FrozenSet_1_T]
    GetAlternateLookup_MethodGroup_FrozenSet_1_T = typing.TypeVar('GetAlternateLookup_MethodGroup_FrozenSet_1_T')
    class GetAlternateLookup_MethodGroup(typing.Generic[GetAlternateLookup_MethodGroup_FrozenSet_1_T]):
        GetAlternateLookup_MethodGroup_FrozenSet_1_T = FrozenSet_1.GetAlternateLookup_MethodGroup_FrozenSet_1_T
        def __getitem__(self, t:typing.Type[GetAlternateLookup_1_T1]) -> GetAlternateLookup_1[GetAlternateLookup_MethodGroup_FrozenSet_1_T, GetAlternateLookup_1_T1]: ...

        GetAlternateLookup_1_FrozenSet_1_T = typing.TypeVar('GetAlternateLookup_1_FrozenSet_1_T')
        GetAlternateLookup_1_T1 = typing.TypeVar('GetAlternateLookup_1_T1')
        class GetAlternateLookup_1(typing.Generic[GetAlternateLookup_1_FrozenSet_1_T, GetAlternateLookup_1_T1]):
            GetAlternateLookup_1_FrozenSet_1_T = FrozenSet_1.GetAlternateLookup_MethodGroup.GetAlternateLookup_1_FrozenSet_1_T
            GetAlternateLookup_1_TAlternate = FrozenSet_1.GetAlternateLookup_MethodGroup.GetAlternateLookup_1_T1
            def __call__(self) -> FrozenSet_1.AlternateLookup_2[GetAlternateLookup_1_FrozenSet_1_T, GetAlternateLookup_1_TAlternate]:...


    # Skipped TryGetAlternateLookup due to it being static, abstract and generic.

    TryGetAlternateLookup : TryGetAlternateLookup_MethodGroup[FrozenSet_1_T]
    TryGetAlternateLookup_MethodGroup_FrozenSet_1_T = typing.TypeVar('TryGetAlternateLookup_MethodGroup_FrozenSet_1_T')
    class TryGetAlternateLookup_MethodGroup(typing.Generic[TryGetAlternateLookup_MethodGroup_FrozenSet_1_T]):
        TryGetAlternateLookup_MethodGroup_FrozenSet_1_T = FrozenSet_1.TryGetAlternateLookup_MethodGroup_FrozenSet_1_T
        def __getitem__(self, t:typing.Type[TryGetAlternateLookup_1_T1]) -> TryGetAlternateLookup_1[TryGetAlternateLookup_MethodGroup_FrozenSet_1_T, TryGetAlternateLookup_1_T1]: ...

        TryGetAlternateLookup_1_FrozenSet_1_T = typing.TypeVar('TryGetAlternateLookup_1_FrozenSet_1_T')
        TryGetAlternateLookup_1_T1 = typing.TypeVar('TryGetAlternateLookup_1_T1')
        class TryGetAlternateLookup_1(typing.Generic[TryGetAlternateLookup_1_FrozenSet_1_T, TryGetAlternateLookup_1_T1]):
            TryGetAlternateLookup_1_FrozenSet_1_T = FrozenSet_1.TryGetAlternateLookup_MethodGroup.TryGetAlternateLookup_1_FrozenSet_1_T
            TryGetAlternateLookup_1_TAlternate = FrozenSet_1.TryGetAlternateLookup_MethodGroup.TryGetAlternateLookup_1_T1
            def __call__(self, lookup: clr.Reference[FrozenSet_1.AlternateLookup_2[TryGetAlternateLookup_1_FrozenSet_1_T, TryGetAlternateLookup_1_TAlternate]]) -> bool:...



    AlternateLookup_GenericClasses_FrozenSet_1_T = typing.TypeVar('AlternateLookup_GenericClasses_FrozenSet_1_T')
    class AlternateLookup_GenericClasses(typing.Generic[AlternateLookup_GenericClasses_FrozenSet_1_T], abc.ABCMeta):
        AlternateLookup_GenericClasses_FrozenSet_1_T = FrozenSet_1.AlternateLookup_GenericClasses_FrozenSet_1_T
        Generic_AlternateLookup_GenericClasses_AlternateLookup_2_TAlternate = typing.TypeVar('Generic_AlternateLookup_GenericClasses_AlternateLookup_2_TAlternate')
        def __getitem__(self, types : typing.Type[Generic_AlternateLookup_GenericClasses_AlternateLookup_2_TAlternate]) -> typing.Type[FrozenSet_1.AlternateLookup_2[AlternateLookup_GenericClasses_FrozenSet_1_T, Generic_AlternateLookup_GenericClasses_AlternateLookup_2_TAlternate]]: ...

    AlternateLookup : AlternateLookup_GenericClasses[FrozenSet_1_T]

    AlternateLookup_2_T = typing.TypeVar('AlternateLookup_2_T')
    AlternateLookup_2_TAlternate = typing.TypeVar('AlternateLookup_2_TAlternate')
    class AlternateLookup_2(typing.Generic[AlternateLookup_2_T, AlternateLookup_2_TAlternate]):
        AlternateLookup_2_T = FrozenSet_1.AlternateLookup_2_T
        AlternateLookup_2_TAlternate = FrozenSet_1.AlternateLookup_2_TAlternate
        @property
        def Set(self) -> FrozenSet_1[AlternateLookup_2_T]: ...
        def Contains(self, item: AlternateLookup_2_TAlternate) -> bool: ...
        def TryGetValue(self, equalValue: AlternateLookup_2_TAlternate, actualValue: clr.Reference[AlternateLookup_2_T]) -> bool: ...


    Enumerator_GenericClasses_FrozenSet_1_T = typing.TypeVar('Enumerator_GenericClasses_FrozenSet_1_T')
    class Enumerator_GenericClasses(typing.Generic[Enumerator_GenericClasses_FrozenSet_1_T], abc.ABCMeta):
        Enumerator_GenericClasses_FrozenSet_1_T = FrozenSet_1.Enumerator_GenericClasses_FrozenSet_1_T
        def __call__(self) -> FrozenSet_1.Enumerator_1[Enumerator_GenericClasses_FrozenSet_1_T]: ...

    Enumerator : Enumerator_GenericClasses[FrozenSet_1_T]

    Enumerator_1_T = typing.TypeVar('Enumerator_1_T')
    class Enumerator_1(typing.Generic[Enumerator_1_T], IEnumerator_1[Enumerator_1_T]):
        Enumerator_1_T = FrozenSet_1.Enumerator_1_T
        @property
        def Current(self) -> Enumerator_1_T: ...
        def MoveNext(self) -> bool: ...


