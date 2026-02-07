from __future__ import annotations

from typing import TYPE_CHECKING

from aqt import gui_hooks, mw
from aqt.reviewer import Reviewer
from jaspythonutils.sysutils.typed import non_optional
from JAStudio.Core.Note import CardTypes, DifficultyCalculator, KanjiNote, SentenceNote, VocabNote

from jastudio.anki_extentions.card_ex import CardEx
from jastudio.ankiutils import app, ui_utils

if TYPE_CHECKING:
    from anki.cards import Card

_real_auto_advance_to_answer_if_enabled = Reviewer._auto_advance_to_answer_if_enabled  # noqa  # pyright: ignore[reportPrivateUsage]

def is_handled_card(card: CardEx) -> bool:
    if card.type().name != CardTypes.Reading:
        return False

    import jastudio.note.ankijpnote
    note = jastudio.note.ankijpnote.AnkiJPNote.note_from_card(non_optional(mw.reviewer.card))
    return isinstance(note, SentenceNote | VocabNote | KanjiNote)

def seconds_to_show_question(card: CardEx) -> float:
    note = card.note()

    def default_time_allowed() -> float:
        if isinstance(note, SentenceNote):
            return DifficultyCalculator(startingSeconds=app.config().AutoadvanceSentenceStartingSeconds.GetValue(),
                                        hiraganaSeconds=app.config().AutoadvanceSentenceHiraganaSeconds.GetValue(),
                                        katakataSeconds=app.config().AutoadvanceSentenceKatakanaSeconds.GetValue(),
                                        kanjiSeconds=app.config().AutoadvanceSentenceKanjiSeconds.GetValue()).AllowedSeconds(note.Question.WithoutInvisibleSpace())
        if isinstance(note, VocabNote):
            return DifficultyCalculator(startingSeconds=app.config().AutoadvanceVocabStartingSeconds.GetValue(),
                                        hiraganaSeconds=app.config().AutoadvanceVocabHiraganaSeconds.GetValue(),
                                        katakataSeconds=app.config().AutoadvanceVocabKatakanaSeconds.GetValue(),
                                        kanjiSeconds=app.config().AutoadvanceVocabKanjiSeconds.GetValue()).AllowedSeconds(note.GetQuestion())
        if isinstance(note, KanjiNote):
            return card.get_deck().get_config().get_seconds_to_show_question()
        raise Exception("We should never get here")

    time_allowed = default_time_allowed()
    if app.config().BoostFailedCardAllowedTime.GetValue():
        sequential_failures = card.sequential_again_answers_today()
        if sequential_failures > 0:
            config_bostfactor = app.config().BoostFailedCardAllowedTimeByFactor.GetValue()
            multiplier = config_bostfactor ** sequential_failures

            time_allowed *= multiplier

    return time_allowed

def _auto_advance_to_answer_if_enabled(reviewer: Reviewer) -> None:
    if not app.is_initialized():
        return

    card = CardEx(non_optional(mw.reviewer.card))
    if not is_handled_card(card):
        _real_auto_advance_to_answer_if_enabled(reviewer)
        return

    mw.reviewer._clear_auto_advance_timers()  # noqa  # pyright: ignore[reportPrivateUsage]
    allowed_milliseconds = int(seconds_to_show_question(card) * 1000)

    mw.reviewer._show_answer_timer = mw.reviewer.mw.progress.timer(  # pyright: ignore[reportUnknownMemberType, reportPrivateUsage]
        allowed_milliseconds,
        mw.reviewer._on_show_answer_timeout,  # noqa  # pyright: ignore[reportPrivateUsage]
        repeat=False,
        parent=mw.reviewer.mw,
    )

def _auto_start_auto_advance(html: str, anki_card: Card, _display_type: str) -> str:
    if (app.is_initialized()
            and ui_utils.is_displaytype_displaying_review_question(_display_type)
            and is_handled_card(CardEx(anki_card))
            and not mw.reviewer.auto_advance_enabled):
        mw.reviewer.toggle_auto_advance()

    return html

def init() -> None:
    Reviewer._auto_advance_to_answer_if_enabled = _auto_advance_to_answer_if_enabled # type: ignore  # pyright: ignore[reportAttributeAccessIssue, reportPrivateUsage]
    gui_hooks.card_will_show.append(_auto_start_auto_advance)
