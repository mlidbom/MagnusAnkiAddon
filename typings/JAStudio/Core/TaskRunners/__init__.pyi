import typing, abc
from System.Collections.Generic import List_1
from System import Func_2, Func_1, IDisposable, Func_5
from System.Threading.Tasks import Task_1
from JAStudio.Core.Configuration import JapaneseConfig

class InvisibleTaskRunner(ITaskProgressRunner):
    def __init__(self, windowTitle: str, labelText: str) -> None: ...
    def Close(self) -> None: ...
    def Dispose(self) -> None: ...
    def IsHidden(self) -> bool: ...
    def RunGc(self) -> None: ...
    def SetLabelText(self, labelText: str) -> None: ...
    # Skipped ProcessWithProgress due to it being static, abstract and generic.

    ProcessWithProgress : ProcessWithProgress_MethodGroup
    class ProcessWithProgress_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[ProcessWithProgress_2_T1], typing.Type[ProcessWithProgress_2_T2]]) -> ProcessWithProgress_2[ProcessWithProgress_2_T1, ProcessWithProgress_2_T2]: ...

        ProcessWithProgress_2_T1 = typing.TypeVar('ProcessWithProgress_2_T1')
        ProcessWithProgress_2_T2 = typing.TypeVar('ProcessWithProgress_2_T2')
        class ProcessWithProgress_2(typing.Generic[ProcessWithProgress_2_T1, ProcessWithProgress_2_T2]):
            ProcessWithProgress_2_TInput = InvisibleTaskRunner.ProcessWithProgress_MethodGroup.ProcessWithProgress_2_T1
            ProcessWithProgress_2_TOutput = InvisibleTaskRunner.ProcessWithProgress_MethodGroup.ProcessWithProgress_2_T2
            def __call__(self, items: List_1[ProcessWithProgress_2_TInput], processItem: Func_2[ProcessWithProgress_2_TInput, ProcessWithProgress_2_TOutput], message: str, runGc: bool = ..., minimumItemsToGc: int = ...) -> List_1[ProcessWithProgress_2_TOutput]:...


    # Skipped ProcessWithProgressAsync due to it being static, abstract and generic.

    ProcessWithProgressAsync : ProcessWithProgressAsync_MethodGroup
    class ProcessWithProgressAsync_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[ProcessWithProgressAsync_2_T1], typing.Type[ProcessWithProgressAsync_2_T2]]) -> ProcessWithProgressAsync_2[ProcessWithProgressAsync_2_T1, ProcessWithProgressAsync_2_T2]: ...

        ProcessWithProgressAsync_2_T1 = typing.TypeVar('ProcessWithProgressAsync_2_T1')
        ProcessWithProgressAsync_2_T2 = typing.TypeVar('ProcessWithProgressAsync_2_T2')
        class ProcessWithProgressAsync_2(typing.Generic[ProcessWithProgressAsync_2_T1, ProcessWithProgressAsync_2_T2]):
            ProcessWithProgressAsync_2_TInput = InvisibleTaskRunner.ProcessWithProgressAsync_MethodGroup.ProcessWithProgressAsync_2_T1
            ProcessWithProgressAsync_2_TOutput = InvisibleTaskRunner.ProcessWithProgressAsync_MethodGroup.ProcessWithProgressAsync_2_T2
            def __call__(self, items: List_1[ProcessWithProgressAsync_2_TInput], processItem: Func_2[ProcessWithProgressAsync_2_TInput, ProcessWithProgressAsync_2_TOutput], message: str) -> Task_1[List_1[ProcessWithProgressAsync_2_TOutput]]:...


    # Skipped RunOnBackgroundThreadAsync due to it being static, abstract and generic.

    RunOnBackgroundThreadAsync : RunOnBackgroundThreadAsync_MethodGroup
    class RunOnBackgroundThreadAsync_MethodGroup:
        def __getitem__(self, t:typing.Type[RunOnBackgroundThreadAsync_1_T1]) -> RunOnBackgroundThreadAsync_1[RunOnBackgroundThreadAsync_1_T1]: ...

        RunOnBackgroundThreadAsync_1_T1 = typing.TypeVar('RunOnBackgroundThreadAsync_1_T1')
        class RunOnBackgroundThreadAsync_1(typing.Generic[RunOnBackgroundThreadAsync_1_T1]):
            RunOnBackgroundThreadAsync_1_TResult = InvisibleTaskRunner.RunOnBackgroundThreadAsync_MethodGroup.RunOnBackgroundThreadAsync_1_T1
            def __call__(self, message: str, action: Func_1[RunOnBackgroundThreadAsync_1_TResult]) -> Task_1[RunOnBackgroundThreadAsync_1_TResult]:...


    # Skipped RunOnBackgroundThreadWithSpinningProgressDialog due to it being static, abstract and generic.

    RunOnBackgroundThreadWithSpinningProgressDialog : RunOnBackgroundThreadWithSpinningProgressDialog_MethodGroup
    class RunOnBackgroundThreadWithSpinningProgressDialog_MethodGroup:
        def __getitem__(self, t:typing.Type[RunOnBackgroundThreadWithSpinningProgressDialog_1_T1]) -> RunOnBackgroundThreadWithSpinningProgressDialog_1[RunOnBackgroundThreadWithSpinningProgressDialog_1_T1]: ...

        RunOnBackgroundThreadWithSpinningProgressDialog_1_T1 = typing.TypeVar('RunOnBackgroundThreadWithSpinningProgressDialog_1_T1')
        class RunOnBackgroundThreadWithSpinningProgressDialog_1(typing.Generic[RunOnBackgroundThreadWithSpinningProgressDialog_1_T1]):
            RunOnBackgroundThreadWithSpinningProgressDialog_1_TResult = InvisibleTaskRunner.RunOnBackgroundThreadWithSpinningProgressDialog_MethodGroup.RunOnBackgroundThreadWithSpinningProgressDialog_1_T1
            def __call__(self, message: str, action: Func_1[RunOnBackgroundThreadWithSpinningProgressDialog_1_TResult]) -> RunOnBackgroundThreadWithSpinningProgressDialog_1_TResult:...




