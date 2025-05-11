from anki.notes import Note
from note.kanjinote import KanjiNote
from note.note_constants import NoteTypes
from note.radicalnote import RadicalNote
from note.vocabnote import VocabNote
from wanikani.wanikani_api_client import WanikaniClient

waniClient = WanikaniClient.get_instance()


def update_from_wanikani(note: Note) -> None:
    # noinspection PyProtectedMember
    note_type = note._note_type['name']  # noqa: SLF001
    if note_type == NoteTypes.Vocab:
        vocab_note = VocabNote(note)
        vocab_note.update_from_wani(waniClient.get_vocab(vocab_note.get_question()))
    if note_type == NoteTypes.Kanji:
        kanji_note = KanjiNote(note)
        kanji_note.update_from_wani(waniClient.get_kanji_by_name(kanji_note.get_question()))
    if note_type == NoteTypes.Radical:
        radical_note = RadicalNote(note)
        radical_note.update_from_wani(waniClient.get_radical(radical_note.get_answer()))