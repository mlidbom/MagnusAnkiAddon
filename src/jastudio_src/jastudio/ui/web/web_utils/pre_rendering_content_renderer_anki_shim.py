from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from JAStudio.Core.Note import JPNote, Mine

from jastudio.ankiutils import app

if TYPE_CHECKING:

    from anki.cards import Card
    from JAStudio.Core.UI.Web import PreRenderingContentRenderer


class PrerenderingContentRendererAnkiShim[TNote: JPNote](Slots):
    def __init__(self, cls: type[TNote], renderer: PreRenderingContentRenderer[TNote]) -> None:
        self._cls: type[TNote] = cls
        self._renderer: PreRenderingContentRenderer[TNote] = renderer

    def render(self, html: str, card: Card, type_of_display: str) -> str:
        if not app.is_initialized():
            return Mine.app_still_loading_message

        note = app.col().note_from_note_id(card.nid if card.nid else card.note().id)

        if not isinstance(note, self._cls):
            return html

        return self._renderer.render(note, html, type_of_display)
