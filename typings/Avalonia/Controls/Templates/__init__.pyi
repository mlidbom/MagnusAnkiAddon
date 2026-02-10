import typing, clr, abc
from Avalonia.Collections import AvaloniaList_1, ResetBehavior
from System import Action_1
from Avalonia.Controls.Primitives import TemplatedControl
from Avalonia.Controls import Control, INameScope

class DataTemplates(AvaloniaList_1[IDataTemplate]):
    def __init__(self) -> None: ...
    @property
    def Capacity(self) -> int: ...
    @Capacity.setter
    def Capacity(self, value: int) -> int: ...
    @property
    def Count(self) -> int: ...
    @property
    def ResetBehavior(self) -> ResetBehavior: ...
    @ResetBehavior.setter
    def ResetBehavior(self, value: ResetBehavior) -> ResetBehavior: ...
    @property
    def Validate(self) -> Action_1[IDataTemplate]: ...
    @Validate.setter
    def Validate(self, value: Action_1[IDataTemplate]) -> Action_1[IDataTemplate]: ...
    def __getitem__(self, index: int) -> IDataTemplate: ...
    def __setitem__(self, index: int, value: IDataTemplate) -> None: ...


class IControlTemplate(ITemplate_2[TemplatedControl, TemplateResult_1[Control]], typing.Protocol):
    pass


class IDataTemplate(ITemplate_2[typing.Any, Control], typing.Protocol):
    @abc.abstractmethod
    def Match(self, data: typing.Any) -> bool: ...


class IDataTemplateHost(typing.Protocol):
    @property
    def DataTemplates(self) -> DataTemplates: ...
    @property
    def IsDataTemplatesInitialized(self) -> bool: ...


class ITemplate_GenericClasses(abc.ABCMeta):
    Generic_ITemplate_GenericClasses_ITemplate_2_TParam = typing.TypeVar('Generic_ITemplate_GenericClasses_ITemplate_2_TParam')
    Generic_ITemplate_GenericClasses_ITemplate_2_TControl = typing.TypeVar('Generic_ITemplate_GenericClasses_ITemplate_2_TControl')
    def __getitem__(self, types : typing.Tuple[typing.Type[Generic_ITemplate_GenericClasses_ITemplate_2_TParam], typing.Type[Generic_ITemplate_GenericClasses_ITemplate_2_TControl]]) -> typing.Type[ITemplate_2[Generic_ITemplate_GenericClasses_ITemplate_2_TParam, Generic_ITemplate_GenericClasses_ITemplate_2_TControl]]: ...

ITemplate : ITemplate_GenericClasses

ITemplate_2_TParam = typing.TypeVar('ITemplate_2_TParam')
ITemplate_2_TControl = typing.TypeVar('ITemplate_2_TControl')
class ITemplate_2(typing.Generic[ITemplate_2_TParam, ITemplate_2_TControl], typing.Protocol):
    @abc.abstractmethod
    def Build(self, param: ITemplate_2_TParam) -> ITemplate_2_TControl: ...


class ITemplateResult(typing.Protocol):
    @property
    def NameScope(self) -> INameScope: ...
    @property
    def Result(self) -> typing.Any: ...


class TemplateResult_GenericClasses(abc.ABCMeta):
    Generic_TemplateResult_GenericClasses_TemplateResult_1_T = typing.TypeVar('Generic_TemplateResult_GenericClasses_TemplateResult_1_T')
    def __getitem__(self, types : typing.Type[Generic_TemplateResult_GenericClasses_TemplateResult_1_T]) -> typing.Type[TemplateResult_1[Generic_TemplateResult_GenericClasses_TemplateResult_1_T]]: ...

TemplateResult : TemplateResult_GenericClasses

TemplateResult_1_T = typing.TypeVar('TemplateResult_1_T')
class TemplateResult_1(typing.Generic[TemplateResult_1_T], ITemplateResult):
    def __init__(self, result: TemplateResult_1_T, nameScope: INameScope) -> None: ...
    @property
    def NameScope(self) -> INameScope: ...
    @property
    def Result(self) -> TemplateResult_1_T: ...
    def Deconstruct(self, result: clr.Reference[TemplateResult_1_T], scope: clr.Reference[INameScope]) -> None: ...

