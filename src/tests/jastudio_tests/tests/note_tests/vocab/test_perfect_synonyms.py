from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from jaslib.note.vocabulary.vocabnote import VocabNote
from jastudio.ankiutils import app
from jastudio_tests.fixtures.collection_factory import inject_empty_collection
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from collections.abc import Iterator

    from jastudio.note.collection.anki_jp_collection import AnkiJPCollection

# noinspection PyUnusedFunction
@pytest.fixture(scope="function", autouse=True)
def empty_collection() -> Iterator[AnkiJPCollection]:
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
    assert third.related_notes.perfect_synonyms.get() == QSet()

    first.user.answer.set("first_latest")
    assert first.get_answer() == "first_latest"
    assert second.get_answer() == "first_latest"
    assert third.get_answer() == "third_new"

def test_perfect_synonyms_are_kept_in_sync_on_add() -> None:
    first = VocabNote.factory.create("first", "", [])
    second = VocabNote.factory.create("second", "", [])
    first.related_notes.perfect_synonyms.add_overwriting_the_answer_of_the_added_synonym(second.get_question())

    assert first.related_notes.perfect_synonyms.get() == {"second"}
    assert second.related_notes.perfect_synonyms.get() == {"first"}

    third = VocabNote.factory.create("third", "", [])
    fourth = VocabNote.factory.create("fourth", "", [])
    second.related_notes.perfect_synonyms.add_overwriting_the_answer_of_the_added_synonym(third.get_question())
    second.related_notes.perfect_synonyms.add_overwriting_the_answer_of_the_added_synonym(fourth.get_question())

    assert first.related_notes.perfect_synonyms.get() == {"second", "third", "fourth"}
    assert second.related_notes.perfect_synonyms.get() == {"first", "third", "fourth"}
    assert third.related_notes.perfect_synonyms.get() == {"first", "second", "fourth"}
    assert fourth.related_notes.perfect_synonyms.get() == {"first", "second", "third"}