class ITaskProgressRunner(IDisposable, typing.Protocol):
    @abc.abstractmethod
    def Close(self) -> None: ...
    @abc.abstractmethod
    def IsHidden(self) -> bool: ...
    @abc.abstractmethod
    def RunGc(self) -> None: ...
    @abc.abstractmethod
    def SetLabelText(self, text: str) -> None: ...
    # Skipped ProcessWithProgress due to it being static, abstract and generic.

    ProcessWithProgress : ProcessWithProgress_MethodGroup
    class ProcessWithProgress_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[ProcessWithProgress_2_T1], typing.Type[ProcessWithProgress_2_T2]]) -> ProcessWithProgress_2[ProcessWithProgress_2_T1, ProcessWithProgress_2_T2]: ...

        ProcessWithProgress_2_T1 = typing.TypeVar('ProcessWithProgress_2_T1')
        ProcessWithProgress_2_T2 = typing.TypeVar('ProcessWithProgress_2_T2')
        class ProcessWithProgress_2(typing.Generic[ProcessWithProgress_2_T1, ProcessWithProgress_2_T2]):
            ProcessWithProgress_2_TInput = ITaskProgressRunner.ProcessWithProgress_MethodGroup.ProcessWithProgress_2_T1
            ProcessWithProgress_2_TOutput = ITaskProgressRunner.ProcessWithProgress_MethodGroup.ProcessWithProgress_2_T2
            def __call__(self, items: List_1[ProcessWithProgress_2_TInput], processItem: Func_2[ProcessWithProgress_2_TInput, ProcessWithProgress_2_TOutput], message: str, runGc: bool = ..., minimumItemsToGc: int = ...) -> List_1[ProcessWithProgress_2_TOutput]:...


    # Skipped ProcessWithProgressAsync due to it being static, abstract and generic.

    ProcessWithProgressAsync : ProcessWithProgressAsync_MethodGroup
    class ProcessWithProgressAsync_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[ProcessWithProgressAsync_2_T1], typing.Type[ProcessWithProgressAsync_2_T2]]) -> ProcessWithProgressAsync_2[ProcessWithProgressAsync_2_T1, ProcessWithProgressAsync_2_T2]: ...

        ProcessWithProgressAsync_2_T1 = typing.TypeVar('ProcessWithProgressAsync_2_T1')
        ProcessWithProgressAsync_2_T2 = typing.TypeVar('ProcessWithProgressAsync_2_T2')
        class ProcessWithProgressAsync_2(typing.Generic[ProcessWithProgressAsync_2_T1, ProcessWithProgressAsync_2_T2]):
            ProcessWithProgressAsync_2_TInput = ITaskProgressRunner.ProcessWithProgressAsync_MethodGroup.ProcessWithProgressAsync_2_T1
            ProcessWithProgressAsync_2_TOutput = ITaskProgressRunner.ProcessWithProgressAsync_MethodGroup.ProcessWithProgressAsync_2_T2
            def __call__(self, items: List_1[ProcessWithProgressAsync_2_TInput], processItem: Func_2[ProcessWithProgressAsync_2_TInput, ProcessWithProgressAsync_2_TOutput], message: str) -> Task_1[List_1[ProcessWithProgressAsync_2_TOutput]]:...


    # Skipped RunOnBackgroundThreadAsync due to it being static, abstract and generic.

    RunOnBackgroundThreadAsync : RunOnBackgroundThreadAsync_MethodGroup
    class RunOnBackgroundThreadAsync_MethodGroup:
        def __getitem__(self, t:typing.Type[RunOnBackgroundThreadAsync_1_T1]) -> RunOnBackgroundThreadAsync_1[RunOnBackgroundThreadAsync_1_T1]: ...

        RunOnBackgroundThreadAsync_1_T1 = typing.TypeVar('RunOnBackgroundThreadAsync_1_T1')
        class RunOnBackgroundThreadAsync_1(typing.Generic[RunOnBackgroundThreadAsync_1_T1]):
            RunOnBackgroundThreadAsync_1_TResult = ITaskProgressRunner.RunOnBackgroundThreadAsync_MethodGroup.RunOnBackgroundThreadAsync_1_T1
            def __call__(self, message: str, action: Func_1[RunOnBackgroundThreadAsync_1_TResult]) -> Task_1[RunOnBackgroundThreadAsync_1_TResult]:...


    # Skipped RunOnBackgroundThreadWithSpinningProgressDialog due to it being static, abstract and generic.

    RunOnBackgroundThreadWithSpinningProgressDialog : RunOnBackgroundThreadWithSpinningProgressDialog_MethodGroup
    class RunOnBackgroundThreadWithSpinningProgressDialog_MethodGroup:
        def __getitem__(self, t:typing.Type[RunOnBackgroundThreadWithSpinningProgressDialog_1_T1]) -> RunOnBackgroundThreadWithSpinningProgressDialog_1[RunOnBackgroundThreadWithSpinningProgressDialog_1_T1]: ...

        RunOnBackgroundThreadWithSpinningProgressDialog_1_T1 = typing.TypeVar('RunOnBackgroundThreadWithSpinningProgressDialog_1_T1')
        class RunOnBackgroundThreadWithSpinningProgressDialog_1(typing.Generic[RunOnBackgroundThreadWithSpinningProgressDialog_1_T1]):
            RunOnBackgroundThreadWithSpinningProgressDialog_1_TResult = ITaskProgressRunner.RunOnBackgroundThreadWithSpinningProgressDialog_MethodGroup.RunOnBackgroundThreadWithSpinningProgressDialog_1_T1
            def __call__(self, message: str, action: Func_1[RunOnBackgroundThreadWithSpinningProgressDialog_1_TResult]) -> RunOnBackgroundThreadWithSpinningProgressDialog_1_TResult:...




class TaskRunner:
    def Create(self, windowTitle: str, labelText: str, visible: typing.Optional[bool] = ..., allowCancel: bool = ..., modal: bool = ...) -> ITaskProgressRunner: ...
    def Current(self, windowTitle: str, labelText: str = ..., forceHide: bool = ..., inhibitGc: bool = ..., forceGc: bool = ..., allowCancel: bool = ..., modal: bool = ...) -> TaskRunnerScope: ...
    def SetUiTaskRunnerFactory(self, factory: Func_5[str, str, bool, bool, ITaskProgressRunner]) -> None: ...


class TaskRunnerScope(IDisposable):
    def __init__(self, taskRunner: TaskRunner, config: JapaneseConfig, windowTitle: str, labelText: str, forceHide: bool, inhibitGc: bool, forceGc: bool, allowCancel: bool, modal: bool) -> None: ...
    @property
    def Runner(self) -> ITaskProgressRunner: ...
    def Dispose(self) -> None: ...

