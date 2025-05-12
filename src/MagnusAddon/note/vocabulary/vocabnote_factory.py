from __future__ import annotations

from typing import TYPE_CHECKING

from anki.notes import Note
from language_services.jamdict_ex.dict_lookup import DictLookup
from note.note_constants import NoteTypes
from sysutils import ex_sequence

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote

class VocabNoteFactory:
    @staticmethod
    def create_with_dictionary(question: str) -> VocabNote:
        from note.vocabulary.vocabnote import VocabNote
        dict_entry = DictLookup.lookup_word_shallow(question)
        if not dict_entry.found_words():
            readings1 = []
            return VocabNote.factory.create(question, "TODO", readings1)
        readings = list(set(ex_sequence.flatten([ent.kana_forms() for ent in dict_entry.entries])))
        created = VocabNote.factory.create(question, "TODO", readings)
        created.generate_and_set_answer()
        return created

    @staticmethod
    def create(question: str, answer: str, readings: list[str]) -> VocabNote:
        from ankiutils import app
        from note.vocabulary.vocabnote import VocabNote
        backend_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Vocab))
        note = VocabNote(backend_note)
        note.set_question(question)
        note.set_user_answer(answer)
        note.readings.set(readings)
        note.update_generated_data()
        app.anki_collection().addNote(backend_note)
        return note
