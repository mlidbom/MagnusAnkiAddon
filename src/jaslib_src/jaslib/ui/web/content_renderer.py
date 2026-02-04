from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jaslib.note.jpnote import JPNote
from jaslib.ui.web.display_type import DisplayType
from jaspythonutils.sysutils.timeutil import StopWatch

if TYPE_CHECKING:
    from collections.abc import Callable
    from concurrent.futures import Future


class ContentRenderer[TNote: JPNote](Slots):
    """Content rendering with prerendering support. Portable to C#."""

    def __init__(
        self,
        render_methods: dict[str, Callable[[TNote], str]],
        schedule_task: Callable[[Callable[[], str]], Future[str]]
    ) -> None:
        self._render_methods: dict[str, Callable[[TNote], str]] = render_methods
        self._schedule_task: Callable[[Callable[[], str]], Future[str]] = schedule_task
        self._promises: dict[str, Future[str]] | None = None

    def render(self, note: TNote, html: str, type_of_display: str) -> str:
        """Main entry point. Dispatches based on display type."""
        if DisplayType.is_displaying_review_question(type_of_display):
            self._schedule_prerender(note)
        elif DisplayType.is_displaying_review_answer(type_of_display) and self._has_pending_prerender():
            html = self._apply_prerendered(html)
        elif DisplayType.is_displaying_answer(type_of_display):
            html = self._render_synchronously(note, html)
        return html

    def _schedule_prerender(self, note: TNote) -> None:
        """Call when question is shown to start prerendering."""
        def make_task(rm: Callable[[TNote], str], t: str) -> Callable[[], str]:
            return lambda: self._render_with_timing(rm, note, t)

        self._promises = {
            tag: self._schedule_task(make_task(rm, tag))
            for tag, rm in self._render_methods.items()
        }

    def _render_with_timing(self, render_method: Callable[[TNote], str], note: TNote, tag: str) -> str:
        with StopWatch.log_warning_if_slower_than(0.5, f"rendering:{tag}"):
            return render_method(note)

    def _apply_prerendered(self, html: str) -> str:
        """Apply prerendered results. Call when answer shown after prerendering."""
        if not self._promises:
            return html
        with StopWatch.log_warning_if_slower_than(0.01, "fetching_results"):
            for tag, future in self._promises.items():
                html = html.replace(tag, future.result())
            self._promises = None
        return html

    def _render_synchronously(self, note: TNote, html: str) -> str:
        """Render all tags synchronously. For edit/preview mode."""
        with StopWatch.log_warning_if_slower_than(0.5, "live_rendering"):
            for tag, render_method in self._render_methods.items():
                html = html.replace(tag, self._render_with_timing(render_method, note, tag))
        return html

    def _has_pending_prerender(self) -> bool:
        return self._promises is not None
