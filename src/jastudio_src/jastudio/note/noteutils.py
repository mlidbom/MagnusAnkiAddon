from __future__ import annotations

from typing import TYPE_CHECKING

from anki.consts import QUEUE_TYPE_SUSPENDED
from anki.notes import Note, NoteId
from jaslib.note.collection.card_studying_status import CardStudyingStatus
from jaslib.note.note_constants import NoteTypes
from jaslib.sysutils import typed
from jaslib.sysutils.memory_usage import string_auto_interner
from jaslib.sysutils.typed import non_optional, str_
from jaslib.task_runners.task_progress_runner import TaskRunner
from jastudio.ankiutils import app
from typed_linq_collections.q_iterable import query

if TYPE_CHECKING:
    from anki.cards import Card
    from anki.collection import Collection
    from anki.dbproxy import Row
    from jastudio.anki_extentions.card_ex import CardEx

_studying_status_cache: dict[NoteId, dict[str, bool]] = {}

def _is_being_studied(card: Card) -> bool:
    return card.queue != QUEUE_TYPE_SUSPENDED  # and card.queue != QUEUE_TYPE_NEW

def _card_type(card: Card) -> str:
    return str_(card.template()["name"])

def update_in_studying_cache(card_ex: CardEx) -> None:
    if card_ex.note_ex().id in _studying_status_cache:
        cached = _studying_status_cache.pop(card_ex.note_ex().id)
        cached[card_ex.card_type] = not card_ex.is_suspended()

def clear_studying_cache() -> None:
    _studying_status_cache.clear()

def has_card_being_studied_cached(note_id: int, card_type: str = "") -> bool:
    typed_note_id = NoteId(note_id)
    cached = _studying_status_cache.get(typed_note_id)
    if cached is None:
        note = app.anki_collection().get_note(typed_note_id)
        _ensure_card_status_is_cached(note)
        cached = _studying_status_cache[typed_note_id]

    if card_type:
        return cached.get(card_type, False)

    return any(cached.values())

def _ensure_card_status_is_cached(note: Note) -> None:
    if note.id not in _studying_status_cache:
        _studying_status_cache[note.id] = {_card_type(card): _is_being_studied(card) for card in note.cards()}

class CardStudyingStatusFactory:
    @classmethod
    def from_row(cls, row: Row) -> CardStudyingStatus:
        note_id: NoteId = NoteId(typed.int_(row[0]))  # pyright: ignore[reportAny]
        card_type: str = string_auto_interner.auto_intern(typed.str_(row[1]))  # pyright: ignore[reportAny]
        is_suspended: bool = typed.int_(row[2]) == QUEUE_TYPE_SUSPENDED  # pyright: ignore[reportAny]
        note_type_name: str = string_auto_interner.auto_intern(typed.str_(row[3]))  # pyright: ignore[reportAny]

        return CardStudyingStatus(note_id, card_type, is_suspended, note_type_name)

# don't use temporary variables, it will break our memory profiling using tracemalloc
def fetch_card_studying_statuses(col: Collection, ) -> list[CardStudyingStatus]:
    sql_query = f"""
        SELECT cards.nid as note_id, templates.name as card_type, cards.queue as queue, notetypes.name as note_type
        FROM cards
        JOIN notes ON cards.nid = notes.id
        JOIN notetypes on notetypes.id = notes.mid
        JOIN templates ON templates.ntid = notes.mid and templates.ord = cards.ord
        WHERE notetypes.name COLLATE NOCASE IN ('{NoteTypes.Sentence}', '{NoteTypes.Vocab}', '{NoteTypes.Kanji}')
    """

    with TaskRunner.current("Fetching card studying status from Anki db") as task_runner:
        return task_runner.run_on_background_thread_with_spinning_progress_dialog(
                "Fetching card studying status from Anki db",
                lambda: query(non_optional(col.db).all(sql_query)).select(CardStudyingStatusFactory.from_row).to_list())
