from __future__ import annotations

from autoslot import Slots


class TimeSpan(Slots):
    """Represents a time duration with various unit accessors and formatting methods."""

    def __init__(self, seconds: float) -> None:
        self._total_seconds = seconds

    @property
    def total_seconds(self) -> float:
        return self._total_seconds

    @property
    def hours(self) -> int:
        return int(self._total_seconds // 3600)

    @property
    def minutes(self) -> int:
        return int((self._total_seconds % 3600) // 60)

    @property
    def seconds(self) -> int:
        return int(self._total_seconds % 60)

    @property
    def milliseconds(self) -> int:
        return int((self._total_seconds * 1000) % 1000)

    @property
    def microseconds(self) -> int:
        return int((self._total_seconds * 1_000_000) % 1000)

    def format_as_hh_mm_ss(self) -> str:
        return f"{self.hours:02}:{self.minutes:02}:{self.seconds:02}"

    def format_as_ss_ttt(self) -> str:
        return f"{self.seconds:02}.{self.milliseconds:03d}"

    def format_as_ss_ttt_ttt(self) -> str:
        return f"{self.seconds:02}.{self.milliseconds:03d} {self.microseconds:03d}"

    def auto_format(self) -> str:
        if self.total_seconds < 1:
            return self.format_as_ss_ttt_ttt()
        if self.total_seconds < 60:
            return self.format_as_ss_ttt()
        return self.format_as_hh_mm_ss()
