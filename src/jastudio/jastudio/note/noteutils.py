from __future__ import annotations

from typing import TYPE_CHECKING

from anki.consts import QUEUE_TYPE_SUSPENDED
from anki.notes import NoteId
from jastudio.note.note_constants import NoteTypes
from sysutils import typed
from sysutils.memory_usage import string_auto_interner
from sysutils.typed import non_optional, str_
from typed_linq_collections.q_iterable import query

if TYPE_CHECKING:
    from anki.cards import Card
    from anki.collection import Collection
    from anki.dbproxy import Row
    from anki.notes import Note
    from jastudio.qt_utils.i_task_progress_runner import ITaskRunner

_studying_status_cache: dict[NoteId, dict[str, bool]] = {}

def _is_being_studied(card: Card) -> bool:
    return card.queue != QUEUE_TYPE_SUSPENDED  # and card.queue != QUEUE_TYPE_NEW

def _card_type(card: Card) -> str:
    return str_(card.template()["name"])

def remove_from_studying_cache(note_id: NoteId) -> None:
    if note_id in _studying_status_cache:
        _studying_status_cache.pop(note_id)

def clear_studying_cache() -> None:
    _studying_status_cache.clear()

def has_card_being_studied_cached(note: Note, card_type: str = "") -> bool:
    _ensure_card_status_is_cached(note)

    if card_type:
        cached = _studying_status_cache[note.id]
        return cached.get(card_type, False)

    return any(_studying_status_cache[note.id].values())

def _ensure_card_status_is_cached(note: Note) -> None:
    if note.id not in _studying_status_cache:
        _studying_status_cache[note.id] = {_card_type(card): _is_being_studied(card) for card in note.cards()}

class CardStudyingStatus:
    def __init__(self, row: Row) -> None:
        self.note_id: NoteId = NoteId(typed.int_(row[0])) # pyright: ignore[reportAny]
        self.card_type: str = string_auto_interner.auto_intern(typed.str_(row[1])) # pyright: ignore[reportAny]
        self.queue: int = typed.int_(row[2]) # pyright: ignore[reportAny]

def initialize_studying_cache(col: Collection, task_runner: ITaskRunner) -> None:
    clear_studying_cache()

    sql_query = f"""
    SELECT cards.nid as note_id, templates.name as card_type, cards.queue as queue
    FROM cards
    JOIN notes ON cards.nid = notes.id
    JOIN notetypes on notetypes.id = notes.mid
    JOIN templates ON templates.ntid = notes.mid and templates.ord = cards.ord
    WHERE notetypes.name COLLATE NOCASE IN ('{NoteTypes.Sentence}', '{NoteTypes.Vocab}', '{NoteTypes.Kanji}')
"""

    #don't use temporary variables, it will break our memory profiling using tracemalloc
    def fetch_card_studying_statuses() -> list[CardStudyingStatus]:
        return task_runner.run_on_background_thread_with_spinning_progress_dialog("Fetching card studying status from Anki db", lambda: query(non_optional(col.db).all(sql_query)).select(CardStudyingStatus).to_list())

    def cache_card(row: CardStudyingStatus) -> None:
        if row.note_id not in _studying_status_cache: _studying_status_cache[row.note_id] = {}
        _studying_status_cache[row.note_id][row.card_type] = row.queue != QUEUE_TYPE_SUSPENDED

    task_runner.process_with_progress(fetch_card_studying_statuses(), cache_card, "Populating studying status cache")
