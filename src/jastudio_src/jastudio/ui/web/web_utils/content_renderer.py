from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jaslib.note.jpnote import JPNote
from jaslib.note.note_constants import Mine
from jaslib.ui.web.content_renderer import ContentRenderer

from jastudio.ankiutils import app
from jastudio.sysutils import app_thread_pool

if TYPE_CHECKING:
    from collections.abc import Callable

    from anki.cards import Card


class PrerenderingAnswerContentRenderer[TNote: JPNote](Slots):
    """Anki-specific adapter. Stays in Python."""

    def __init__(self, cls: type[TNote], render_methods: dict[str, Callable[[TNote], str]]) -> None:
        self._cls: type[TNote] = cls
        self._renderer: ContentRenderer[TNote] = ContentRenderer[TNote](render_methods, app_thread_pool.pool.submit)

    def render(self, html: str, card: Card, type_of_display: str) -> str:
        if not app.is_initialized():
            return Mine.app_still_loading_message

        note = app.col().note_from_note_id(card.nid if card.nid else card.note().id)

        if not isinstance(note, self._cls):
            return html

        return self._renderer.render(note, html, type_of_display)
