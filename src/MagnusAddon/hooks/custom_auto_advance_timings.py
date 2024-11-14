from typing import Any

from anki.cards import Card
from aqt import gui_hooks, mw

from note import cardutils
from note.difficulty_calculator import DifficultyCalculator
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.note_constants import CardTypes
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import timeutil, typed
from sysutils.typed import non_optional

def _monkey_patch(html:str, _card:Any, display_type:str) -> str:
    if not display_type.startswith('review'):
        return html

    def is_handled_card() -> bool:
        if cardutils.card_type(non_optional(mw.reviewer.card)) != CardTypes.reading:
            return False

        note = JPNote.note_from_card(non_optional(mw.reviewer.card))
        return isinstance(note, SentenceNote) or isinstance(note, VocabNote) or isinstance(note, KanjiNote)

    def seconds_to_show_question() -> float:
        card = non_optional(mw.reviewer.card)
        note = JPNote.note_from_card(card)
        if isinstance(note, SentenceNote):
            return DifficultyCalculator(starting_seconds=3.0, hiragana_seconds=0.7, katakata_seconds=1.0, kanji_seconds=1.5).allowed_seconds(note.get_question())
        elif isinstance(note, VocabNote):
            return DifficultyCalculator(starting_seconds=3.0, hiragana_seconds=0.5, katakata_seconds=0.7, kanji_seconds=1.0).allowed_seconds(note.get_question())
        elif isinstance(note, KanjiNote):
            return int(mw.reviewer.mw.col.decks.config_dict_for_deck_id(card.current_deck_id())["secondsToShowQuestion"])

        raise Exception("We should never get here")


    def patched_auto_advance_to_answer_if_enabled() -> None:
        if not is_handled_card():
            _real_auto_advance_to_answer_if_enabled()
            return

        mw.reviewer._clear_auto_advance_timers() # noqa
        allowed_milliseconds = int(seconds_to_show_question() * 1000)

        mw.reviewer._show_answer_timer = mw.reviewer.mw.progress.timer(
            allowed_milliseconds,
            mw.reviewer._on_show_answer_timeout, # noqa
            repeat=False,
            parent=mw.reviewer.mw,
        )

        print(f"Set allowed time to: {timeutil.format_seconds_as_ss_ttt(allowed_milliseconds)}")

    if is_handled_card() and not mw.reviewer.auto_advance_enabled:
        mw.reviewer.toggle_auto_advance()

    if not hasattr(mw.reviewer, "is_patched_by_magnus_addon_for_auto_advance_timings"):
        _real_auto_advance_to_answer_if_enabled = mw.reviewer._auto_advance_to_answer_if_enabled # noqa
        mw.reviewer._auto_advance_to_answer_if_enabled = patched_auto_advance_to_answer_if_enabled # type: ignore
        mw.reviewer.is_patched_by_magnus_addon_for_auto_advance_timings = True # type: ignore

    return html

def init() -> None:
    gui_hooks.card_will_show.append(_monkey_patch)
