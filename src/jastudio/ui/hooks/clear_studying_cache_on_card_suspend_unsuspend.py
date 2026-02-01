from __future__ import annotations

from typing import TYPE_CHECKING

from aqt import gui_hooks
from note import noteutils

from jastudio.ankiutils import app

if TYPE_CHECKING:
    from collections.abc import Sequence

    from anki.cards import CardId
    from anki.collection import OpChanges, OpChangesWithCount


def _monkey_patch(html:str, _card:object, _something_else_again:object) -> str:
    def remove_cards_from_cache(ids: Sequence[CardId]) -> None:
        cards = [app.anki_collection().get_card(card_id) for card_id in ids]
        for card in cards:
            noteutils.remove_from_studying_cache(card.note().id)

    def _monkey_patched_suspend_cards(ids: Sequence[CardId]) -> OpChangesWithCount:
        remove_cards_from_cache(ids)
        return _real_suspend_cards(ids)

    def _monkey_patched_unsuspend_cards(ids: Sequence[CardId]) -> OpChanges:
        remove_cards_from_cache(ids)
        return _real_unsuspend_cards(ids)

    scheduler = app.anki_scheduler()

    #todo this silliness is because I patch the instance instead of the class...
    if not hasattr(scheduler, "is_patched_by_magnus_addon_for_suspend"):
        _real_suspend_cards = scheduler.suspend_cards
        _real_unsuspend_cards = scheduler.unsuspend_cards

        scheduler.suspend_cards = _monkey_patched_suspend_cards  # type: ignore
        scheduler.unsuspend_cards = _monkey_patched_unsuspend_cards  # type: ignore
        scheduler.is_patched_by_magnus_addon_for_suspend = True  # type: ignore  # pyright: ignore[reportAttributeAccessIssue]

    return html




def init() -> None:
    gui_hooks.card_will_show.append(_monkey_patch) #should not be needed, but for some reason fixes a bug where the cache is not updated, my best guess is the scheduler is replaced for some reason. It ONLY happens with my personal profile, not the development profile...
