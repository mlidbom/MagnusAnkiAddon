from typing import List
from anki.notes import Note
from aqt import mw, gui_hooks, dialogs

from .wani import *
from .my_anki import *


def setup_buttons(buttons, the_editor):
    btn = the_editor.addButton("", "Unsuspend vocab dependencies",
                               lambda local_editor: unsuspend_vocab_with_dependencies(local_editor.note))
    buttons.append(btn)

    btn = the_editor.addButton("", "Unsuspend kanji dependencies",
                               lambda local_editor: unsuspend_kanji_with_dependencies(local_editor.note))
    buttons.append(btn)


def get_kanji_dependencies(kanji_note: Note) -> List[Note]:
    radical_names = [item.strip() for item in
                     kanji_note[Wani.KanjiFields.Radicals_Names].split(",") + kanji_note[
                         Wani.KanjiFields.Radicals_Icons_Names].split(",")]
    radical_note_ids = [mw.col.find_notes(
        "{}:{} {}:{}".format(SearchTags.NoteType, Wani.NoteType.Radical, Wani.RadicalFields.Radical_Name,
                             radical_name)) for radical_name in
        radical_names]
    radical_note_ids = [item for sublist in radical_note_ids for item in sublist]
    radical_notes = [mw.col.get_note(note_id) for note_id in radical_note_ids]
    return radical_notes


def get_vocab_dependencies(vocab_note: Note) -> List[Note]:
    kanji_names = [item.strip() for item in vocab_note[Wani.VocabFields.Kanji].split(",")]
    kanji_note_ids = [mw.col.find_notes(
        "{}:{} {}:{}".format(SearchTags.NoteType, Wani.NoteType.Kanji, Wani.KanjiFields.Kanji, kanji_name)) for
        kanji_name in kanji_names]
    kanji_note_ids = [item for sublist in kanji_note_ids for item in sublist]
    kanji_notes = [mw.col.get_note(note_id) for note_id in kanji_note_ids]
    return kanji_notes


def unsuspend_kanji_with_dependencies(kanji_note: Note) -> None:
    radicals = get_kanji_dependencies(kanji_note)
    for radical in radicals:
        print("Unsuspending radical card:{}".format(radical[Wani.RadicalFields.Radical_Name]))
        mw.col.sched.unsuspend_cards(radical.card_ids())

    print("Unsuspending kanji card:{}".format(kanji_note[Wani.KanjiFields.Kanji_Meaning]))
    mw.col.sched.unsuspend_cards(kanji_note.card_ids())
    refresh_search()


def unsuspend_vocab_with_dependencies(vocab_note: Note) -> None:
    kanji_notes = get_vocab_dependencies(vocab_note)
    for kanji_note in kanji_notes:
        unsuspend_kanji_with_dependencies(kanji_note)

    for kanji_note in kanji_notes:
        print("Unsuspending kanji card:{}".format(kanji_note[Wani.KanjiFields.Kanji_Meaning]))
        mw.col.sched.unsuspend_cards(kanji_note.card_ids())

    print("Unsuspending vocab card:{}".format(vocab_note[Wani.VocabFields.Vocab_Meaning]))
    mw.col.sched.unsuspend_cards(vocab_note.card_ids())
    refresh_search()


def refresh_search():
    browser = dialogs.open('Browser', mw)
    browser.onSearchActivated()


gui_hooks.editor_did_init_buttons.append(setup_buttons)
