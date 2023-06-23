from aqt.utils import showInfo

from .wani_collection import WaniCollection
from .wanikani_note import *

waniClient = WanikaniClient.get_instance()


def update_from_wanikani(note: Note):
    # noinspection PyProtectedMember
    note_type = note._note_type['name']
    if note_type == Wani.NoteType.Vocab:
        vocab_note = WaniVocabNote(note)
        vocab_note.update_from_wani(waniClient.get_vocab(vocab_note.get_vocab()))
    if note_type == Wani.NoteType.Kanji:
        kanji_note = WaniKanjiNote(note)
        kanji_note.update_from_wani(waniClient.get_kanji_by_name(kanji_note.get_kanji()))
    if note_type == Wani.NoteType.Radical:
        radical_note = WaniRadicalNote(note)
        radical_note.update_from_wani(waniClient.get_radical(radical_note.get_radical_name()))


def update_radical() -> None:
    all_radicals: list[WaniRadicalNote] = WaniCollection.fetch_all_radical_notes()
    fetched = 0
    failed: str = ""
    for radical_note in all_radicals:
        try:
            wani_radical = waniClient.get_radical(radical_note.get_radical_name())
            radical_note.update_from_wani(wani_radical)
            fetched = fetched + 1
        except KeyError:
            failed = failed + "," + radical_note.get_radical_name()

    message = "Successfully matched {} radical notes.\n Failed:{}".format(fetched, failed)
    print(message)
    showInfo(message)


def update_kanji() -> None:
    all_kanji: list[WaniKanjiNote] = WaniCollection.fetch_all_kanji_notes()
    fetched = 0
    failed: str = ""
    for kanji_note in all_kanji:
        try:
            wani_kanji = waniClient.get_kanji_by_name(kanji_note.get_kanji())
            kanji_note.update_from_wani(wani_kanji)
            fetched = fetched + 1
        except KeyError:
            failed = failed + "," + kanji_note.get_kanji()

    message = "Successfully matched {} kanji notes.\n Failed:{}".format(fetched, failed)
    print(message)
    showInfo(message)


def update_vocab() -> None:
    all_vocabulary: list[WaniVocabNote] = WaniCollection.fetch_all_vocab_notes()
    updated = 0
    failed: str = ""
    for vocab_note in all_vocabulary:
        try:
            wani_vocab = waniClient.get_vocab(vocab_note.get_vocab())
            vocab_note.update_from_wani(wani_vocab)
            updated = updated + 1
        except KeyError:
            failed = failed + "," + vocab_note.get_vocab()

    message = "Successfully matched {} vocab notes.\n Failed:{}".format(updated, failed)
    print(message)
    showInfo(message)


def delete_missing_radicals() -> None:
    all_radicals = WaniCollection.fetch_all_radical_notes()
    deleted = 0
    deleted_radicals: str = ""
    for radical_note in all_radicals:
        try:
            waniClient.get_radical(radical_note.get_radical_name())
        except KeyError:
            deleted = deleted + 1
            deleted_radicals = deleted_radicals + "," + radical_note.get_radical_name()

    message = "Deleted {} radical notes.".format(deleted, deleted_radicals)
    print(message)
    showInfo(message)


def delete_missing_kanji() -> None:
    all_kanji: list[WaniKanjiNote] = WaniCollection.fetch_all_kanji_notes()
    deleted = 0
    deleted_kanji: str = ""
    for kanji_note in all_kanji:
        try:
            waniClient.get_kanji_by_name(kanji_note.get_kanji())
        except KeyError:
            deleted = deleted + 1
            deleted_kanji = deleted_kanji + "," + kanji_note.get_kanji()

    message = "Deleted {} kanji notes.".format(deleted, deleted_kanji)
    print(message)
    showInfo(message)


def delete_missing_vocab() -> None:
    all_vocabulary: list[WaniVocabNote] = WaniCollection.fetch_all_vocab_notes()
    deleted = 0
    deleted_vocab: str = ""
    for vocab_note in all_vocabulary:
        try:
            waniClient.get_vocab(vocab_note.get_vocab())
        except KeyError:
            deleted = deleted + 1
            deleted_vocab = deleted_vocab + "," + vocab_note.get_vocab()
            vocab_note.delete()

    message = "Deleted {} vocab notes.".format(deleted, deleted_vocab)
    print(message)
    showInfo(message)
