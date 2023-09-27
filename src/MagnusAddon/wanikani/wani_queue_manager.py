from typing import Optional, Callable

import aqt.browser
from anki.notes import Note

from aqt import dialogs, mw

from sysutils.utils import StringUtils
from wanikani.wani_collection import *
from wanikani.utils.wani_utils import CardUtils
from wanikani.wani_constants import Wani


def unsuspend_with_dependencies(note: Note) -> None:
    visit_note_dependencies(note, WaniCollection.unsuspend_note_cards)

def prioritize_with_dependencies(note: Note) -> None:
    visit_note_dependencies(note, CardUtils.prioritize_note_cards)

def answer_again_with_zero_interval_for_new_note_cards_with_dependencies(note: Note) -> None:
    prioritize_with_dependencies(note)
    visit_note_dependencies(note, CardUtils.answer_again_with_zero_interval_for_new_note_cards)


def visit_note_dependencies(note: Note, callback: Callable[[WaniNote, str], None]) -> None:
    # noinspection PyProtectedMember
    note_type = note._note_type['name']
    if note_type == Wani.NoteType.Vocab:
        visit_vocab_with_dependencies(WaniVocabNote(note), callback)
    if note_type == Wani.NoteType.Kanji:
        visit_kanji_with_dependencies(WaniKanjiNote(note), None, callback)
    if note_type == Wani.NoteType.Radical:
        visit_radical_with_dependencies(WaniRadicalNote(note), None, callback)

    refresh_search()


def visit_vocab_with_dependencies(vocab_note: WaniVocabNote, callback: Callable[[WaniNote, str], None]) -> None:
    kanji_list = StringUtils.extract_characters(vocab_note.get_question())
    kanji_notes = WaniCollection.fetch_kanji_notes(kanji_list)

    for kanji_note in kanji_notes:
        visit_kanji_with_dependencies(kanji_note, None, callback)

    callback(vocab_note, vocab_note.get_active_answer())


def visit_kanji_with_dependencies(kanji_note: WaniKanjiNote,
                                  calling_radical_note: Optional[WaniRadicalNote],
                                  callback: Callable[[WaniNote, str], None]) -> None:
    radical_dependencies_names = StringUtils.extract_comma_separated_values(
        kanji_note.get_radicals_names()) + StringUtils.extract_comma_separated_values(
        kanji_note.get_radicals_icons_names())

    if calling_radical_note is not None and calling_radical_note.get_a() in radical_dependencies_names:
        return  # We do not want to unsuspend the kanji that depends on the radical, only kanji upon which the radical depends

    radical_dependencies_notes = WaniCollection.fetch_radical_notes(radical_dependencies_names)
    for radical in radical_dependencies_notes:
        if calling_radical_note is None or radical.get_a() != calling_radical_note.get_a():
            visit_radical_with_dependencies(radical, kanji_note, callback)

    callback(kanji_note, kanji_note.get_active_answer())


def visit_radical_with_dependencies(radical_note: WaniRadicalNote,
                                    calling_kanji_note: Optional[WaniKanjiNote],
                                    callback: Callable[[WaniNote, str], None]):
    kanji_dependencies_notes = WaniCollection.fetch_kanji_notes([radical_note.get_q()])
    for kanji_note in kanji_dependencies_notes:
        if calling_kanji_note is None or kanji_note.get_question() != calling_kanji_note.get_question():
            visit_kanji_with_dependencies(kanji_note, radical_note, callback)

    callback(radical_note, radical_note.get_a())


def refresh_search() -> None:
    browser: aqt.browser.Browser = dialogs.open('Browser', mw)
    browser.onSearchActivated()


def prioritize_selected_cards(card_ids: Sequence[int]):
    cards = [facade.col().get_card(card_id) for card_id in card_ids]
    for card in cards:
        CardUtils.prioritize(card)

    refresh_search()
