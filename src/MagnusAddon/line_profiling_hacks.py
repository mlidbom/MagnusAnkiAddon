from __future__ import annotations

import os
from typing import TYPE_CHECKING, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

is_running_line_profiling = os.environ.get("LINE_PROFILE") == "1"

# noinspection PyUnusedName
ParameterSpec = ParamSpec("ParameterSpec")  # Preserves parameter types and names
# noinspection PyUnusedName
ReturnValueType = TypeVar("ReturnValueType")  # Preserves return type

if is_running_line_profiling:
    from line_profiler_pycharm import profile  # pyright: ignore [reportMissingTypeStubs, reportUnknownVariableType, reportAssignmentType]
else:
    def profile[**ParameterSpec, ReturnValueType](func: Callable[ParameterSpec, ReturnValueType]) -> Callable[ParameterSpec, ReturnValueType]:
        return func

def profile_lines[**ParameterSpec, ReturnValueType](func: Callable[ParameterSpec, ReturnValueType]) -> Callable[ParameterSpec, ReturnValueType]:
    return profile(func)
