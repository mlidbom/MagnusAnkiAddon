from __future__ import annotations

import time
from typing import TYPE_CHECKING

from jastudio.ankiutils.audio_suppressor import audio_suppressor
from aqt import gui_hooks
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from anki.cards import Card
    from anki.notes import Note


class UglyUITimingBasedHacksData(Slots):
    def __init__(self) -> None:
        self._last_editor_typing_time: float = 0.0
        self._last_reviewer_showed_answer_time: float = 0.0

    def typed_in_note(self, _note: Note) -> None:
        audio_suppressor.suppress_for_seconds(.1)
        self._last_editor_typing_time = time.time()

    def reviewer_showed_answer(self, _card:Card) -> None:
        #audio_suppressor.suppress_for_seconds(.3) #I keep not getting audio when quickly moving through audio cards
        self._last_reviewer_showed_answer_time = time.time()

ugly_timing_hacks = UglyUITimingBasedHacksData()

def on_reviewer_show_answer(_card: Card) -> None: ugly_timing_hacks.reviewer_showed_answer(_card)
def typed_in_editor(note:Note) -> None: ugly_timing_hacks.typed_in_note(note)

def init() -> None:
    gui_hooks.reviewer_did_show_answer.append(on_reviewer_show_answer)
    gui_hooks.editor_did_fire_typing_timer.append(typed_in_editor)  # pyright: ignore[reportUnknownMemberType]