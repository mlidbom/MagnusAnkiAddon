from __future__ import annotations

from typing import override

from autoslot import Slots


class MatchRequirement(Slots):
    """Base class for all match requirements."""

    @property
    def is_fulfilled(self) -> bool: raise NotImplementedError()

    @property
    def failure_reason(self) -> str: raise NotImplementedError()

    @override
    def __repr__(self) -> str: return self.failure_reason