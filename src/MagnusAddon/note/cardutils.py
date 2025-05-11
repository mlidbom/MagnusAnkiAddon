# noinspection PyUnresolvedReferences
import time

from anki.cards import *
from anki.consts import QUEUE_TYPE_NEW
from ankiutils import app
from note.jpnote import JPNote
from note.note_constants import NoteTypes


class CardUtils:
    @staticmethod
    def is_new(card: Card) -> bool:
        return card.queue == QUEUE_TYPE_NEW

    @classmethod
    def get_note_type_priority(cls, card: Card) -> int:
        note_type_name = card.note_type()["name"]
        if note_type_name == NoteTypes.Radical: return 1
        if note_type_name == NoteTypes.Kanji: return 2
        if note_type_name == NoteTypes.Vocab: return 3

        return 4  # It's nice to use it for other note types too so default them to 4.

    @classmethod
    def prioritize(cls, card: Card) -> None:
        if CardUtils.is_new(card):
            card.due = cls.get_note_type_priority(card)
            card.flush()

    @classmethod
    def prioritize_note_cards(cls, note: JPNote, name: str) -> None:
        cards = [app.anki_collection().get_card(card_id) for card_id in note.card_ids()]
        for card in cards:
            print("Prioritizing {}: {}".format(JPNote.get_note_type_name(note), name))
            CardUtils.prioritize(card)

    @classmethod
    def answer_again_with_zero_interval_for_new_note_cards(cls, note: JPNote, name: str) -> None:
        cards = [app.anki_collection().get_card(card_id) for card_id in note.card_ids()]
        for card in cards:
            if CardUtils.is_new(card):
                print("Answering new card again {}: {}".format(JPNote.get_note_type_name(note), name))
                card.start_timer()  # answerCard crashes unless I do this.
                app.anki_collection().sched.answerCard(card, 1)
                card.due = int(time.time())
                card.flush()
