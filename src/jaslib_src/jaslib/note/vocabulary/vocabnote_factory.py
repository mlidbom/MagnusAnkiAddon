# from __future__ import annotations
#
# from typing import TYPE_CHECKING
#
# from autoslot import Slots
#
# from jaslib import app
# from jaslib.language_services.jamdict_ex.dict_lookup import DictLookup
# from jaslib.note.tags import Tags
#
# if TYPE_CHECKING:
#     from collections.abc import Callable
#
#     from jaslib.language_services.jamdict_ex.dict_lookup_result import DictLookupResult
#     from jaslib.note.vocabulary.vocabnote import VocabNote
#
# class VocabNoteFactory(Slots):
#     @classmethod
#     def create_with_dictionary(cls, question: str) -> VocabNote:
#         from jaslib.note.vocabulary.vocabnote import VocabNote
#         lookup_result: DictLookupResult = DictLookup.lookup_word(question)
#         if not lookup_result.found_words():
#             return VocabNote.factory.create(question, "", [])
#
#         created = VocabNote.factory.create(question, lookup_result.format_answer(), lookup_result.readings())
#         created.tags.set(Tags.Source.jamdict)
#         created.update_generated_data()
#         return created
#
#     @classmethod
#     def create(cls, question: str, answer: str, readings: list[str], initializer: Callable[[VocabNote], None] | None = None) -> VocabNote:
#         from jaslib.note.vocabulary.vocabnote import VocabNote
#         note = VocabNote()
#         note.question.set(question)
#         note.source_answer.set(answer)  # pyright: ignore [reportPrivateUsage]
#         note.readings.set(readings)
#         if initializer is not None: initializer(note)
#         app.col().vocab.add(note)
#         return note
#
#
#     @classmethod
#     def create_from_user_data(cls, question: str, answer: str, readings: list[str], initializer: Callable[[VocabNote], None] | None = None) -> VocabNote:
#         note = cls.create(question, answer, readings, initializer)
#         note.user.answer.set(note.source_answer.value)
#         note.source_answer.set("")
#
#         return note
