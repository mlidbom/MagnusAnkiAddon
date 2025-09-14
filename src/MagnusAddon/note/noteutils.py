from __future__ import annotations

from typing import TYPE_CHECKING

from anki.consts import QUEUE_TYPE_SUSPENDED
from anki.notes import NoteId
from note.note_constants import NoteTypes
from sysutils import typed
from sysutils.typed import non_optional, str_

if TYPE_CHECKING:
    from anki.cards import Card
    from anki.collection import Collection
    from anki.dbproxy import Row
    from anki.notes import Note
    from qt_utils.task_runner_progress_dialog import ITaskRunner

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

def initialize_studying_cache(col: Collection, task_runner: ITaskRunner) -> None:
    query = f"""
    SELECT cards.nid as note_id, templates.name as card_type, cards.queue as queue
    FROM cards
    JOIN notes ON cards.nid = notes.id
    JOIN notetypes on notetypes.id = notes.mid
    JOIN templates ON templates.ntid = notes.mid and templates.ord = cards.ord
    WHERE notetypes.name COLLATE NOCASE IN ('{NoteTypes.Sentence}', '{NoteTypes.Vocab}', '{NoteTypes.Kanji}')
"""

    studying_status_rows: list[Row] = non_optional(col.db).all(query)

    clear_studying_cache()

    def cache_card(row: Row) -> None:
        note_id = NoteId(typed.int_(row[0]))
        card_type = typed.str_(row[1])
        queue = typed.int_(row[2])
        if note_id not in _studying_status_cache: _studying_status_cache[note_id] = {}
        _studying_status_cache[note_id][card_type] = queue != QUEUE_TYPE_SUSPENDED

    task_runner.process_with_progress(studying_status_rows, cache_card, "Populating studying status cache")
