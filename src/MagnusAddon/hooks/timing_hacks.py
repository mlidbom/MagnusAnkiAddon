from anki.cards import Card
from anki.notes import Note
import time
from aqt import gui_hooks


class UglyUITimingBasedHacksData:
    def __init__(self) -> None:
        self._last_editor_typing_time = 0.0
        self._last_reviewer_showed_answer_time = 0.0
        self._last_editor_typing_note = None

    def typed_in_note(self, note: Note) -> None:
        self._last_editor_typing_time = time.time()
        self._last_editor_typing_note = note

    def reviewer_showed_answer(self, _card:Card) -> None:
        self._last_reviewer_showed_answer_time = time.time()

    def reviewer_just_showed_answer(self) -> bool:
        return time.time() - self._last_reviewer_showed_answer_time < 1

    def typed_in_editor_in_last_seconds(self, seconds: float) -> bool:
        return time.time() - self._last_editor_typing_time < seconds

ugly_timing_hacks = UglyUITimingBasedHacksData()

def on_reviewer_show_answer(_card: any) -> None: ugly_timing_hacks.reviewer_showed_answer(_card)
def typed_in_editor(note:Note) -> None: ugly_timing_hacks.typed_in_note(note)

def init() -> None:
    gui_hooks.reviewer_did_show_answer.append(on_reviewer_show_answer)
    gui_hooks.editor_did_fire_typing_timer.append(typed_in_editor)