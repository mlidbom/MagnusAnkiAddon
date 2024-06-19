from anki.cards import Card
from anki.consts import QUEUE_TYPE_NEW, QUEUE_TYPE_SUSPENDED
from anki.notes import Note, NoteId

from sysutils.typed import checked_cast

_card_is_studying_cache: dict[NoteId, dict[str, bool]] = dict()

def _is_being_studied(card: Card) -> bool:
    return card.queue != QUEUE_TYPE_SUSPENDED #and card.queue != QUEUE_TYPE_NEW

def _card_type(card: Card) -> str:
    return checked_cast(str, card.template()['name'])

def remove_from_cache(note_id: NoteId) -> None:
    if note_id in _card_is_studying_cache:
        _card_is_studying_cache.pop(note_id)

def clear_studying_cache() -> None:
    _card_is_studying_cache.clear()

def has_card_being_studied_cached(note: Note, card_type:str = "") -> bool:
    if note.id not in _card_is_studying_cache:
        _card_is_studying_cache[note.id] = {_card_type(card): _is_being_studied(card) for card in note.cards()}

    if card_type:
        cached = _card_is_studying_cache[note.id]
        return cached[card_type] if card_type in cached else False

    return any(_card_is_studying_cache[note.id].values())
