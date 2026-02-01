from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jaslib.note.jpnote import JPNote
from jaslib.sysutils.timeutil import StopWatch

if TYPE_CHECKING:
    from collections.abc import Callable
    from concurrent.futures import Future

class PrerenderingAnswerContentRenderer[TNote: JPNote](Slots):
    def __init__(self, cls: type[TNote], render_methods: dict[str, Callable[[TNote], str]]) -> None:
        self._cls: type[TNote] = cls
        self._render_methods: dict[str, Callable[[TNote], str]] = render_methods
        self._promises: dict[str, Future[str]] | None = None


    def render(self, html: str, note: JPNote, type_of_display: str) -> str:  # pyright: ignore

        if isinstance(note, self._cls):
            with StopWatch.log_warning_if_slower_than(0.5, "live_rendering"):
                for tag, render_method in self._render_methods.items():
                    with StopWatch.log_warning_if_slower_than(0.001, f"rendering:{tag}"):
                        html = html.replace(tag, render_method(note))

        return html
