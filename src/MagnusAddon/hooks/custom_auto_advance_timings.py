from typing import Any

from anki.cards import Card
from aqt import gui_hooks, mw

from note.jpnote import JPNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import timeutil, typed

def _monkey_patch(html:str, _card:Any, _something_else_again:Any) -> str:
    reviewer = mw.reviewer

    def is_handled_card() -> bool:
        note = JPNote.note_from_card(typed.checked_cast(Card, reviewer.card))
        return isinstance(note, SentenceNote) or isinstance(note, VocabNote)

    def milliseconds_to_show_question() -> int:
        note = JPNote.note_from_card(typed.checked_cast(Card, reviewer.card))
        if isinstance(note, SentenceNote):
            return note.get_allowed_read_review_time_milliseconds()
        elif isinstance(note, VocabNote):
            return note.get_allowed_read_review_time_milliseconds()
        else:
           raise Exception("This should never happen")


    def patched_auto_advance_to_answer_if_enabled() -> None:
        if not is_handled_card():
            _real_auto_advance_to_answer_if_enabled()
            return

        reviewer._clear_auto_advance_timers() # noqa
        allowed_milliseconds = milliseconds_to_show_question()
        if not reviewer.auto_advance_enabled:
            reviewer.toggle_auto_advance()

        reviewer._show_answer_timer = reviewer.mw.progress.timer(
            allowed_milliseconds,
            reviewer._on_show_answer_timeout, # noqa
            repeat=False,
            parent=reviewer.mw,
        )

        print(f"Set allowed time to: {timeutil.format_seconds_as_ss_ttt(allowed_milliseconds)}")


    if not hasattr(reviewer, "is_patched_by_magnus_addon_for_auto_advance_timings"):
        _real_auto_advance_to_answer_if_enabled = reviewer._auto_advance_to_answer_if_enabled # noqa
        reviewer._auto_advance_to_answer_if_enabled = patched_auto_advance_to_answer_if_enabled # type: ignore
        reviewer.is_patched_by_magnus_addon_for_auto_advance_timings = True # type: ignore

    return html

def init() -> None:
    gui_hooks.card_will_show.append(_monkey_patch)
