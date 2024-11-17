from anki.cards import Card
from aqt import gui_hooks, mw
from aqt.reviewer import Reviewer

from anki_extentions.card_ex import CardEx
from ankiutils import app
from note.difficulty_calculator import DifficultyCalculator
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.note_constants import CardTypes
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils.typed import non_optional

_real_auto_advance_to_answer_if_enabled = Reviewer._auto_advance_to_answer_if_enabled # noqa


def is_handled_card(card: CardEx) -> bool:
    if card.type().name != CardTypes.reading:
        return False

    note = JPNote.note_from_card(non_optional(mw.reviewer.card))
    return isinstance(note, SentenceNote) or isinstance(note, VocabNote) or isinstance(note, KanjiNote)

def seconds_to_show_question(card: CardEx) -> float:
    note = card.note()

    def default_time_allowed() -> float:
        if isinstance(note, SentenceNote):
            return DifficultyCalculator(starting_seconds=3.0, hiragana_seconds=0.7, katakata_seconds=1.0, kanji_seconds=1.5).allowed_seconds(note.get_question())
        elif isinstance(note, VocabNote):
            return DifficultyCalculator(starting_seconds=3.0, hiragana_seconds=0.5, katakata_seconds=0.7, kanji_seconds=1.0).allowed_seconds(note.get_question())
        elif isinstance(note, KanjiNote):
            return card.get_deck().get_config().get_seconds_to_show_question()
        raise Exception("We should never get here")

    time_allowed = default_time_allowed()
    if app.config().boost_failed_card_allowed_time.get_value():
        sequential_failures = card.sequential_again_answers_today()
        if sequential_failures > 0:
            config_bostfactor = app.config().boost_failed_card_allowed_time_by_factor.get_value()
            multiplier = config_bostfactor ** sequential_failures

            time_allowed *= multiplier

    return time_allowed



def _auto_advance_to_answer_if_enabled(reviewer:Reviewer) -> None:
    card = CardEx(non_optional(mw.reviewer.card))
    if not is_handled_card(card):
        _real_auto_advance_to_answer_if_enabled(reviewer)
        return

    mw.reviewer._clear_auto_advance_timers() # noqa
    allowed_milliseconds = int(seconds_to_show_question(card) * 1000)

    mw.reviewer._show_answer_timer = mw.reviewer.mw.progress.timer(
        allowed_milliseconds,
        mw.reviewer._on_show_answer_timeout, # noqa
        repeat=False,
        parent=mw.reviewer.mw,
    )

def _auto_start_auto_advance(html:str, anki_card:Card, _display_type:str) -> str:
    if is_handled_card(CardEx(anki_card)) and not mw.reviewer.auto_advance_enabled:
        mw.reviewer.toggle_auto_advance()

    return html

def init() -> None:
    Reviewer._auto_advance_to_answer_if_enabled = _auto_advance_to_answer_if_enabled  # type: ignore
    gui_hooks.card_will_show.append(_auto_start_auto_advance)