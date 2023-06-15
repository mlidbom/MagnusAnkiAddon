from typing import List
from anki.notes import Note
from aqt import mw, gui_hooks, dialogs

from .my_anki import *
from .wani import *


def setup_buttons(buttons, the_editor):
    btn = the_editor.addButton("", "Unsuspend with dependencies",
                               lambda local_editor: unsuspend_with_dependencies(local_editor.note))
    buttons.append(btn)


def unsuspend_with_dependencies(note: Note) -> None:
    note_type = get_note_type_name(note)
    if note_type == Wani.NoteType.Vocab:
        unsuspend_vocab_with_dependencies(note)
    if note_type == Wani.NoteType.Kanji:
        unsuspend_kanji_with_dependencies(note, None)
    if note_type == Wani.NoteType.Radical:
        unsuspend_radical_with_dependencies(note, None)

    refresh_search()


def unsuspend_vocab_with_dependencies(vocab_note: Note) -> None:
    kanji_dependencies_names = extract_characters(vocab_note[Wani.VocabFields.Vocab])
    kanji_dependencies_notes = fetch_notes_by_note_type_and_field_value(Wani.NoteType.Kanji, Wani.KanjiFields.Kanji,
                                                                        kanji_dependencies_names)

    for kanji_note in kanji_dependencies_notes:
        unsuspend_kanji_with_dependencies(kanji_note, None)

    unsuspend_note_cards(vocab_note, vocab_note[Wani.VocabFields.Vocab_Meaning])


def unsuspend_kanji_with_dependencies(kanji_note: Note, calling_radical_note: Note) -> None:
    radical_dependencies_names = extract_comma_separated_values(
        kanji_note[Wani.KanjiFields.Radicals_Names]) + extract_comma_separated_values(
        kanji_note[Wani.KanjiFields.Radicals_Icons_Names])

    if calling_radical_note is not None and calling_radical_note[
        Wani.RadicalFields.Radical_Name] in radical_dependencies_names:
        return  # We do not want to unsuspend the kanji that depends on the radical, only kanji upon which the radical depends

    radical_dependencies_notes = fetch_notes_by_note_type_and_field_value(Wani.NoteType.Radical,
                                                                          Wani.RadicalFields.Radical_Name,
                                                                          radical_dependencies_names)
    for radical in radical_dependencies_notes:
        unsuspend_radical_with_dependencies(radical, kanji_note)

    unsuspend_note_cards(kanji_note, kanji_note[Wani.KanjiFields.Kanji_Meaning])


def unsuspend_radical_with_dependencies(radical_note: Note, calling_kanji_note: Note):
    kanji_dependencies_notes = fetch_notes_by_note_type_and_field_value(Wani.NoteType.Kanji, Wani.KanjiFields.Kanji,
                                                                        [radical_note[Wani.RadicalFields.Radical]])
    for kanji in kanji_dependencies_notes:
        if calling_kanji_note is None or kanji[Wani.KanjiFields.Kanji] != calling_kanji_note[Wani.KanjiFields.Kanji]:
            unsuspend_kanji_with_dependencies(kanji, radical_note)

    unsuspend_note_cards(radical_note, radical_note[Wani.RadicalFields.Radical_Name])


def unsuspend_note_cards(note: Note, name: str):
    print("Unsuspending {}: {}".format(get_note_type_name(note), name))
    mw.col.sched.unsuspend_cards(note.card_ids())


def fetch_notes_by_note_type_and_field_value(note_type: str, field: str, field_values: List):
    note_ids = [mw.col.find_notes(
        "{}:{} {}:{}".format(SearchTags.NoteType, note_type, field, field_value))
        for field_value in field_values]

    note_ids = flatten_list(note_ids)
    notes = fetch_notes_by_id(note_ids)
    return notes


def fetch_notes_by_id(note_ids: List):
    return [mw.col.get_note(note_id) for note_id in note_ids]


def extract_comma_separated_values(string: str) -> List:
    result = [item.strip() for item in string.split(",")]
    return [] + result


def extract_characters(string):
    return [char for char in string if not char.isspace()]


def flatten_list(the_list: List):
    return [item for sub_list in the_list for item in sub_list]


def refresh_search():
    browser = dialogs.open('Browser', mw)
    browser.onSearchActivated()


def get_note_type_name(note):
    return note._note_type['name']  # Todo: find how to do this without digging into protected members


gui_hooks.editor_did_init_buttons.append(setup_buttons)
