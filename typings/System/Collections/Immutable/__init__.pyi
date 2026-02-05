import typing, clr, abc
from System.Collections.Generic import IReadOnlyList_1, IEnumerable_1, IEqualityComparer_1, IList_1, IComparer_1, IEnumerator_1
from System import Predicate_1, IEquatable_1, ReadOnlyMemory_1, Array_1, ReadOnlySpan_1, Range, Span_1, Comparison_1
from System.Collections import IList, IStructuralEquatable, IStructuralComparable

class IImmutableList_GenericClasses(abc.ABCMeta):
    Generic_IImmutableList_GenericClasses_IImmutableList_1_T = typing.TypeVar('Generic_IImmutableList_GenericClasses_IImmutableList_1_T')
    def __getitem__(self, types : typing.Type[Generic_IImmutableList_GenericClasses_IImmutableList_1_T]) -> typing.Type[IImmutableList_1[Generic_IImmutableList_GenericClasses_IImmutableList_1_T]]: ...

IImmutableList : IImmutableList_GenericClasses

IImmutableList_1_T = typing.TypeVar('IImmutableList_1_T')
class IImmutableList_1(typing.Generic[IImmutableList_1_T], IReadOnlyList_1[IImmutableList_1_T], typing.Protocol):
    @abc.abstractmethod
    def Add(self, value: IImmutableList_1_T) -> IImmutableList_1[IImmutableList_1_T]: ...
    @abc.abstractmethod
    def AddRange(self, items: IEnumerable_1[IImmutableList_1_T]) -> IImmutableList_1[IImmutableList_1_T]: ...
    @abc.abstractmethod
    def Clear(self) -> IImmutableList_1[IImmutableList_1_T]: ...
    @abc.abstractmethod
    def IndexOf(self, item: IImmutableList_1_T, index: int, count: int, equalityComparer: IEqualityComparer_1[IImmutableList_1_T]) -> int: ...
    @abc.abstractmethod
    def Insert(self, index: int, element: IImmutableList_1_T) -> IImmutableList_1[IImmutableList_1_T]: ...
    @abc.abstractmethod
    def InsertRange(self, index: int, items: IEnumerable_1[IImmutableList_1_T]) -> IImmutableList_1[IImmutableList_1_T]: ...
    @abc.abstractmethod
    def LastIndexOf(self, item: IImmutableList_1_T, index: int, count: int, equalityComparer: IEqualityComparer_1[IImmutableList_1_T]) -> int: ...
    @abc.abstractmethod
    def Remove(self, value: IImmutableList_1_T, equalityComparer: IEqualityComparer_1[IImmutableList_1_T]) -> IImmutableList_1[IImmutableList_1_T]: ...
    @abc.abstractmethod
    def RemoveAll(self, match: Predicate_1[IImmutableList_1_T]) -> IImmutableList_1[IImmutableList_1_T]: ...
    @abc.abstractmethod
    def RemoveAt(self, index: int) -> IImmutableList_1[IImmutableList_1_T]: ...
    @abc.abstractmethod
    def Replace(self, oldValue: IImmutableList_1_T, newValue: IImmutableList_1_T, equalityComparer: IEqualityComparer_1[IImmutableList_1_T]) -> IImmutableList_1[IImmutableList_1_T]: ...
    @abc.abstractmethod
    def SetItem(self, index: int, value: IImmutableList_1_T) -> IImmutableList_1[IImmutableList_1_T]: ...
    # Skipped RemoveRange due to it being static, abstract and generic.

    RemoveRange : RemoveRange_MethodGroup[IImmutableList_1_T]
    RemoveRange_MethodGroup_IImmutableList_1_T = typing.TypeVar('RemoveRange_MethodGroup_IImmutableList_1_T')
    class RemoveRange_MethodGroup(typing.Generic[RemoveRange_MethodGroup_IImmutableList_1_T]):
        RemoveRange_MethodGroup_IImmutableList_1_T = IImmutableList_1.RemoveRange_MethodGroup_IImmutableList_1_T
        @typing.overload
        def __call__(self, index: int, count: int) -> IImmutableList_1[RemoveRange_MethodGroup_IImmutableList_1_T]:...
        @typing.overload
        def __call__(self, items: IEnumerable_1[RemoveRange_MethodGroup_IImmutableList_1_T], equalityComparer: IEqualityComparer_1[RemoveRange_MethodGroup_IImmutableList_1_T]) -> IImmutableList_1[RemoveRange_MethodGroup_IImmutableList_1_T]:...



class ImmutableArray_GenericClasses(abc.ABCMeta):
    Generic_ImmutableArray_GenericClasses_ImmutableArray_1_T = typing.TypeVar('Generic_ImmutableArray_GenericClasses_ImmutableArray_1_T')
    def __getitem__(self, types : typing.Type[Generic_ImmutableArray_GenericClasses_ImmutableArray_1_T]) -> typing.Type[ImmutableArray_1[Generic_ImmutableArray_GenericClasses_ImmutableArray_1_T]]: ...

ImmutableArray : ImmutableArray_GenericClasses

