from typing import Optional

import aqt.browser

from aqt import dialogs

from magnus.utils import StringUtils
from magnus.wani_collection import *
from magnus.wani_utils import CardUtils


def unsuspend_with_dependencies(note: Note) -> None:
    # noinspection PyProtectedMember
    note_type = note._note_type['name']
    if note_type == Wani.NoteType.Vocab:
        unsuspend_vocab_with_dependencies(WaniVocabNote(note))
    if note_type == Wani.NoteType.Kanji:
        unsuspend_kanji_with_dependencies(WaniKanjiNote(note), None)
    if note_type == Wani.NoteType.Radical:
        unsuspend_radical_with_dependencies(WaniRadicalNote(note), None)

    refresh_search()


def unsuspend_vocab_with_dependencies(vocab_note: WaniVocabNote) -> None:
    kanji_dependencies_names = StringUtils.extract_characters(vocab_note.get_vocab())
    kanji_dependencies_notes = WaniCollection.fetch_kanji_notes(kanji_dependencies_names)

    for kanji_note in kanji_dependencies_notes:
        unsuspend_kanji_with_dependencies(kanji_note, None)

    WaniCollection.unsuspend_note_cards(vocab_note, vocab_note.get_vocab_meaning())


def unsuspend_kanji_with_dependencies(kanji_note: WaniKanjiNote,
                                      calling_radical_note: Optional[WaniRadicalNote]) -> None:
    radical_dependencies_names = StringUtils.extract_comma_separated_values(
        kanji_note.get_radicals_names()) + StringUtils.extract_comma_separated_values(
        kanji_note.get_radicals_icons_names())

    if calling_radical_note is not None and calling_radical_note.get_radical_name() in radical_dependencies_names:
        return  # We do not want to unsuspend the kanji that depends on the radical, only kanji upon which the radical depends

    radical_dependencies_notes = WaniCollection.fetch_radical_notes(radical_dependencies_names)
    for radical in radical_dependencies_notes:
        unsuspend_radical_with_dependencies(radical, kanji_note)

    WaniCollection.unsuspend_note_cards(kanji_note, kanji_note.get_kanji_meaning())


def unsuspend_radical_with_dependencies(radical_note: WaniRadicalNote, calling_kanji_note: Optional[WaniKanjiNote]):
    kanji_dependencies_notes = WaniCollection.fetch_kanji_notes([radical_note.get_radical()])
    for kanji_note in kanji_dependencies_notes:
        if calling_kanji_note is None or kanji_note.get_kanji() != calling_kanji_note.get_kanji():
            unsuspend_kanji_with_dependencies(kanji_note, radical_note)

    WaniCollection.unsuspend_note_cards(radical_note, radical_note.get_radical_name())


def refresh_search():
    browser: aqt.browser.Browser = dialogs.open('Browser', mw)
    browser.onSearchActivated()


def prioritize_cards_with_dependencies(card_ids : List[int]):
    something = card_ids
    cards = [mw.col.get_card(id) for id in card_ids]
    for card in cards:
        print(CardUtils.is_new(card))
