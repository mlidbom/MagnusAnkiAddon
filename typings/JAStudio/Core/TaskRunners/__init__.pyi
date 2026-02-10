import typing
from System.Collections.Generic import List_1
from System import Func_2, Func_1, IDisposable, Action_1, Action, Func_5, IEquatable_1
from System.Threading.Tasks import Task_1, Task, ParallelOptions

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
            def __call__(self, items: List_1[ProcessWithProgress_2_TInput], processItem: Func_2[ProcessWithProgress_2_TInput, ProcessWithProgress_2_TOutput], message: str, threads: ThreadCount) -> List_1[ProcessWithProgress_2_TOutput]:...


    # Skipped ProcessWithProgressAsync due to it being static, abstract and generic.

    ProcessWithProgressAsync : ProcessWithProgressAsync_MethodGroup
    class ProcessWithProgressAsync_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[ProcessWithProgressAsync_2_T1], typing.Type[ProcessWithProgressAsync_2_T2]]) -> ProcessWithProgressAsync_2[ProcessWithProgressAsync_2_T1, ProcessWithProgressAsync_2_T2]: ...

        ProcessWithProgressAsync_2_T1 = typing.TypeVar('ProcessWithProgressAsync_2_T1')
        ProcessWithProgressAsync_2_T2 = typing.TypeVar('ProcessWithProgressAsync_2_T2')
        class ProcessWithProgressAsync_2(typing.Generic[ProcessWithProgressAsync_2_T1, ProcessWithProgressAsync_2_T2]):
            ProcessWithProgressAsync_2_TInput = InvisibleTaskRunner.ProcessWithProgressAsync_MethodGroup.ProcessWithProgressAsync_2_T1
            ProcessWithProgressAsync_2_TOutput = InvisibleTaskRunner.ProcessWithProgressAsync_MethodGroup.ProcessWithProgressAsync_2_T2
            def __call__(self, items: List_1[ProcessWithProgressAsync_2_TInput], processItem: Func_2[ProcessWithProgressAsync_2_TInput, ProcessWithProgressAsync_2_TOutput], message: str, threads: ThreadCount) -> Task_1[List_1[ProcessWithProgressAsync_2_TOutput]]:...


    # Skipped RunOnBackgroundThreadWithSpinningProgressDialog due to it being static, abstract and generic.

    RunOnBackgroundThreadWithSpinningProgressDialog : RunOnBackgroundThreadWithSpinningProgressDialog_MethodGroup
    class RunOnBackgroundThreadWithSpinningProgressDialog_MethodGroup:
        def __getitem__(self, t:typing.Type[RunOnBackgroundThreadWithSpinningProgressDialog_1_T1]) -> RunOnBackgroundThreadWithSpinningProgressDialog_1[RunOnBackgroundThreadWithSpinningProgressDialog_1_T1]: ...

        RunOnBackgroundThreadWithSpinningProgressDialog_1_T1 = typing.TypeVar('RunOnBackgroundThreadWithSpinningProgressDialog_1_T1')
        class RunOnBackgroundThreadWithSpinningProgressDialog_1(typing.Generic[RunOnBackgroundThreadWithSpinningProgressDialog_1_T1]):
            RunOnBackgroundThreadWithSpinningProgressDialog_1_TResult = InvisibleTaskRunner.RunOnBackgroundThreadWithSpinningProgressDialog_MethodGroup.RunOnBackgroundThreadWithSpinningProgressDialog_1_T1
            def __call__(self, message: str, action: Func_1[RunOnBackgroundThreadWithSpinningProgressDialog_1_TResult]) -> RunOnBackgroundThreadWithSpinningProgressDialog_1_TResult:...


    # Skipped RunOnBackgroundThreadWithSpinningProgressDialogAsync due to it being static, abstract and generic.

    RunOnBackgroundThreadWithSpinningProgressDialogAsync : RunOnBackgroundThreadWithSpinningProgressDialogAsync_MethodGroup
    class RunOnBackgroundThreadWithSpinningProgressDialogAsync_MethodGroup:
        def __getitem__(self, t:typing.Type[RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1]) -> RunOnBackgroundThreadWithSpinningProgressDialogAsync_1[RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1]: ...

        RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1 = typing.TypeVar('RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1')
        class RunOnBackgroundThreadWithSpinningProgressDialogAsync_1(typing.Generic[RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1]):
            RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_TResult = InvisibleTaskRunner.RunOnBackgroundThreadWithSpinningProgressDialogAsync_MethodGroup.RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1
            def __call__(self, message: str, action: Func_1[RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_TResult]) -> Task_1[RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_TResult]:...




