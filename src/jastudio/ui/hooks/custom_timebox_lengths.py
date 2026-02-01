from __future__ import annotations

from typing import TYPE_CHECKING

import aqt.utils
from aqt import gui_hooks
from aqt.overview import Overview
from sysutils import typed

from jastudio.anki_extentions.card_ex import CardEx
from jastudio.anki_extentions.deck_ex import DeckEx
from jastudio.ankiutils import app
from jastudio.note.note_constants import CardTypes, NoteTypes

if TYPE_CHECKING:
    from anki.cards import CardId
    from aqt.webview import WebContent


def adjust_timebox(_web_content: WebContent, context: object) -> None:
    if isinstance(context, Overview):
        deck = DeckEx(app.anki_collection().decks.current())
        deck_card_ids = app.anki_collection().find_cards(f"deck:{deck.name}")
        if deck_card_ids:
            first_card_id: CardId = deck_card_ids[0]

            card = CardEx(app.anki_collection().get_card(first_card_id))
            note = card.note()
            notetype = note.get_type()

            card_notetype_timebox_minutes: dict[tuple[str, str], int] = {
                (NoteTypes.Sentence, CardTypes.reading): app.config().timebox_sentence_read.get_value(),
                (NoteTypes.Sentence, CardTypes.listening): app.config().timebox_sentence_listen.get_value(),

                (NoteTypes.Vocab, CardTypes.reading): app.config().timebox_vocab_read.get_value(),
                (NoteTypes.Vocab, CardTypes.listening): app.config().timebox_vocab_listen.get_value(),

                (NoteTypes.Kanji, CardTypes.reading): app.config().timebox_kanji_read.get_value(),
            }

            key = (notetype.name, typed.str_(card.type().name))
            if key in card_notetype_timebox_minutes:
                timebox = card_notetype_timebox_minutes[key]
                app.anki_config().set_timebox_seconds(card_notetype_timebox_minutes[key] * 60)
                aqt.utils.tooltip(f"Set timebox to {timebox} minutes")

def init() -> None:
    gui_hooks.webview_will_set_content.append(adjust_timebox)  # pyright: ignore[reportUnknownMemberType]