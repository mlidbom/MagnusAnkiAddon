from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots
from sysutils import ex_sequence

if TYPE_CHECKING:
    from note.notefields.json_object_field import MutableSerializedObjectField
    from note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class Synonyms(Slots):
    def __init__(self, vocab: WeakRef[VocabNote], data: MutableSerializedObjectField[RelatedVocabData]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self._data: MutableSerializedObjectField[RelatedVocabData] = data

    def strings(self) -> set[str]: return self._data.get().synonyms

    def _save(self) -> None:
        self.strings().discard(self._vocab().get_question())  # todo: this is cleanup after a bug. Remove soon
        self._data.save()

    def notes(self) -> list[VocabNote]:
        return app.col().vocab.with_any_form_in_prefer_exact_match(list(self.strings()))

    def add(self, synonym: str) -> None:
        if synonym == self._vocab().get_question(): return
        self.strings().add(synonym)

        for similar in app.col().vocab.with_question(synonym):
            if self._vocab().get_question() not in similar.related_notes.synonyms.strings():
                similar.related_notes.synonyms.add(self._vocab().get_question())

        self._save()

    def add_transitively_one_level(self, synonym: str) -> None:
        new_synonym_notes = app.col().vocab.with_any_form_in_prefer_exact_match([synonym])

        for synonym_note in new_synonym_notes:
            for my_synonym in self.strings():
                synonym_note.related_notes.synonyms.add(my_synonym)

        synonyms_of_new_synonym_strings = set(ex_sequence.flatten([list(note.related_notes.synonyms.strings()) for note in new_synonym_notes])) | {note.get_question() for note in new_synonym_notes}
        for new_synonym in synonyms_of_new_synonym_strings:
            self.add(new_synonym)

    def remove(self, to_remove: str) -> None:
        self.strings().remove(to_remove)

        for similar in app.col().vocab.with_question(to_remove):
            if self._vocab().get_question() in similar.related_notes.synonyms.strings():
                similar.related_notes.synonyms.remove(self._vocab().get_question())

        self._save()
