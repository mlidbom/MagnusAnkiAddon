import typing, abc
from Avalonia.Styling import ISetterInstance
from System import IDisposable, IEquatable_1, Exception, IObservable_1, IObserver_1
from Avalonia import AvaloniaObject, AvaloniaProperty, IDescription

class BindingExpressionBase(ISetterInstance, IDisposable, abc.ABC):
    def Dispose(self) -> None: ...
    def UpdateSource(self) -> None: ...
    def UpdateTarget(self) -> None: ...


class BindingMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : BindingMode # 0
    OneWay : BindingMode # 1
    TwoWay : BindingMode # 2
    OneTime : BindingMode # 3
    OneWayToSource : BindingMode # 4


class BindingPriority(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    LocalValue : BindingPriority # 0
    StyleTrigger : BindingPriority # 1
    Template : BindingPriority # 2
    TemplatedParent : BindingPriority # 2
    Style : BindingPriority # 3
    Inherited : BindingPriority # 4
    Unset : BindingPriority # 2147483647
    Animation : BindingPriority # -1


class BindingValue_GenericClasses(abc.ABCMeta):
    Generic_BindingValue_GenericClasses_BindingValue_1_T = typing.TypeVar('Generic_BindingValue_GenericClasses_BindingValue_1_T')
    def __getitem__(self, types : typing.Type[Generic_BindingValue_GenericClasses_BindingValue_1_T]) -> typing.Type[BindingValue_1[Generic_BindingValue_GenericClasses_BindingValue_1_T]]: ...

BindingValue : BindingValue_GenericClasses

BindingValue_1_T = typing.TypeVar('BindingValue_1_T')
class BindingValue_1(typing.Generic[BindingValue_1_T], IEquatable_1[BindingValue_1[BindingValue_1_T]]):
    def __init__(self, value: BindingValue_1_T) -> None: ...
    @classmethod
    @property
    def DoNothing(cls) -> BindingValue_1[BindingValue_1_T]: ...
    @property
    def Error(self) -> Exception: ...
    @property
    def HasError(self) -> bool: ...
    @property
    def HasValue(self) -> bool: ...
    @property
    def Type(self) -> BindingValueType: ...
    @classmethod
    @property
    def Unset(cls) -> BindingValue_1[BindingValue_1_T]: ...
    @property
    def Value(self) -> BindingValue_1_T: ...
    def GetHashCode(self) -> int: ...
    def __eq__(self, left: BindingValue_1[BindingValue_1_T], right: BindingValue_1[BindingValue_1_T]) -> bool: ...
    # Operator not supported op_Implicit(optional: Optional`1)
    # Operator not supported op_Implicit(value: T)
    def __ne__(self, left: BindingValue_1[BindingValue_1_T], right: BindingValue_1[BindingValue_1_T]) -> bool: ...
    def ToOptional(self) -> Optional_1[BindingValue_1_T]: ...
    def ToString(self) -> str: ...
    def ToUntyped(self) -> typing.Any: ...
    def WithValue(self, value: BindingValue_1_T) -> BindingValue_1[BindingValue_1_T]: ...
    # Skipped BindingError due to it being static, abstract and generic.

    BindingError : BindingError_MethodGroup[BindingValue_1_T]
    BindingError_MethodGroup_BindingValue_1_T = typing.TypeVar('BindingError_MethodGroup_BindingValue_1_T')
    class BindingError_MethodGroup(typing.Generic[BindingError_MethodGroup_BindingValue_1_T]):
        BindingError_MethodGroup_BindingValue_1_T = BindingValue_1.BindingError_MethodGroup_BindingValue_1_T
        @typing.overload
        def __call__(self, e: Exception) -> BindingValue_1[BindingError_MethodGroup_BindingValue_1_T]:...
        @typing.overload
        def __call__(self, e: Exception, fallbackValue: Optional_1[BindingError_MethodGroup_BindingValue_1_T]) -> BindingValue_1[BindingError_MethodGroup_BindingValue_1_T]:...
        @typing.overload
        def __call__(self, e: Exception, fallbackValue: BindingError_MethodGroup_BindingValue_1_T) -> BindingValue_1[BindingError_MethodGroup_BindingValue_1_T]:...

    # Skipped DataValidationError due to it being static, abstract and generic.

    DataValidationError : DataValidationError_MethodGroup[BindingValue_1_T]
    DataValidationError_MethodGroup_BindingValue_1_T = typing.TypeVar('DataValidationError_MethodGroup_BindingValue_1_T')
    class DataValidationError_MethodGroup(typing.Generic[DataValidationError_MethodGroup_BindingValue_1_T]):
        DataValidationError_MethodGroup_BindingValue_1_T = BindingValue_1.DataValidationError_MethodGroup_BindingValue_1_T
        @typing.overload
        def __call__(self, e: Exception) -> BindingValue_1[DataValidationError_MethodGroup_BindingValue_1_T]:...
        @typing.overload
        def __call__(self, e: Exception, fallbackValue: Optional_1[DataValidationError_MethodGroup_BindingValue_1_T]) -> BindingValue_1[DataValidationError_MethodGroup_BindingValue_1_T]:...
        @typing.overload
        def __call__(self, e: Exception, fallbackValue: DataValidationError_MethodGroup_BindingValue_1_T) -> BindingValue_1[DataValidationError_MethodGroup_BindingValue_1_T]:...

    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup[BindingValue_1_T]
    Equals_MethodGroup_BindingValue_1_T = typing.TypeVar('Equals_MethodGroup_BindingValue_1_T')
    class Equals_MethodGroup(typing.Generic[Equals_MethodGroup_BindingValue_1_T]):
        Equals_MethodGroup_BindingValue_1_T = BindingValue_1.Equals_MethodGroup_BindingValue_1_T
        @typing.overload
        def __call__(self, other: BindingValue_1[Equals_MethodGroup_BindingValue_1_T]) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...

    # Skipped FromUntyped due to it being static, abstract and generic.

    FromUntyped : FromUntyped_MethodGroup[BindingValue_1_T]
    FromUntyped_MethodGroup_BindingValue_1_T = typing.TypeVar('FromUntyped_MethodGroup_BindingValue_1_T')
    class FromUntyped_MethodGroup(typing.Generic[FromUntyped_MethodGroup_BindingValue_1_T]):
        FromUntyped_MethodGroup_BindingValue_1_T = BindingValue_1.FromUntyped_MethodGroup_BindingValue_1_T
        @typing.overload
        def __call__(self, value: typing.Any) -> BindingValue_1[FromUntyped_MethodGroup_BindingValue_1_T]:...
        @typing.overload
        def __call__(self, value: typing.Any, targetType: typing.Type[typing.Any]) -> BindingValue_1[FromUntyped_MethodGroup_BindingValue_1_T]:...

    # Skipped GetValueOrDefault due to it being static, abstract and generic.

    GetValueOrDefault : GetValueOrDefault_MethodGroup[BindingValue_1_T]
    GetValueOrDefault_MethodGroup_BindingValue_1_T = typing.TypeVar('GetValueOrDefault_MethodGroup_BindingValue_1_T')
    class GetValueOrDefault_MethodGroup(typing.Generic[GetValueOrDefault_MethodGroup_BindingValue_1_T]):
        GetValueOrDefault_MethodGroup_BindingValue_1_T = BindingValue_1.GetValueOrDefault_MethodGroup_BindingValue_1_T
        def __getitem__(self, t:typing.Type[GetValueOrDefault_1_T1]) -> GetValueOrDefault_1[GetValueOrDefault_MethodGroup_BindingValue_1_T, GetValueOrDefault_1_T1]: ...

        GetValueOrDefault_1_BindingValue_1_T = typing.TypeVar('GetValueOrDefault_1_BindingValue_1_T')
        GetValueOrDefault_1_T1 = typing.TypeVar('GetValueOrDefault_1_T1')
        class GetValueOrDefault_1(typing.Generic[GetValueOrDefault_1_BindingValue_1_T, GetValueOrDefault_1_T1]):
            GetValueOrDefault_1_BindingValue_1_T = BindingValue_1.GetValueOrDefault_MethodGroup.GetValueOrDefault_1_BindingValue_1_T
            GetValueOrDefault_1_TResult = BindingValue_1.GetValueOrDefault_MethodGroup.GetValueOrDefault_1_T1
            @typing.overload
            def __call__(self) -> GetValueOrDefault_1_TResult:...
            @typing.overload
            def __call__(self, defaultValue: GetValueOrDefault_1_TResult) -> GetValueOrDefault_1_TResult:...

        @typing.overload
        def __call__(self) -> GetValueOrDefault_MethodGroup_BindingValue_1_T:...
        @typing.overload
        def __call__(self, defaultValue: GetValueOrDefault_MethodGroup_BindingValue_1_T) -> GetValueOrDefault_MethodGroup_BindingValue_1_T:...



class BindingValueType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    UnsetValue : BindingValueType # 0
    DoNothing : BindingValueType # 1
    TypeMask : BindingValueType # 255
    HasValue : BindingValueType # 256
    Value : BindingValueType # 258
    HasError : BindingValueType # 512
    BindingError : BindingValueType # 515
    DataValidationError : BindingValueType # 516
    BindingErrorWithFallback : BindingValueType # 771
    DataValidationErrorWithFallback : BindingValueType # 772


class IBinding(typing.Protocol):
    @abc.abstractmethod
    def Initiate(self, target: AvaloniaObject, targetProperty: AvaloniaProperty, anchor: typing.Any = ..., enableDataValidation: bool = ...) -> InstancedBinding: ...


class IndexerDescriptor(IDescription, IObservable_1[typing.Any]):
    def __init__(self) -> None: ...
    @property
    def Description(self) -> str: ...
    @property
    def Mode(self) -> BindingMode: ...
    @Mode.setter
    def Mode(self, value: BindingMode) -> BindingMode: ...
    @property
    def Priority(self) -> BindingPriority: ...
    @Priority.setter
    def Priority(self, value: BindingPriority) -> BindingPriority: ...
    @property
    def Property(self) -> AvaloniaProperty: ...
    @Property.setter
    def Property(self, value: AvaloniaProperty) -> AvaloniaProperty: ...
    @property
    def Source(self) -> AvaloniaObject: ...
    @Source.setter
    def Source(self, value: AvaloniaObject) -> AvaloniaObject: ...
    @property
    def SourceObservable(self) -> IObservable_1[typing.Any]: ...
    @SourceObservable.setter
    def SourceObservable(self, value: IObservable_1[typing.Any]) -> IObservable_1[typing.Any]: ...
    # Operator not supported op_LogicalNot(binding: IndexerDescriptor)
    def __invert__(self, binding: IndexerDescriptor) -> IndexerDescriptor: ...
    def Subscribe(self, observer: IObserver_1[typing.Any]) -> IDisposable: ...
    def WithMode(self, mode: BindingMode) -> IndexerDescriptor: ...
    def WithPriority(self, priority: BindingPriority) -> IndexerDescriptor: ...


class InstancedBinding:
    @property
    def Mode(self) -> BindingMode: ...
    @property
    def Observable(self) -> IObservable_1[typing.Any]: ...
    @property
    def Priority(self) -> BindingPriority: ...
    @property
    def Source(self) -> IObservable_1[typing.Any]: ...
    @staticmethod
    def OneWay(observable: IObservable_1[typing.Any], priority: BindingPriority = ...) -> InstancedBinding: ...
    @staticmethod
    def OneWayToSource(observer: IObserver_1[typing.Any], priority: BindingPriority = ...) -> InstancedBinding: ...
    @staticmethod
    def TwoWay(observable: IObservable_1[typing.Any], observer: IObserver_1[typing.Any], priority: BindingPriority = ...) -> InstancedBinding: ...
    def WithPriority(self, priority: BindingPriority) -> InstancedBinding: ...
    # Skipped OneTime due to it being static, abstract and generic.

    OneTime : OneTime_MethodGroup
    class OneTime_MethodGroup:
        @typing.overload
        def __call__(self, observable: IObservable_1[typing.Any], priority: BindingPriority = ...) -> InstancedBinding:...
        @typing.overload
        def __call__(self, value: typing.Any, priority: BindingPriority = ...) -> InstancedBinding:...



class Optional_GenericClasses(abc.ABCMeta):
    Generic_Optional_GenericClasses_Optional_1_T = typing.TypeVar('Generic_Optional_GenericClasses_Optional_1_T')
    def __getitem__(self, types : typing.Type[Generic_Optional_GenericClasses_Optional_1_T]) -> typing.Type[Optional_1[Generic_Optional_GenericClasses_Optional_1_T]]: ...

Optional : Optional_GenericClasses

Optional_1_T = typing.TypeVar('Optional_1_T')
class Optional_1(typing.Generic[Optional_1_T], IEquatable_1[Optional_1[Optional_1_T]]):
    def __init__(self, value: Optional_1_T) -> None: ...
    @classmethod
    @property
    def Empty(cls) -> Optional_1[Optional_1_T]: ...
    @property
    def HasValue(self) -> bool: ...
    @property
    def Value(self) -> Optional_1_T: ...
    def GetHashCode(self) -> int: ...
    def __eq__(self, x: Optional_1[Optional_1_T], y: Optional_1[Optional_1_T]) -> bool: ...
    # Operator not supported op_Implicit(value: T)
    def __ne__(self, x: Optional_1[Optional_1_T], y: Optional_1[Optional_1_T]) -> bool: ...
    def ToObject(self) -> Optional_1[typing.Any]: ...
    def ToString(self) -> str: ...
    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup[Optional_1_T]
    Equals_MethodGroup_Optional_1_T = typing.TypeVar('Equals_MethodGroup_Optional_1_T')
    class Equals_MethodGroup(typing.Generic[Equals_MethodGroup_Optional_1_T]):
        Equals_MethodGroup_Optional_1_T = Optional_1.Equals_MethodGroup_Optional_1_T
        @typing.overload
        def __call__(self, other: Optional_1[Equals_MethodGroup_Optional_1_T]) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...

    # Skipped GetValueOrDefault due to it being static, abstract and generic.

    GetValueOrDefault : GetValueOrDefault_MethodGroup[Optional_1_T]
    GetValueOrDefault_MethodGroup_Optional_1_T = typing.TypeVar('GetValueOrDefault_MethodGroup_Optional_1_T')
    class GetValueOrDefault_MethodGroup(typing.Generic[GetValueOrDefault_MethodGroup_Optional_1_T]):
        GetValueOrDefault_MethodGroup_Optional_1_T = Optional_1.GetValueOrDefault_MethodGroup_Optional_1_T
        def __getitem__(self, t:typing.Type[GetValueOrDefault_1_T1]) -> GetValueOrDefault_1[GetValueOrDefault_MethodGroup_Optional_1_T, GetValueOrDefault_1_T1]: ...

        GetValueOrDefault_1_Optional_1_T = typing.TypeVar('GetValueOrDefault_1_Optional_1_T')
        GetValueOrDefault_1_T1 = typing.TypeVar('GetValueOrDefault_1_T1')
        class GetValueOrDefault_1(typing.Generic[GetValueOrDefault_1_Optional_1_T, GetValueOrDefault_1_T1]):
            GetValueOrDefault_1_Optional_1_T = Optional_1.GetValueOrDefault_MethodGroup.GetValueOrDefault_1_Optional_1_T
            GetValueOrDefault_1_TResult = Optional_1.GetValueOrDefault_MethodGroup.GetValueOrDefault_1_T1
            @typing.overload
            def __call__(self) -> GetValueOrDefault_1_TResult:...
            @typing.overload
            def __call__(self, defaultValue: GetValueOrDefault_1_TResult) -> GetValueOrDefault_1_TResult:...

        @typing.overload
        def __call__(self) -> GetValueOrDefault_MethodGroup_Optional_1_T:...
        @typing.overload
        def __call__(self, defaultValue: GetValueOrDefault_MethodGroup_Optional_1_T) -> GetValueOrDefault_MethodGroup_Optional_1_T:...


