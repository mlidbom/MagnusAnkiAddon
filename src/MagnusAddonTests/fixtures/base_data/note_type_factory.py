from __future__ import annotations

from typing import TYPE_CHECKING

from fixtures.base_data.kanji_factory import create_kanji
from fixtures.base_data.sentence_factory import create_sentence
from fixtures.base_data.vocab_factory import create_vocab

if TYPE_CHECKING:
    from anki.collection import Collection


def add_note_types(collection: Collection) -> None:
    collection.models.add_dict(create_vocab().to_dict())
    collection.models.add_dict(create_sentence().to_dict())
    collection.models.add_dict(create_kanji().to_dict())











