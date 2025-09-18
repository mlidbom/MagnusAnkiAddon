from __future__ import annotations

from typing import TYPE_CHECKING, ParamSpec, TypeVar

from ankiutils import app

if TYPE_CHECKING:
    from collections.abc import Callable

# noinspection PyUnusedName
ParameterSpec = ParamSpec("ParameterSpec")  # Preserves parameter types and names
# noinspection PyUnusedName
ReturnValueType = TypeVar("ReturnValueType")    # Preserves return type

if app.is_running_line_profiling:
    from line_profiler_pycharm import profile  # pyright: ignore [reportMissingTypeStubs, reportUnknownVariableType, reportAssignmentType]
else:
    def profile[**ParameterSpec, ReturnValueType](func: Callable[ParameterSpec, ReturnValueType]) -> Callable[ParameterSpec, ReturnValueType]:
        return func


def profile_lines[**ParameterSpec, ReturnValueType](func: Callable[ParameterSpec, ReturnValueType]) -> Callable[ParameterSpec, ReturnValueType]:
    return profile(func)