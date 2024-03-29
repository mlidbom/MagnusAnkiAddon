from anki.notes import Note
from aqt.utils import showInfo

from note.kanjinote import KanjiNote
from note.radicalnote import RadicalNote
from note.vocabnote import VocabNote
from ankiutils import app
from note.note_constants import NoteTypes
from wanikani.wanikani_api_client import WanikaniClient

waniClient = WanikaniClient.get_instance()


def update_from_wanikani(note: Note) -> None:
    # noinspection PyProtectedMember
    note_type = note._note_type['name']
    if note_type == NoteTypes.Vocab:
        vocab_note = VocabNote(note)
        vocab_note.update_from_wani(waniClient.get_vocab(vocab_note.get_question()))
    if note_type == NoteTypes.Kanji:
        kanji_note = KanjiNote(note)
        kanji_note.update_from_wani(waniClient.get_kanji_by_name(kanji_note.get_question()))
    if note_type == NoteTypes.Radical:
        radical_note = RadicalNote(note)
        radical_note.update_from_wani(waniClient.get_radical(radical_note.get_answer()))


def update_radical() -> None:
    all_radicals: list[RadicalNote] = app.col().radicals.all()
    fetched = 0
    failed: str = ""
    for radical_note in all_radicals:
        try:
            wani_radical = waniClient.get_radical(radical_note.get_answer())
            radical_note.update_from_wani(wani_radical)
            fetched += 1
        except KeyError:
            failed = failed + "," + radical_note.get_answer()

    message = "Successfully matched {} radical notes.\n Failed:{}".format(fetched, failed)
    print(message)
    showInfo(message)


def update_kanji() -> None:
    all_kanji = app.col().kanji.all()
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
    all_vocabulary: list[VocabNote] = app.col().vocab.all_wani()
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
    all_radicals:list[RadicalNote] = app.col().radicals.all()
    deleted = 0
    deleted_radicals: str = ""
    for radical_note in all_radicals:
        try:
            waniClient.get_radical(radical_note.get_answer())
        except KeyError:
            deleted += 1
            deleted_radicals = deleted_radicals + "," + radical_note.get_answer()

    message = f"Deleted {deleted} radical notes."
    print(message)
    showInfo(message)


def delete_missing_kanji() -> None:
    all_kanji: list[KanjiNote] = app.col().kanji.all()
    deleted = 0
    deleted_kanji: str = ""
    for kanji_note in all_kanji:
        try:
            waniClient.get_kanji_by_name(kanji_note.get_question())
        except KeyError:
            deleted += 1
            deleted_kanji = deleted_kanji + "," + kanji_note.get_question()

    message = f"Deleted {deleted} kanji notes."
    print(message)
    showInfo(message)


def delete_missing_vocab() -> None:
    all_vocabulary: list[VocabNote] = app.col().vocab.all_wani()
    deleted = 0
    deleted_vocab: str = ""
    for vocab_note in all_vocabulary:
        try:
            waniClient.get_vocab(vocab_note.get_question())
        except KeyError:
            deleted += 1
            deleted_vocab = deleted_vocab + "," + vocab_note.get_question()
            vocab_note.delete()

    message = f"Deleted {deleted} vocab notes."
    print(message)
    showInfo(message)