ImmutableArray_1_T = typing.TypeVar('ImmutableArray_1_T')
class ImmutableArray_1(typing.Generic[ImmutableArray_1_T], IImmutableList_1[ImmutableArray_1_T], IList_1[ImmutableArray_1_T], IList, IStructuralEquatable, IStructuralComparable, IEquatable_1[ImmutableArray_1[ImmutableArray_1_T]]):
    Empty : ImmutableArray_1[ImmutableArray_1_T]
    @property
    def IsDefault(self) -> bool: ...
    @property
    def IsDefaultOrEmpty(self) -> bool: ...
    @property
    def IsEmpty(self) -> bool: ...
    @property
    def Length(self) -> int: ...
    def Add(self, item: ImmutableArray_1_T) -> ImmutableArray_1[ImmutableArray_1_T]: ...
    def AsMemory(self) -> ReadOnlyMemory_1[ImmutableArray_1_T]: ...
    def Clear(self) -> ImmutableArray_1[ImmutableArray_1_T]: ...
    def GetEnumerator(self) -> ImmutableArray_1.Enumerator_1[ImmutableArray_1_T]: ...
    def GetHashCode(self) -> int: ...
    def Insert(self, index: int, item: ImmutableArray_1_T) -> ImmutableArray_1[ImmutableArray_1_T]: ...
    def ItemRef(self, index: int) -> clr.Reference[ImmutableArray_1_T]: ...
    @typing.overload
    def __eq__(self, left: ImmutableArray_1[ImmutableArray_1_T], right: ImmutableArray_1[ImmutableArray_1_T]) -> bool: ...
    @typing.overload
    def __eq__(self, left: typing.Optional[ImmutableArray_1[ImmutableArray_1_T]], right: typing.Optional[ImmutableArray_1[ImmutableArray_1_T]]) -> bool: ...
    @typing.overload
    def __ne__(self, left: ImmutableArray_1[ImmutableArray_1_T], right: ImmutableArray_1[ImmutableArray_1_T]) -> bool: ...
    @typing.overload
    def __ne__(self, left: typing.Optional[ImmutableArray_1[ImmutableArray_1_T]], right: typing.Optional[ImmutableArray_1[ImmutableArray_1_T]]) -> bool: ...
    def RemoveAll(self, match: Predicate_1[ImmutableArray_1_T]) -> ImmutableArray_1[ImmutableArray_1_T]: ...
    def RemoveAt(self, index: int) -> ImmutableArray_1[ImmutableArray_1_T]: ...
    def SetItem(self, index: int, item: ImmutableArray_1_T) -> ImmutableArray_1[ImmutableArray_1_T]: ...
    def Slice(self, start: int, length: int) -> ImmutableArray_1[ImmutableArray_1_T]: ...
    def ToBuilder(self) -> ImmutableArray_1.Builder_1[ImmutableArray_1_T]: ...
    # Skipped AddRange due to it being static, abstract and generic.

    AddRange : AddRange_MethodGroup[ImmutableArray_1_T]
    AddRange_MethodGroup_ImmutableArray_1_T = typing.TypeVar('AddRange_MethodGroup_ImmutableArray_1_T')
    class AddRange_MethodGroup(typing.Generic[AddRange_MethodGroup_ImmutableArray_1_T]):
        AddRange_MethodGroup_ImmutableArray_1_T = ImmutableArray_1.AddRange_MethodGroup_ImmutableArray_1_T
        def __getitem__(self, t:typing.Type[AddRange_1_T1]) -> AddRange_1[AddRange_MethodGroup_ImmutableArray_1_T, AddRange_1_T1]: ...

        AddRange_1_ImmutableArray_1_T = typing.TypeVar('AddRange_1_ImmutableArray_1_T')
        AddRange_1_T1 = typing.TypeVar('AddRange_1_T1')
        class AddRange_1(typing.Generic[AddRange_1_ImmutableArray_1_T, AddRange_1_T1]):
            AddRange_1_ImmutableArray_1_T = ImmutableArray_1.AddRange_MethodGroup.AddRange_1_ImmutableArray_1_T
            AddRange_1_TDerived = ImmutableArray_1.AddRange_MethodGroup.AddRange_1_T1
            @typing.overload
            def __call__(self, items: ImmutableArray_1[AddRange_1_TDerived]) -> ImmutableArray_1[AddRange_1_ImmutableArray_1_T]:...
            @typing.overload
            def __call__(self, items: Array_1[AddRange_1_TDerived]) -> ImmutableArray_1[AddRange_1_ImmutableArray_1_T]:...

        @typing.overload
        def __call__(self, items: ImmutableArray_1[AddRange_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[AddRange_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, items: Array_1[AddRange_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[AddRange_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, items: ReadOnlySpan_1[AddRange_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[AddRange_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, items: IEnumerable_1[AddRange_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[AddRange_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, items: ImmutableArray_1[AddRange_MethodGroup_ImmutableArray_1_T], length: int) -> ImmutableArray_1[AddRange_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, items: Array_1[AddRange_MethodGroup_ImmutableArray_1_T], length: int) -> ImmutableArray_1[AddRange_MethodGroup_ImmutableArray_1_T]:...

    # Skipped As due to it being static, abstract and generic.

    As : As_MethodGroup[ImmutableArray_1_T]
    As_MethodGroup_ImmutableArray_1_T = typing.TypeVar('As_MethodGroup_ImmutableArray_1_T')
    class As_MethodGroup(typing.Generic[As_MethodGroup_ImmutableArray_1_T]):
        As_MethodGroup_ImmutableArray_1_T = ImmutableArray_1.As_MethodGroup_ImmutableArray_1_T
        def __getitem__(self, t:typing.Type[As_1_T1]) -> As_1[As_MethodGroup_ImmutableArray_1_T, As_1_T1]: ...

        As_1_ImmutableArray_1_T = typing.TypeVar('As_1_ImmutableArray_1_T')
        As_1_T1 = typing.TypeVar('As_1_T1')
        class As_1(typing.Generic[As_1_ImmutableArray_1_T, As_1_T1]):
            As_1_ImmutableArray_1_T = ImmutableArray_1.As_MethodGroup.As_1_ImmutableArray_1_T
            As_1_TOther = ImmutableArray_1.As_MethodGroup.As_1_T1
            def __call__(self) -> ImmutableArray_1[As_1_TOther]:...


    # Skipped AsSpan due to it being static, abstract and generic.

    AsSpan : AsSpan_MethodGroup[ImmutableArray_1_T]
    AsSpan_MethodGroup_ImmutableArray_1_T = typing.TypeVar('AsSpan_MethodGroup_ImmutableArray_1_T')
    class AsSpan_MethodGroup(typing.Generic[AsSpan_MethodGroup_ImmutableArray_1_T]):
        AsSpan_MethodGroup_ImmutableArray_1_T = ImmutableArray_1.AsSpan_MethodGroup_ImmutableArray_1_T
        @typing.overload
        def __call__(self) -> ReadOnlySpan_1[AsSpan_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, range: Range) -> ReadOnlySpan_1[AsSpan_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, start: int, length: int) -> ReadOnlySpan_1[AsSpan_MethodGroup_ImmutableArray_1_T]:...

    # Skipped CastArray due to it being static, abstract and generic.

    CastArray : CastArray_MethodGroup[ImmutableArray_1_T]
    CastArray_MethodGroup_ImmutableArray_1_T = typing.TypeVar('CastArray_MethodGroup_ImmutableArray_1_T')
    class CastArray_MethodGroup(typing.Generic[CastArray_MethodGroup_ImmutableArray_1_T]):
        CastArray_MethodGroup_ImmutableArray_1_T = ImmutableArray_1.CastArray_MethodGroup_ImmutableArray_1_T
        def __getitem__(self, t:typing.Type[CastArray_1_T1]) -> CastArray_1[CastArray_MethodGroup_ImmutableArray_1_T, CastArray_1_T1]: ...

        CastArray_1_ImmutableArray_1_T = typing.TypeVar('CastArray_1_ImmutableArray_1_T')
        CastArray_1_T1 = typing.TypeVar('CastArray_1_T1')
        class CastArray_1(typing.Generic[CastArray_1_ImmutableArray_1_T, CastArray_1_T1]):
            CastArray_1_ImmutableArray_1_T = ImmutableArray_1.CastArray_MethodGroup.CastArray_1_ImmutableArray_1_T
            CastArray_1_TOther = ImmutableArray_1.CastArray_MethodGroup.CastArray_1_T1
            def __call__(self) -> ImmutableArray_1[CastArray_1_TOther]:...


    # Skipped CastUp due to it being static, abstract and generic.

    CastUp : CastUp_MethodGroup[ImmutableArray_1_T]
    CastUp_MethodGroup_ImmutableArray_1_T = typing.TypeVar('CastUp_MethodGroup_ImmutableArray_1_T')
    class CastUp_MethodGroup(typing.Generic[CastUp_MethodGroup_ImmutableArray_1_T]):
        CastUp_MethodGroup_ImmutableArray_1_T = ImmutableArray_1.CastUp_MethodGroup_ImmutableArray_1_T
        def __getitem__(self, t:typing.Type[CastUp_1_T1]) -> CastUp_1[CastUp_MethodGroup_ImmutableArray_1_T, CastUp_1_T1]: ...

        CastUp_1_ImmutableArray_1_T = typing.TypeVar('CastUp_1_ImmutableArray_1_T')
        CastUp_1_T1 = typing.TypeVar('CastUp_1_T1')
        class CastUp_1(typing.Generic[CastUp_1_ImmutableArray_1_T, CastUp_1_T1]):
            CastUp_1_ImmutableArray_1_T = ImmutableArray_1.CastUp_MethodGroup.CastUp_1_ImmutableArray_1_T
            CastUp_1_TDerived = ImmutableArray_1.CastUp_MethodGroup.CastUp_1_T1
            def __call__(self, items: ImmutableArray_1[CastUp_1_TDerived]) -> ImmutableArray_1[CastUp_1_ImmutableArray_1_T]:...


    # Skipped Contains due to it being static, abstract and generic.

    Contains : Contains_MethodGroup[ImmutableArray_1_T]
    Contains_MethodGroup_ImmutableArray_1_T = typing.TypeVar('Contains_MethodGroup_ImmutableArray_1_T')
    class Contains_MethodGroup(typing.Generic[Contains_MethodGroup_ImmutableArray_1_T]):
        Contains_MethodGroup_ImmutableArray_1_T = ImmutableArray_1.Contains_MethodGroup_ImmutableArray_1_T
        @typing.overload
        def __call__(self, item: Contains_MethodGroup_ImmutableArray_1_T) -> bool:...
        @typing.overload
        def __call__(self, item: Contains_MethodGroup_ImmutableArray_1_T, equalityComparer: IEqualityComparer_1[Contains_MethodGroup_ImmutableArray_1_T]) -> bool:...

    # Skipped CopyTo due to it being static, abstract and generic.

    CopyTo : CopyTo_MethodGroup[ImmutableArray_1_T]
    CopyTo_MethodGroup_ImmutableArray_1_T = typing.TypeVar('CopyTo_MethodGroup_ImmutableArray_1_T')
    class CopyTo_MethodGroup(typing.Generic[CopyTo_MethodGroup_ImmutableArray_1_T]):
        CopyTo_MethodGroup_ImmutableArray_1_T = ImmutableArray_1.CopyTo_MethodGroup_ImmutableArray_1_T
        @typing.overload
        def __call__(self, destination: Array_1[CopyTo_MethodGroup_ImmutableArray_1_T]) -> None:...
        @typing.overload
        def __call__(self, destination: Span_1[CopyTo_MethodGroup_ImmutableArray_1_T]) -> None:...
        @typing.overload
        def __call__(self, destination: Array_1[CopyTo_MethodGroup_ImmutableArray_1_T], destinationIndex: int) -> None:...
        @typing.overload
        def __call__(self, sourceIndex: int, destination: Array_1[CopyTo_MethodGroup_ImmutableArray_1_T], destinationIndex: int, length: int) -> None:...

    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup[ImmutableArray_1_T]
    Equals_MethodGroup_ImmutableArray_1_T = typing.TypeVar('Equals_MethodGroup_ImmutableArray_1_T')
    class Equals_MethodGroup(typing.Generic[Equals_MethodGroup_ImmutableArray_1_T]):
        Equals_MethodGroup_ImmutableArray_1_T = ImmutableArray_1.Equals_MethodGroup_ImmutableArray_1_T
        @typing.overload
        def __call__(self, other: ImmutableArray_1[Equals_MethodGroup_ImmutableArray_1_T]) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...

    # Skipped IndexOf due to it being static, abstract and generic.

    IndexOf : IndexOf_MethodGroup[ImmutableArray_1_T]
    IndexOf_MethodGroup_ImmutableArray_1_T = typing.TypeVar('IndexOf_MethodGroup_ImmutableArray_1_T')
    class IndexOf_MethodGroup(typing.Generic[IndexOf_MethodGroup_ImmutableArray_1_T]):
        IndexOf_MethodGroup_ImmutableArray_1_T = ImmutableArray_1.IndexOf_MethodGroup_ImmutableArray_1_T
        @typing.overload
        def __call__(self, item: IndexOf_MethodGroup_ImmutableArray_1_T) -> int:...
        @typing.overload
        def __call__(self, item: IndexOf_MethodGroup_ImmutableArray_1_T, startIndex: int) -> int:...
        @typing.overload
        def __call__(self, item: IndexOf_MethodGroup_ImmutableArray_1_T, startIndex: int, count: int) -> int:...
        @typing.overload
        def __call__(self, item: IndexOf_MethodGroup_ImmutableArray_1_T, startIndex: int, equalityComparer: IEqualityComparer_1[IndexOf_MethodGroup_ImmutableArray_1_T]) -> int:...
        @typing.overload
        def __call__(self, item: IndexOf_MethodGroup_ImmutableArray_1_T, startIndex: int, count: int, equalityComparer: IEqualityComparer_1[IndexOf_MethodGroup_ImmutableArray_1_T]) -> int:...

    # Skipped InsertRange due to it being static, abstract and generic.

    InsertRange : InsertRange_MethodGroup[ImmutableArray_1_T]
    InsertRange_MethodGroup_ImmutableArray_1_T = typing.TypeVar('InsertRange_MethodGroup_ImmutableArray_1_T')
    class InsertRange_MethodGroup(typing.Generic[InsertRange_MethodGroup_ImmutableArray_1_T]):
        InsertRange_MethodGroup_ImmutableArray_1_T = ImmutableArray_1.InsertRange_MethodGroup_ImmutableArray_1_T
        @typing.overload
        def __call__(self, index: int, items: ImmutableArray_1[InsertRange_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[InsertRange_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, index: int, items: Array_1[InsertRange_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[InsertRange_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, index: int, items: ReadOnlySpan_1[InsertRange_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[InsertRange_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, index: int, items: IEnumerable_1[InsertRange_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[InsertRange_MethodGroup_ImmutableArray_1_T]:...

    # Skipped LastIndexOf due to it being static, abstract and generic.

    LastIndexOf : LastIndexOf_MethodGroup[ImmutableArray_1_T]
    LastIndexOf_MethodGroup_ImmutableArray_1_T = typing.TypeVar('LastIndexOf_MethodGroup_ImmutableArray_1_T')
    class LastIndexOf_MethodGroup(typing.Generic[LastIndexOf_MethodGroup_ImmutableArray_1_T]):
        LastIndexOf_MethodGroup_ImmutableArray_1_T = ImmutableArray_1.LastIndexOf_MethodGroup_ImmutableArray_1_T
        @typing.overload
        def __call__(self, item: LastIndexOf_MethodGroup_ImmutableArray_1_T) -> int:...
        @typing.overload
        def __call__(self, item: LastIndexOf_MethodGroup_ImmutableArray_1_T, startIndex: int) -> int:...
        @typing.overload
        def __call__(self, item: LastIndexOf_MethodGroup_ImmutableArray_1_T, startIndex: int, count: int) -> int:...
        @typing.overload
        def __call__(self, item: LastIndexOf_MethodGroup_ImmutableArray_1_T, startIndex: int, count: int, equalityComparer: IEqualityComparer_1[LastIndexOf_MethodGroup_ImmutableArray_1_T]) -> int:...

    # Skipped OfType due to it being static, abstract and generic.

    OfType : OfType_MethodGroup[ImmutableArray_1_T]
    OfType_MethodGroup_ImmutableArray_1_T = typing.TypeVar('OfType_MethodGroup_ImmutableArray_1_T')
    class OfType_MethodGroup(typing.Generic[OfType_MethodGroup_ImmutableArray_1_T]):
        OfType_MethodGroup_ImmutableArray_1_T = ImmutableArray_1.OfType_MethodGroup_ImmutableArray_1_T
        def __getitem__(self, t:typing.Type[OfType_1_T1]) -> OfType_1[OfType_MethodGroup_ImmutableArray_1_T, OfType_1_T1]: ...

        OfType_1_ImmutableArray_1_T = typing.TypeVar('OfType_1_ImmutableArray_1_T')
        OfType_1_T1 = typing.TypeVar('OfType_1_T1')
        class OfType_1(typing.Generic[OfType_1_ImmutableArray_1_T, OfType_1_T1]):
            OfType_1_ImmutableArray_1_T = ImmutableArray_1.OfType_MethodGroup.OfType_1_ImmutableArray_1_T
            OfType_1_TResult = ImmutableArray_1.OfType_MethodGroup.OfType_1_T1
            def __call__(self) -> IEnumerable_1[OfType_1_TResult]:...


    # Skipped Remove due to it being static, abstract and generic.

    Remove : Remove_MethodGroup[ImmutableArray_1_T]
    Remove_MethodGroup_ImmutableArray_1_T = typing.TypeVar('Remove_MethodGroup_ImmutableArray_1_T')
    class Remove_MethodGroup(typing.Generic[Remove_MethodGroup_ImmutableArray_1_T]):
        Remove_MethodGroup_ImmutableArray_1_T = ImmutableArray_1.Remove_MethodGroup_ImmutableArray_1_T
        @typing.overload
        def __call__(self, item: Remove_MethodGroup_ImmutableArray_1_T) -> ImmutableArray_1[Remove_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, item: Remove_MethodGroup_ImmutableArray_1_T, equalityComparer: IEqualityComparer_1[Remove_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[Remove_MethodGroup_ImmutableArray_1_T]:...

    # Skipped RemoveRange due to it being static, abstract and generic.

    RemoveRange : RemoveRange_MethodGroup[ImmutableArray_1_T]
    RemoveRange_MethodGroup_ImmutableArray_1_T = typing.TypeVar('RemoveRange_MethodGroup_ImmutableArray_1_T')
    class RemoveRange_MethodGroup(typing.Generic[RemoveRange_MethodGroup_ImmutableArray_1_T]):
        RemoveRange_MethodGroup_ImmutableArray_1_T = ImmutableArray_1.RemoveRange_MethodGroup_ImmutableArray_1_T
        @typing.overload
        def __call__(self, items: ImmutableArray_1[RemoveRange_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[RemoveRange_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, items: IEnumerable_1[RemoveRange_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[RemoveRange_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, index: int, length: int) -> ImmutableArray_1[RemoveRange_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, items: ImmutableArray_1[RemoveRange_MethodGroup_ImmutableArray_1_T], equalityComparer: IEqualityComparer_1[RemoveRange_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[RemoveRange_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, items: Array_1[RemoveRange_MethodGroup_ImmutableArray_1_T], equalityComparer: IEqualityComparer_1[RemoveRange_MethodGroup_ImmutableArray_1_T] = ...) -> ImmutableArray_1[RemoveRange_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, items: ReadOnlySpan_1[RemoveRange_MethodGroup_ImmutableArray_1_T], equalityComparer: IEqualityComparer_1[RemoveRange_MethodGroup_ImmutableArray_1_T] = ...) -> ImmutableArray_1[RemoveRange_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, items: IEnumerable_1[RemoveRange_MethodGroup_ImmutableArray_1_T], equalityComparer: IEqualityComparer_1[RemoveRange_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[RemoveRange_MethodGroup_ImmutableArray_1_T]:...

    # Skipped Replace due to it being static, abstract and generic.

    Replace : Replace_MethodGroup[ImmutableArray_1_T]
    Replace_MethodGroup_ImmutableArray_1_T = typing.TypeVar('Replace_MethodGroup_ImmutableArray_1_T')
    class Replace_MethodGroup(typing.Generic[Replace_MethodGroup_ImmutableArray_1_T]):
        Replace_MethodGroup_ImmutableArray_1_T = ImmutableArray_1.Replace_MethodGroup_ImmutableArray_1_T
        @typing.overload
        def __call__(self, oldValue: Replace_MethodGroup_ImmutableArray_1_T, newValue: Replace_MethodGroup_ImmutableArray_1_T) -> ImmutableArray_1[Replace_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, oldValue: Replace_MethodGroup_ImmutableArray_1_T, newValue: Replace_MethodGroup_ImmutableArray_1_T, equalityComparer: IEqualityComparer_1[Replace_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[Replace_MethodGroup_ImmutableArray_1_T]:...

    # Skipped Sort due to it being static, abstract and generic.

    Sort : Sort_MethodGroup[ImmutableArray_1_T]
    Sort_MethodGroup_ImmutableArray_1_T = typing.TypeVar('Sort_MethodGroup_ImmutableArray_1_T')
    class Sort_MethodGroup(typing.Generic[Sort_MethodGroup_ImmutableArray_1_T]):
        Sort_MethodGroup_ImmutableArray_1_T = ImmutableArray_1.Sort_MethodGroup_ImmutableArray_1_T
        @typing.overload
        def __call__(self) -> ImmutableArray_1[Sort_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, comparison: Comparison_1[Sort_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[Sort_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, comparer: IComparer_1[Sort_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[Sort_MethodGroup_ImmutableArray_1_T]:...
        @typing.overload
        def __call__(self, index: int, count: int, comparer: IComparer_1[Sort_MethodGroup_ImmutableArray_1_T]) -> ImmutableArray_1[Sort_MethodGroup_ImmutableArray_1_T]:...


    Builder_GenericClasses_ImmutableArray_1_T = typing.TypeVar('Builder_GenericClasses_ImmutableArray_1_T')
    class Builder_GenericClasses(typing.Generic[Builder_GenericClasses_ImmutableArray_1_T], abc.ABCMeta):
        Builder_GenericClasses_ImmutableArray_1_T = ImmutableArray_1.Builder_GenericClasses_ImmutableArray_1_T
        def __call__(self) -> ImmutableArray_1.Builder_1[Builder_GenericClasses_ImmutableArray_1_T]: ...

    Builder : Builder_GenericClasses[ImmutableArray_1_T]

    Builder_1_T = typing.TypeVar('Builder_1_T')
    class Builder_1(typing.Generic[Builder_1_T], IReadOnlyList_1[Builder_1_T], IList_1[Builder_1_T]):
        Builder_1_T = ImmutableArray_1.Builder_1_T
        @property
        def Capacity(self) -> int: ...
        @Capacity.setter
        def Capacity(self, value: int) -> int: ...
        @property
        def Count(self) -> int: ...
        @Count.setter
        def Count(self, value: int) -> int: ...
        def Add(self, item: Builder_1_T) -> None: ...
        def Clear(self) -> None: ...
        def Contains(self, item: Builder_1_T) -> bool: ...
        def DrainToImmutable(self) -> ImmutableArray_1[Builder_1_T]: ...
        def GetEnumerator(self) -> IEnumerator_1[Builder_1_T]: ...
        def Insert(self, index: int, item: Builder_1_T) -> None: ...
        def ItemRef(self, index: int) -> clr.Reference[Builder_1_T]: ...
        def MoveToImmutable(self) -> ImmutableArray_1[Builder_1_T]: ...
        def RemoveAll(self, match: Predicate_1[Builder_1_T]) -> None: ...
        def RemoveAt(self, index: int) -> None: ...
        def Reverse(self) -> None: ...
        def ToArray(self) -> Array_1[Builder_1_T]: ...
        def ToImmutable(self) -> ImmutableArray_1[Builder_1_T]: ...
        # Skipped AddRange due to it being static, abstract and generic.

        AddRange : AddRange_MethodGroup[Builder_1_T]
        AddRange_MethodGroup_Builder_1_T = typing.TypeVar('AddRange_MethodGroup_Builder_1_T')
        class AddRange_MethodGroup(typing.Generic[AddRange_MethodGroup_Builder_1_T]):
            AddRange_MethodGroup_Builder_1_T = ImmutableArray_1.Builder_1.AddRange_MethodGroup_Builder_1_T
            def __getitem__(self, t:typing.Type[AddRange_1_T1]) -> AddRange_1[AddRange_MethodGroup_Builder_1_T, AddRange_1_T1]: ...

            AddRange_1_Builder_1_T = typing.TypeVar('AddRange_1_Builder_1_T')
            AddRange_1_T1 = typing.TypeVar('AddRange_1_T1')
            class AddRange_1(typing.Generic[AddRange_1_Builder_1_T, AddRange_1_T1]):
                AddRange_1_Builder_1_T = ImmutableArray_1.Builder_1.AddRange_MethodGroup.AddRange_1_Builder_1_T
                AddRange_1_TDerived = ImmutableArray_1.Builder_1.AddRange_MethodGroup.AddRange_1_T1
                @typing.overload
                def __call__(self, items: ImmutableArray_1[AddRange_1_TDerived]) -> None:...
                @typing.overload
                def __call__(self, items: Array_1[AddRange_1_TDerived]) -> None:...
                @typing.overload
                def __call__(self, items: ImmutableArray_1.Builder_1[AddRange_1_TDerived]) -> None:...
                @typing.overload
                def __call__(self, items: ReadOnlySpan_1[AddRange_1_TDerived]) -> None:...

            @typing.overload
            def __call__(self, items: ImmutableArray_1[AddRange_MethodGroup_Builder_1_T]) -> None:...
            @typing.overload
            def __call__(self, items: Array_1[AddRange_MethodGroup_Builder_1_T]) -> None:...
            @typing.overload
            def __call__(self, items: ImmutableArray_1.Builder_1[AddRange_MethodGroup_Builder_1_T]) -> None:...
            @typing.overload
            def __call__(self, items: ReadOnlySpan_1[AddRange_MethodGroup_Builder_1_T]) -> None:...
            @typing.overload
            def __call__(self, items: IEnumerable_1[AddRange_MethodGroup_Builder_1_T]) -> None:...
            @typing.overload
            def __call__(self, items: ImmutableArray_1[AddRange_MethodGroup_Builder_1_T], length: int) -> None:...
            @typing.overload
            def __call__(self, items: Array_1[AddRange_MethodGroup_Builder_1_T], length: int) -> None:...

        # Skipped CopyTo due to it being static, abstract and generic.

        CopyTo : CopyTo_MethodGroup[Builder_1_T]
        CopyTo_MethodGroup_Builder_1_T = typing.TypeVar('CopyTo_MethodGroup_Builder_1_T')
        class CopyTo_MethodGroup(typing.Generic[CopyTo_MethodGroup_Builder_1_T]):
            CopyTo_MethodGroup_Builder_1_T = ImmutableArray_1.Builder_1.CopyTo_MethodGroup_Builder_1_T
            @typing.overload
            def __call__(self, destination: Array_1[CopyTo_MethodGroup_Builder_1_T]) -> None:...
            @typing.overload
            def __call__(self, destination: Span_1[CopyTo_MethodGroup_Builder_1_T]) -> None:...
            @typing.overload
            def __call__(self, array: Array_1[CopyTo_MethodGroup_Builder_1_T], index: int) -> None:...
            @typing.overload
            def __call__(self, sourceIndex: int, destination: Array_1[CopyTo_MethodGroup_Builder_1_T], destinationIndex: int, length: int) -> None:...

        # Skipped IndexOf due to it being static, abstract and generic.

        IndexOf : IndexOf_MethodGroup[Builder_1_T]
        IndexOf_MethodGroup_Builder_1_T = typing.TypeVar('IndexOf_MethodGroup_Builder_1_T')
        class IndexOf_MethodGroup(typing.Generic[IndexOf_MethodGroup_Builder_1_T]):
            IndexOf_MethodGroup_Builder_1_T = ImmutableArray_1.Builder_1.IndexOf_MethodGroup_Builder_1_T
            @typing.overload
            def __call__(self, item: IndexOf_MethodGroup_Builder_1_T) -> int:...
            @typing.overload
            def __call__(self, item: IndexOf_MethodGroup_Builder_1_T, startIndex: int) -> int:...
            @typing.overload
            def __call__(self, item: IndexOf_MethodGroup_Builder_1_T, startIndex: int, count: int) -> int:...
            @typing.overload
            def __call__(self, item: IndexOf_MethodGroup_Builder_1_T, startIndex: int, equalityComparer: IEqualityComparer_1[IndexOf_MethodGroup_Builder_1_T]) -> int:...
            @typing.overload
            def __call__(self, item: IndexOf_MethodGroup_Builder_1_T, startIndex: int, count: int, equalityComparer: IEqualityComparer_1[IndexOf_MethodGroup_Builder_1_T]) -> int:...

        # Skipped InsertRange due to it being static, abstract and generic.

        InsertRange : InsertRange_MethodGroup[Builder_1_T]
        InsertRange_MethodGroup_Builder_1_T = typing.TypeVar('InsertRange_MethodGroup_Builder_1_T')
        class InsertRange_MethodGroup(typing.Generic[InsertRange_MethodGroup_Builder_1_T]):
            InsertRange_MethodGroup_Builder_1_T = ImmutableArray_1.Builder_1.InsertRange_MethodGroup_Builder_1_T
            @typing.overload
            def __call__(self, index: int, items: ImmutableArray_1[InsertRange_MethodGroup_Builder_1_T]) -> None:...
            @typing.overload
            def __call__(self, index: int, items: IEnumerable_1[InsertRange_MethodGroup_Builder_1_T]) -> None:...

        # Skipped LastIndexOf due to it being static, abstract and generic.

        LastIndexOf : LastIndexOf_MethodGroup[Builder_1_T]
        LastIndexOf_MethodGroup_Builder_1_T = typing.TypeVar('LastIndexOf_MethodGroup_Builder_1_T')
        class LastIndexOf_MethodGroup(typing.Generic[LastIndexOf_MethodGroup_Builder_1_T]):
            LastIndexOf_MethodGroup_Builder_1_T = ImmutableArray_1.Builder_1.LastIndexOf_MethodGroup_Builder_1_T
            @typing.overload
            def __call__(self, item: LastIndexOf_MethodGroup_Builder_1_T) -> int:...
            @typing.overload
            def __call__(self, item: LastIndexOf_MethodGroup_Builder_1_T, startIndex: int) -> int:...
            @typing.overload
            def __call__(self, item: LastIndexOf_MethodGroup_Builder_1_T, startIndex: int, count: int) -> int:...
            @typing.overload
            def __call__(self, item: LastIndexOf_MethodGroup_Builder_1_T, startIndex: int, count: int, equalityComparer: IEqualityComparer_1[LastIndexOf_MethodGroup_Builder_1_T]) -> int:...

        # Skipped Remove due to it being static, abstract and generic.

        Remove : Remove_MethodGroup[Builder_1_T]
        Remove_MethodGroup_Builder_1_T = typing.TypeVar('Remove_MethodGroup_Builder_1_T')
        class Remove_MethodGroup(typing.Generic[Remove_MethodGroup_Builder_1_T]):
            Remove_MethodGroup_Builder_1_T = ImmutableArray_1.Builder_1.Remove_MethodGroup_Builder_1_T
            @typing.overload
            def __call__(self, element: Remove_MethodGroup_Builder_1_T) -> bool:...
            @typing.overload
            def __call__(self, element: Remove_MethodGroup_Builder_1_T, equalityComparer: IEqualityComparer_1[Remove_MethodGroup_Builder_1_T]) -> bool:...

        # Skipped RemoveRange due to it being static, abstract and generic.

        RemoveRange : RemoveRange_MethodGroup[Builder_1_T]
        RemoveRange_MethodGroup_Builder_1_T = typing.TypeVar('RemoveRange_MethodGroup_Builder_1_T')
        class RemoveRange_MethodGroup(typing.Generic[RemoveRange_MethodGroup_Builder_1_T]):
            RemoveRange_MethodGroup_Builder_1_T = ImmutableArray_1.Builder_1.RemoveRange_MethodGroup_Builder_1_T
            @typing.overload
            def __call__(self, items: IEnumerable_1[RemoveRange_MethodGroup_Builder_1_T]) -> None:...
            @typing.overload
            def __call__(self, index: int, length: int) -> None:...
            @typing.overload
            def __call__(self, items: IEnumerable_1[RemoveRange_MethodGroup_Builder_1_T], equalityComparer: IEqualityComparer_1[RemoveRange_MethodGroup_Builder_1_T]) -> None:...

        # Skipped Replace due to it being static, abstract and generic.

        Replace : Replace_MethodGroup[Builder_1_T]
        Replace_MethodGroup_Builder_1_T = typing.TypeVar('Replace_MethodGroup_Builder_1_T')
        class Replace_MethodGroup(typing.Generic[Replace_MethodGroup_Builder_1_T]):
            Replace_MethodGroup_Builder_1_T = ImmutableArray_1.Builder_1.Replace_MethodGroup_Builder_1_T
            @typing.overload
            def __call__(self, oldValue: Replace_MethodGroup_Builder_1_T, newValue: Replace_MethodGroup_Builder_1_T) -> None:...
            @typing.overload
            def __call__(self, oldValue: Replace_MethodGroup_Builder_1_T, newValue: Replace_MethodGroup_Builder_1_T, equalityComparer: IEqualityComparer_1[Replace_MethodGroup_Builder_1_T]) -> None:...

        # Skipped Sort due to it being static, abstract and generic.

        Sort : Sort_MethodGroup[Builder_1_T]
        Sort_MethodGroup_Builder_1_T = typing.TypeVar('Sort_MethodGroup_Builder_1_T')
        class Sort_MethodGroup(typing.Generic[Sort_MethodGroup_Builder_1_T]):
            Sort_MethodGroup_Builder_1_T = ImmutableArray_1.Builder_1.Sort_MethodGroup_Builder_1_T
            @typing.overload
            def __call__(self) -> None:...
            @typing.overload
            def __call__(self, comparison: Comparison_1[Sort_MethodGroup_Builder_1_T]) -> None:...
            @typing.overload
            def __call__(self, comparer: IComparer_1[Sort_MethodGroup_Builder_1_T]) -> None:...
            @typing.overload
            def __call__(self, index: int, count: int, comparer: IComparer_1[Sort_MethodGroup_Builder_1_T]) -> None:...

        def __getitem__(self, index: int) -> Builder_1_T: ...
        def __setitem__(self, index: int, value: Builder_1_T) -> None: ...


    Enumerator_GenericClasses_ImmutableArray_1_T = typing.TypeVar('Enumerator_GenericClasses_ImmutableArray_1_T')
    class Enumerator_GenericClasses(typing.Generic[Enumerator_GenericClasses_ImmutableArray_1_T], abc.ABCMeta):
        Enumerator_GenericClasses_ImmutableArray_1_T = ImmutableArray_1.Enumerator_GenericClasses_ImmutableArray_1_T
        def __call__(self) -> ImmutableArray_1.Enumerator_1[Enumerator_GenericClasses_ImmutableArray_1_T]: ...

    Enumerator : Enumerator_GenericClasses[ImmutableArray_1_T]

    Enumerator_1_T = typing.TypeVar('Enumerator_1_T')
    class Enumerator_1(typing.Generic[Enumerator_1_T]):
        Enumerator_1_T = ImmutableArray_1.Enumerator_1_T
        @property
        def Current(self) -> Enumerator_1_T: ...
        def MoveNext(self) -> bool: ...

    def __getitem__(self, index: int) -> ImmutableArray_1_T: ...

