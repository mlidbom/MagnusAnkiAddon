from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Generic, TypeVar

from ankiutils import app, ui_utils
from autoslot import Slots
from note.jpnote import JPNote
from note.note_constants import Mine
from sysutils import app_thread_pool
from sysutils.timeutil import StopWatch
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from concurrent.futures import Future

    from anki.cards import Card

TNote = TypeVar("TNote", bound=JPNote)

class PrerenderingAnswerContentRenderer(Generic[TNote], Slots):
    def __init__(self, cls: type[TNote], render_methods: dict[str, Callable[[TNote], str]]) -> None:
        self._cls = cls
        self._render_methods = render_methods
        self._promises: dict[str, Future[str]] | None = None

    @staticmethod
    def _schedule_render_method(_render_method: Callable[[TNote], str], tag: str, note: TNote) -> Future[str]:
        def run_render_method() -> str:
            with StopWatch.log_warning_if_slower_than(0.5, f"rendering:{tag}"):
                return _render_method(note)

        return app_thread_pool.pool.submit(run_render_method if app.is_initialized() else lambda: Mine.app_still_loading_message)

    def render(self, html: str, card: Card, type_of_display: str) -> str:
        note = JPNote.note_from_card(card)

        if isinstance(note, self._cls):
            def schedule_all() -> None:
                self._promises = {tag_: self._schedule_render_method(render_method_, tag_, note) for tag_, render_method_ in self._render_methods.items()}

            def render_scheduled(_html: str) -> str:
                for tag_, content in non_optional(self._promises).items():
                    _html = _html.replace(tag_, content.result())
                self._promises = None
                return _html

            if ui_utils.is_displaytype_displaying_review_question(type_of_display):
                schedule_all()
            elif ui_utils.is_displaytype_displaying_review_answer(type_of_display) and self._promises:
                with StopWatch.log_warning_if_slower_than(0.01, "fetching_results"):
                    html = render_scheduled(html)
            elif ui_utils.is_displaytype_displaying_answer(type_of_display):
                with StopWatch.log_warning_if_slower_than(0.5, "live_rendering"):
                    for tag, render_method in self._render_methods.items():
                        with StopWatch.log_warning_if_slower_than(0.001, f"rendering:{tag}"):
                            html = html.replace(tag, render_method(note) if app.is_initialized() else Mine.app_still_loading_message)

        return html
