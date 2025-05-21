from __future__ import annotations

from typing import TYPE_CHECKING

import aqt.browser
from ankiutils import app
from aqt import gui_hooks
from note import queue_manager
from note.jpnote import JPNote
from note.sentences.sentencenote import SentenceNote
from note.vocabulary import vocabnote_context_sentences
from note.vocabulary.vocabnote import VocabNote
from sysutils import ex_lambda
from sysutils.typed import non_optional
from ui.qt_menu import right_click_menu, shortcutfinger

if TYPE_CHECKING:
    from collections.abc import Sequence

    from anki.cards import Card, CardId
    from PyQt6.QtWidgets import QMenu


def spread_due_dates(cards: Sequence[CardId], start_day: int, days: int) -> None:
    anki_col = app.col().anki_collection
    scheduler = anki_col.sched
    for index, card_id in enumerate(cards):
        card: Card = anki_col.get_card(card_id)
        new_due = start_day + (index * days)
        scheduler.set_due_date([card.id], str(new_due))

    app.get_ui_utils().refresh()

def setup_browser_context_menu(browser: aqt.browser.Browser, menu: QMenu) -> None:
    magnus_menu: QMenu = non_optional(menu.addMenu("&Magnus"))
    selected_cards = browser.selected_cards()

    if len(selected_cards) == 1:
        magnus_menu.addAction("Prioritize selected cards", lambda: queue_manager.prioritize_selected_cards(selected_cards))

        card = app.anki_collection().get_card(selected_cards[0])
        note = JPNote.note_from_card(card)
        right_click_menu.build_browser_right_click_menu(non_optional(magnus_menu.addMenu(shortcutfinger.home3("Note"))), note)

    if len(selected_cards) > 0:
        spread_menu: QMenu = non_optional(magnus_menu.addMenu("&Spread selected cards"))
        for start_day in [0,1,2,3,4,5,6,7,8,9]:
            start_day_menu: QMenu = non_optional(spread_menu.addMenu(f"First card in {start_day} days"))
            for days_apart in [1,2,3,4,5,6,7,8,9]:
                start_day_menu.addAction(f"{days_apart} days apart", ex_lambda.bind3(spread_due_dates, selected_cards, start_day, days_apart))

    selected_notes = {app.col().note_from_note_id(note_id) for note_id in browser.selectedNotes()}
    selected_vocab:set[VocabNote] = {note for note in selected_notes if isinstance(note, VocabNote)}
    vocab_that_can_generate_audio = [note for note in selected_vocab if vocabnote_context_sentences.can_generate_sentences_from_context_sentences(note, False)]
    if vocab_that_can_generate_audio:
        def generate_sentences() -> None:
            for vocab in vocab_that_can_generate_audio:
                vocabnote_context_sentences.generate_sentences_from_context_sentences(vocab, False)

        magnus_menu.addAction("Generate sentences from context sentences for vocab", generate_sentences)

    selected_sentences:list[SentenceNote] = [note for note in selected_notes if isinstance(note, SentenceNote)]
    if selected_sentences:
        from batches import local_note_updater

        magnus_menu.addAction("Reparse sentence words", lambda: local_note_updater.reparse_sentences(selected_sentences))


def init() -> None:
    gui_hooks.browser_will_show_context_menu.append(setup_browser_context_menu)
