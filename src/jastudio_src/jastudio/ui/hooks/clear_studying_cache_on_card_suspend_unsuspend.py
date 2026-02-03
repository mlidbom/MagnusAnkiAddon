from __future__ import annotations

from typing import TYPE_CHECKING

from aqt import gui_hooks

from jastudio.anki_extentions.card_ex import CardEx
from jastudio.ankiutils import app
from jastudio.note import studing_status_helper

if TYPE_CHECKING:
    from collections.abc import Sequence

    from anki.cards import CardId
    from anki.collection import OpChanges, OpChangesWithCount


def _monkey_patch(html:str, _card:object, _something_else_again:object) -> str:
    def update_cards_in_cache(ids: Sequence[CardId]) -> None:
        cards = [CardEx.from_id(card_id) for card_id in ids]
        for card in cards:
            studing_status_helper.update_in_studying_cache(card)

    def _monkey_patched_suspend_cards(ids: Sequence[CardId]) -> OpChangesWithCount:
        return_val = _real_suspend_cards(ids)
        update_cards_in_cache(ids)
        return return_val

    def _monkey_patched_unsuspend_cards(ids: Sequence[CardId]) -> OpChanges:
        return_val = _real_unsuspend_cards(ids)
        update_cards_in_cache(ids)
        return return_val

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