class ITaskProgressRunner(IDisposable, typing.Protocol):
    # Skipped ProcessWithProgress due to it being static, abstract and generic.

    ProcessWithProgress : ProcessWithProgress_MethodGroup
    class ProcessWithProgress_MethodGroup:
        @typing.overload
        def __getitem__(self, t:typing.Type[ProcessWithProgress_1_T1]) -> ProcessWithProgress_1[ProcessWithProgress_1_T1]: ...

        ProcessWithProgress_1_T1 = typing.TypeVar('ProcessWithProgress_1_T1')
        class ProcessWithProgress_1(typing.Generic[ProcessWithProgress_1_T1]):
            ProcessWithProgress_1_TInput = ITaskProgressRunner.ProcessWithProgress_MethodGroup.ProcessWithProgress_1_T1
            @typing.overload
            def __call__(self, items: List_1[ProcessWithProgress_1_TInput], processItem: Action_1[ProcessWithProgress_1_TInput], message: str) -> None:...
            @typing.overload
            def __call__(self, items: List_1[ProcessWithProgress_1_TInput], processItem: Action_1[ProcessWithProgress_1_TInput], message: str, threads: ThreadCount) -> None:...

        @typing.overload
        def __getitem__(self, t:typing.Tuple[typing.Type[ProcessWithProgress_2_T1], typing.Type[ProcessWithProgress_2_T2]]) -> ProcessWithProgress_2[ProcessWithProgress_2_T1, ProcessWithProgress_2_T2]: ...

        ProcessWithProgress_2_T1 = typing.TypeVar('ProcessWithProgress_2_T1')
        ProcessWithProgress_2_T2 = typing.TypeVar('ProcessWithProgress_2_T2')
        class ProcessWithProgress_2(typing.Generic[ProcessWithProgress_2_T1, ProcessWithProgress_2_T2]):
            ProcessWithProgress_2_TInput = ITaskProgressRunner.ProcessWithProgress_MethodGroup.ProcessWithProgress_2_T1
            ProcessWithProgress_2_TOutput = ITaskProgressRunner.ProcessWithProgress_MethodGroup.ProcessWithProgress_2_T2
            @typing.overload
            def __call__(self, items: List_1[ProcessWithProgress_2_TInput], processItem: Func_2[ProcessWithProgress_2_TInput, ProcessWithProgress_2_TOutput], message: str) -> List_1[ProcessWithProgress_2_TOutput]:...
            @typing.overload
            def __call__(self, items: List_1[ProcessWithProgress_2_TInput], processItem: Func_2[ProcessWithProgress_2_TInput, ProcessWithProgress_2_TOutput], message: str, threads: ThreadCount) -> List_1[ProcessWithProgress_2_TOutput]:...


    # Skipped ProcessWithProgressAsync due to it being static, abstract and generic.

    ProcessWithProgressAsync : ProcessWithProgressAsync_MethodGroup
    class ProcessWithProgressAsync_MethodGroup:
        @typing.overload
        def __getitem__(self, t:typing.Tuple[typing.Type[ProcessWithProgressAsync_2_T1], typing.Type[ProcessWithProgressAsync_2_T2]]) -> ProcessWithProgressAsync_2[ProcessWithProgressAsync_2_T1, ProcessWithProgressAsync_2_T2]: ...

        ProcessWithProgressAsync_2_T1 = typing.TypeVar('ProcessWithProgressAsync_2_T1')
        ProcessWithProgressAsync_2_T2 = typing.TypeVar('ProcessWithProgressAsync_2_T2')
        class ProcessWithProgressAsync_2(typing.Generic[ProcessWithProgressAsync_2_T1, ProcessWithProgressAsync_2_T2]):
            ProcessWithProgressAsync_2_TInput = ITaskProgressRunner.ProcessWithProgressAsync_MethodGroup.ProcessWithProgressAsync_2_T1
            ProcessWithProgressAsync_2_TOutput = ITaskProgressRunner.ProcessWithProgressAsync_MethodGroup.ProcessWithProgressAsync_2_T2
            @typing.overload
            def __call__(self, items: List_1[ProcessWithProgressAsync_2_TInput], processItem: Func_2[ProcessWithProgressAsync_2_TInput, ProcessWithProgressAsync_2_TOutput], message: str) -> Task_1[List_1[ProcessWithProgressAsync_2_TOutput]]:...
            @typing.overload
            def __call__(self, items: List_1[ProcessWithProgressAsync_2_TInput], processItem: Func_2[ProcessWithProgressAsync_2_TInput, ProcessWithProgressAsync_2_TOutput], message: str, threadCount: ThreadCount) -> Task_1[List_1[ProcessWithProgressAsync_2_TOutput]]:...

        @typing.overload
        def __getitem__(self, t:typing.Type[ProcessWithProgressAsync_1_T1]) -> ProcessWithProgressAsync_1[ProcessWithProgressAsync_1_T1]: ...

        ProcessWithProgressAsync_1_T1 = typing.TypeVar('ProcessWithProgressAsync_1_T1')
        class ProcessWithProgressAsync_1(typing.Generic[ProcessWithProgressAsync_1_T1]):
            ProcessWithProgressAsync_1_TInput = ITaskProgressRunner.ProcessWithProgressAsync_MethodGroup.ProcessWithProgressAsync_1_T1
            @typing.overload
            def __call__(self, items: List_1[ProcessWithProgressAsync_1_TInput], processItem: Action_1[ProcessWithProgressAsync_1_TInput], message: str) -> Task:...
            @typing.overload
            def __call__(self, items: List_1[ProcessWithProgressAsync_1_TInput], processItem: Action_1[ProcessWithProgressAsync_1_TInput], message: str, threadCount: ThreadCount) -> Task:...


    # Skipped RunOnBackgroundThreadWithSpinningProgressDialog due to it being static, abstract and generic.

    RunOnBackgroundThreadWithSpinningProgressDialog : RunOnBackgroundThreadWithSpinningProgressDialog_MethodGroup
    class RunOnBackgroundThreadWithSpinningProgressDialog_MethodGroup:
        def __getitem__(self, t:typing.Type[RunOnBackgroundThreadWithSpinningProgressDialog_1_T1]) -> RunOnBackgroundThreadWithSpinningProgressDialog_1[RunOnBackgroundThreadWithSpinningProgressDialog_1_T1]: ...

        RunOnBackgroundThreadWithSpinningProgressDialog_1_T1 = typing.TypeVar('RunOnBackgroundThreadWithSpinningProgressDialog_1_T1')
        class RunOnBackgroundThreadWithSpinningProgressDialog_1(typing.Generic[RunOnBackgroundThreadWithSpinningProgressDialog_1_T1]):
            RunOnBackgroundThreadWithSpinningProgressDialog_1_TResult = ITaskProgressRunner.RunOnBackgroundThreadWithSpinningProgressDialog_MethodGroup.RunOnBackgroundThreadWithSpinningProgressDialog_1_T1
            def __call__(self, message: str, action: Func_1[RunOnBackgroundThreadWithSpinningProgressDialog_1_TResult]) -> RunOnBackgroundThreadWithSpinningProgressDialog_1_TResult:...


    # Skipped RunOnBackgroundThreadWithSpinningProgressDialogAsync due to it being static, abstract and generic.

    RunOnBackgroundThreadWithSpinningProgressDialogAsync : RunOnBackgroundThreadWithSpinningProgressDialogAsync_MethodGroup
    class RunOnBackgroundThreadWithSpinningProgressDialogAsync_MethodGroup:
        def __getitem__(self, t:typing.Type[RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1]) -> RunOnBackgroundThreadWithSpinningProgressDialogAsync_1[RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1]: ...

        RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1 = typing.TypeVar('RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1')
        class RunOnBackgroundThreadWithSpinningProgressDialogAsync_1(typing.Generic[RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1]):
            RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_TResult = ITaskProgressRunner.RunOnBackgroundThreadWithSpinningProgressDialogAsync_MethodGroup.RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1
            def __call__(self, message: str, action: Func_1[RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_TResult]) -> Task_1[RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_TResult]:...

        def __call__(self, message: str, action: Action) -> Task:...



