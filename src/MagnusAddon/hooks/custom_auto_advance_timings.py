from typing import Any

from anki.cards import Card
from aqt import gui_hooks, mw

from note import cardutils
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.note_constants import CardTypes
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import timeutil, typed

def _monkey_patch(html:str, _card:Any, _something_else_again:Any) -> str:
    reviewer = mw.reviewer

    def is_handled_card() -> bool:
        if cardutils.card_type(typed.checked_cast(Card, reviewer.card)) != CardTypes.reading:
            return False

        note = JPNote.note_from_card(typed.checked_cast(Card, reviewer.card))
        return isinstance(note, SentenceNote) or isinstance(note, VocabNote) or isinstance(note, KanjiNote)

    def milliseconds_to_show_question() -> int:
        card = typed.checked_cast(Card, reviewer.card)
        note = JPNote.note_from_card(card)
        if isinstance(note, SentenceNote):
            return note.get_allowed_read_review_time_milliseconds()
        elif isinstance(note, VocabNote):
            return note.get_allowed_read_review_time_milliseconds()
        elif isinstance(note, KanjiNote):
            return int(reviewer.mw.col.decks.config_dict_for_deck_id(card.current_deck_id())["secondsToShowQuestion"] * 1000)

        raise Exception("We should never get here")


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
