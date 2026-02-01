from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from typed_linq_collections.q_iterable import query

if TYPE_CHECKING:
    from jaslib.note.notefields.json_object_field import MutableSerializedObjectField
    from jaslib.note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData
    from jaslib.note.vocabulary.vocabnote import VocabNote
    from jaslib.sysutils.weak_ref import WeakRef
    from typed_linq_collections.collections.q_set import QSet

# noinspection PyUnusedFunction
class Synonyms(Slots):
    def __init__(self, vocab: WeakRef[VocabNote], data: MutableSerializedObjectField[RelatedVocabData]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self._data: MutableSerializedObjectField[RelatedVocabData] = data

    def strings(self) -> QSet[str]: return self._data.get().synonyms

    def _save(self) -> None:
        self.strings().discard(self._vocab().get_question())  # todo: this is cleanup after a bug. Remove soon
        self._data.save()

    def notes(self) -> list[VocabNote]:
        return app.col().vocab.with_any_form_in_prefer_disambiguation_name_or_exact_match(list(self.strings()))

    def add(self, synonym: str) -> None:
        if synonym == self._vocab().get_question(): return
        self.strings().add(synonym)

        for similar in app.col().vocab.with_question(synonym):
            if self._vocab().get_question() not in similar.related_notes.synonyms.strings():
                similar.related_notes.synonyms.add(self._vocab().get_question())

        self._save()

    def add_transitively_one_level(self, synonym: str) -> None:
        new_synonym_notes = query(app.col().vocab.with_any_form_in_prefer_disambiguation_name_or_exact_match([synonym]))

        for synonym_note in new_synonym_notes:
            for my_synonym in self.strings():
                synonym_note.related_notes.synonyms.add(my_synonym)

        synonyms_of_new_synonym_strings = (new_synonym_notes.select_many(lambda new_synonym_note: new_synonym_note.related_notes.synonyms.strings()).to_set()  # set(ex_sequence.flatten([list(note.related_notes.synonyms.strings()) for note in new_synonym_notes]))
                                           | new_synonym_notes.select(lambda new_synonym_note: new_synonym_note.get_question()).to_set())  # {note.get_question() for note in new_synonym_notes}
        for new_synonym in synonyms_of_new_synonym_strings:
            self.add(new_synonym)

    def remove(self, to_remove: str) -> None:
        self.strings().remove(to_remove)

        for similar in app.col().vocab.with_question(to_remove):
            if self._vocab().get_question() in similar.related_notes.synonyms.strings():
                similar.related_notes.synonyms.remove(self._vocab().get_question())

        self._save()
