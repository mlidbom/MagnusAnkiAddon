from __future__ import annotations

from typing import TYPE_CHECKING

from anki.notes import Note
from ankiutils import app
from autoslot import Slots
from language_services.jamdict_ex.dict_lookup import DictLookup
from note.note_constants import NoteTypes
from sysutils import ex_sequence

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote


class VocabNoteFactory(Slots):
    @staticmethod
    def create_with_dictionary(question: str) -> VocabNote:
        from note.vocabulary.vocabnote import VocabNote
        dict_entry = DictLookup.lookup_word(question)
        if not dict_entry.found_words():
            return VocabNote.factory.create(question, "TODO", [])
        readings = list(set(ex_sequence.flatten([ent.kana_forms() for ent in dict_entry.entries])))
        created = VocabNote.factory.create(question, "TODO", readings)
        created.generate_and_set_answer()
        return created

    @staticmethod
    def create(question: str, answer: str, readings: list[str]) -> VocabNote:
        from note.vocabulary.vocabnote import VocabNote
        backend_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Vocab))
        note = VocabNote(backend_note)
        note.question.set(question)
        note.user.answer.set(answer)
        note.readings.set(readings)
        note.update_generated_data()
        app.col().vocab.add(note)
        return note