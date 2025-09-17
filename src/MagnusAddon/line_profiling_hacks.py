from __future__ import annotations

import os
from typing import TYPE_CHECKING, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

# noinspection PyUnusedName
ParameterSpec = ParamSpec("ParameterSpec")  # Preserves parameter types and names
# noinspection PyUnusedName
ReturnValueType = TypeVar("ReturnValueType")    # Preserves return type

if os.environ.get("PC_LINE_PROFILER_STATS_FILENAME") is not None or os.environ.get("LINE_PROFILE") == "1":
    from line_profiler_pycharm import profile  # pyright: ignore [reportMissingTypeStubs, reportUnknownVariableType, reportAssignmentType]
else:
    def profile[**ParameterSpec, ReturnValueType](func: Callable[ParameterSpec, ReturnValueType]) -> Callable[ParameterSpec, ReturnValueType]:
        return func


def profile_lines[**ParameterSpec, ReturnValueType](func: Callable[ParameterSpec, ReturnValueType]) -> Callable[ParameterSpec, ReturnValueType]:
    return profile(func)