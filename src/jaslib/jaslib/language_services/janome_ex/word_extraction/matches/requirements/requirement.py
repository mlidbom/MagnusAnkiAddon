from __future__ import annotations

from typing import override

from autoslot import Slots
from jaslib.sysutils.abstract_method_called_error import AbstractMethodCalledError


class MatchRequirement(Slots):
    """Base class for all match requirements."""

    @property
    def is_fulfilled(self) -> bool: raise AbstractMethodCalledError()

    @property
    def failure_reason(self) -> str: raise AbstractMethodCalledError()

    @override
    def __repr__(self) -> str: return self.failure_reason