# noinspection PyUnresolvedReferences
from __future__ import annotations

from typing import TYPE_CHECKING

from anki.consts import QUEUE_TYPE_NEW
from autoslot import Slots
from note.note_constants import NoteTypes

if TYPE_CHECKING:
    from anki.cards import Card


class CardUtils(Slots):
    @staticmethod
    def is_new(card: Card) -> bool:
        return card.queue == QUEUE_TYPE_NEW

    @classmethod
    def get_note_type_priority(cls, card: Card) -> int:
        note_type_name = card.note_type()["name"]
        if note_type_name == NoteTypes.Kanji: return 1
        if note_type_name == NoteTypes.Vocab: return 2

        return 4  # It's nice to use it for other note types too so default them to 4.

    @classmethod
    def prioritize(cls, card: Card) -> None:
        if CardUtils.is_new(card):
            card.due = cls.get_note_type_priority(card)
            card.flush()