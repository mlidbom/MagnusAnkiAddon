from concurrent.futures import Future
from typing import Callable, Generic, Optional, TypeVar

from anki.cards import Card
from ankiutils import app, ui_utils
from note.jpnote import JPNote
from sysutils.typed import checked_cast

TNote = TypeVar('TNote', bound=JPNote)

class PrerenderingAnswerContentRenderer(Generic[TNote]):
    def __init__(self, cls: type[TNote], render_method:Callable[[TNote], dict[str, str]]) -> None:
        self._cls = cls
        self._render_method = render_method
        self._promise:Optional[Future[dict[str, str]]] = None

    @staticmethod
    def _make_replacements(replacements:dict[str, str], html:str) -> str:
        for tag, content in replacements.items():
            html = html.replace(tag, content)
        return html

    def render(self, html: str, card: Card, type_of_display: str) -> str:
        note = JPNote.note_from_card(card)

        if isinstance(note, self._cls):
            app.ensure_initialized()

            if ui_utils.is_displaytype_displaying_review_question(type_of_display):
                self._promise = app.thread_pool_executor.submit(lambda: self._render_method(checked_cast(self._cls, note)))
            elif ui_utils.is_displaytype_displaying_review_answer(type_of_display) and self._promise:
                value = self._promise.result()
                self._promise = None # We need to clear it or editing the current card will not show any updates
                return self._make_replacements(value, html)
            elif ui_utils.is_displaytype_displaying_answer(type_of_display):
                return self._make_replacements(self._render_method(checked_cast(self._cls, note)), html)

        return html


class PrerenderingAnswerSingleTagContentRenderer(PrerenderingAnswerContentRenderer[TNote]):
    def __init__(self, cls: type[TNote], tag_to_replace:str, render_method:Callable[[TNote], str]) -> None:
        def wrapped_render_method(note:TNote) -> dict[str, str]:
            return { tag_to_replace: render_method(note) }

        super().__init__(cls, wrapped_render_method)