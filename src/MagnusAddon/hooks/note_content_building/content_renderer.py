from concurrent.futures import Future
from typing import Callable, Generic, Optional, TypeVar

from anki.cards import Card
from ankiutils import ui_utils
from note.jpnote import JPNote
from sysutils import app_thread_pool
from sysutils.timeutil import StopWatch
from sysutils.typed import checked_cast
from ankiutils import app

TNote = TypeVar('TNote', bound=JPNote)

class PrerenderingAnswerContentRenderer(Generic[TNote]):
    def __init__(self, cls: type[TNote], render_method:dict[str, Callable[[TNote], str]]) -> None:
        self._cls = cls
        self._render_methods = render_method
        self._promises:Optional[dict[str, Future[str]]] = None

    @staticmethod
    def _schedule_render_method(_render_method:Callable[[TNote], str], section:str, note:TNote) -> Future[str]:
        def run_render_method() -> str:
            with StopWatch.log_warning_if_slower_than(f"PrerenderingAnswerContentRenderer.rendering {section}", 0.2):
                return _render_method(note)

        return app_thread_pool.pool.submit(run_render_method)


    def render(self, html: str, card: Card, type_of_display: str) -> str:
        with StopWatch.log_warning_if_slower_than("PrerenderingAnswerContentRenderer.render", 0.01):
            app.wait_for_initialization()
            note = JPNote.note_from_card(card)

            if isinstance(note, self._cls):
                if ui_utils.is_displaytype_displaying_review_question(type_of_display):
                    self._promises = {key: self._schedule_render_method(render_method, key, note) for key, render_method in self._render_methods.items()}
                elif ui_utils.is_displaytype_displaying_review_answer(type_of_display) and self._promises:
                    for tag, content in self._promises.items():
                        with StopWatch.log_warning_if_slower_than(f"PrerenderingAnswerContentRenderer.render.fetching_result {tag}", 0.001):
                            html = html.replace(tag, content.result())
                    self._promises = None
                elif ui_utils.is_displaytype_displaying_answer(type_of_display):
                    for tag, renderer in self._render_methods.items():
                        html = html.replace(tag, renderer(checked_cast(self._cls, note)))

            return html


class PrerenderingAnswerSingleTagContentRenderer(PrerenderingAnswerContentRenderer[TNote]):
    def __init__(self, cls: type[TNote], tag_to_replace:str, render_method:Callable[[TNote], str]) -> None:
        super().__init__(cls, {tag_to_replace: render_method})
