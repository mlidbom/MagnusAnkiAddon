# noinspection PyUnresolvedReferences
from typing import Optional, Callable, Sequence

# noinspection PyUnresolvedReferences
from ankiutils import app
from aqt.browser import Browser  # type: ignore
from anki.cards import CardId
from aqt import dialogs, mw

from note.waninote import WaniNote
# noinspection PyUnresolvedReferences
from note.vocabnote import VocabNote
# noinspection PyUnresolvedReferences
from note.kanjinote import KanjiNote
# noinspection PyUnresolvedReferences
from note.radicalnote import RadicalNote
from sysutils.stringutils import StringUtils
from note.jp_collection import *
from note.cardutils import CardUtils
from anki.notes import Note
from note.note_constants import NoteTypes
from ankiutils import app


def unsuspend_with_dependencies(note: Note) -> None:
    visit_note_dependencies(note, app.col().unsuspend_note_cards)

def prioritize_with_dependencies(note: Note) -> None:
    visit_note_dependencies(note, CardUtils.prioritize_note_cards)

def answer_again_with_zero_interval_for_new_note_cards_with_dependencies(note: Note) -> None:
    prioritize_with_dependencies(note)
    visit_note_dependencies(note, CardUtils.answer_again_with_zero_interval_for_new_note_cards)


def visit_note_dependencies(note: Note, callback: Callable[[WaniNote, str], None]) -> None:
    # noinspection PyProtectedMember
    note_type = note._note_type['name']
    if note_type == NoteTypes.Vocab:
        visit_vocab_with_dependencies(VocabNote(note), callback)
    if note_type == NoteTypes.Kanji:
        visit_kanji_with_dependencies(KanjiNote(note), None, callback)
    if note_type == NoteTypes.Radical:
        visit_radical_with_dependencies(RadicalNote(note), None, callback)

    refresh_search()


def visit_vocab_with_dependencies(vocab_note: VocabNote, callback: Callable[[WaniNote, str], None]) -> None:
    kanji_list = StringUtils.extract_characters(vocab_note.get_question())
    kanji_notes = app.col().kanji.by_kanji(kanji_list)

    for kanji_note in kanji_notes:
        visit_kanji_with_dependencies(kanji_note, None, callback)

    callback(vocab_note, vocab_note.get_active_answer())


def visit_kanji_with_dependencies(kanji_note: KanjiNote,
                                  calling_radical_note: Optional[RadicalNote],
                                  callback: Callable[[WaniNote, str], None]) -> None:
    radical_dependencies_names = StringUtils.extract_comma_separated_values(
        kanji_note.get_radicals_names()) + StringUtils.extract_comma_separated_values(
        kanji_note.get_radicals_icons_names())

    if calling_radical_note is not None and calling_radical_note.get_a() in radical_dependencies_names:
        return  # We do not want to unsuspend the kanji that depends on the radical, only kanji upon which the radical depends

    radical_dependencies_notes = app.col().radicals.by_answer(radical_dependencies_names)
    for radical in radical_dependencies_notes:
        if calling_radical_note is None or radical.get_a() != calling_radical_note.get_a():
            visit_radical_with_dependencies(radical, kanji_note, callback)

    callback(kanji_note, kanji_note.get_active_answer())


def visit_radical_with_dependencies(radical_note: RadicalNote,
                                    calling_kanji_note: Optional[KanjiNote],
                                    callback: Callable[[WaniNote, str], None]) -> None:
    kanji_dependencies_notes = app.col().kanji.by_kanji([radical_note.get_q()])
    for kanji_note in kanji_dependencies_notes:
        if calling_kanji_note is None or kanji_note.get_question() != calling_kanji_note.get_question():
            visit_kanji_with_dependencies(kanji_note, radical_note, callback)

    callback(radical_note, radical_note.get_a())


def refresh_search() -> None:
    browser: Browser = dialogs.open('Browser', mw)
    browser.onSearchActivated()


def prioritize_selected_cards(card_ids: Sequence[CardId]) -> None:
    cards = [app.anki_collection().get_card(card_id) for card_id in card_ids]
    for card in cards:
        CardUtils.prioritize(card)

    refresh_search()
