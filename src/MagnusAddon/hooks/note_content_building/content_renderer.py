from concurrent.futures import Future
from typing import Callable, Generic, Optional, TypeVar

from anki.cards import Card
from ankiutils import app, ui_utils
from note.jpnote import JPNote
from sysutils import app_thread_pool
from sysutils.timeutil import StopWatch
from sysutils.typed import non_optional

TNote = TypeVar('TNote', bound=JPNote)

class PrerenderingAnswerContentRenderer(Generic[TNote]):
    def __init__(self, cls: type[TNote], render_methods:dict[str, Callable[[TNote], str]]) -> None:
        self._cls = cls
        self._render_methods = render_methods
        self._promises:Optional[dict[str, Future[str]]] = None

    @staticmethod
    def _schedule_render_method(_render_method:Callable[[TNote], str], section:str, note:TNote) -> Future[str]:
        def run_render_method() -> str:
            with StopWatch.log_warning_if_slower_than(0.5, f"rendering:{section}"):
                return _render_method(note)

        return app_thread_pool.pool.submit(run_render_method)


    def render(self, html: str, card: Card, type_of_display: str) -> str:
        app.wait_for_initialization()
        note = JPNote.note_from_card(card)

        if isinstance(note, self._cls):
            def schedule_all() -> None:
                self._promises = {key: self._schedule_render_method(render_method, key, note) for key, render_method in self._render_methods.items()}

            def render_scheduled(_html:str) -> str:
                for tag, content in non_optional(self._promises).items():
                    _html = _html.replace(tag, content.result())
                self._promises = None
                return _html

            if ui_utils.is_displaytype_displaying_review_question(type_of_display):
                schedule_all()
            elif ui_utils.is_displaytype_displaying_review_answer(type_of_display) and self._promises:
                with StopWatch.log_warning_if_slower_than(0.01, "fetching_results"):
                    html = render_scheduled(html)
            elif ui_utils.is_displaytype_displaying_answer(type_of_display):
                with StopWatch.log_warning_if_slower_than(0.5, "live_rendering"):
                    schedule_all()
                    html = render_scheduled(html)

        return html
