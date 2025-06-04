from __future__ import annotations

from typing import TYPE_CHECKING

from anki.consts import QUEUE_TYPE_SUSPENDED
from sysutils.typed import str_

if TYPE_CHECKING:
    from anki.cards import Card
    from anki.notes import Note, NoteId

_studying_status_cache: dict[NoteId, dict[str, bool]] = {}

def _is_being_studied(card: Card) -> bool:
    return card.queue != QUEUE_TYPE_SUSPENDED #and card.queue != QUEUE_TYPE_NEW

def _card_type(card: Card) -> str:
    return str_(card.template()["name"])

def remove_from_studying_cache(note_id: NoteId) -> None:
    if note_id in _studying_status_cache:
        _studying_status_cache.pop(note_id)

def clear_studying_cache() -> None:
    _studying_status_cache.clear()

def has_card_being_studied_cached(note: Note, card_type:str = "") -> bool:
    _ensure_card_status_is_cached(note)

    if card_type:
        cached = _studying_status_cache[note.id]
        return cached.get(card_type, False)

    return any(_studying_status_cache[note.id].values())

def _ensure_card_status_is_cached(note: Note) -> None:
    if note.id not in _studying_status_cache:
        #todo: performance: this code lists note cards, then inside _is_being_studied turns right around and fetches the note, which is slow.
        # We should cache by the ord member of the card instead, which, I believe is the id of the card type,
        # but this requires some infrastructure for getting the ord from the card name and switching to using that everywhere
        _studying_status_cache[note.id] = {_card_type(card): _is_being_studied(card) for card in note.cards()}
