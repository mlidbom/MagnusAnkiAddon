from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from ankiutils import app
from aqt import dialogs, mw
from note.cardutils import CardUtils
from note.kanjinote import KanjiNote
from note.note_constants import NoteTypes
from note.radicalnote import RadicalNote
from note.vocabulary.vocabnote import VocabNote
from sysutils import ex_str

if TYPE_CHECKING:
    from collections.abc import Sequence

    from anki.cards import CardId
    from anki.notes import Note
    from aqt.browser import Browser
    from note.waninote import WaniNote


def unsuspend_with_dependencies(note: Note) -> None:
    visit_note_dependencies(note, app.col().unsuspend_note_cards)

def prioritize_with_dependencies(note: Note) -> None:
    visit_note_dependencies(note, CardUtils.prioritize_note_cards)

def answer_again_with_zero_interval_for_new_note_cards_with_dependencies(note: Note) -> None:
    prioritize_with_dependencies(note)
    visit_note_dependencies(note, CardUtils.answer_again_with_zero_interval_for_new_note_cards)


def visit_note_dependencies(note: Note, callback: Callable[[WaniNote, str], None]) -> None:
    # noinspection PyProtectedMember
    note_type = note._note_type["name"]
    if note_type == NoteTypes.Vocab:
        visit_vocab_with_dependencies(VocabNote(note), callback)
    if note_type == NoteTypes.Kanji:
        visit_kanji_with_dependencies(KanjiNote(note), None, callback)
    if note_type == NoteTypes.Radical:
        visit_radical_with_dependencies(RadicalNote(note), None, callback)

    refresh_search()


def visit_vocab_with_dependencies(vocab_note: VocabNote, callback: Callable[[WaniNote, str], None]) -> None:
    kanji_list = ex_str.extract_characters(vocab_note.get_question())
    kanji_notes = app.col().kanji.with_any_kanji_in(kanji_list)

    for kanji_note in kanji_notes:
        visit_kanji_with_dependencies(kanji_note, None, callback)

    callback(vocab_note, vocab_note.get_answer())


def visit_kanji_with_dependencies(kanji_note: KanjiNote,
                                  calling_radical_note: RadicalNote | None,
                                  callback: Callable[[WaniNote, str], None]) -> None:
    radical_dependencies_names = kanji_note.get_radical_dependencies_names()

    if calling_radical_note is not None and calling_radical_note.get_answer() in radical_dependencies_names:
        return  # We do not want to unsuspend the kanji that depends on the radical, only kanji upon which the radical depends

    radical_dependencies_notes:list[RadicalNote] = app.col().radicals.with_any_answer_in(radical_dependencies_names)
    for radical in radical_dependencies_notes:
        if calling_radical_note is None or radical.get_answer() != calling_radical_note.get_answer():
            visit_radical_with_dependencies(radical, kanji_note, callback)

    callback(kanji_note, kanji_note.get_answer())


def visit_radical_with_dependencies(radical_note: RadicalNote,
                                    calling_kanji_note: KanjiNote | None,
                                    callback: Callable[[WaniNote, str], None]) -> None:
    kanji_dependencies_notes = app.col().kanji.with_any_kanji_in([radical_note.get_question()])
    for kanji_note in kanji_dependencies_notes:
        if calling_kanji_note is None or kanji_note.get_question() != calling_kanji_note.get_question():
            visit_kanji_with_dependencies(kanji_note, radical_note, callback)

    callback(radical_note, radical_note.get_answer())


def refresh_search() -> None:
    browser: Browser = dialogs.open("Browser", mw)
    browser.onSearchActivated()


def prioritize_selected_cards(card_ids: Sequence[CardId]) -> None:
    cards = [app.anki_collection().get_card(card_id) for card_id in card_ids]
    for card in cards:
        CardUtils.prioritize(card)

    refresh_search()
