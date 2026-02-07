# from __future__ import annotations
#
# from typing import TYPE_CHECKING
#
# from autoslot import Slots
#
# from jaslib import app
#
# if TYPE_CHECKING:
#     from jaspythonutils.sysutils.weak_ref import WeakRef
#
#     from jaslib.note.notefields.json_object_field import MutableSerializedObjectField
#     from jaslib.note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData
#     from jaslib.note.vocabulary.vocabnote import VocabNote
#
# class ErgativeTwin(Slots):
#     def __init__(self, vocab: WeakRef[VocabNote], data: MutableSerializedObjectField[RelatedVocabData]) -> None:
#         self._vocab: WeakRef[VocabNote] = vocab
#         self._data: MutableSerializedObjectField[RelatedVocabData] = data
#
#     def get(self) -> str: return self._data.get().ergative_twin
#
#     def set(self, value: str) -> None:
#         self._data.get().ergative_twin = value
#
#         for twin in app.col().vocab.with_question(value):
#             if twin.related_notes.ergative_twin.get() != self._vocab().get_question():
#                 twin.related_notes.ergative_twin.set(self._vocab().get_question())
#
#         self._data.save()
#
#     def remove(self) -> None:
#         for twin in app.col().vocab.with_question(self._vocab().get_question()):
#             if twin.related_notes.ergative_twin.get() == self._vocab().get_question():
#                 twin.related_notes.ergative_twin.remove()
#
#         self._data.get().ergative_twin = ""
#
#         self._data.save()
