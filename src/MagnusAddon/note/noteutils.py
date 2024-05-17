from anki.cards import Card
from anki.consts import QUEUE_TYPE_NEW, QUEUE_TYPE_SUSPENDED
from anki.notes import Note, NoteId

from sysutils.typed import checked_cast

_card_is_studying_cache: dict[NoteId, list[Card]] = dict()

def _is_being_studied(card: Card) -> bool:
    return card.queue != QUEUE_TYPE_SUSPENDED and card.queue != QUEUE_TYPE_NEW

def _card_type(card: Card) -> str:
    return checked_cast(str, card.template()['name'])

def clear_studying_cache() -> None:
    _card_is_studying_cache.clear()

def has_card_being_studied_cached(note: Note, card_type:str = "") -> bool:
    if note.id not in _card_is_studying_cache:
        _card_is_studying_cache[note.id] = note.cards()

    return any(_is_being_studied(card) for card in _card_is_studying_cache[note.id] if _card_type(card) == card_type or card_type == "")
