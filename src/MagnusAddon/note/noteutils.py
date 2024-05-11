from anki.consts import QUEUE_TYPE_NEW, QUEUE_TYPE_SUSPENDED
from anki.notes import Note, NoteId

_card_is_studying_cache: dict[NoteId, bool] = dict()
def has_card_being_studied(note: Note) -> bool:
    return any([card for card in note.cards() if card.queue != QUEUE_TYPE_SUSPENDED and card.queue != QUEUE_TYPE_NEW])

def has_card_being_studied_cached(note: Note) -> bool:
    if note.id not in _card_is_studying_cache:
        _card_is_studying_cache[note.id] = has_card_being_studied(note)

    return _card_is_studying_cache[note.id]
