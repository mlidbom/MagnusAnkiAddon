
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from autoslot import Slots
from JAStudio.Core.Note import JPNote, Mine

if TYPE_CHECKING:
    from anki.cards import Card


class _DotNetRenderer[TNote](Protocol):
    def Render(self, note: TNote, html: str, typeOfDisplay: str) -> str: ...


class DotNetPrerenderingContentRendererAnkiShim[TNote: JPNote](Slots):
    def __init__(self, cls: type[TNote], renderer: _DotNetRenderer[TNote]) -> None:
        self._cls: type[TNote] = cls
        self._renderer: _DotNetRenderer[TNote] = renderer

    def render(self, html: str, card: Card, type_of_display: str) -> str:
        from jastudio.ui import dotnet_ui_root

        collection = dotnet_ui_root.Services.CoreApp.Collection
        if not collection.IsInitialized:
            return Mine.AppStillLoadingMessage

        note = collection.NoteFromExternalId(card.nid if card.nid else card.note().id)

        if not isinstance(note, self._cls):
            return html

        return self._renderer.Render(note, html, type_of_display)