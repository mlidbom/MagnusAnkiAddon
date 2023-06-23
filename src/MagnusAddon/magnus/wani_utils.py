from anki.cards import Card
from anki.consts import *

class CardUtils:
    def is_new(card: Card) -> bool:
        return card.queue == QUEUE_TYPE_NEW