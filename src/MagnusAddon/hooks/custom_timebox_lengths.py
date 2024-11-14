from typing import Dict, Tuple

import anki
import aqt.utils
from anki.cards import CardId
from anki.decks import DeckDict
from anki.models import NotetypeDict
from aqt import gui_hooks
from aqt import mw
from aqt.overview import Overview
from aqt.webview import WebContent

from note.note_constants import NoteTypes, CardTypes
from sysutils import typed
from sysutils.typed import checked_cast_generics

def adjust_timebox(_web_content: WebContent, context: object) -> None:
    if isinstance(context, Overview):
        deck: DeckDict = mw.col.decks.current()
        deck_card_ids = mw.col.find_cards(f"deck:{deck['name']}")
        if deck_card_ids:
            first_card_id: CardId = deck_card_ids[0]

            card = mw.col.get_card(first_card_id)
            note = card.note()
            notetype: NotetypeDict = checked_cast_generics(NotetypeDict, note.note_type())

            card_notetype_timebox_minutes: Dict[Tuple[str, str], int] = {
                (NoteTypes.Sentence, CardTypes.reading): 10,
                (NoteTypes.Sentence, CardTypes.listening): 5,

                (NoteTypes.Vocab, CardTypes.reading): 10,
                (NoteTypes.Vocab, CardTypes.listening): 5,

                (NoteTypes.Kanji, CardTypes.reading): 5,
            }

            key = (typed.str_(notetype["name"]), typed.str_(card.template()["name"]))
            if key in card_notetype_timebox_minutes:
                timebox = card_notetype_timebox_minutes[key]
                mw.col.conf.set('timeLim', card_notetype_timebox_minutes[key] * 60)
                aqt.utils.tooltip(f"Set timbox to {timebox} minutes")

gui_hooks.webview_will_set_content.append(adjust_timebox)