from anki.cards import Card
from anki.consts import *
from aqt import mw

from magnus.wanikani_note import WaniNote


class CardUtils:

    def is_new(card: Card) -> bool:
        return card.queue == QUEUE_TYPE_NEW

    @classmethod
    def prioritize(cls, card: Card):
        if(CardUtils.is_new(card)):
            card.due = 0
            card.flush()

    @classmethod
    def prioritize_note_cards(cls, note: WaniNote, name: str):
        cards = [mw.col.get_card(card_id) for card_id in note.card_ids()]
        for card in cards:
            print("Prioritizing {}: {}".format(WaniNote.get_note_type_name(note), name))
            CardUtils.prioritize(card)
