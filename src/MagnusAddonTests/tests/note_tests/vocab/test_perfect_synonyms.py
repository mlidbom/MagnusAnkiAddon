from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from ankiutils import app
from fixtures.collection_factory import inject_empty_collection
from note.vocabulary.vocabnote import VocabNote

if TYPE_CHECKING:
    from collections.abc import Iterator

    from note.collection.jp_collection import JPCollection

# noinspection PyUnusedFunction
@pytest.fixture(scope="function", autouse=True)
def empty_collection() -> Iterator[JPCollection]:
    with inject_empty_collection() as collection:
        yield collection

def test_answer_syncs_to_synonym_on_add() -> None:
    first = VocabNote.factory.create("first", "first_answer", [])
    second = VocabNote.factory.create("second", "second_answer", [])
    app.col().flush_cache_updates()
    first.related_notes.perfect_synonyms.add_overwriting_the_answer_of_the_added_synonym(second.get_question())
    assert second.get_answer() == "first_answer"

def test_answer_syncs_to_added_synonym_on_update() -> None:
    first = VocabNote.factory.create("first", "first_answer", [])
    second = VocabNote.factory.create("second", "second_answer", [])

    first.related_notes.perfect_synonyms.add_overwriting_the_answer_of_the_added_synonym(second.get_question())

    first.user.answer.set("new answer")
    assert second.get_answer() == "new answer"

    third = VocabNote.factory.create("third", "third_answer", [])
    third.related_notes.perfect_synonyms.add_overwriting_the_answer_of_the_added_synonym(first.get_question())
    assert first.get_answer() == "third_answer"
    assert second.get_answer() == "third_answer"

    third.user.answer.set("third_new")
    assert first.get_answer() == "third_new"
    assert second.get_answer() == "third_new"

    assert first.related_notes.perfect_synonyms.get() == {second.get_question(), third.get_question()}
    assert second.related_notes.perfect_synonyms.get() == {first.get_question(), third.get_question()}
    assert third.related_notes.perfect_synonyms.get() == {first.get_question(), second.get_question()}

    first.related_notes.perfect_synonyms.remove(third.get_question())
    assert first.related_notes.perfect_synonyms.get() == {second.get_question()}
    assert second.related_notes.perfect_synonyms.get() == {first.get_question()}
    assert third.related_notes.perfect_synonyms.get() == set()

    first.user.answer.set("first_latest")
    assert first.get_answer() == "first_latest"
    assert second.get_answer() == "first_latest"
    assert third.get_answer() == "third_new"