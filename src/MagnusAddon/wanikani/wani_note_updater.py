from anki.notes import Note
from aqt.utils import showInfo

from note.kanjinote import KanjiNote
from note.radicalnote import RadicalNote
from note.vocabnote import VocabNote
from note.jp_collection import JPCollection
from wanikani.wani_constants import NoteFields
from wanikani.wanikani_api_client import WanikaniClient

waniClient = WanikaniClient.get_instance()


def update_from_wanikani(note: Note):
    # noinspection PyProtectedMember
    note_type = note._note_type['name']
    if note_type == NoteFields.NoteType.Vocab:
        vocab_note = VocabNote(note)
        vocab_note.update_from_wani(waniClient.get_vocab(vocab_note.get_question()))
    if note_type == NoteFields.NoteType.Kanji:
        kanji_note = KanjiNote(note)
        kanji_note.update_from_wani(waniClient.get_kanji_by_name(kanji_note.get_question()))
    if note_type == NoteFields.NoteType.Radical:
        radical_note = RadicalNote(note)
        radical_note.update_from_wani(waniClient.get_radical(radical_note.get_a()))


def update_radical() -> None:
    all_radicals: list[RadicalNote] = JPCollection.fetch_all_radical_notes()
    fetched = 0
    failed: str = ""
    for radical_note in all_radicals:
        try:
            wani_radical = waniClient.get_radical(radical_note.get_a())
            radical_note.update_from_wani(wani_radical)
            fetched += 1
        except KeyError:
            failed = failed + "," + radical_note.get_a()

    message = "Successfully matched {} radical notes.\n Failed:{}".format(fetched, failed)
    print(message)
    showInfo(message)


def update_kanji() -> None:
    all_kanji: list[KanjiNote] = JPCollection.fetch_all_kanji_notes()
    fetched = 0
    failed: str = ""
    for kanji_note in all_kanji:
        try:
            wani_kanji = waniClient.get_kanji_by_name(kanji_note.get_question())
            kanji_note.update_from_wani(wani_kanji)
            fetched += 1
        except KeyError:
            failed = failed + "," + kanji_note.get_question()

    message = "Successfully matched {} kanji notes.\n Failed:{}".format(fetched, failed)
    print(message)
    showInfo(message)


def update_vocab() -> None:
    all_vocabulary: list[VocabNote] = JPCollection.fetch_all_wani_vocab_notes()
    updated = 0
    failed: str = ""
    for vocab_note in all_vocabulary:
        try:
            wani_vocab = waniClient.get_vocab(vocab_note.get_question())
            vocab_note.update_from_wani(wani_vocab)
            updated += 1
        except KeyError:
            failed = failed + "," + vocab_note.get_question()

    message = "Successfully matched {} vocab notes.\n Failed:{}".format(updated, failed)
    print(message)
    showInfo(message)


def delete_missing_radicals() -> None:
    all_radicals = JPCollection.fetch_all_radical_notes()
    deleted = 0
    deleted_radicals: str = ""
    for radical_note in all_radicals:
        try:
            waniClient.get_radical(radical_note.get_a())
        except KeyError:
            deleted += 1
            deleted_radicals = deleted_radicals + "," + radical_note.get_a()

    message = "Deleted {} radical notes.".format(deleted, deleted_radicals)
    print(message)
    showInfo(message)


def delete_missing_kanji() -> None:
    all_kanji: list[KanjiNote] = JPCollection.fetch_all_kanji_notes()
    deleted = 0
    deleted_kanji: str = ""
    for kanji_note in all_kanji:
        try:
            waniClient.get_kanji_by_name(kanji_note.get_question())
        except KeyError:
            deleted += 1
            deleted_kanji = deleted_kanji + "," + kanji_note.get_question()

    message = "Deleted {} kanji notes.".format(deleted, deleted_kanji)
    print(message)
    showInfo(message)


def delete_missing_vocab() -> None:
    all_vocabulary: list[VocabNote] = JPCollection.fetch_all_wani_vocab_notes()
    deleted = 0
    deleted_vocab: str = ""
    for vocab_note in all_vocabulary:
        try:
            waniClient.get_vocab(vocab_note.get_question())
        except KeyError:
            deleted += 1
            deleted_vocab = deleted_vocab + "," + vocab_note.get_question()
            vocab_note.delete()

    message = "Deleted {} vocab notes.".format(deleted, deleted_vocab)
    print(message)
    showInfo(message)