class TaskRunner:
    def Current(self, windowTitle: str, forceHide: bool = ..., allowCancel: bool = ..., modal: bool = ...) -> ITaskProgressRunner: ...
    def SetUiTaskRunnerFactory(self, factory: Func_5[str, str, bool, bool, ITaskProgressRunner]) -> None: ...


class TaskRunnerScope(ITaskProgressRunner):
    def Close(self) -> None: ...
    def Dispose(self) -> None: ...
    def IsHidden(self) -> bool: ...
    def RunGc(self) -> None: ...
    def SetLabelText(self, text: str) -> None: ...
    # Skipped ProcessWithProgress due to it being static, abstract and generic.

    ProcessWithProgress : ProcessWithProgress_MethodGroup
    class ProcessWithProgress_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[ProcessWithProgress_2_T1], typing.Type[ProcessWithProgress_2_T2]]) -> ProcessWithProgress_2[ProcessWithProgress_2_T1, ProcessWithProgress_2_T2]: ...

        ProcessWithProgress_2_T1 = typing.TypeVar('ProcessWithProgress_2_T1')
        ProcessWithProgress_2_T2 = typing.TypeVar('ProcessWithProgress_2_T2')
        class ProcessWithProgress_2(typing.Generic[ProcessWithProgress_2_T1, ProcessWithProgress_2_T2]):
            ProcessWithProgress_2_TInput = TaskRunnerScope.ProcessWithProgress_MethodGroup.ProcessWithProgress_2_T1
            ProcessWithProgress_2_TOutput = TaskRunnerScope.ProcessWithProgress_MethodGroup.ProcessWithProgress_2_T2
            def __call__(self, items: List_1[ProcessWithProgress_2_TInput], processItem: Func_2[ProcessWithProgress_2_TInput, ProcessWithProgress_2_TOutput], message: str, threads: ThreadCount) -> List_1[ProcessWithProgress_2_TOutput]:...


    # Skipped ProcessWithProgressAsync due to it being static, abstract and generic.

    ProcessWithProgressAsync : ProcessWithProgressAsync_MethodGroup
    class ProcessWithProgressAsync_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[ProcessWithProgressAsync_2_T1], typing.Type[ProcessWithProgressAsync_2_T2]]) -> ProcessWithProgressAsync_2[ProcessWithProgressAsync_2_T1, ProcessWithProgressAsync_2_T2]: ...

        ProcessWithProgressAsync_2_T1 = typing.TypeVar('ProcessWithProgressAsync_2_T1')
        ProcessWithProgressAsync_2_T2 = typing.TypeVar('ProcessWithProgressAsync_2_T2')
        class ProcessWithProgressAsync_2(typing.Generic[ProcessWithProgressAsync_2_T1, ProcessWithProgressAsync_2_T2]):
            ProcessWithProgressAsync_2_TInput = TaskRunnerScope.ProcessWithProgressAsync_MethodGroup.ProcessWithProgressAsync_2_T1
            ProcessWithProgressAsync_2_TOutput = TaskRunnerScope.ProcessWithProgressAsync_MethodGroup.ProcessWithProgressAsync_2_T2
            def __call__(self, items: List_1[ProcessWithProgressAsync_2_TInput], processItem: Func_2[ProcessWithProgressAsync_2_TInput, ProcessWithProgressAsync_2_TOutput], message: str, threadCount: ThreadCount) -> Task_1[List_1[ProcessWithProgressAsync_2_TOutput]]:...


    # Skipped RunOnBackgroundThreadWithSpinningProgressDialog due to it being static, abstract and generic.

    RunOnBackgroundThreadWithSpinningProgressDialog : RunOnBackgroundThreadWithSpinningProgressDialog_MethodGroup
    class RunOnBackgroundThreadWithSpinningProgressDialog_MethodGroup:
        def __getitem__(self, t:typing.Type[RunOnBackgroundThreadWithSpinningProgressDialog_1_T1]) -> RunOnBackgroundThreadWithSpinningProgressDialog_1[RunOnBackgroundThreadWithSpinningProgressDialog_1_T1]: ...

        RunOnBackgroundThreadWithSpinningProgressDialog_1_T1 = typing.TypeVar('RunOnBackgroundThreadWithSpinningProgressDialog_1_T1')
        class RunOnBackgroundThreadWithSpinningProgressDialog_1(typing.Generic[RunOnBackgroundThreadWithSpinningProgressDialog_1_T1]):
            RunOnBackgroundThreadWithSpinningProgressDialog_1_TResult = TaskRunnerScope.RunOnBackgroundThreadWithSpinningProgressDialog_MethodGroup.RunOnBackgroundThreadWithSpinningProgressDialog_1_T1
            def __call__(self, message: str, action: Func_1[RunOnBackgroundThreadWithSpinningProgressDialog_1_TResult]) -> RunOnBackgroundThreadWithSpinningProgressDialog_1_TResult:...


    # Skipped RunOnBackgroundThreadWithSpinningProgressDialogAsync due to it being static, abstract and generic.

    RunOnBackgroundThreadWithSpinningProgressDialogAsync : RunOnBackgroundThreadWithSpinningProgressDialogAsync_MethodGroup
    class RunOnBackgroundThreadWithSpinningProgressDialogAsync_MethodGroup:
        def __getitem__(self, t:typing.Type[RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1]) -> RunOnBackgroundThreadWithSpinningProgressDialogAsync_1[RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1]: ...

        RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1 = typing.TypeVar('RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1')
        class RunOnBackgroundThreadWithSpinningProgressDialogAsync_1(typing.Generic[RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1]):
            RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_TResult = TaskRunnerScope.RunOnBackgroundThreadWithSpinningProgressDialogAsync_MethodGroup.RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_T1
            def __call__(self, message: str, action: Func_1[RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_TResult]) -> Task_1[RunOnBackgroundThreadWithSpinningProgressDialogAsync_1_TResult]:...




class ThreadCount(IEquatable_1[ThreadCount]):
    AllLogicalCores : ThreadCount
    HalfLogicalCores : ThreadCount
    One : ThreadCount
    @property
    def IsSequential(self) -> bool: ...
    @property
    def ParallelOptions(self) -> ParallelOptions: ...
    @property
    def Threads(self) -> int: ...
    @staticmethod
    def FractionOfLogicalCores(fraction: float) -> ThreadCount: ...
    def GetHashCode(self) -> int: ...
    def __eq__(self, left: ThreadCount, right: ThreadCount) -> bool: ...
    def __ne__(self, left: ThreadCount, right: ThreadCount) -> bool: ...
    def ToString(self) -> str: ...
    @staticmethod
    def WithThreads(count: int) -> ThreadCount: ...
    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        @typing.overload
        def __call__(self, other: ThreadCount) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...


