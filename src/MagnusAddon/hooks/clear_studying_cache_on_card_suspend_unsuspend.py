from typing import Sequence

from anki.cards import CardId
from anki.collection import OpChangesWithCount
from aqt import gui_hooks

from ankiutils import app
from note import noteutils


def _monkey_patch() -> None:
    scheduler = app.col().anki_collection.sched
    _real_suspend_cards = scheduler.suspend_cards
    _real_unsuspend_cards = scheduler.unsuspend_cards

    def remove_cards_from_cache(ids: Sequence[CardId]) -> None:
        cards = [app.col().anki_collection.get_card(card_id) for card_id in ids]
        for card in cards:
            noteutils.remove_from_studying_cache(card.note().id)

    def _monkey_patched_suspend_cards(ids: Sequence[CardId]) -> OpChangesWithCount:
        remove_cards_from_cache(ids)
        return _real_suspend_cards(ids)

    def _monkey_patched_unsuspend_cards(ids: Sequence[CardId]) -> OpChangesWithCount:
        remove_cards_from_cache(ids)
        return _real_unsuspend_cards(ids)

    scheduler.suspend_cards = _monkey_patched_suspend_cards  # type: ignore
    scheduler.unsuspend_cards = _monkey_patched_unsuspend_cards  # type: ignore



def init() -> None:
    gui_hooks.main_window_did_init.append(_monkey_patch)
